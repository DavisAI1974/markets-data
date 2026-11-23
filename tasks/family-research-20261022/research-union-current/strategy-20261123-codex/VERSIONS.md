# Fifteen natural gas strategies for paper trading

**All fifteen go forward independently.** The Oct 2, 3, 17 and 18, 2023 trade days supplied observations for v2. Paper trading is the first trial. Read the numbered sections as prospective rules. Each “why” explains the design choice. The actual observations and their limits are in [the evidence record](EVIDENCE.md).

## How to read and run v2

- **p** is a trade print that arms a rule. **q** is the very next trade print, including a print whose aggressor is unknown. The decision becomes knowable at q’s received nanosecond and tape position. A quote at a print is the stored book at that row. Comparisons between p and q describe endpoints. Each intervening message remains on the tape.
- Dipole and exhaustion are the stored natural gas 60-second and 20-second lines respectively. Positive means bought size exceeds sold size over the line’s own span. A sign transition here compares the values at p and q. Old trades leaving a span can contribute. The sign change alone does not identify its cause. A reported buyer or seller requires the tape’s aggressor side.
- At p, arm for one next print. If q misses any condition, the arm expires there. q may itself serve as a new p. For a paper entry, start one independent paper idea per strategy when flat, and ignore further entry arms while it is active. For management, p and q must refer to the same open paper position in the specified direction. Attach a management rule separately to each eligible paper position. Do not add or reverse a position unless the rule says so.
- **After q**, observe every tape row in order, including nontrade messages. Read line and book conditions there. A condition on the print is checked only on a trade row. The first stated invalidation ends the idea. An actual close of the managed position releases its pending warnings. While a hold or warning is active for that position, keep its original q reference. Once it clears, arm only on a fresh eligible print. If an exit and a warning-release condition first appear on the same row, give the exit priority.
- At a marked settlement row, a trade-day boundary or a detected gap, end the observation as interrupted and reset. Resume with fresh prints. Use the stored trade-day and settlement marks. A trade day runs from 6 pm Eastern the evening before through 5 pm Eastern on the named date. The intervening hour belongs to neither trade day.
- If a required input is missing at p or q, let the arm expire without action. Unknown aggressor is missing only for a rule that requires it. If an active rule loses a required monitoring input, mark the assessment indeterminate and clear its reference. Do not manufacture a price or a paper exit. Missing paper-position state makes a management action unavailable. Research reference prices are actual prints; quotes, D and E each keep their own values.
- **What would contradict it on paper?** Starting strictly after q, record each print and both sides of the book until the specified end. For an upward/downward entry or hold, a first changed print below/above q contradicts the immediate price thesis. For an exit or caution on an upward position, the prediction is down; for one on a downward position it is up. Follow the warning’s price reference even after it requests an exit: observe only through the first subsequent distinct print or an interruption. A first changed print in the opposite direction contradicts that warning. Keep equal prints individually. If the observation ends with no distinct print, price response is unresolved. Log the actual invalidation row even if a favorable print came first. No time target or fill assumption enters the observation.
- Paper records for these strategies can coexist. A warning or exit in one strategy’s record never erases another strategy's entry, hold or opposing idea. The examples stop at q. The future paths described above are reserved for paper trading.

## CX01 · Enter on buying that carries into a new event

**Arm.** Both lines are positive. **At q.** Both stay positive, the print and the bid rise, and q belongs to a different exchange event. Open an upward paper idea.

**Manage.** Keep it while the bid holds at or above q’s bid and both lines stay positive. Close at the first breach.

**Why.** A higher print can be another piece of the same exchange event. A fresh event with a higher bid gives an independent book observation.

## CX02 · Enter when selling moves the bid down

**Arm.** Both lines are negative. **At q.** Both stay negative. A reported seller prints below p in a different exchange event, with a lower bid. Open downward.

**Manage.** Close on the first bid above q’s bid or when either line reaches zero or turns positive.

**Why.** A lower print can occur without a new bid, and a print can have an unknown aggressor. Neither establishes this particular selling sequence.

## CX03 · Re-enter upward after a pullback

**Arm.** Dipole is positive and exhaustion is zero or negative. **At q.** Dipole stays positive. Exhaustion is now positive and a reported buyer trades at the best offer. Open upward.

**Manage.** Keep the recovery while both lines are positive and the offer holds at or above q’s offer. Close at the first breach.

**Why.** The flow turn can occur away from the offer. Requiring a purchase there ties the entry to a transaction at the asking price.

## CX04 · Re-enter downward after a bounce

**Arm.** Dipole is negative and exhaustion is zero or positive. **At q.** Dipole stays negative. Exhaustion is now negative, a reported seller trades at the bid, and the offer is at or below its value at p. Open downward.

