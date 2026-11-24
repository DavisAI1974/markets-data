# Plan for ticket 38: every data layer reaches the decider (2026-11-24, twenty-sixth session)

Greg, 2026-11-24, on reading that the per-tick dipole and exhaustion columns do not reach a decider: "I have said
multiple times with you that every data layer has to be available to agents nd supposedly that was fixed".

His rule (decisions file, twenty-fourth session): NO DATA LAYER IS DROPPED for a decider: the MBO data, the planes
and ROOT's calculations, the dipole above all, the market conditions. After-the-fact data is kept and joined to
every decision for learning; it is kept out only of what a decider reads at the instant it decides.

## What is so today (not fixed)

Measured by the check of the Excel sheets for trade day 2023-10-02 (reviewer run 182): of 458 columns, 27 are in
the packet at the signal's moment, 13 are in the after-the-fact file, and 418 are not placed.
- The stored rows (408 columns for every tick) are read through 10 columns only; the other 398 are named and not
  given (Markets `tools/kgraph/signal_packet.py` lines 515 to 519).
- A layer whose rows carry a tape position and no time is not placed at all. `calc-research_columns`, which holds
  the per-tick `dipole_60s` and `exhaustion_20s`, is one of them (lines 667 to 673; 784,130 of its 820,670 rows
  hold no time of their own). By the ticket, 35 of the 63 layers on the branch are named in the foot and not placed.
- The 20 columns of the crypto and ng program's own trades are not placed. By his rule those are observation and
  verification only; they stay out and are named, with that rule as the reason.
- The MBO window is one layer with no id for each message (the ticket's open point 4). Its real shape is unknown
  until one pass of the tape; it is not part of this plan.

## What is built

A. THE STORED ROWS, EVERY COLUMN. The rows plane is read with all its columns. It is read by part and by row group,
so that memory holds one part at a time and size is never a reason to leave a column out. A question's folder
holds, for the rows that became known since the previous question, every column. The brief's text still shows a
layer's count and head; the rows themselves are in the folder's files, each with its id, and a decision may rest
on any id. The size of a question's folder is measured and reported; nothing is cut to make it smaller.

B. A LAYER WHOSE ROWS CARRY A TAPE POSITION AND NO TIME IS PLACED BY THE TIME OF THAT TICK. The time a tick was
received is read from the rows plane at the row's `position_on_tape`. THE LEAKAGE GUARD: this is right only for a
layer whose row at position p was made from ticks up to p and no later. So each layer of the branch gets ONE entry
in a table kept in the code as data: the layer, the column (or the position look-up) that says when a row became
KNOWN, and the place in the calculation's own code or in `root/DECLARED_CONSTANTS.md` that shows it. No entry is
guessed. A layer whose known-at time cannot be shown from the calculation's own code is not placed; it is listed,
by name, with what was looked at, for the main session and Greg. The same table settles the layers the reviewer
questioned: the peaks, the humps and the "open at the end" layers, which today are placed by the latest time on
the row, which may not be the time the row became known.

C. THE REVIEWER'S POINTS ON THE PACKET (run 182, its last section): times compared as whole nanoseconds, not as
floating point (two times 100 nanoseconds apart compare equal today); the count of a layer's rows for the whole
trade day taken out of everything a decider is handed (it tells how many rows are still to come); every
calculation and every read the graph names for the trade day is either placed or named, none dropped by the
`.parquet` filter; receipts and pictures named, not only counted; the reason text that is applied to the wrong
layers; the door runs its checks of the rows it writes, not only of each layer's head; the earlier file is matched
on trade day and commit; the three assertions that cannot fail.

D. THE AFTER-THE-FACT FILE LEAVES THE FOLDER A DECIDER READS. It is written beside the question's folder, not in
it, and the folder holds no pointer to it.

E. THE CHECK THAT HOLDS IT. For trade day 2023-10-02 every one of the 458 columns of the daily sheets is in the
packet at the moment, or in the after-the-fact file, or is one of the 20 program-trade columns; the three counts
are asserted as figures, from a packet that is really built, and the count of columns "not placed" for any other
reason is zero. A column added to a sheet later fails the check until it is placed.

## Order

The reviewer reads this plan before the builder of A and B starts (it touches the placing of rows in time). The
builder of C and D starts now: those points come from the reviewer's own read. Then A, B and E. Then the reviewer
reads the whole change, with the stored planes present (a git folder holding the branch `root-rows-20231002`).

## What this plan does not do

It runs no paper run and puts nothing through the engine or the tape. It reads the stored planes of one of the
four trade days, which the existing checks of the packet already do.

## CHANGED AFTER THE REVIEWER'S READ OF THIS PLAN (run 203, `../reviews-20261124/REVIEW_RUN_203_TICKET_38_PLAN.md`)

What the read found, and what the plan now says. Parts A and B above stand as amended here.

1. ONE ENTRY FOR EACH GROUP OF COLUMNS, NOT FOR EACH LAYER. `calc-research_columns` holds, on the same row, the
   per-tick reads (`dipole_60s`, `exhaustion_20s`, the information measure), which are made from trades up to the
   tick, and 316 columns that say how a move or a hump ENDED, written on the tick where it BEGAN. So the table of
   part B has an entry for each group of columns of each layer: when that group became known, and the place in the
   calculation's code that shows it.
2. WHERE EACH GROUP GOES. Known at its tick: in the packet, placed by the tick. Known later (an end, an outcome, a
   row made from what was still open when the tape ended): placed at the time it BECAME known if the layer carries
   that time (`known_received_time_ns`, `known_position`) and the code shows every column of the group is no later
   than it; otherwise in the after-the-fact file. Nothing is left out of both.
3. THE SAME NANOSECOND. Several ticks share a nanosecond. A row is handed to a decider only if its tick is at or
   before the SIGNAL'S OWN tick on the tape: the time first, the tape position to break the tie (the rule the
   stored reads already use, `root/research_threads.py` lines 157 to 169). The signal's tape position is carried
   with its moment.
