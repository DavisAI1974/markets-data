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
