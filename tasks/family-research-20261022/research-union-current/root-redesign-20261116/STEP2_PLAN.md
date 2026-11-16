# Step 2 plan (Desktop session, started 2026-11-16)

Status: DRAFT. Nothing here is approved, built or run. Each result is gone through with Greg, one at a time,
and its status line is changed only on his word. Claude's calls are marked as calls and are his to correct.

Written from: `STEP2_BRIEF_FOR_DESKTOP.md`, the "Seventh session" section of `ROOT_GAMEPLAN_DECISIONS.md`,
`STEP1_STEP2_LAYOUTS.md` (all in this folder, as of `c1fbb44`), and the old Step 2 documents and programs on Markets
branch `chatgpt/ng-exhaustion-chain-phase2-20260817` (`1bec694`), read and not run.

This session builds nothing, runs nothing, and writes to this file only.

## Decisions (Greg's words)

- 2026-11-16, on where this file is kept (it was pushed to markets-data, he had said "the markets repo"):
  "That repo is fine also"
- 2026-11-16, told that Step 2 found no new events and mostly waits for the grouping:
  "Definitely new results haha. You tell me, what was the origional intent, does it add value, how do we create
  those calcs and if the first things are of no value, then what can we do to create more value with what we have
  and could we fill some possible gaps that you could see"
  Read as: Step 2 is to give new results, not only a re-reading of the old ones, and Claude is to say what it was
  for, what is worth keeping, and what could be added. Claude's answer is the next section. None of it is approved.
- 2026-11-16, on Step 2's own grouping: "And did we have a completely unique way of grouping the famies
  together from what st1 did in the old calcs? If so I'd like to keep that in there. Can't remember off the top of
  my head"
  Answer given: yes, it did (see "Step 2's own grouping" below). Read as: Step 2's own grouping is kept in the
  plan.
- 2026-11-16, the aims for Step 2, after the gaps were put to him: "We can merge our ideas together. Whatever is
  going to give us better more unique real trading signals or eplain the lifecycle of a trade better or dipole
  better and a deeper look into if those two things couple of correlate to again get better trade signals is the
  goals we want to aim at. However we can do those things"
  Read as: his ideas and Claude's are merged into one plan. Its aims are (1) better and more unique real trading
  signals, (2) explaining the lifecycle of a trade better, (3) explaining the dipole better, (4) a deeper look at
  whether the trade lifecycle and the dipole couple or correlate. How it is done is left to Claude to propose.
- 2026-11-16, on how the suggestions are put to him: "Run through all of your suggestions. Do them in one swoop
  instead of a little piece at a time"
  Read as: every suggestion is laid out for him together, in full, as the rest of Step 1 was. It is not read as a
  word to build or run: this session builds and runs nothing, and each calculation is approved by him first. The
  layouts are in "The suggestions laid out together" below.
- 2026-11-16, on the trade legs: "And let's take the next step from step 1 metaphorically and start looking at
  how our calcs start to act in relation some way with the trade legs. Can we take things from st1 and use them in
  some way to start defining trades or dirrerent parts of the trade lifecycle"
  Read as: the step after Step 1 is to lay what Step 1 records against the trade legs, and to use Step 1's turns
  to start defining a trade and the parts of its life. Laid out as I and J in "The suggestions laid out together".
  This corrects Claude's earlier reading of "the lifecycle of a trade": a trade is anchored on a leg, a move in
  price, and Step 1's turns mark the parts of its life.

## The merged plan, by Greg's aims (Claude's proposal, 2026-11-16; nothing approved, nothing built)

**Claude's reading of two words, corrected by Greg the same hour.** "The lifecycle of a trade" was first read
as the life of one peak. On his word about the trade legs it is: a trade is anchored on a leg, a move in price,
and Step 1's turns mark the parts of its life (see I and J). "The dipole" is the Native dipole with its own life: before
birth, birth, recognition, what follows, exhaustion.

Everything sits on the same tick rows, each fact at the tick it became known. Four layers, then the grouping.

1. **Each peak's own life.** Step 1, pieces 1 and 2. Built or being built by the code session. Serves aim 2.
2. **The links between peaks.** The core of the old Step 2, as facts and without letters: the peak before and
   after, same side or not, the times between, whether their stories overlap, the three models' values at each
   step back. Added to it: the state at each tick, meaning how many peak stories are open on each side and how old
   each is. Serves aims 2 and 1.
3. **The book between and during.** For each pair of neighbouring peaks, and for each stage of a peak's life: how
   much resting size was added, pulled and traded on each side, as it happened. Serves aims 2, 3 and 1. This is
   where the signals can be unlike anyone else's: the old work did not read the book, and we hold all of it at
   every tick.
4. **The dipole beside the peaks.** Each recorded Native dipole's birth, recognition and end placed on the tick
   rows at the tick each was known. Then, case by case: for every dipole, where each of its stages falls in the
   story of the peak or peaks around it; for every peak, whether a dipole was alive at that tick and at what
   stage. Serves aims 3 and 4. This was gap 6 below; on his word it moves up to a main part of the plan.

**The grouping stage,** after all four trade days have run all of it, with Greg:
- single peaks, with the Step 1 families A, B and C as the base;
- chains, with Step 2's own groupings as the base (lifespan, pieces, growth);
- dipoles, by what their recorded lives show;
- the coupling: which groupings of one line up with which of the other, each with its list of individual cases.

