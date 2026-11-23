# Handoff R, end of the fifteenth session (2026-11-23)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff Q as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Fifteenth session" and the entries after it (the last
entries are the newest). Desktop writes to the same branch: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. ADD to it; never
   start another. Its sections dated 2026-11-23 govern where they differ from what is above them. EVERYTHING in it
   that speaks of "the dipole at the tick", "the exhaustion at the tick", runs of trades as an exhaustion or
   stretches of the dipole is a record of work that was DELETED and is not to be used.
3. The decisions file, from "Fifteenth session" to the end of the session entries.
4. Markets `CLAUDE.md` on `ccr-b66f34d5-h6ra1t`: the rule "DIPOLE AND EXHAUSTION MEAN THE CRYPTO FORMULAS".

**Do NOT open last week's strategy material** (the handoff and review of 2026-11-13, the fifteen candidates, the
selected cases). Nothing of it is used.

## FIRST: THE MIDPOINT HAS TO BE DISCUSSED WITH GREG (his word at the close)

"Be sure to note in the handoff that midpoint has to be discussed". Do not build on the mid price, store it, or put
it in a sheet until this has been talked through with him. What is known, so the talk starts from facts:
- The price line in the stored `trade-renders/` pictures is the MID price: halfway between the best bid and the
  best ask. It was Claude's call, made because the crypto dipole picture's price was the mid
  (`_dipole_price_overlay.py`, Markets `75b15fa`). Greg never said "mid".
- THE MID IS NOT A STORED COLUMN ANYWHERE. It is worked out inside the picture program (`root/trade_renders.py`,
  `quotes`) and inside the crypto and ng run for the program's own use. It has not been approved as a calculation.
- The best bid and the best ask ARE stored columns on every tick (`best_bid`, `best_ask`, `gap`, and the four
  "moved from / moved to" marks; `root/rows.py`, sections D and E), and in the Excel short-stretch file.
- His read of the two test pictures: "Price is either a mix of or closely resembles one in shape and movement which
  is interesting." Said to him: the mid is exactly halfway between the two, so "a mix" is how that line is made.
  What is not made that way is WHICH of the two stepped at each move.
- Per tick the mid only ever moves by half a tick, so the "how fast the price changes" graph has strokes of one
  height: it says when and which way, never how much.
- Things to settle with him, none decided: whether the mid is the right price line at all (against the trade
  prints, the best bid, the best ask, or the side the trade was made on); whether it becomes a stored column and
  goes into the Excel sheets; whether the price rate graph stays.

## Where it stopped, in Greg's words

"It's alright that it's blocky. I see what I wanted to. Price is either a mix of or closely resembles one in shape
and movement which is interesting. Is that already a separate column in the spreadsheets?" (answered: yes, see
above); then "Create the handoff and print the drop in for a new chat. Be sure to note in the handoff that midpoint
has to be discussed".

No pod is running. The account was read at the end and shows none.

## What he decided this session (do not re-ask)

- DIPOLE AND EXHAUSTION ARE THE CRYPTO FORMULAS. "We should not be reinventing the wheel! The instructions should have
  been explicit to follow the crypto formulas." One figure, bought minus sold over bought plus sold over the trades
  of a span of time, read at the nanosecond: the EXHAUSTION over the last 20 seconds, the DIPOLE over the last 60
  seconds. Both are STORED (`crypto-ng-tick/`). "Ticked by nano" is the time of the read, never a new formula. The
  20 and the 60 are what Claude read in the crypto scripts; he confirmed the source, not the numbers.
- "DELETE ANYTHING THAT YOU RAN YOUR WAY." Done (see "Deleted"). Claude's own versions are not to be made again.
- NO HARD CODED START OR STOP FOR A GRAPH. "Dipole and exhaustion start and stop by when the data says and not our
  predetermined values." A graph starts where its line began to show. No "20 seconds before the trade".
- "2 TRADES BACK IS GREAT": a picture's frame starts two trades (or trade legs) back.
- THE PICTURES ARE SET UP AS THE CRYPTO PICTURES WERE: "Show each individual trade and their prebirths like this
  without designated start times". He is not worried about the 2,000 averaging; nothing is averaged here.
- THE RATE LINES ARE PER TICK, NOT PER SECOND: "instead of per sec, we are doing per tick like price".
- THE PRICE GRAPH CARRIES TWO POINTS: "Just show price graph with 2 points: bought and sold".
- THE DIPOLE AND EXHAUSTION GRAPHS STAY AS THEY ARE for the time being: "the exhaustion and dipole does show movement
  when the trades are executed".
