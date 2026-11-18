# Sample pictures of 2026-11-18 (twelfth session). Samples only: one stretch of one trade day.

Greg, at the close: "create and push everything". These are the pictures drawn in the session and sent to him, with
the programs that drew them. They are SAMPLES, drawn from stored files of trade day Tue Oct 17, 2023 (the rows, the
stored runs of trades, the stored trade legs, the pinned dipoles table). They are not a calculation output, they
have no receipt, and nothing on any `root-rows` branch was changed. Each program reads the stored files only.

Read from `root-rows-20231017` `9dc46c9`: `rows-20231017-part000` and `-part002`, `calc-turn_peaks-*` (the same
parts), `calc-flow_peak-20231017-part002`, `calc-leg_peaks-facts-20231017-part000`,
`renders/dipoles-pinned-20231017.parquet`.

The stretch of the first eleven pictures starts at the 2,000th trade of rows part 2 (11:58:32.200 Eastern), taken
by position and not by what happened there, and runs for a count of trades (40, 150 or 600: numbers of Claude's,
to be replaced by Greg's choice).

| Pictures | What they are | Greg's word on them |
|---|---|---|
| `three_renders_smooth_*` (2) | THE THREE RENDERS AS HE ASKED: the trade price curve drawn smooth through every trade; the dipole at the tick; the exhaustion at the tick. No window. | The current form. |
| `three_renders_nano_*` (2) | The same three, the trade price joined with straight lines. | "Print the render of the trade leg as a smooth curve" |
| `dipole_leg_pair_*` (2) | The stacked pair for the first two recorded dipoles of the trade day born on a trade leg's first trade (20:28:01 and 20:46:56 Eastern): the trade leg's price above, the dipole at the tick below. | "Let's start there" |
| `three_tier_sample_*` (3), `three_tier_wholebook_*` (2) | Claude's own selections, NOT what he asked for: the best bid and ask with the trades, the run of trades on one side, the lean of the resting orders (at the best prices; whole book). | "those aren't the 3 renders I asked for". Kept as additions for later. |
| `tick_against_20s_*` (2) | Claude's own selections again, with a 20-second strip. | The same. The 20-second strip: "That window gives us nothing but a visual to confirm from." |

What the two tick lines are (Claude's calls, stated to Greg, his to correct; in `ROOT_GAMEPLAN_DECISIONS.md`,
"Twelfth session"):
- The exhaustion at the tick: each run of trades on one side as it builds trade by trade; its high is its last
  trade (the peak with no window, stored in `turn_peaks`).
- The dipole at the tick: the size of the latest run of buying minus the size of the latest run of selling, over
  the two together (the run under way against the run it took over from). It changes at every trade. A new figure,
  read off the stored runs in the session; not a stored calculation.

NOT YET DRAWN, and it is the next thing: the exhaustion render made exactly as the crypto work made it (see
`NEXT_SESSION_HANDOFF_20261118O.md`).