**Where the signals come from (aim 1).** Claude's view: a signal is something that repeats, ahead of something
else that repeats, seen case by case. So the signals are read at the grouping stage, from layers 1 to 4. Nothing
in the calculations is a signal by itself. The old paper play stays in git as the record. No cost, fee or fill
is assumed anywhere, and no entry or exit time is fixed in advance.

**Two things that have to be settled before layer 4 is laid out.**
- Which record of the dipole is used. The dipole is not yet defined as a ROOT calculation (the decisions file
  lists it among those that need a definition first). What exists is Native's own record of each candidate.
  Claude's call: use Native's record for this look, marked as Native's and not as a ROOT calculation. It can be
  placed on the rows now, and what it shows may help write the definition.
- Whether Native's record was cut on the old day boundaries. To be checked by the code session before anything
  is placed.

**First measurement proposed for layer 4** (for the code session, once approved; nothing is run here): for every
recorded Native birth on the four trade days, the flow of piece 1 at that tick and the nearest peak, listed one
line per birth. Claude's guess, held loosely: many births will sit where the flow is fully one-sided, because the
independent pass of 2026-11-13 found the 20-second ratio at exactly plus or minus 1 in the birth second of every
candidate it had. That pass used the old one-second series, so the list is what will tell us.

## The suggestions laid out together (2026-11-16)

Status: LAID OUT, awaiting Greg's word. Nothing is built or run. On his yes the code session builds; this session
does not.

Five are new calculations (A to D, and I). Four need no new calculation, because the others and Step 1 already
carry them (E to G, and J). One is a way of seeing the result (H). All follow the standing rules: only the four
trade days; a row holds only what was known at its tick; nothing is written back; no fixed marks, labels, caps or
minimum counts; empty is never zero; every trade individually; no cost of trading anywhere.

How anything is stored, the same as Step 1: new columns are their own files beside the rows files, in the same row
order, and no row is added or removed. Facts go in the facts table beside the rows, one line per fact: the tick it
became known, what it is about, what the fact is, its value. Each calculation has one check, run once on that part:
every value recounted from the stored rows by a different method, and playback equal at two cuts.

### A. The links between peaks

**What we want.** For every peak, how it stands to the peaks around it, written as facts. This is the chain,
without letters and without a depth.

**What the old work did.** Put the events of a week in order and read the 2, 3 or 4 before each one as a string
of state letters. Left out an event when one before it had ended less than 60 seconds earlier, or when the next
one began before its ending was confirmed. Never ran across a week boundary.

**What is written.** Facts, at the tick a peak becomes known, naming that peak:
- The last peak on its own side, and the last peak on the other side. For each: the tick of its high, the time
  between the two highs, the last trade price at each high, and whether that earlier peak's story was still open
  at this tick. Whichever of the two is nearer is "the peak before".
And at the tick a peak's story ends:
- How many later peaks had already become known while its story was open, and the first of them.

**Claude's calls.**
- One link back on each side, not a list of every earlier peak. Any earlier peak is reached by following the links
  back one at a time, so nothing is capped and nothing is repeated.
- No peak is left out for being close to another or for overlapping. Overlap is a fact.
- A link never crosses 6 pm. The first peak of a trade day on each side has that link empty, with the reason.
- "Before" goes by the tick a peak became known, since that is the order a reader meets them in.

**Not promised.** Nothing about how many peaks overlap. Reported after the first trade day.

**Needs.** Piece 2 (for when a story is open or ended). The three models' values at each step back are piece 4 and
stay with the code session's layout.

### B. The state at each tick

**What we want.** At any tick, what is in play: which peak stories have not ended yet, on each side. This is what
the old result 3 called a rolling state, recorded directly.

**What the old work did.** Did not record it. It was inferred afterwards, from strings of four state letters and
model scores.

**What is written.** New columns on every row, for the buy side and for the sell side:
- how many peak stories are open at this tick;
- how many of those have reached zero and not yet come back;
- the tick of the high of the oldest open one, of the newest open one, and of the largest open one.

**Claude's calls.**
- "Open" means the peak has become known and its story has not ended, by piece 2's own ending (coming back,
  beaten, or 5 pm).
- These are counts and places on the tape. No average is taken.
- With no open story on a side, its three tick columns are empty, not zero.

**Not promised.** How many stories can be open at once. Reported after the first trade day.

**Needs.** Piece 2.

### C. The book through a peak's life and between peaks

**What we want.** What happened in the resting orders while the flow rose, peaked and faded, and from one peak
to the next: how much size was added, pulled and filled, on each side.

**What the old work did.** Step 1 took one figure: the average imbalance of the top 10 levels over seconds 41 to
60 after the peak, and its change from the 20 seconds before. Step 2 did not read the book.

**What is written.** New columns on every row: running totals since the 6 pm open of the trade day, for the bid
side and for the ask side:
- size added (a new order, or an order made larger);
- size pulled (a cancel, or an order made smaller);
- size filled (traded away);
- size moved (an order changing price: it leaves one line and joins another).
Each total is kept twice: for the whole side, and for actions at the best price of that tick.

With running totals on every row, the amount between any two ticks is one subtraction. So the book between two
peaks, or between any two turns of a peak's story, or across a stage of a dipole, is read straight off the two
rows that the facts already name. No stretch of time is picked in advance.