- THE SCALE of a line graph is set by the line itself: "I'm not worried about different heights. I just want to see
  if dipole and exhaustion correlate somehow to price curve".
- THE BLOCKY BEST BID AND BEST OFFER CURVES STAND: "It's alright that it's blocky. I see what I wanted to."
- THE EXCEL SHEETS take dipole and exhaustion from the crypto calculation only: "make sure your new calcs don't end
  up on the excel sheet".
- What he is looking for across the graphs: not the same direction or size, "just something correlating".

## What exists now

**Code:** Markets branch `ccr-b66f34d5-h6ra1t`, `35d45df` (the session's own branch; nothing on the trunk). It holds
everything of `ccr-92cbec22-u0cbuj` (`e8cd626`) EXCEPT the three deleted programs, plus:
- `root/trade_renders.py`: one picture per trade of the crypto and ng program, set up the crypto way. Options:
  `--random N` (a repeatable pick), `--only <trade day>:<trade number>` (named trades), `--quotes` (adds the best
  bid and the best offer).
- `root/leg_renders.py`: one picture per stored trade leg, with the two crypto lines.
- `root/pod_leg_renders.sh`: ONE pod, several trade days at once, each pinned to its own CPUs. It runs either
  program. `DAYS='...'` names the trade days.
- `CLAUDE.md`: the crypto-formula rule, no hard coded start or stop, the Excel rule.
- REMOVED: `root/tick_renders.py`, `root/continuing.py`, `root/four_graphs.py`. Older session branches still hold
  them; no branch is deleted or rewritten without his word.
- NOT RUN in the session: no test suite was run on this branch. `tests/root/test_outside.py::test_no_hidden_numbers`
  skips in the container; its rule was applied by hand to every file changed.

**Stored, each file fetched and proved against its receipt, `FILES.md` up to date on every branch:**
`root-rows-20231002` `612efec`, `-20231003` `85fd853`, `-20231017` `1eccc49`, `-20231018` `afa9bc7`.
- `crypto-ng-tick/` (all four; the fourteenth session's): the 20-second exhaustion line, the 60-second line, the
  turns, the program's trades, every trade on the tape, the humps. THIS IS WHAT STANDS for dipole and exhaustion.
- `trade-renders/` (all four): 10 trades of the program picked at random per trade day, 40 pictures. Five graphs
  on one clock in seconds from the trade's start: (1) the mid price with two points, bought and sold; (2) the
  dipole, 60 seconds; (3) the exhaustion, 20 seconds; (4) the dipole's change per tick; (5) the mid price's
  change per tick. An index table holds one line for EVERY trade of the program.
- `trade-renders-quotes-test/` (Oct 2 and Oct 18 only): one picture each (trade 883; trade 982) with the best bid
  and the best offer added as two graphs under the price. A test of his idea.
- `leg-renders/` (all four): 10 stored trade legs picked at random per trade day, 40 pictures, the trade price as
  it printed with the two crypto lines. Kept; whether they stay is his to say.
- Counts, written by the jobs: trades of the program 1,794; 1,895; 1,672; 1,682 (7,043). Stored trade legs 6,119;
  6,907; 5,660; 5,120 (23,806).

**Deleted this session, on his word, each removal confirmed on the remote:**
- From the four daily branches: `tick-renders/` (thirteenth session), `continuing/` and `four-graphs/` (fourteenth
  session), and three earlier sets of this session's own pictures. Each `FILES.md` says what and why.
- From this branch: `three-renders-samples-20261118/` (the twelfth session's samples).
- KEPT and why: `calc-turn_peaks-*` (the peak with no window; he asked for it himself on 2026-11-17); Native's
  pinned dipoles and their renders; the counts in the record pages, as a record only.

## Open with him, each put once (after the midpoint)

1. What the shaded "trade" should be. The stored trade leg ends at any single print one tick back, so its band is
   often a piece of the move the eye sees. The crypto-style pictures use the program's own trade. Whether
   `leg-renders/` stays.
2. Every trade, not 40. All 7,043 trades of the program at the measured size is about 1.4 gigabytes in git; all
   23,806 trade legs about 3.9. Needs his word on where they are stored.
3. Whether the best bid and best offer graphs go into every picture, or stay a test.
4. The count Claude offered and did not build: for every tick where the price steps, which way and how far it
   went and which way and how far each line moved, each on its own line, nothing averaged. A new count: his yes.
5. Whether the 60-second line is his "dipole". Crypto also had a longer dipole read before an entry (the lean over
   30 bars, with divergence against the price drift, `odcore/info_dipole.py`). Not built; its span needs his word.
6. One sentence on the read-me page of `ROOT_dipoles_pinned.xlsx` speaks of "a line made at the tick". Words about
   a plan, not data. Left because Desktop writes to that file.
7. Carried from handoffs O, P and Q: whether a brief dip through zero should end a hump; steps or curve for one
   event's line; the Excel sheets for the crypto and ng outputs (nothing is in a sheet yet); the full workbooks;
   his stacked-pair question counted with no window; TELL HIM before the strategies start (he raises the effort
   setting): 15 versions laid out in one message, and first how a version is formed blind to its own trade day;
   his open calls (deleting last week's two folders from `main`; the five-step process and its two streams;
   Bedrock; Native's missing two hours); removing the stopped chain matching code.

## To remember when the pictures are read

- A print moves the dipole and the exhaustion on its own nanosecond, so "something changes in the other two when a
  trade happens" cannot fail. What is not automatic: which way and how far each moves, what each did BEFORE the
  trade's start, and the lines moving with no print (an old trade leaving the 20 or the 60 seconds).
- The program starts a trade at the first trade AGAINST its own side after a turn. So the exhaustion line steps
  against the trade at zero and steps back 20 seconds later. Made by the rule, as in the crypto graphs.
- By eye in a handful, nothing measured: in the trade leg pictures the lines turned after the price, not before;
  one trade (trade day Oct 18, trade 982) shows the dive before zero and the recovery after it in all three
  lines; others show the dipole against the trade through its life. Leads, not results.
- NOT PROVED (carried): that the program's trades equal what the July files would have made.

## How a launch goes now (as done this session; six launches, all passed first time)

- The session REFUSES to start a pod unless Greg has typed the word "go" AFTER the price was on his screen. Twice
  this session Claude read an instruction as the go and the start was refused. Do not try: state the price and
  wait for "go".
- The session's cloud environment is "Markets" with LIMITED network. Every new pod address needs an approval card
  (`update_environment`, add `<pod id>-8000.proxy.runpod.net`; take the dead one off in the same card).
- General Purpose `cpu3g`, 8 CPUs, $0.32 an hour; read the price again at the time. Pass `dataCenterIds` with
  United States centres. Each run this session was three to five minutes: 2 to 3 cents.
- Image `python:3.12`. The pod's command, in one string: make `/root/work/out`, start `python3 -m http.server 8000`
  there, clone the code branch (`--depth 1 --filter=blob:none --no-checkout`, then `sparse-checkout set root
  crypto_ng`, then `checkout`), then
  `bash code/root/pod_leg_renders.sh <FULL 40-character commit> <leg_renders | trade_renders> [options]`, then
  `sleep infinity`. CHECK THE COMMAND BEFORE SENDING IT: one launch went out with a placeholder where the commit
  goes and had to be deleted.
- Each trade day's output is served under `/d<trade day>/`. Fetch and prove with
  `python3 -m root.pod_fetch <address>/d<trade day> <trade day> <commit> --into <folder> <leg_renders|trade_renders>`.
- The daily branches: clone each as its own shallow copy with `--filter=blob:none --no-checkout`, then
  `sparse-checkout set --no-cone '/FILES.md' '/<folder>/'`. NEVER list one with file sizes.
- WHEN NEW DATA REPLACES OLD: start the pod, delete the old from the branches, confirm it is gone on the remote,
  and only then fetch the new.
- Store, push, confirm each push on the remote, THEN delete the pod and read the account. After ANY restart of
  the session, read the account first (it restarted once this session with no pod up).

## Slips of this session, so they are not made again

- The first 40 pictures drew Claude's own tick versions under the names dipole and exhaustion, and left the crypto
  exhaustion line out. Two sessions of his work on bringing the crypto calculation back were set aside. All of it
  is deleted and the rule is in `CLAUDE.md`.
- He was told a picture would start at the humps the trade leg touches; that can start it at the trade's own first
  trade with no prebirth. Corrected to two back.
- "It changes at the same moments" was called built in several times without saying plainly that the calculations
  themselves are independent of the price. It confused him. Say both halves together.
- A pod was started with a placeholder in its command.
- Instructions were read as the go for a pod twice.
- Long answers. He reads on a phone: answer the question in the first lines.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now. In this session it
was not used.
