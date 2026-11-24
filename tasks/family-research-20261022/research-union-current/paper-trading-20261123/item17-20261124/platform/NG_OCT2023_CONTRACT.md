# The contract of the purchased NG tape, for an agent plan

Recorded by Ccode on November 24, 2026 for checklist item 17. This is not a plan: it holds the two things every plan for the purchased archive `data/nymex_mbo/ng_v0_oct2023` needs, and where each came from. No plan file exists yet. The rules' placement and size choices are not made.

## Databento instrument ID

`150611`, as an integer. Every record of all seven tape files carries this one ID, and each file's own symbol mapping gives `NG.v.0` as `150611` for its dates.

| Tape file | Records | Instrument IDs in the file |
| --- | --- | --- |
| `NG_v0_mbo_20231001.dbn.zst` | 12,532 | 150611 |
| `NG_v0_mbo_20231002.dbn.zst` | 813,342 | 150611 |
| `NG_v0_mbo_20231003.dbn.zst` | 879,077 | 150611 |
| `NG_v0_mbo_20231015.dbn.zst` | 29,063 | 150611 |
| `NG_v0_mbo_20231016.dbn.zst` | 925,662 | 150611 |
| `NG_v0_mbo_20231017.dbn.zst` | 858,976 | 150611 |
| `NG_v0_mbo_20231018.dbn.zst` | 760,803 | 150611 |

## Nautilus futures instrument definition

Instrument 150611 is NGX3, the November 2023 natural gas future. The exchange's own definition records for it are stored in markets-data under `data/outside/ng_oct2023/raw/curve/NG_FUT_definition_<UTC clock day>.dbn.zst`. NautilusTrader 1.231.0's Databento loader (`DatabentoDataLoader.from_dbn_file`) turned the stored record into the definition below, and `FuturesContract.to_dict` wrote it out. Nothing was typed by hand.

The record used is the one the exchange sent at the Sunday start-up of the first trade week, in `NG_FUT_definition_20231001.dbn.zst` (sha256 `b7d7c3a63c301fb588ff572f806145a4098bf9070b9a92d18b5b88d21867de8b`). The records in the other six stored files that hold one (September 29, October 2, 3, 16, 17 and 18) give the same definition; only `ts_event` and `ts_init` differ.

```json
{
  "type": "FuturesContract",
  "id": "NGX3.GLBX",
  "raw_symbol": "NGX3",
  "asset_class": "COMMODITY",
  "currency": "USD",
  "price_precision": 3,
  "price_increment": "0.001",
  "size_precision": 0,
  "size_increment": "1",
  "multiplier": "10000",
  "max_quantity": null,
  "min_quantity": "1",
  "max_price": null,
  "min_price": null,
  "lot_size": "1",
  "underlying": "NG",
  "activation_ns": 1290637800000000000,
  "expiration_ns": 1698431400000000000,
  "margin_init": "0",
  "margin_maint": "0",
  "maker_fee": "0",
  "taker_fee": "0",
  "ts_event": 1696158307834444822,
  "ts_init": 1696158307834444822,
  "exchange": "XNYM",
  "tick_scheme_name": null,
  "info": {}
}
```

Both fees and both margins are zero in the definition, so the matcher's fee model adds no trade cost. The exchange record also gives a smallest order of 1 contract and a largest of 1,999 (`min_trade_vol`, `max_trade_vol`).

## Two things the code does that a manager's entry depends on

Read from the code on this branch. Nothing was run.

- A manager is attached to every open position on its side, whichever entry rule opened it, Claude's CL rules and Codex's CX rules alike (`engine.py`, `manage`, called for each open position).
- When the parent's trade closes, the engine drops the manager's state for that trade (`engine.py`, `close_trade`). No exit of the manager's own can come after that. With `on_parent_close` set to `hold`, the manager's own position is carried to the run stop and flattened there.

## What was not done

No check, validation or test was run and no paper session was started. The loader call above only converted the stored definition record.