**Claude's calls.**
- Running totals are sums of single messages, each of which stays on its own row. They are not averages.
- They start at zero at 6 pm, as the flow does. The book itself carries over; only the counting of activity
  starts fresh.
- A change of price is counted as moved, not as pulled and added, because nothing left or joined the side.
- "At the best price" is read from the book at that tick. How far from the best price each single action
  happened is already on its row, so no number of levels is picked.
- Trades the tape gives no side for are counted in their own column, as in piece 1.

**Not promised.** Nothing about what the totals will show.

**Needs.** Only the stored rows. It does not wait for piece 2 and can run beside it.

### D. The dipole beside the peaks

**What we want.** Each Native dipole's life on the same rows as the peaks, so that for every dipole, and for every
peak, we can see case by case how the two stand to each other.

**What the old work did.** Never put them together. The exhaustion chain work (August 2026) and the dipole work
(October 2023 trade days) were done apart.

**What is written.**
- Facts, at the tick each stage of a dipole could first be known: its birth, its recognition, its end. Each names
  its dipole and carries Native's own time for that stage beside the tick it is placed at.
- On each of those fact lines, the peaks in play: the nearest peak on each side (the tick of its high), the time
  since that high, and whether its story was open, past zero, or ended at this tick. The flow at that tick is
  already on the row.
- On the line where a peak becomes known: whether a dipole was alive at that tick, which one, its side against
  the peak's side, the time since its birth, and whether it had been recognized yet.
- Columns on every row: how many dipoles are alive at this tick, on each side.

**Claude's calls.**
- Native's own record of each candidate is used, marked as Native's and not as a ROOT calculation. The dipole is
  not yet defined in ROOT; what this shows may help write that definition.
- A stage is placed at the tick it could be known, not at the time of its label. Where the two differ, both are
  kept. (The independent pass of 2026-11-13 found the two differ.)
- Native's candidate number ties the lines together. It is a label and never an input.
- A candidate whose record falls outside the trade day as now defined (6 pm to 5 pm) is listed for Greg and not
  placed.

**To settle first.** Whether Native's record was cut on the old day boundaries. The code session checks before
anything is placed.

**First thing to come out of it.** One line per recorded birth: the flow at that tick, and the nearest peak on
each side. Claude's guess, held loosely: many births will sit where the flow is fully one-sided. The list is what
will tell us.

**Not promised.** That every Native candidate can be placed, or how many there are per trade day.

**Needs.** Piece 1 (built), then A and B for the peaks in play.

### E. The shape carried along the chain (no new calculation)

Piece 2 already records each peak's rise and fade turn by turn. The links of A put those in order along a chain.
So a chain's shape is every member's own recorded shape, one after another, with nothing reduced to a letter.

### F. Where in the trade day (no new calculation)

The clock, the trade day, the 5 pm to 6 pm stretch and the settlement window are on every row. The old Step 2
did not use them. At the grouping stage they are one more thing every peak, chain and dipole is looked at
against.

### G. The small peaks (no new calculation)

Every peak is kept, with its size and its standing so far in the trade day on its row. A to D treat every peak
alike. No size is picked to separate small from large; whether size separates them is seen at the grouping stage.

### H. One render per instance (a way of seeing, made after A to D exist)

One picture per peak with its chain, and one per dipole: its whole life from before to after, with the layers
stacked on the same clock. The layers: the flow, the peak's turns, the open stories on each side, the book totals,
the price, the dipole's stages. Drawn from the stored rows and facts, with the plotted points reconciled to the
rows on every chart. No part of a life is cut away from the rest.

Claude's call: the program draws any instance on request, and all the dipoles. How the full set for 34,278 peaks
is delivered is asked once the first ones are in view.

### I. The legs beside the peaks (added on Greg's word, 2026-11-16)

**What we want.** Every leg on the same rows as the peaks, so that for every leg, and for every peak, we can see
case by case how the flow and the move in price stand to each other. This is the step after Step 1: what Step 1
records, laid against the trade legs.

**What the earlier work did.** The leg was made from trade prices: a run of prints stepping one way. The
independent pass of 2026-11-13 measured 23,615 such legs on the four dates. Of the 13,661 legs one print tick
long, the quote did not move with the leg in 85.6 of 100: the prints were going back and forth between the bid
and the ask. Of the 32 selected cases, the 8 large lasting ones were moves of the quote of 3 to 8 ticks. That pass
could not see the quote between trades. The eight trade types (large or small, up or down, lasting or brief) were
names given by how each leg turned out.

**What is different now.** The rows carry the best bid and the best ask at every tick, with a mark on the tick
each one moves. So a move in price can be read from the quote itself, at every tick, and not only where a trade
happened to print.

**What is written.**
- The quote's own runs, as facts at the tick each becomes known, the same way a peak's story is written: a run of
  the best bid starts, each new furthest price it reaches, and its first step back. The same for the best ask.
- The print leg as the earlier work defined it, unchanged, placed on the rows at the tick each of its turns
  became known. It is Greg's existing material and stays.
- On each leg fact line, the peaks in play: the nearest peak on each side (the tick of its high), the time since
  that high, and where its story stood (rising to its high not yet known, fading, past zero, ended).
- On each peak fact line (the high becoming known, each new low, reaching zero, coming back, beaten): the run of
  the quote in progress at that tick on each side, which way it is going, how far it has gone so far, and the time
  since it started.

