# The life of every peak on the clock, no defined window (Desktop session, 2026-11-17, about 05:40 to 05:50 Eastern)

New files only. Nothing existing is changed. Not in the daily sheets or the workbook yet: this folder is the
hand-over to Code for them.

## Greg's words this is made on

- "I was trying to explain to you to use the same process and procedure as we used on the 55 we run and apply those
  to the new run. We don't need the old ut puts with the new data, but we want to know how they were defined and
  grouped"
- "And let's get away from defined windows a d see how long or short these groups and families actually last and
  where their true begininngs and ends are pinned to the timestamps"
- "Peaks are fine" (05:39; his answer to whether the family step runs on the stored peaks).

This is the first step of that process on the new run: the events, each with its true beginning and end on the
clock. In the 55-week run every event was read through fixed stretches (60 s before, 60 s after). Here each peak is
read over its own life. No family or group is made here.

## Read from (nothing made again)

- `root-rows-20231002` `6037f23`, `-20231003` `33b3652`, `-20231017` `a76923a`, `-20231018` `8a6175f`:
  `calc-turn_peaks-facts` (the peaks with no window, lines "no window" / "peak known").
- The same branches at `daac81d`, `e4ffcc9`, `74f4225`, `d2c34be`: `rows` (the received clock of each tick),
  `calc-flow_peak`, `calc-peak_story-facts` (the fact "build-up": the low the flow rose from),
  `calc-chain_peaks-facts` (where each story ended).

## What a life is (Claude's calls, Greg's to correct)

- **Peak with no window** (a run of trades on one side): begins at the first trade of the run, ends at the last
  trade of the run (its high). It becomes known at the first tick after.
- **20-second peak**: begins at the low its flow rose from, reaches its high, ends where its story ended (came back
  or beaten). Its high and its lows are still read through the 20-second flow; only the beginning and the end are
  its own.
- Lots: for a peak with no window the size traded in the run; for a 20-second peak bought minus sold at the high.

## Files

| File | What it is |
|---|---|
| `peak-lives-<trade day>.parquet` (4) | One line per peak, both kinds: 21,092 (Oct 2), 23,261 (Oct 3), 19,020 (Oct 17), 17,516 (Oct 18). 20-second peaks 9,525 / 10,577 / 8,619 / 7,967 and peaks with no window 11,567 / 12,684 / 10,401 / 9,549, equal to the stored counts. Columns: `trade_day`, `kind`, `side`, `lots`, `trades`, then for the beginning, the high, the end and the tick it became known: `..._position`, `..._received_time_ns`, `..._et` (Eastern); `begin_to_high_ns`, `high_to_end_ns`, `begin_to_end_ns`, `high_to_known_ns`; `ended_by`. |
| `peak_lives_<trade day>.png` (4) | One clock, three panels: price (every trade); every peak with no window drawn from its beginning to its end at the height of how long it lasted; the same for every 20-second peak. Lives with no length are on the bottom line; lives whose beginning or end is not stored are on the top line at their high. Every peak is on the image (checked in the script). |
| `lives.py`, `render_lives.py`, `load.py` | The programs. |
| `MANIFEST.json` | Path, bytes, sha256 and source of every file. |

## What was measured (counts of peaks; the powers of ten are a scale, not groups put on the peaks)

Peaks with no window, first trade to last trade (44,201; none empty):

| How long | Oct 2 | Oct 3 | Oct 17 | Oct 18 | All four |
|---|---:|---:|---:|---:|---:|
| no length (begins and ends on one tick) | 4,256 | 4,805 | 4,053 | 3,803 | 16,917 |
| under 1 ms | 795 | 748 | 645 | 549 | 2,737 |
| 1 to 10 ms | 1,432 | 1,421 | 1,070 | 978 | 4,901 |
| 10 to 100 ms | 1,215 | 1,393 | 1,019 | 829 | 4,456 |
| 0.1 to 1 s | 924 | 1,111 | 844 | 752 | 3,631 |
| 1 to 10 s | 2,056 | 2,294 | 1,932 | 1,702 | 7,984 |
| 10 to 100 s | 818 | 840 | 767 | 865 | 3,290 |
| 100 to 1,000 s | 71 | 72 | 71 | 71 | 285 |

Trades in the run: 1 trade 16,468; 2 trades 9,537; 3 trades 6,030; 4 or 5 6,251; 6 to 10 4,587; 11 to 20 1,176;
21 to 50 143; 51 to 100 9.

20-second peaks, the low it rose from to the end of its story (36,688; 147 empty: 142 with no low stored, 5 whose
story was still open at the last tick):

| How long | Oct 2 | Oct 3 | Oct 17 | Oct 18 | All four |
|---|---:|---:|---:|---:|---:|
| under 1 ms | 1 | 0 | 0 | 0 | 1 |
| 1 to 10 ms | 32 | 34 | 26 | 25 | 117 |
| 10 to 100 ms | 260 | 257 | 161 | 134 | 812 |
| 0.1 to 1 s | 577 | 742 | 395 | 325 | 2,039 |
| 1 to 10 s | 3,189 | 3,729 | 2,854 | 2,271 | 12,043 |
| 10 to 100 s | 4,891 | 5,311 | 4,627 | 4,663 | 19,492 |
| 100 to 1,000 s | 531 | 469 | 522 | 512 | 2,034 |
| 1,000 to 10,000 s | 1 | 1 | 1 | 0 | 3 |

Single cases: the longest life with no window is a sell run on trade day Oct 3, 21:47:51.578 to 22:00:35.006
Eastern, 763.4 s, 16 trades, 27 lots. The longest 20-second life is a sell peak on trade day Oct 17: begins
18:22:51, high 18:22:56, ends 18:44:21, 1,290.5 s, came back. On each trade day the four longest lives with no
window all fall between 19:18 and 01:21 Eastern.

What the tables and renders show, on all four trade days:

- Peaks with no window: the count falls from 1 to 10 ms down to 0.1 to 1 s and rises again at 1 to 10 s
  (for example Oct 2: 1,432, 1,215, 924, then 2,056). Two stretches of length hold most of the lives that have a
  length, with fewer between them.
- On the renders almost no life with no window lies between no length and about 100 microseconds.
- In the day session the lives with no window stop at a few tens of seconds; in the evening and overnight they run
  to hundreds of seconds.
- The 20-second lives sit mostly between 1 and 100 s (31,535 of the 36,541 with a length).
- On the Oct 17 render the lives line up in upright streaks at particular clock times (about 08:10, 09:00, 10:00
  and 14:30), in both kinds.

Readings, not measured: the two stretches of length may be two different things happening (a burst inside one
exchange event, and a run built over seconds); the 20-second lives may take their length from the window itself.
Neither was tested here.

## Not done

- The family step itself (the 55-week process on these events: describe each life's shape with no price and
  nothing from after it, count identical shapes once, split 2 through 8 ways with every split reported, leave one
  trade day out) is not started. Each life's shape has to be described over its own length, not over fixed seconds;
  how is to be put to Greg before it is built.
- 16,917 lives with no window are a single tick and have no shape of their own; what goes before and after them on
  the clock is what they have.
