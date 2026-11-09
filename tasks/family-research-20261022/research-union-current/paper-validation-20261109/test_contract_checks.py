"""Synthetic contract checks; neither a backtest nor broker certification."""
import unittest
from dataclasses import replace
from contract_checks import Group, Trade, flow, R1Signal, Invalidation, quote_fill, pnl, activation_blockers

S = 1_000_000_000
T = 1_794_000_000_123_456_789

def group(n=1, offset=0, **changes):
    base = Group(n, T + offset, T + offset, 3000, 3001, 3, 1,
                 1, 1, True, True, 60*S, 0, 0)
    return replace(base, **changes)

class ContractTests(unittest.TestCase):
    def test_flow_excludes_left_boundary_and_future(self):
        trades = [Trade(T-5*S, T-5*S, 'B', 100), Trade(T, T, 'S', 2),
                  Trade(T+1, T+1, 'B', 100), Trade(T, T+1, 'B', 100)]
        self.assertEqual(flow(trades, T, 5*S), (0, 2, 0, -1))

    def test_empty_is_missing_unknown_is_separate(self):
        self.assertEqual(flow([Trade(T,T,'N',7)], T, 5*S), (0,0,7,None))

    def test_balanced_is_zero(self):
        self.assertEqual(flow([Trade(T,T,'B',1),Trade(T,T,'S',1)], T, 5*S)[3], 0)

    def test_clock_float_rejected(self):
        with self.assertRaises(ValueError):
            flow([], float(T), 5*S)

    def test_later_group_confirms_long(self):
        r = R1Signal()
        self.assertEqual(r.step(group()), 'armed')
        self.assertEqual(r.step(group(2,1,bid=3001,ask=3002)), 'confirm_buy')

    def test_short_is_symmetric(self):
        r = R1Signal()
        self.assertEqual(r.step(group(f5=-1,f60=-1,bid_size=1,ask_size=3)), 'armed')
        self.assertEqual(r.step(group(2,1,bid=2999,ask=3000,f5=-1,f60=-1,bid_size=1,ask_size=3)), 'confirm_sell')

    def test_same_group_never_confirms(self):
        r = R1Signal(); r.step(group())
        self.assertEqual(r.step(group(bid=3001,ask=3002)), 'pause')

    def test_expiry_alone_cannot_arm(self):
        self.assertEqual(R1Signal().step(group(fresh=False)), 'idle')

    def test_both_quotes_must_move(self):
        r = R1Signal(); r.step(group())
        self.assertEqual(r.step(group(2,1,ask=3002)), 'waiting')

    def test_at_deadline_disarms(self):
        r = R1Signal(); r.step(group())
        self.assertEqual(r.step(group(2,5*S,bid=3001,ask=3002)), 'disarmed')

    def test_sign_failure_consumes_arm(self):
        r = R1Signal(); r.step(group())
        self.assertEqual(r.step(group(2,1,f60=-1)), 'disarmed')

    def test_input_guards(self):
        for changes in [dict(known_ns=T+1),dict(continuous=False),dict(warmup_ns=60*S-1),
                        dict(ask=3000),dict(ask=3003),dict(bid_size=0),
                        dict(quote_age_ns=S+1),dict(silence_ns=S+1)]:
            with self.subTest(changes=changes):
                self.assertEqual(R1Signal().step(group(**changes)), 'pause')

    def test_failure_does_not_auto_resume(self):
        r = R1Signal(); r.step(group(continuous=False))
        self.assertEqual(r.step(group(2,1)), 'pause')

    def test_consumed_confirmation_needs_new_edge(self):
        r = R1Signal(); r.step(group()); r.step(group(2,1,bid=3001,ask=3002))
        self.assertEqual(r.step(group(3,2,bid=3002,ask=3003)), 'idle')
        r.step(group(4,3,fresh=False))
        self.assertEqual(r.step(group(5,4)), 'armed')

    def test_empty_flow_requires_persistent_invalidation(self):
        v = Invalidation(1)
        self.assertFalse(v.step(group(f5=None)))
        self.assertFalse(v.step(group(2,S-1,f5=None)))
        self.assertTrue(v.step(group(3,S,f5=None)))

    def test_agreement_resets_invalidation(self):
        v = Invalidation(1); v.step(group(f5=-1)); v.step(group(2,S//2))
        self.assertFalse(v.step(group(3,S,f5=-1)))

    def test_gap_invalidates_immediately(self):
        self.assertTrue(Invalidation(1).step(group(continuous=False)))

    def test_arrival_required_and_same_group_excluded(self):
        g = group(2,10)
        self.assertIsNone(quote_fill('B',1,T,None,g))
        self.assertIsNone(quote_fill('B',2,T,T,g))
        self.assertIsNone(quote_fill('B',1,T,T+11,g))
        self.assertEqual(quote_fill('B',1,T,T+10,g), 3001)
        self.assertEqual(quote_fill('S',1,T,T+10,g), 3000)

    def test_invalid_quote_never_fills(self):
        self.assertIsNone(quote_fill('B',1,T,T,group(2,1,ask_size=0)))
        self.assertIsNone(quote_fill('B',1,T,T,group(2,1,known_ns=T+2)))

    def test_unknown_fees_are_not_zero(self):
        self.assertEqual(pnl(1,3001,3004,None), {'gross_ticks':3,'stress_ticks':1,'net_ticks':None})
        self.assertEqual(pnl(-1,3004,3001,5)['net_ticks'], 2.5)

    def test_unconfigured_activation_remains_blocked(self):
        reasons = activation_blockers({})
        self.assertIn('execution_adapter',reasons)
        self.assertIn('fees_round_turn_usd',reasons)
        self.assertIn('full_runner_acceptance_receipt',reasons)

    def test_r2_has_same_operational_requirements_as_r1(self):
        self.assertEqual(activation_blockers({},'R2'),activation_blockers({},'R1'))

    def test_unknown_rule_still_rejected(self):
        self.assertIn('unknown_strategy',activation_blockers({},'R99'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