**Claude's calls.**
- The best bid and the best ask are followed separately. They are not combined into a midpoint, which is an
  average of two prices.
- A run ends at the first step back, whatever its size. No minimum length and no minimum size: one-tick runs are
  kept, as every peak is kept.
- The eight trade types are not assigned in advance (his rule on labels). They are the base for grouping legs at
  the grouping stage, as A, B and C are for peaks.
- A run never crosses 6 pm.

**To settle first.** Whether the earlier print legs were cut on the old day boundaries. The code session checks,
as for Native's record.

**Not promised.** How many runs of the quote there are. Reported after the first trade day, and Greg hears before
anything is capped.

**Needs.** The quote's runs need only the rows and can run now, beside C. The lines that name peaks need piece 2.

### J. The parts of a trade's life, from Step 1's turns (no new calculation; a way of defining)

Greg asked whether things from Step 1 can be used to start defining trades or the parts of a trade's life.
Claude's answer: yes. Each thing Step 1 records about a peak is a turn at a known tick, and a part of a trade's
life can be defined as the stretch between two turns. No length of time and no level is picked.

| Turn, as Step 1 records it | The stretch it opens |
|---|---|
| The low the rise started from | The flow building on one side |
| The high | The push at its most one-sided |
| Each new low of the fade | The push giving out, step by step |
| Reaching zero | The push spent |
| Coming back, or beaten by a larger peak | The same side pushing again |
| A peak on the other side becoming known | The other side taking over |

Beside these go the leg's own turns from I: the quote starts to run, reaches its furthest price, takes its first
step back.

A trade is then anchored on a leg, with the peak stories around it as its parts: what the flow was doing before
the quote started to run, while it ran, and after its first step back. Which of Step 1's turns the leg's turns sit
on, and in what order, is not assumed. It is read from the lines of I, case by case, and the definition of each
part is settled with Greg at the grouping stage from how they line up.

Claude's guess, held loosely: the quote's run and the flow's rise will not line up the same way in every leg. In
the eight large lasting cases of 2026-11-13, the buying and selling in the 5 seconds before the leg leaned with
the leg in two, against it in two, and was even in four. The lists of I are what will tell us.

### The order they can be built in

- C and the quote's runs of I now, beside piece 2. They need only the rows.
- A and B after piece 2.
- D and the rest of I after A and B, once the checks on Native's record and on the earlier legs are done.
- H after D and I, with the legs as one more layer.
- Then the grouping stage, with Greg. J is settled there.

### Every call of Claude's in this layout, in one place, his to correct

