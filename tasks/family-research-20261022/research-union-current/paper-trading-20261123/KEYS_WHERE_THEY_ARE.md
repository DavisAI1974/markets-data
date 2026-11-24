# Where the keys are kept (names only, never a value)

Greg, 2026-11-24: "Write those into something so i don't have to keep finding them for you every chat".
His own rule, item 32 of the platform checklist: keys and tokens never in any file, print or commit. markets-data and
paper-trading-platform are public. So this file holds the NAMES and the PLACES. A session reads this file and checks
the place by name. It does not ask Greg for a key.

| Key | Name it is read by | Where it is kept | Who reads it |
| --- | --- | --- | --- |
| Pushover application token (application "Paper trade alert") | `PUSHOVER_APP_TOKEN` | GitHub: paper-trading-platform, Settings, Secrets and variables, Actions | every paper workflow and the run-end notice |
| Pushover user key | `PUSHOVER_USER_KEY` | the same place | the same |
| The same two, for a session | the same two names | the "Markets" cloud environment, as environment variables (Pushover takes them in the request body, so a network secret cannot carry them) | the agent budget hook; a test notice from a session |
| markets-data deploy key | `MARKETS_DATA_DEPLOY_KEY` | GitHub Actions secrets, paper-trading-platform | the workflows that push records |
| markets-data token | `MARKETS_DATA_TOKEN` | the same place | the stored-tape run |
| Capture key | `PAPER_CAPTURE_KEY` | the same place | recorder and checkpoint |
| Phone page writer token | `PAPER_RELAY_TOKEN` | the same place, and on Render | the runner's posts to the phone page |
| Phone page address | `PAPER_RELAY_URL` | GitHub Actions VARIABLE (not a secret) | the runner |
| Phone page password | `PAPER_VIEW_PASSWORD` | Render only | Greg's sign-in to the page |
| Databento | `DATABENTO_API_KEY` | GitHub Actions secrets; in a cloud session the proxy signs requests to hist.databento.com by itself | live recorder; sessions |
| tastytrade SANDBOX test keys | `TASTY_SANDBOX_*` | `tasty-sandbox.env` beside this file, on Greg's word ("they are only test keys") | sandbox only |

How a session checks, without printing a value: `test -n "$PUSHOVER_APP_TOKEN" && echo set`.

State on 2026-11-24, end of the twenty-second session: the two Pushover names were NOT set in the Markets environment
(checked by name). Greg showed both values in screenshots in that chat; Claude wrote them nowhere. A session cannot
enter them: the environment's own rule is that the person types a secret into its settings. Whether the GitHub
Actions secret `PUSHOVER_APP_TOKEN` holds the token of the application "Paper trade alert" cannot be read from a
session; the first run's start notice shows it.

## What a run of the stored tape reads (added 2026-11-24, twenty-third session)

Read from `purchased_mbo_paper.yml` and `.github/actions/markets-data/action.yml` on the platform branch. The
workflow reads every one of these from GitHub by itself. No session holds one, needs one, or asks Greg for one.

| Name | Needed for the stored-tape run (tape `purchased-archive`) | State, as far as it can be seen without the value |
| --- | --- | --- |
| `MARKETS_DATA_DEPLOY_KEY` | yes: it pushes the run's records | set: the verification runs used it and passed |
| `PUSHOVER_APP_TOKEN`, `PUSHOVER_USER_KEY` | yes: the runner refuses to start without them | recorded as set by Codex on 2026-11-23 |
| `PAPER_RELAY_URL` (a variable), `PAPER_RELAY_TOKEN` | yes: the runner refuses to start without the phone page | NOT listed when Codex looked on 2026-11-23; not seen since |
| `MARKETS_DATA_TOKEN` | NO: with the deploy key the push goes over SSH and the token is never read | does not matter |
| `PAPER_CAPTURE_KEY` | NO: only the `purchased-capture` and `live-capture` tapes read it | does not matter |
| `DATABENTO_API_KEY` | NO: only a live recording reads it | does not matter |
| any tastytrade or broker key | NO: the platform is our own; it sends no order anywhere | does not matter |

A session cannot list the secret names of the repository. A name that is missing shows itself in the run's first
minute: the runner refuses to start and says which name.