4. WHICH ROWS AT ALL. Only the four trade days; a trade day's rows from 6 pm Eastern the evening before to the
   moment; the rows of the 5 pm to 6 pm stretch and of the Sunday start-up are not handed to a decider (they are
   named, with that rule as the reason).
5. THE CHECK OF PART E COVERS EVERY LAYER, not only the Excel sheets: every column of each of the 63 layers of the
   branch is in exactly one place: the packet at the moment, the after-the-fact file, or the program's own trades;
   the count in no place is zero, and it is asserted. The Excel sheets' 458 columns stay as a second check.
6. BEFORE THE BUILDER OF A AND B STARTS: the calculation code of each layer is read for when its columns become
   known (scout runs 207 and 208), and the table is written from those places. The reviewer reads the table with
   the change.

## LAID AGAINST HIS OWN WORDS AND THE DAILY SHEETS (twenty-sixth session, on his word)

Greg, 2026-11-24: "Read our discussion about data layers a nd after the fact data and how it gets handled. Discussions
in your sessions fro m today"; "You need to look at daily excel sheets to see data layers". DEC below is
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`. Nothing here was calculated: his words, the two Excel files'
own pages, file names of the four daily branches, and the code read by scout runs 207 and 208.

### What his words already settle (not to be asked again)

1. A decider is given EVERY data layer: the MBO, all the planes and ROOT's calculations, the dipole above all, the
   market conditions. Nobody chooses what to thin (DEC:7196).
2. Layers may be put in graph form to save room; none is dropped. The whole of every layer is written beside the
   brief; a written decider gets all of it; a live agent's brief shows the head of every layer and says where the
   rest is (DEC:7196 to 7209; "don't only rely on graphs if need be", DEC:7286).
3. Everything stays in while the deciders and strategies are first run and learned from; dropping anything later is
   his decision, from the runs. Each decision's own line records every layer its packet held and which layers the
   decider named as its grounds (DEC:7230).
4. After-the-fact data is a layer and it is KEPT: joined to its decision, taken or skipped, and read by the agents
   that write the next decider, each decision its own line, nothing averaged. It is kept out of one place only: the
   packet a decider reads at the instant it decides (DEC:7236).
5. ROOT's after-the-fact columns, the peaks, and the columns Native wrote later than the moment go into that same
   afterwards layer (DEC:7245). This settles the earlier line "held back until he rules" (DEC:7215).

### What the sheets show

- "The daily sheets" are the four `root-rows-<trade day>` branches (DEC:4317). The only Excel files are the short
  stretch of trade day 2023-10-02 and the pinned workbook.
- THE STORED-ROWS SHEET HAS 408 COLUMNS, AND ITS OWN `COLUMNS` PAGE MARKS EVERY ONE "Shown to Frankie: yes". Its
  sections are the layers as he sees them: A the native tape, 16 columns (the MBO message itself); B our labels, 8;
  C what this tick did, 23; D the book at this tick, 31; E change-of-state marks, 7; G the outside data points, 323
  (the market conditions; column names carry x01 to x13, none carries x04). The page has no section F: its READ ME
  says calculated columns are filled as each is built, and they are stored as column files beside the rows. So
  part A of this plan (all 408 columns to the decider) is what the sheet has said all along. The packet gives 10.
- The pinned workbook: dipoles 25 columns, peaks 5, crypto and ng 20, the same on all four trade days.
  408 + 25 + 5 + 20 = 458, the figure the check of run 102 counts.
- THE FOUR BRANCHES DO NOT HOLD THE SAME STORED TABLES (file names compared, columns not): 63 on 2023-10-02, 59 on
  10-03, 62 on 10-17, 60 on 10-18. `trade-legs-6pm-to-8pm-legs`, `-stretches` and `-trades` are on 10-02 and 10-17
  only; `trade-renders-quotes-test/trade-renders-index` is on 10-02 only. His word was "They should have same
  columns on each day". Said to him; these four are tables of one stretch and one test, and whether they are made
  for the other days is his.

### What the scouts found, for the known-at table of part B (their reports: `../scout-20261124/SCOUT_RUN_207_...` and `SCOUT_RUN_208_...`)

- The 16 per-tick calculation layers of `root/calcs`: every per-tick column is the value at its own tick (each
  writer quoted). They go in the packet, placed by the tick.
- 15 of the 16 facts tables write each line at the tick it became known, with `known_position` and
  `known_received_time_ns` on the line. They go in the packet, placed by that time, the tape position breaking a
  tie.
- The 8 "open at the end" tables are written after the last tick. Afterwards layer.
- The 20-second line, the 60-second line and the information measure: each row is a read at its own moment. Packet.
- Columns set at a later tick than their row's start, each named in scout 208's report: the crypto and ng turns
  (`what_became_of_it`, `program_trade`), the program's trades (the end columns), the tape trades (the three
  program columns), the humps (ended, furthest, how it ended), `research-moves` (second step, the end columns, the
  level columns), `research-humps` (ended, furthest, the next columns), `dipoles-pinned`, `leg-renders-index` (the
  end columns), the three `trade-legs` tables. By plan point 2: placed at the time they became known where the row
  carries it and the code shows it; otherwise the afterwards layer.
- NOT REACHED by either scout: `research-trace-first-steps`, `trade-renders-index`; read in part only:
  `book-pictures`, `vendor-restatements`, `dipoles-pinned`, `leg-renders-index`, the `trade-legs` tables. No
  writer of `peak-lives` is in `root/` (the layer sits in a folder named `desktop`). None of these is placed until
  its code is read.
- THE TWO SCOUTS DISAGREE ON `root/dipole_peaks.py`, AND THE CODE AS READ BY THE MAIN SESSION BACKS SCOUT 208
  (lines 165 to 185, 204, 223 to 233). `dipoles()` keeps one record for each of Native's dipoles and every later
  line of Native's updates that same record, the closing line's polarity and magnitude included; it finishes
  before `follow()` walks the tape. So the line placed at the tick a dipole was RECOGNIZED, and the per-tick
  counts `native_dipoles_known_plus` and `native_dipoles_known_minus` from that tick on, can carry a polarity
  Native wrote only later. NOT CHECKED ON THE DATA: whether Native's recognized line already carries the same
  polarity is not known from the code. Until it is shown, by point 5 above those columns go to the afterwards
  layer, not the packet. If it is so in the data it is also a fault in a stored ROOT output (its own rule: no
  value on a row uses anything that arrived after that row's tick): that goes to the reviewer and to Greg before
  anything is rebuilt.

### What changes in this plan

a. The packet names its layers the way the sheet does (sections A to E and G, then each calculation, then the
   lines), so a decider's brief and his sheet read the same.
b. Native's later-written columns need no ruling: afterwards layer (point 5).
c. `dipole-peaks`: the polarity columns as above.
d. THE 20 COLUMNS OF THE CRYPTO AND NG PROGRAM'S OWN TRADES are kept out of the packet AND out of the afterwards
   layer by this plan, on his rule that they are observation and verification only. That is Claude's reading
   where two of his rules meet (no layer dropped; the program's trades are never an input); it is his to correct.
e. When part D is read: the afterwards record must still join to its decision by the decision's id from the
   learning side, now that the file is outside the decider's folder.