1. A trade is anchored on a leg, a move in price. The parts of its life are the stretches between Step 1's turns
   (corrected on Greg's word; see J).
2. Links: one back on each side, followed back as far as wanted; no cap.
3. No peak left out for closeness or overlap.
4. Nothing crosses 6 pm.
5. Book totals: added, pulled, filled, moved; whole side and at the best price; from zero at 6 pm.
6. The dipole: Native's own record, marked as such, placed at the tick each stage could be known.
7. Renders: any instance on request, all dipoles; delivery of the full peak set asked later.
8. The old paper play stays in git as the record and is not carried into the calculations.
9. Legs: the quote's own runs are recorded, best bid and best ask separately, no midpoint, no minimum size; the
   earlier print legs are kept unchanged beside them.
10. The eight trade types are the base for grouping legs later, not assigned in advance.

## The original intent, what is worth keeping, and the gaps (Claude's view, put to Greg 2026-11-16)

Everything in this section is Claude's reading and proposal. The two quoted purposes are from the old documents.

### What Step 2 was meant to do

From the study contract of 2026-08-17 (`NG_EXHAUSTION_CHAIN_STUDY_CONTRACT_20260817.json`):
- Step 1 was to find the chains with nothing named or sorted in advance. The contract sets "no naming until
  frozen" and marks predefined categories, a predefined long or short cut-off and a predefined number of groups all
  as false.
- Step 2 was then to "describe and categorize already-discovered chains based on the characteristics they actually
  exhibit", with the names given afterwards.
- It listed twelve characteristics to look at. They are in the table below.

From the gate into Phase 2, the same day: after describing the chains, turn the strongest of what was found into a
paper play.

So the intent had two halves: describe the chains by everything they show, then make a paper play. The first half
is the same rule Greg set on 2026-11-16: let the data be what it is, and group afterwards.

### What it looked at, of the twelve

As far as the 22 Step 2 documents and the two Step 2 programs show.

| Characteristic the contract listed | Looked at in Step 2 | What ROOT holds for it now |
|---|---|---|
| The sequence of sides | Yes: same side or other side between neighbours | The side of every peak, off the tape |
| Family A, B or C | Not found in any result | Not assigned; the base of the grouping later |
| Family A's state after | Not found | Not assigned |
| The four after-states | Yes. This was the main lens: the letters S, O, P, X | Replaced by what piece 2 records |
| The shape of the exhaustion curve | Not found | Every new low of the fade and the low the rise started from (piece 2) |
| Late flow | Only inside the letters (it split S from O) | Bought and sold size on every row |
| The book, 10 levels, and its change | Once, as one of several inputs in a search for a rule to set some cases of one branch aside; no rule was found | The whole book at every tick |
| When the ending came | Yes, as the point the entry was timed from | Reaching zero and coming back, as measured |
| Price after the ending | Yes, at fixed seconds | The price on every row |
| Time between events | Yes: the time a chain took, and the timing groups | Measured for every pair of peaks |
| Time of day and place in the session | Not found | On every row |
| Hours since the weekly reopen | Not found | On every row |

About five of the twelve were looked at. The chains were read almost entirely through four letters, the side, and
the price at fixed seconds. A good share of the work then went to the paper play and how to manage it (results 5,
6, 7 and 12).

### What is worth keeping

Claude's view. These are leads to look at again, not answers: they were read from about a tenth of the peaks,
through four letters.
- **The recent few peaks carry it, not one old origin** (result 3). It says where to look: a short stretch of
  recent stories.
- **The same short pieces turn up inside different chains** (results 8 and 9). This fits Greg's word that the data
  will group "more ways than one with different pieces in different groups".
- **Chains come in distinct lengths of time** (result 10).
- **Cases that go the other way are kept and taken apart** (result 11). Already his rule.

What adds little at this stage: the paper play and what follows it (results 5, 6, 12) answer a trading question,
which comes after we know what dictates what happens next. Result 1 is built into ROOT already, since a row holds
only what was known at its tick.

### How the calculations are made

Two steps.
1. **Now, with no labels: the links between peaks, as facts.** For every peak: the peak before and after, same
   side or not, the times between, whether their stories overlap, and the three models' values at each step back
   (piece 4). To this are added the characteristics below, measured on each link.
2. **At the grouping stage: the descriptions.** How often a piece recurs, which pieces go on, what lengths of time
   there are. Each is read from the facts of step 1 and keeps its list of individual cases.

### Gaps that could be filled with what we hold

Each is a proposal. None is approved and none is laid out in detail yet. Each would be a measured fact per peak or
per pair of peaks, with no label and no fixed mark.

1. **The book between two peaks.** From one peak's high to the next: how much resting size was added, pulled and
   traded on each side, as it happened. The old Step 2 did not look at the book. We hold all of it at every tick;
   the old work had 10 levels once a second.
2. **The shape carried along the chain.** A peak's rise and fade as piece 2 records them, kept whole for each
   peak in a chain and not reduced to a letter.
3. **The state as it stands at each tick.** How many peak stories are open on each side at that tick, and how old
   each is. This is result 3's "rolling state" recorded directly, without letters.
4. **Where in the trade day.** Time since the 6 pm open, the settlement window, the 5 pm to 6 pm stretch. On the
   rows already; Step 2 did not use it.
5. **The small peaks.** About nine in ten of the peaks were never seen by the old Step 2. Whether small ones sit
   between large ones in a way that repeats is open.
6. **The dipole lifecycle beside the peaks** (moved up to layer 4 of the merged plan on Greg's word). The Native dipole births are read
   from the same 20-second flow. Whether each birth sits on or beside one of the 34,278 peaks is not measured; a
   count would settle it.

## Step 2's own grouping (KEPT, on Greg's word 2026-11-16)

Step 2 did not use the Step 1 families. A, B and C do not appear in any of its 22 documents. It made its own
grouping, and of a different thing.

| | Step 1 | Step 2 |
|---|---|---|
| What is grouped | One event | A whole chain |
| By what | The shape of the 60 seconds before the peak | How long the chain lived, and what pieces it is made of |
| How | Nearest of three fixed centres; every event put in exactly one | Groups read from the measured values; one chain sits in more than one grouping |

Step 2's groupings, in its own words where quoted:
1. **By how long the chain lived** ("timing / lifespan families"). At depth 2: about 126 s, 215 s, and a rare
   long group about 798 s. At depth 3: about 211 s and 609 s. (Result 10.)
2. **By the pieces inside** ("modules"). Pairs and triplets of states with the side relation between neighbours,
   such as PP|S, that recur inside chains that are otherwise different. (Result 8.)
3. **By which pieces grow into longer chains** ("extension families"). The old documents speak of "multiple
   short-to-long growth families rather than one universal chain-growth grammar". (Result 9.)
4. **A delayed group, named but not worked out.** Cases against the trade at +60 seconds that came back later: "a
   delayed/re-origin family", to be discovered separately "instead of forcing every valid instance into a fixed
   +60 outcome".

The part that is Step 2's own idea: these are separate axes. "Module identity and timing family are separate
axes." The same chain has a lifespan group and its piece groups at once, and the lifespan groups held steadier
from block to block than the pieces that filled them.

How it is kept (Claude's call, following his word on the old Step 1 families): it is not applied inside the
calculations. At the grouping stage it is the base for grouping chains, as A, B and C are the base for grouping
single peaks: the new values are looked at against the old lifespan centres and the old pieces, to see the same
groups, different ones, or the same with additions. What has to be written per peak now so that this can be done
later is already on the list below: the time back to each earlier peak, the side relation, and the three models'
values.

## What reading Step 2 against the rules shows

Put to Greg first, because it bears on all thirteen results.

1. **Step 2 made new results from the same events.** It found no new events: it read the Step 1 event table and
   described it, by counting, timing and comparing. So the old Step 2 adds very little to a tick row. Almost all of
   it is a reading of what Step 1 wrote.

2. **Nearly all of it is written in state letters, chain depths, or both.** Under the rule "no labels, groups or
   identifiers until all four trade days have run all their calculations", neither exists while the calculations
   run. The parts that need neither are few: which side a peak is on against the peaks before and after it
   (results 7 and 13), and the times between peaks (results 2 and 10).

3. **So Step 2 falls into two parts** (Claude's reading, his to correct):
   - A small part that can be written per peak before any grouping. Listed under "What can be written per peak
     now".
   - The rest, which is made at the grouping stage, from the per-peak values, once the groups have shown
     themselves.

4. **The pooling is of two kinds.**
   - Pooled by the nature of the question. "How often does this piece recur" or "what share went on" has no
     answer for one case. Results 1, 3, 8, 9, 10 and 13, and the counts in result 2.
   - Pooled only in how it was reported. Results 2 (the times), 4, 5, 6, 7 and 12. In these the old programs
     worked out a value for every case, then wrote out only the mean, the median or the count. The individual
     values were not written out, and the event tables they were made from have expired.
   Under his rule both kinds keep their individual values, and the pooled figure sits beside them as an addition.

5. **"The peaks before" is not the same thing it was.** The old strings (S,S,O,S and the rest) were strings of
   the old events, about 850 a UTC clock day, none within 45 seconds of a stronger one. In the old paper play the newest of the
   four events before was a median 123 seconds back and the oldest a median 467 seconds back. Now there are
   34,278 peaks over the four trade days, about one every 9 or 10 seconds, and their stories overlap. Counting
   back four peaks now covers a much shorter stretch of time than counting back four old events did.
   Claude's call: count back over every peak, since none is held back. Each peak's size and its standing so far in
   the trade day are already on its row, so the grouping stage can look at the larger ones on their own.

## What can be written per peak now (no labels, no fixed marks)

Claude's proposal. Not approved. The code session builds; this is only the list.

- **The peak before, and same side or not.** Already decided with the chain link (piece 4).
- **The time back to each earlier peak** that the chain link values are written for: from this peak's high to that
  peak's high. A measured time, nothing more.
- **Whether the next peak became known before this one's story ended,** and the time between the two. The old
  programs left such cases out. Here it is a fact about the peak and nothing is left out.
- **The three models' values at each step back.** Piece 4, decided as B, to be laid out by the code session after
  piece 2 exists.

Price is not added: the last trade price is on every tick row, and piece 2 records the price at each turn of a
peak's story.

## The thirteen results

Each in his form: what we want, what it did, what changes. Then what individual values lie underneath, and
whether the pooling was on purpose.

### Result 1: the causal region

Status: not yet gone through with Greg.

**What we want.** To know whether the earlier peaks still tell us something about a peak when only what was
already known at the time is used.

**What it did.** Took the three models' gains at depths 2, 3 and 4, using only information known 30 or 60 seconds
after an ending. Reported one mean gain per model for the five discovery blocks of weeks together, for the
confirmation block and for the held-back week, with a shuffle test value. All were above zero.

**What changes.**
- The 30 and 60 seconds are marks picked in advance. They go. In ROOT a row holds only what was known at its tick,
  so the "known at the time" condition is already how every value is made.
- No blocks of weeks. Each trade day's peaks are scored by models taught on the other three (piece 4 as played
  back to Greg). That gives four trade days to look across, not blocks.
- Depths 2, 3 and 4 are not picked in advance. The values are written for each step back, and how far to go is
  settled with him from the values.

**Underneath.** For every peak, each model's own gain at each step back. Piece 4 writes these.

**Pooling.** On purpose: "does it stay above zero" is asked over many peaks. It is an addition, made after the
per-peak values exist. Nothing new is built for this result.

### Result 2: short and long chains

Status: not yet gone through with Greg.

**What we want.** How far back the link between peaks reaches, and how much time that covers.

**What it did.** Out of 156,422 scored events, counted how many reached each depth: 20,562 at depth 1 or more,
1,725 at 2 or more, 133 at 3 or more, 9 at 4 or more, 1 at 5. Gave the median time a chain took at each depth:
65 s, 143 s, 216.5 s, 279 s, and 2,477 s for the one chain of depth 5.

**What changes.**
- A depth is a label made from the model values (all three models above zero, counted back one step at a time).
  It is not written in advance. The values it was made from are.
- The time is written per peak, for each step back.
- No depth cap. The old programs stopped at 12 steps back (6 in the causal version).

**Underneath.** Per peak: the time back to each earlier peak, and the three model values at that step.

**Pooling.** The counts are pooled by nature. The median times were only how it was reported; each chain had its
own time.

### Result 3: one origin, or rolling

Status: not yet gone through with Greg.

**What we want.** Whether a long chain is one old peak whose effect carries on, or a state that is refreshed by
the last few peaks.

**What it did.** On the held-back week, compared neighbouring depths for chains from the same origin: the odds
ratios were near 1 for all three models. Then took the S,S,O,S cases and split them by the state of a fifth, older
event: the mean move stayed above zero in each of the four splits (+0.083, +0.425, +0.239 and +0.308 ticks). Read
as: the last four states carry it, not one old origin.

**What changes.**
- The second half is written in state letters, so it waits for the grouping.
- The first half reads the model values at neighbouring steps back, which piece 4 writes per peak. It can be
  looked at across the four trade days once those exist.
- The four in "the last four" came from the old events. See point 5 at the top.

**Underneath.** Per peak: the model values at each step back, and which earlier peak each step is.

**Pooling.** On purpose: an odds ratio is a statement about many cases. Nothing new is built for this result.

### Result 4: the play search

Status: not yet gone through with Greg.

**What we want.** Whether what the last few peaks did says something about what price does after the next one.

**What it did.** Took the exact string of state letters of the 2, 3 or 4 events before, sometimes split by
whether the current event was on the same side as the one before. Measured the price move from 5 seconds after
the current event's ending to 30 or 60 seconds after. Reported, per string, the mean move in each block of weeks,
the share of weeks above zero and a shuffle test value. Only events that passed its conditions entered. For the
four-before case that was 50,658 of the 235,170 events (about 22 in 100). Left out were events whose ending was
not confirmed within 5 seconds, events whose next event began before the ending was confirmed, and events where
one of the events before had ended less than 60 seconds before it began. No string ran across a week boundary.

**What changes.**
- Strings of letters need the groups. This is made at the grouping stage.
- The 5, 30 and 60 seconds are marks picked in advance. They go. Claude's call: nothing is put in their place. The
  price is on every tick row, and piece 2 records it at each turn of a peak's story.
- No event is left out for being close to another. Whether peaks overlap is recorded as a fact (see the list
  above).
- No blocks of weeks.

**Underneath.** Per peak: its own story (piece 2), the peaks before it, and the price on the rows after it.

**Pooling.** Reporting only. The program worked out a move for every case and wrote out only the mean per string.

### Result 5: the frozen paper play

Status: not yet gone through with Greg. One question for him below.

**What we want.** A rule that could be followed on paper to see whether one pattern held up going forward.

**What it did.** `NG_CHAIN_D4_SSOS_CONTINUATION_V1`: the four events before read S,S,O,S; enter on the current
event's side 5 seconds after its ending, leave 30 seconds after. 1,242 cases among 49,832 in the 54 base weeks,
mean +0.256 ticks, stated before any cost. 27 cases in the held-back week, mean +0.815 ticks.

**What changes.**
- It is a rule with a fixed entry and a fixed exit, written in state letters. Both are ruled out inside the
  calculations.
- It is a trading rule, not a measurement of the market. Claude's call: it is not a ROOT calculation and nothing
  of it is written on the rows. The old rule stays in git as it is.
- If it is wanted later, it is laid against the groups once they exist.

**Underneath.** The 1,242 individual moves. They were worked out by the old program and not kept.

**Pooling.** Reporting only.

**Question for Greg.** Is the paper play to be carried into ROOT in any form, or left as the old record until
after the grouping?

### Result 6: after the exit

Status: not yet gone through with Greg.

**What we want.** After one setup has played out, how long until the next one, and what happens in between.

**What it did.** For 666 P,O,X cases in the base weeks: 650 reached another full setup before the weekly close.
Median wait 14,462.5 seconds (about 4 hours), a quarter under 6,982 seconds, a quarter over 25,956 seconds.
Median of 178.5 events in between.

**What changes.**
- "A setup" is defined by letters and by the two plays. It waits for the grouping.
- The wait ran to the weekly close. Now nothing runs across 5 pm. Claude's call: a wait still running at 5 pm is
  recorded as still open at the end of the trade day, as an open peak is.

**Underneath.** Per case: its own wait and its own count of events in between. Worked out by the old program, not
kept.

**Pooling.** Reporting only for the medians. The count of how many reached another setup is pooled by nature.

### Result 7: opposite and same side branches

Status: not yet gone through with Greg.

**What we want.** Whether it matters that the current peak is on the same side as an earlier one or the opposite
side, and what price did in each case.

**What it did.** Split P,O,X cases by whether the current event was on the opposite or the same side as the last
X event. Opposite: 207 cases over 36 weeks, mean about +0.401 ticks. Same side: sorted the cases that were below
zero at +60 seconds into "shallow" (no worse than 1 tick against at +30 s, exactly 1 tick against at +60 s) and
"deep" (2 ticks or more against at both), and gave the share of each that was back to zero or better at +120 or
+300 seconds: 20 of 30 against 1 of 11.

**What changes.**
- Same side or opposite side is read off the tape. It is not a label, and it is written per peak now.
- "Shallow" and "deep" are groups made from fixed tick marks at fixed seconds. They go. How far price went
  against a peak, and when, is on the rows; whether it separates into groups is seen at the grouping stage.
- P,O,X needs the letters.

**Underneath.** Per case: the side relation, and the price on the rows after.

**Pooling.** The means were reporting only. The shares and the test value are pooled by nature.

### Result 8: reusable pieces

Status: not yet gone through with Greg.

**What we want.** Whether the same short piece (two or three peaks in a row, of given kinds) turns up inside
chains that are otherwise different.

**What it did.** Inside chains of depth 2 or more, counted each pair and triplet of state letters together with
whether each neighbour was on the same side or the other side. PP|S, two persistent events on the same side, was
counted 291 times before the held-back week and 38 times in it. Wrote the count, the number of weeks and the
number of different whole chains it sat in. A piece counted fewer than 3 times was not shown, and only the first 50 of
each size were shown.

**What changes.**
- Needs the letters and the depths. Made at the grouping stage.
- The minimum of 3 and the first-50 cut come off. Every piece is kept with its count.
- The same-side part is available now.

**Underneath.** Every occurrence: which peaks, in which chain, at which ticks. The old program did not write
these out.

**Pooling.** On purpose. "How often does it recur" only exists over many cases. The list of occurrences is kept
beside the count.

### Result 9: which pieces extend

Status: not yet gone through with Greg.

**What we want.** Whether a chain that starts with a given pair is more likely to go on.

**What it did.** For each pair at the start of a chain of depth 1 or more: the share that reached depth 2,
against the share for all pairs in the same block of weeks. PP|S came out at 1.27, 1.22, 1.29 and 1.20 times the
block's share. A pair needed 30 cases to be shown, only the first 80 were shown, and the first 18 weeks were left
out.

**What changes.**
- Needs the letters, and "reached depth 2" is a label.
- No blocks of weeks: the comparison share would be per trade day or over the four.
- The minimum of 30 and the first-80 cut come off.

**Underneath.** Per chain start: which pair it was, and the model values at the next step back.

**Pooling.** On purpose. A share only exists over many cases.

### Result 10: timing families

Status: not yet gone through with Greg.

**What we want.** Whether chains come in distinct lengths of time.

**What it did.** Fitted a mixture model to the log of the time each chain took. The number of groups was chosen
by comparing fits with one, two and three groups, and then fixed in the program: three at depth 2 (centres about
126 s, 215 s and 798 s; 947, 380 and 52 chains) and two at depth 3 (about 211 s and 609 s; 83 and 10 chains). The
freeze document calls the centres a description and not cut-offs.

**What changes.**
- This is a grouping. It belongs to the grouping stage, after all four trade days have run.
- The groups are a model's fit. Under "let the data be what it is" the times themselves are looked at first.
- Claude's call, following his word on the old families: the old centres are the base that the new times are
  looked at against, to see the same groups, different ones, or the same with additions.

**Underneath.** Every chain's own time. Written per peak (see the list above).

**Pooling.** On purpose, as a grouping. It never stood in for the individual times in principle, but the old
output kept only the centres and the counts.

### Result 11: the cases the old work called failed folds

Status: not yet gone through with Greg.

**What we want.** When a pattern goes one way in most stretches and another way in one, to find out why, and
never to delete the cases.

**What it did.** A policy, named FLAG_AND_DECOMPOSE: keep every case on both sides, bring back one more event of
context, and look again. Example: O,O,O followed by a change of side came apart into four different behaviours
once the event before was added (X, P, O or S in front). The program behind it took the 1 to 4 events before,
measured the move from 5 to 60 seconds after the ending, and showed a pattern only if it had 20, 12 and 6 cases
in the three blocks.

**What changes.**
- The policy already matches his rules. It carries over as it is: nothing is removed because it differs.
- With no blocks, the same is done when one trade day differs from the others.
- The minimum counts and the fixed 5 and 60 seconds come off.

**Underneath.** Each case with its own context and its own move.

**Pooling.** The policy has none. The means behind the example were reporting only.

### Result 12: the novelty screen

Status: not yet gone through with Greg.

**What we want.** A list of other recurring patterns worth a look, apart from the two already known.

**What it did.** Took out every case already covered by S,S,O,S or P,O,X-opposite, then listed other strings
whose mean move kept its sign in every block (O,O,S,S then a change of side; S,O,O,S then the same side; and
others). The freeze document calls it a queue for later and not a set of plays.

**What changes.**
- Needs the letters and the two plays. Made at the grouping stage, if wanted.
- "Kept its sign in every block" has no blocks to hold across.

**Underneath.** Each case with its own move.

**Pooling.** Reporting only.

### Result 13: aftermath checks

Status: not yet gone through with Greg.

**What we want.** After a peak, which side the next one is on, and what price does.

**What it did.** On 3,429 events from three weeks of 2025: split events by whether the flow was still alive 60
seconds after the peak or had collapsed, and gave the share whose next event was on the same side. Counting only
next events that began after the 60 seconds: 57.58 and 58.15 in 100 for alive (the two halves of the sample),
53.66 and 54.46 in 100 for collapsed. Also gave shares of price moves named continuation, reversal or chop by a
2-tick rule.

**What changes.**
- "Alive at 60 seconds" is a fixed mark. Piece 2 records the time the flow reached zero, whatever it was.
- The 2-tick rule and its three names go (already ruled in piece 2).
- Which side the next peak is on is written per peak now. It needs no letters.

**Underneath.** Per peak: the side of the next peak, the time its own flow took to reach zero, the price after.

**Pooling.** On purpose for the shares. They are an addition to the per-peak facts.

## What cannot be made on four trade days

- **Anything that rested on holding across blocks of weeks** (results 1, 4, 5, 9, 12). There are no blocks and no
  held-back week. What there is: four trade days, each scored by models taught on the other three.
- **Deep chains as a group.** The old work counted 9 chains of depth 4 and 1 of depth 5 in 156,422 scored events.
  Not appearing in four trade days is "not seen yet".
- **Result 6 as it was.** The old wait ran to the weekly close, with a median of about 4 hours and a quarter of
  the waits over 7 hours. A trade day ends at 5 pm.
- **Shuffle tests that used the week as the unit.** The four trade days sit in two weeks.
- **A number-for-number comparison with any old result.** The old work shares no dates with the four trade days
  and its event tables have expired.

## Questions for Greg, one at a time

1. The order: the per-peak facts now, and the letter and depth results at the grouping stage. Is that how he wants
   Step 2 to run?
2. Result 5: is the paper play carried into ROOT in any form, or left as the old record until after the grouping?
3. Point 5 at the top: counting back over every peak (Claude's call), or some other way.
