# What to do with this package

The package is a research and paper-rule specification. It is **not yet a CME or NinjaTrader executable import**. Downloading it does not start trading.

For the CME Practice Simulator already open on your computer, a supported custom JSON strategy upload or automation API has not been established. The [official simulator guide](https://www.cmegroup.com/education/brochures-and-handbooks/trading-simulator-guide) describes manual trading tools. There is no verified upload step to give you for this package.

NinjaTrader's documented route is **Control Center → Tools → Import → NinjaScript** for a platform-specific ZIP. See the [official import guide](https://static.ninjatrader.com/support/helpGuides/nt8/import.htm). The ZIP in this repository is a specification archive, not a NinjaScript ZIP, and must not be imported as one.

Before automated paper trials, the remaining implementation must bind the required data and model states, compile a platform adapter, and verify its import. Native order-ID rules require a suitable order-level feed; standard NinjaTrader depth callbacks do not establish that identity. Missing models and unavailable source fields remain attached to their candidates, with no substituted proxies.

Once that adapter exists, the operational sequence is:

1. Import the compiled platform package using its supported import command.
2. Select a simulation account and the exact Henry Hub contract matching the feed or playback recording. NGZ6 was shown in your CME screenshot; playback contract identity must match its own recording.
3. Load the complete rule manifest. Use the same span, costs, order-size policy and reporting for every candidate, with separate attribution so opposing rules cannot close each other's positions.
4. Connect the matching replay or delayed feed, then enable the strategies. Verify entries, exits and fills in the platform's execution reports and publish the full ledger back to this repository.

No standalone historical strategy test substitutes for those platform paper trades. No platform orders or fills were generated in this reconciliation pass. Session start/end scheduling remains deferred as requested.
