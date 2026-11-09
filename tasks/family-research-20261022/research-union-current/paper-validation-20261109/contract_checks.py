"""Offline reference checks for v1.2. No broker, feed reader, order sender or runner.

Group.index is a locally assigned COMPLETE-group ordinal, not exchange sequence.
Prices are integer NG ticks. Clocks use one already-verified receive-time domain;
actual adapters must establish the local-arrival mapping before calling anything.
No function here grants permission to run a strategy.
"""
from dataclasses import dataclass
import math

SECOND = 1_000_000_000

def exact_int(value):
    if type(value) is not int:
        raise ValueError('Exact integer required; floats and booleans are forbidden')
    return value

def sign(value):
    if value is None or not math.isfinite(value):
        return None
    return (value > 0) - (value < 0)

@dataclass(frozen=True)
class Trade:
    receive_ns: int
    known_ns: int
    side: str
    quantity: int

def flow(trades, now_ns, window_ns):
    exact_int(now_ns); exact_int(window_ns)
    if window_ns <= 0:
        raise ValueError('Positive window required')
    quantities = dict(B=0, S=0, N=0)
    for trade in trades:
        exact_int(trade.receive_ns); exact_int(trade.known_ns); exact_int(trade.quantity)
        if trade.quantity < 0 or trade.side not in quantities:
            raise ValueError('Invalid classified trade')
        if now_ns-window_ns < trade.receive_ns <= now_ns and trade.known_ns <= now_ns:
            quantities[trade.side] += trade.quantity
    b, s, unknown = (quantities[k] for k in ('B','S','N'))
    return b, s, unknown, (b-s)/(b+s) if b+s else None

@dataclass(frozen=True)
class Group:
    index: int
    receive_ns: int
    known_ns: int
    bid: int
    ask: int
    bid_size: int
    ask_size: int
    f5: float | None
    f60: float | None
    fresh: bool
    continuous: bool
    warmup_ns: int
    quote_age_ns: int
    silence_ns: int

    def valid_quote(self):
        values = (self.index,self.receive_ns,self.known_ns,self.bid,self.ask,
                  self.bid_size,self.ask_size,self.warmup_ns,self.quote_age_ns,self.silence_ns)
        return (all(type(x) is int for x in values)
                and self.continuous is True and self.index >= 0
                and 0 <= self.known_ns <= self.receive_ns
                and 0 < self.bid < self.ask and self.ask-self.bid <= 2
                and min(self.bid_size,self.ask_size) >= 1
                and 0 <= self.quote_age_ns <= SECOND
                and 0 <= self.silence_ns <= SECOND)

    def touch_sign(self):
        return sign(self.bid_size-self.ask_size)

class R1Signal:
    """R1 trigger/confirmation only. Confirmation is a signal, never an order.

    No automatic resume. After a pause, a separate future controller must verify
    snapshot/continuity/warmup plus operator resume before making a fresh instance.
    """
    def __init__(self):
        self.arm = None
        self.previous_condition = False
        self.previous_group = None
        self.paused = False

    def step(self, group):
        previous = self.previous_group
        ordered = previous is None or (group.index > previous.index and group.receive_ns >= previous.receive_ns)
        self.previous_group = group
        if self.paused or not group.valid_quote() or group.warmup_ns < 60*SECOND or not ordered:
            self.paused = True
            self.arm = None
            return 'pause'
        direction = sign(group.f5)
        agreement = direction in (-1,1) and sign(group.f60) == direction and group.touch_sign() == direction
        condition = agreement and group.fresh is True
        edge = condition and not self.previous_condition
        self.previous_condition = condition
        if self.arm is not None:
            armed, d = self.arm
            if group.receive_ns-armed.receive_ns >= 5*SECOND or not agreement or direction != d:
                self.arm = None
                return 'disarmed'
            if d*(group.bid-armed.bid) >= 1 and d*(group.ask-armed.ask) >= 1:
                self.arm = None
                return 'confirm_buy' if d == 1 else 'confirm_sell'
            return 'waiting'
        if edge:
            self.arm = group, direction
            return 'armed'
        return 'idle'

class Invalidation:
    """Persistent signal invalidation; not the stop/loss/session controller."""
    def __init__(self, direction):
        if direction not in (-1,1):
            raise ValueError('Direction must be +/-1')
        self.direction = direction
        self.first_bad = None
        self.previous = None

    def step(self, group):
        previous = self.previous
        self.previous = group
        if not group.valid_quote() or (previous and (group.index <= previous.index or group.receive_ns < previous.receive_ns)):
            return True
        if sign(group.f5) == self.direction and group.touch_sign() == self.direction:
            self.first_bad = None
            return False
        if self.first_bad is None:
            self.first_bad = group
            return False
        return group.index > self.first_bad.index and group.receive_ns-self.first_bad.receive_ns >= SECOND

def quote_fill(side, confirmation_group, confirmation_ns, arrival_ns, group):
    """Quote eligibility only; caller must select FIRST eligible group exactly once.

    None means no fill from this observation, never proof that exposure is flat.
    A controller must own IOC cancellation/retries and capacity. Not implemented here.
    """
    if side not in ('B','S'):
        raise ValueError('Explicit buy/sell side required')
    for value in (confirmation_group, confirmation_ns):
        exact_int(value)
    if arrival_ns is None:
        return None
    exact_int(arrival_ns)
    if (arrival_ns < confirmation_ns or not group.valid_quote()
            or group.index <= confirmation_group or group.receive_ns < arrival_ns):
        return None
    return group.ask if side == 'B' else group.bid

def pnl(direction, entry_ticks, exit_ticks, fees_round_turn_usd):
    for value in (direction,entry_ticks,exit_ticks):
        exact_int(value)
    if direction not in (-1,1):
        raise ValueError('Direction must be +/-1')
    if fees_round_turn_usd is not None and (not math.isfinite(fees_round_turn_usd) or fees_round_turn_usd < 0):
        raise ValueError('Nonnegative known fee required')
    gross = direction*(exit_ticks-entry_ticks)
    return dict(gross_ticks=gross,stress_ticks=gross-2,
                net_ticks=None if fees_round_turn_usd is None else gross-fees_round_turn_usd/10)

def activation_blockers(config, strategy='R1'):
    """Missing-evidence inventory, not an activation certificate or config validator."""
    required = ('execution_adapter','contract_id','session_start_utc','session_end_utc',
                'fees_round_turn_usd','arrival_clock_mapping_receipt','full_runner_acceptance_receipt',
                'feed_continuity_receipt','prospective_rule_freeze_receipt')
    blocked = [key for key in required if config.get(key) is None or config.get(key) == '']
    if strategy not in ('R1', 'R2'):
        blocked.append('unknown_strategy')
    return blocked
