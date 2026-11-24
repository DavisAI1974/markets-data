# Your job: choose how each paper strategy places its orders, and how many contracts

You are one of the agents Greg Davis gave this choice to. His decision, as the platform's checklist records it
(item 17): "Paper orders can post a bid or offer, lift an offer or hit a bid. Frankie and the agents choose
placement and size for each strategy." You decide for the rules named at the end of your own brief, one rule at
a time. Nobody has picked for you and there is no expected answer.

This is a decision job, not a build. Read files. Run nothing of the platform: no tests, no checks, no session,
no git command. Write one file, the answer file your own brief names, and nothing else.

## What a plan entry is

For each strategy that takes part, the plan holds:

- `contracts`: a whole number above zero, the size of its opening order.
- `open`: how the opening order is placed. `close`: how the closing order is placed.
  Each is `{"style": "post" | "cross" | "cross_limit", "offset_ticks": <whole number, zero or more>}`.
- For a manager rule only: `entry_rules` (the entry rules whose opens it follows) and `on_parent_close`
  (`"exit"` or `"hold"`).

The guide is [plan guide](platform/README.md). Read it.

## What the matcher does with each choice (read from the code; check any line you doubt)

Code: [paper_execution.py](https://github.com/DavisAI1974/paper-trading-platform/blob/2986b3ce3001bc1926df64a06588b4558a5b648e/paper_platform/paper_execution.py), `engine.py`, `session.py`, same folder.

1. The matcher is given each tape message before the decision engine sees it (`session.py` line 263). An order
   that comes out of a decision is submitted at that decision row's own receive time. No delay is modelled.
2. `post`: a post-only limit that rests at the decision row's quote on the order's OWN side (a buy rests at the
   bid, a sell rests at the offer). `offset_ticks` moves it further away from the other side. It fills only when
   later trading reaches it, by its place in the queue (`paper_execution.py` lines 113 to 130).
3. `cross`: an immediate-or-cancel market order against the displayed book (a buy lifts the offer, a sell hits
   the bid). It takes no offset (line 132).
4. `cross_limit`: an immediate-or-cancel limit at the decision row's quote on the OTHER side (a buy at the
   offer, a sell at the bid). `offset_ticks` is how far beyond that quote it may take. What does not fill at once
   is cancelled.
5. A close first cancels that trade's working orders, then is sized to the contracts actually held, never to
   `contracts` (lines 95 to 105). If nothing is held, no closing order is sent. So a posted open that has not
   filled by the time its close comes is cancelled and that trade never held a position.
6. A posted close is not re-priced. It rests at its price until it fills or until the run stop cancels it and
   flattens what is left.
7. The run stop, and any close the platform marks as administrative, always crosses, whatever the plan says
   (lines 256 to 258 and `flatten`).
8. Each rule in the plan has its own matching venue and its own inventory. Nothing is shared between rules.
9. A rule left out of the plan places no order and keeps writing its research signals. That is a valid state.
10. A fill is written with its own price, quantity and side. Fees and margins in the contract definition are
    zero. No result figure is made.

Managers (the six rules whose file says `"role": "manager"`):

11. In the decision engine every manager is attached to every open position on the manager's side, whichever
    entry rule opened it, Claude's CL rules and Codex's CX rules alike (`engine.py` line 309 calls `manage` for
    each open position; `manage` starts at line 86).
12. In the plan, a manager places orders of ITS OWN in its own venue. When an entry rule listed in its
    `entry_rules` signals an open on the manager's side, the manager opens its own position at that same row,
    before its own condition has confirmed anything (`paper_execution.py` `instructions`, lines 230 to 250).
13. The manager closes its own position on its own "exit" signal. Its "hold", "suspend additions" and
    "release warning" signals place no order.
14. `on_parent_close`: with `"exit"` the manager's position is closed when the parent's trade closes. With
    `"hold"` it is not. The engine drops a manager's state when the parent's trade closes (`engine.py` line 69),
    so no exit of the manager's own can come after that: a held position is carried to the run stop and
    flattened there by a crossing order.
15. A manager with no entry rule listed never opens a position.

## The contract (from the stored exchange definition of the purchased tape)

NGX3, natural gas futures, November 2023, NYMEX. Price step 0.001 dollars per MMBtu. Smallest order 1 contract,
largest 1,999. These are the only size figures on record anywhere for this choice.

## The rules you hold yourself to

- A reason comes from the rule's own words: where in the book its trigger sits, what its closing condition
  reads, what its author wrote about where it acts. Copy the words you rest on, exactly, with the file and line.
- A reason never comes from how likely a fill is, from a better or worse price, from cost, fees, slippage, an
  expected result, or from comparing or ranking rules. None of those enters this work.
- No mid price, anywhere.
- No made-up numbers. A `contracts` figure other than the contract's smallest order, or any `offset_ticks`
  other than zero, needs words from the rule's own text that call for it. If you cannot quote such words, do
  not use such a number.
- "No decision, because <what is missing>" is a valid answer for a rule. Use it whenever the rule's words do not
  settle the choice. A rule with no decision stays out of the plan and is listed as missing. Do not fill a rule
  in to make the count come out. An honest gap is worth more than a guess.
- Decide each rule on its own. Do not copy one rule's choice onto another because they look alike; read each
  rule's words.
- No verdict words about a rule (good, bad, strong, weak, better, worse, winner, loser).

## What to write

One JSON file: a list with one object for each rule you were given, in order.

```
{
  "rule": "<id>",
  "decision": "decided" | "no decision",
  "contracts": <whole number>,                         (only when decided)
  "open":  {"style": "...", "offset_ticks": 0},        (only when decided)
  "close": {"style": "...", "offset_ticks": 0},        (only when decided)
  "entry_rules": ["..."], "on_parent_close": "...",    (managers only, when decided)
  "why_size":  "<one or two plain sentences>",
  "why_open":  "<one or two plain sentences>",
  "open_quote": "<words copied exactly from one line of a file>",
  "open_quote_file": "<path relative to this brief>", "open_quote_line": <line number in that file>,
  "why_close": "<one or two plain sentences>",
  "close_quote": "<words copied exactly from one line of a file>",
  "close_quote_file": "<path relative to this brief>", "close_quote_line": <line number>,
  "why_parents": "...", "parents_quote": "...", "parents_quote_file": "...", "parents_quote_line": <n>,   (managers)
  "missing": "<for no decision: exactly what is missing and who could supply it>"
}
```

Every quote must stand in the named file on the named line, word for word (a quote may be part of a line, never
more than one line). Automated quote checks are deferred during this build-only pass. Quote from the strategy documents named in your own brief (they have real lines), not from a rule's JSON
file (its text is one long line).

When the file is written, reply with: the path, how many rules you decided, how many you left with no
decision, and anything in the code or the documents that you found to be different from what this brief says.
