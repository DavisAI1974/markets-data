# Agent execution plans

Frankie and the Ccode-managed agents can commit a JSON plan in this directory and select its filename in either manual paper workflow. The receipt records the plan, its fingerprint and the platform commit. Inline JSON remains available for a single authorized run.

Supply the contract's actual Nautilus futures instrument definition, its Databento instrument ID and a `rules` object. Each participating strategy specifies its contract quantity and its opening and closing instructions. Unselected rules continue to emit research signals.

| Instruction | Paper order |
| --- | --- |
| `post` | Post-only limit at the current same-side quote. |
| `cross` | Immediate-or-cancel market order against displayed depth. |
| `cross_limit` | Immediate-or-cancel limit at the current opposite quote. |

A leg can be an object with `style` and a nonnegative integer `offset_ticks`. For a post, the offset moves the price further from the other side. For a crossing limit, it sets how far beyond the opposite quote the order may take liquidity. A market order accepts no price offset. The matcher reports each execution separately.

A manager can list originating strategy IDs in `entry_rules`. Its direction selects matching entry signals. It submits its own opening order in its own venue, even when the originating strategy only records research signals. Set `on_parent_close` to `exit` to act when the parent closes, or `hold` to keep the manager's position and orders under its own instructions until its exit or the run stop. Each exit cancels outstanding orders for that trade and sizes its replacement to actual filled inventory. The run stop cancels working orders and attempts to flatten the remainder.

A strategy plan sets execution behavior. A paper run still requires Greg's explicit go.