**Manage.** Close when the offer rises above q’s offer or either line reaches zero or turns positive.

**Why.** A turn in selling pressure can coexist with an advancing offer. This version needs the offer to stop advancing between the two prints.

## CX05 · Exit an upward position when the bid gives way

**Arm.** An upward paper position is open and both lines are positive. **At q.** With that position still open, dipole stays positive, exhaustion turns negative and the bid falls. Issue an exit indication at q.

**Manage.** The exit ends this position’s warning. Any re-entry needs a separate entry trigger. A new upward position can arm it again.

**Why.** This catches a weakening bid before the slower line turns. The print itself can stay at the same price through the flow change.

## CX06 · Exit a downward position as the offer lifts

**Arm.** A downward paper position is open and both lines are negative. **At q.** With that position still open, dipole stays negative, exhaustion turns positive and the offer rises. Issue an exit indication at q.

**Manage.** End the warning with that exit. A new downward position and a fresh pair of prints are needed to arm it again.

**Why.** A positive exhaustion reading can accompany a falling bid. A higher offer supplies a separate reason to end the downward idea.

## CX07 · Follow a buyer to a higher offer

**Arm.** The print is at the best offer. **At q.** A reported buyer pays the new, higher best offer. The bid is unchanged between p and q. Open upward.

**Manage.** Track whether the bid follows. Close on the first offer below q’s offer or bid below q’s bid. A later higher bid is a distinct observation to log.

**Why.** This isolates an offer moving first. It can be a widening market, so the stationary bid matters both at entry and afterward.

## CX08 · Follow a seller to a lower bid

**Arm.** The print is at the best bid. **At q.** A reported seller trades at the new, lower best bid. The offer is unchanged between p and q. Open downward.

**Manage.** Track whether the offer follows. Close on the first bid above q’s bid or offer above q’s offer.

**Why.** A bid can retreat while the offer stays put. The next movement of the offer distinguishes two-sided repricing from an isolated retreat.

## CX09 · Reverse down from a stationary offer

**Arm.** The print is at the best offer and exhaustion is positive. **At q.** The offer is unchanged, the next print is lower and the bid has fallen. Open downward.

**Manage.** Close on the first print at or above p’s print or the first bid above q’s bid.

**Why.** A print can drop from the offer to the bid with neither quote moving. A falling bid distinguishes this reversal proposal.

## CX10 · Reverse up from a stationary bid

**Arm.** The print is at the best bid and exhaustion is negative. **At q.** The bid is unchanged, the next print is higher and the offer has risen. Open upward.

**Manage.** Close on the first print at or below p’s print or the first offer below q’s offer.

**Why.** A print can rise across an unchanged spread. Requiring a higher offer asks whether the book also repriced.

## CX11 · Stay in an upward position when a seller tests a higher bid

**Arm.** An upward paper position is open and dipole is positive. **At q.** Dipole stays positive. The bid rises, the offer is unchanged and a reported seller trades at that higher bid. Maintain the existing position.

**Manage.** Withdraw the hold and issue an exit on the first bid below q’s bid or dipole at or below zero. A fresh position can arm again.

**Why.** Even a lower print can be a sale into a bid that has stepped up. This manages the bid supporting the trade.

## CX12 · Stay in a downward position when a buyer tests a lower offer

**Arm.** A downward paper position is open and dipole is negative. **At q.** Dipole stays negative. The offer falls, the bid is unchanged and a reported buyer pays that lower offer. Maintain the existing position.

**Manage.** Withdraw the hold and issue an exit on the first offer above q’s offer or dipole at or above zero. A fresh position can arm again.

**Why.** A higher print can still be a purchase at a lower asking price. This manages the offer capping the trade.

## CX13 · Question a rise that the bid does not follow

**Arm.** An upward paper position is open and dipole is negative. **At q.** A reported buyer prints above p while exhaustion is negative and the bid is flat or lower. Suspend additions to the upward position.

**Manage.** Release the warning if the bid first rises above q’s bid or exhaustion becomes nonnegative. If a later print first falls below q’s print, issue an exit.

**Why.** A buy can lift the print even while the trade balance leans toward selling. The bid shows whether another buyer has stepped up behind it.

## CX14 · Question a decline that the offer does not follow

**Arm.** A downward paper position is open and dipole is positive. **At q.** A reported seller prints below p while exhaustion is positive and the offer is flat or higher. Suspend additions to the downward position.

**Manage.** Release the warning if the offer first falls below q’s offer or exhaustion becomes nonpositive. If a later print first rises above q’s print, issue an exit.

**Why.** A sale can mark the print down while buying pressure persists. The offer shows whether a seller has actually followed it down.

