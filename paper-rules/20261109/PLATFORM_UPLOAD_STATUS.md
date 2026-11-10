# Platform upload status

The requested proving ground is automated trading in a platform paper account, with platform-recorded entries, exits and fills. Delayed data or old playback is acceptable. A JSON specification, local predicate check or historical midpoint calculation is not such a trade.

## CME Practice Simulator

Current account state was read in Microsoft Edge: Practice Mode, NGZ6 open, $100,000 practice funds, no positions or orders. Click input failed with `coordinate input geometry is unavailable`. Keyboard find opened, but its editable control was not available to the cached input API; no order or account change followed. The separate browser connector did not expose this browser. Login alone does not establish functioning automation.

The official [CME simulator guide](https://www.cmegroup.com/education/brochures-and-handbooks/trading-simulator-guide) documents manual order tickets, charting, the price ladder, trade log and trade plan. It does not document importing custom JSON strategies or a strategy-execution API. We have not established a supported upload or automated execution route for this account. Do not give the user a fictional Upload JSON step or treat the Trade Plan form as an execution engine.

## Deferred NinjaTrader research (user selected CME)

NinjaTrader documents importing a NinjaScript ZIP through Control Center → Tools → Import → NinjaScript. That imports platform code, not arbitrary rule JSON. See the [official import instructions](https://static.ninjatrader.com/support/helpGuides/nt8/import.htm).

Its [strategy instructions](https://static.ninjatrader.com/support/helpGuides/nt8/running_a_ninjascript_strategy.htm) support a strategy in a simulation account, including replay connections. A compatible compiled strategy and its input data are required before enabling it. The configured account and Enabled property control execution.

Standard [market-depth events](https://static.ninjatrader.com/support/helpGuides/nt8/marketdeptheventargs.htm) expose ladder position, price, volume, side and market-maker metadata; this interface does not supply the source native exchange order-ID lifecycle required by every same-order hypothesis. A market-maker identifier is not a native order identity. Do not replace same-order fills/cancels/repricing with aggregate-size changes and call it the same rule. The [OnMarketDepth guide](https://static.ninjatrader.com/support/helpGuides/nt8/onmarketdepth.htm) also warns against assuming fixed ordering between trade and depth callbacks.

No NinjaTrader installation was established. A later check located Windows .NET Framework C# compilers; the earlier PATH-only absence statement was incomplete. This platform route is deferred at the user's instruction. No platform compile, native import or automatic paper trade has been verified. No account, purchase, order or platform configuration was changed by this pass.

## What an honest upload handoff must contain

1. A versioned rule bundle and exact feature/model dependencies for every candidate.
2. A platform-specific strategy package implementing those rules, with required data adapters and verified compilation/import.
3. A replay/live-delayed feed carrying the exact required observations and clocks. Preserve missing inputs without silently substituting proxies or removing candidates.
4. Independent rule attribution so opposing strategies do not overwrite each other's position. Use equal test spans and handling for every candidate.
5. A verified sequence for selecting the paper account, connecting the feed, loading the package, and enabling the strategy, plus confirmation of platform fills.

Until that route is implemented and verified, the user can download the versioned research/rule bundle from GitHub, but it is not truthful to say it can already be uploaded into CME to run automatically. Platform limitations do not remove any hypothesis from the paper universe.
