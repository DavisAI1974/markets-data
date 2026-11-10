# What to do with this package

The package is a research and paper-rule specification. It is **not yet a CME or NinjaTrader executable import**. Downloading it does not start trading.

For the CME Practice Simulator already open on your computer, a supported custom JSON strategy upload or automation API has not been established. The [official simulator guide](https://www.cmegroup.com/education/brochures-and-handbooks/trading-simulator-guide) describes manual trading tools. There is no verified upload step to give you for this package.

CME remains the selected platform. The NinjaTrader exploration is deferred. Keep the existing CME Practice Mode session open; no additional sign-in is currently needed. Browser login has been confirmed, but our desktop tool cannot reliably operate the controls.

Before automated paper trials, the remaining implementation must bind the required data and model states, establish a supported CME execution route, and verify real platform execution reports. Native order-ID rules require a suitable order-level feed; the visible aggregate ladder does not establish that identity. Missing models and unavailable source fields remain attached to their candidates, with no substituted proxies.

Once that adapter exists, the operational sequence is:

1. Import the compiled platform package using its supported import command.
2. Select a simulation account and the exact Henry Hub contract matching the feed or playback recording. NGZ6 was shown in your CME screenshot; playback contract identity must match its own recording.
3. Load the complete rule manifest. Use the same span, costs, order-size policy and reporting for every candidate, with separate attribution so opposing rules cannot close each other's positions.
4. Connect the matching replay or delayed feed, then enable the strategies. Verify entries, exits and fills in the platform's execution reports and publish the full ledger back to this repository.

No standalone historical strategy test substitutes for those platform paper trades. No platform orders or fills were generated in this reconciliation pass. Session start/end scheduling remains deferred as requested.