## CX15 · Enter on a pressure turn at an unchanged price

**Arm.** Exhaustion has a strict positive or negative sign. **At q.** The print, bid and offer equal their respective values at p. Exhaustion now has the opposite strict sign and the reported aggressor agrees with it. Open in that new direction.

**Manage.** For an upward indication close if exhaustion reaches zero or turns negative, or the bid falls below q’s bid. For downward, close if exhaustion reaches zero or turns positive, or the offer rises above q’s offer.

**Why.** The same print price can mask a moving book. Requiring both quote endpoints to match isolates the flow change visible at q.


---

## Earlier proposals preserved

The following is the original v1 freeze. The current paper rules above supersede its one-print management horizon. No historical trial was run.

# Fifteen initial hypotheses · v1

Freeze before downloading any trade-day file. These are proposed event rules. Their signs describe a prospective move in the price of a trade. They never classify a trade by its outcome.

## Read this once for every rule

Use successive natural gas trade prints p, q and u in tape order. Book messages between prints count for settlement and continuity. At p, arm only on the condition given below. At q, the very next trade, check the confirmation. An unconfirmed arm expires at q. A confirmed q is the decision tick and its actual print is the price reference. u, the next trade after q, ends the observation. Record its price alongside the decision price. A move opposite the stated direction contradicts the proposal in that event. An unchanged print leaves the proposed movement unresolved. A new p can be any trade, including a previous q or u. Each arm has its own life. A missing required field cancels that arm. A missing future print leaves the response open. An unknown or marked settlement row, a tape gap or the trade-day boundary breaks the chain. Record interruption without substituting a later price. Decisions are research indications, never fills. No rule is an instruction to execute.

D and E mean the stored 60-second dipole and 20-second exhaustion, read at the print's exact row, in event nanoseconds and tape order. Both are (bought minus sold) divided by (bought plus sold) over their respective spans. Read the displayed best bid and best offer at the specified rows separately. “Up” and “down” name directions only. Every quote inequality is strict where a change is required. Equalities are exact. “Both positive/negative” means D and E at that print. No look-ahead to u decides whether q confirms.

| ID | Situation and stage | Arm on p | Confirm on q and act | Direction to check at u |
|---|---|---|---|---|
| CX01 | Buying pressure, entry | Both positive | Both still positive and print rises from p. Mark entry study. | Up |
| CX02 | Selling pressure, entry | Both negative | Both still negative and print falls. Mark entry study. | Down |
| CX03 | Dipole positive, pullback ends | D positive, E zero or negative | D stays positive and E turns positive. Mark resumption. | Up |
| CX04 | Dipole negative, bounce ends | D negative, E zero or positive | D stays negative and E turns negative. Mark resumption. | Down |
| CX05 | Early warning during a rise | Both positive | D stays positive and E turns negative. Flag an existing upward thesis for review. | Down |
| CX06 | Early warning during a decline | Both negative | D stays negative and E turns positive. Flag an existing downward thesis for review. | Up |
| CX07 | Offer advances, continuation entry | Print equals best offer | Offer rises and q trades at its offer. Mark continuation. | Up |
| CX08 | Bid retreats, continuation entry | Print equals best bid | Bid falls and q trades at its bid. Mark continuation. | Down |
| CX09 | Buyers meet a stationary offer, reversal entry | Print equals best offer and E positive | Offer unchanged and q prints below p. Mark reversal. | Down |
| CX10 | Sellers meet a stationary bid, reversal entry | Print equals best bid and E negative | Bid unchanged and q prints above p. Mark reversal. | Up |
| CX11 | Bid steps up behind buying, active-trade support | D positive | Bid rises, offer unchanged and D still positive. Maintain upward thesis through u. | Up |
| CX12 | Offer steps down behind selling, active-trade support | D negative | Offer falls, bid unchanged and D still negative. Maintain downward thesis through u. | Down |
| CX13 | A rising print meets opposing flow, warning | D negative | Print rises and E negative. Flag the rise for review. | Down |
| CX14 | A falling print meets opposing flow, warning | D positive | Print falls and E positive. Flag the decline for review. | Up |
| CX15 | Prints hold still while pressure changes sides, transition entry | E strictly positive or negative | Print unchanged and E has the opposite strict sign to p. Mark transition in the new E direction. | Sign of E at q |

Management for an entry or resumption is observation from q through u. A warning or support decision manages an already stated price thesis and creates no fresh entry. An adverse u invalidates that indication for this event. Check the bid and the offer alongside the prints to see whether a print move also moves the book. Record terminal and interrupted arms separately. The single following print answers a deliberately narrow question about movement still available after the decision.
