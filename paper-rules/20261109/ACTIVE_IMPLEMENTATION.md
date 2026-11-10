# Active implementation continuation

User renewed the instruction to continue through model recovery, remaining definitions and a working platform paper setup. Free required software installation, paper-platform configuration, strategy import and simulated trades are explicitly authorized. No purchases or live trades. AWS is unavailable and forbidden. Migration remains paused; no completed research worker may be restarted.

Current platform: CME Practice Simulator in Microsoft Edge. The user rejected the NinjaTrader setup route; its unimplemented draft tests are preserved under deferred/. No NinjaTrader installation is authorized by the current platform choice.

Next implementation slices:

1. Recover exact saved median/model bindings and remaining OL/EX definitions from Git and retained files. Distinguish unrecoverable serialized state from a new reconstruction; do not silently refit.
2. Implement order ownership, execution-report accounting and platform transport with synthetic acceptance checks. Never fabricate a paper fill from a quote or a file-write acknowledgement.
3. Bind actual platform installation, simulation account and feed. Import/load the executable adapter and verify a round trip from a defined rule through platform execution reports.
4. Apply the same feed spans and reporting policy to all candidates; preserve unresolved dependencies visibly and continue resolving them. Publish each verified increment in Git.

NinjaTrader ATI is a documented external signal route. Its File interface accepts DAY/GTC, not IOC, and reports cumulative filled amount/average fill price. Therefore it cannot silently replace the existing IOC policy or be claimed to provide individual execution IDs. A transport may be built, but exact IOC semantics require a different supported adapter or an explicitly separate protocol. Source: https://static.ninjatrader.com/support/helpGuides/nt8/commands_and_valid_parameters.htm and https://static.ninjatrader.com/support/helpGuides/nt8/information_update_files.htm

The Windows .NET Framework C# compilers exist at their standard Framework/Framework64 paths, despite not being in PATH. Earlier wording that only checked PATH must not be read as a machine-wide absence claim.

The native browser automation attempt failed with `coordinate input geometry is unavailable`; its prescribed refreshed-window retry failed with `window capture timed out: timed out waiting on channel`. No successful input or order is claimed. Development and read-only source recovery continue independently.
