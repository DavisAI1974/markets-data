# README page for the workbook (text of the first sheet)

Status, 2026-11-16: this is the wording of the README page. The rebuilt workbook has not been written yet; this
page goes in as its first sheet when it is, and is kept up to date here as each part of the rebuild is settled.
Lines marked [to be filled when built] are completed from the build's own receipts, never by hand.

---

## READ THIS FIRST

**Nothing in this workbook is missing by accident.** Where a cell or a column is empty, or where a value repeats down
many rows, there is a stated reason on this page. If you find something empty that this page does not explain, treat
that as a fault and report it.

## What this workbook is

- Natural gas futures (NYMEX Henry Hub, front-month contract), order by order, for four trade days in October 2023:
  Monday Oct 2, Tuesday Oct 3, Tuesday Oct 17 and Wednesday Oct 18.
- It is built from the raw order tape (the exchange's full order-by-order record, as delivered by the data vendor)
  and from published outside figures.
- One sheet per trade day. A trade day has about 770,000 to 880,000 rows.

## What a row is

- **One row is one tick: a single message from the exchange.** An order added, cancelled or changed, a trade, a fill,
  or a clearing of the book. Every message inside a trade day, and in the 5 pm to 6 pm stretch on each side of it,
  has its own row, in the order the tape gives them. Nothing is merged, grouped, sampled or left out.
- Messages from other days of the same week are not rows here. They were still run through the order book, so the
  book is correct at the first row of every sheet. The counts at the end of this page show how every record in the
  raw files is accounted for.
- Several rows can carry the same time down to the nanosecond. They are still separate ticks, in tape order.
- **A trade usually takes several rows:** the trade itself, the fill of each resting order, and then the cancel or
  change that takes the filled size out of the book. Between those rows the book still shows size that has just
  traded. That is how the exchange sends it, and it is shown as it comes.

## The trade day

- **A trade day runs from 6:00 pm Eastern the evening before to 5:00 pm Eastern on the named date.** Tuesday's trade
  day is 6 pm Monday to 5 pm Tuesday. This is the exchange's own session.
- **The hour from 5 pm to 6 pm is marked separately** and belongs to neither trade day. No trades happen in it, but
  orders are removed just after 5 pm and new ones are placed before 6 pm, so those rows are kept and marked.
- A date written alone always means a trade day. A UTC calendar day is only how the vendor packs its files.

## The two clocks, and the position label

- **Exchange time:** when the exchange says the thing happened.
- **Received time:** when the message arrived at the data vendor's recorder at the exchange. This is the first moment
  anyone outside the exchange could have known it.
- Both are on every row. They can differ, and they do not always agree on which of two messages came first.
- **Position** is the row's place on the tape. It is only a label for telling rows apart. It is never used in a
  calculation, and neither are order numbers or trade numbers.

## The order book

- **The book is kept for the whole week.** It starts when the exchange opens on Sunday and is carried straight through
  to Friday. It is not started over each trade day.
- **Each row shows what that tick did to the book,** plus figures for the whole book at that moment and the full line
  of orders at the price that was touched. [The exact columns are listed here when the build is settled.]
- **The complete book is not repeated on every row, and this is not missing data.** A full picture of the whole book
  is stored at every trade, in separate files [location to be filled when built]. The complete book at any other tick
  is that picture plus the changes on the rows after it. It comes out exactly the same as if it had been stored.
- The book was checked against the exchange's own snapshots. [Result to be filled when built.]

## Orders carried over the weekend

- On Sunday the exchange lists again every order left resting from the week before, all with one time stamp. Their
  real entry times are not on the tape.
- For those orders, any "how long it has rested" value is marked **"at least"**. It is a lower limit, not the true age.

## The 13 outside data points

- These are published figures from outside the order tape: positioning, weather, wind and gas burn, storage, and the
  shape of the futures curve.
- **Each one is shown on every row, and the same value repeats until a new one is published.** A storage figure
  repeats for a week; a forecast temperature repeats for its hour. Long runs of identical values are correct.
- A value changes on the row where it actually became available, not at the start of the trade day.
- Where an outside value could not be obtained, the cell is empty with a note saying so. No value is ever estimated or
  filled in.

## Columns that are empty on purpose

| Columns | Why they are empty | When they are filled |
|---|---|---|
| Calculated columns (most of L037 to L071, L074 to L076, S01 to S19) | Each is filled only when its calculation has been built and checked. Until then it is empty, not zero. | As each calculation is completed. The status table below says which are done. |
| Step 1 columns (L080, L083 to L089) | They belong to an earlier 2021 study and are being handled separately. | Later, in their own step. |
| Frankie's output columns (L077 to L079, L090 to L099) | They hold a model's outputs, and that model has not been run on these trade days. | After such a run. |
| Reference fields (L001 to L026, L081, L082) | They name background documents, not market data for a tick, so they are not columns on the trade-day sheets. | Not applicable. |

## Status of this build

| Part | State |
|---|---|
| Raw messages, one row per tick | [to be filled when built] |
| Trade day and position labels | [to be filled when built] |
| Order book columns | [to be filled when built] |
| The 13 outside data points | [to be filled when built] |
| Calculated columns | [to be filled when built, column by column] |

Counts for each trade day (rows, trades, messages in the 5 pm to 6 pm hour) and the fingerprint of each raw file are
listed here from the build's receipt. [to be filled when built]

## Rules this workbook follows

- Every tick and every trade is shown individually. There are no averages, rates or summaries standing in for detail.
- No data is dropped.
- No value on a row uses anything that arrived after that row's tick.
- No trading cost, fee or fill assumption is in any value.
- Nothing is invented. An unavailable value is left empty with its reason.
