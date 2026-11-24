# Run 50: the agent launcher of 297f8a4 read against the code and the model API it calls

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is under the item's number in the platform checklist and in agent-runs.jsonl.

---

REVIEW OF THE AGENT-RUN BUDGET DRAFT (commit 297f8a4), CHECKLIST ITEM 23

How this was done. Everything below is from reading. No project file was executed, imported or parsed, no test was run, and no network call was made. I ran read-only shell commands (ls, grep, sed, find) and read-only git commands (log, show, diff --stat, branch -a, status). `git status` ran twice and can refresh cached stat data in `.git/index`; no tracked file changed. The three draft files are byte-identical to 297f8a4 and hold no tabs, CRs or non-ASCII characters. I loaded the `claude-api` skill and checked the SDK calls against its files: python/claude-api/README.md, streaming.md, sdk-upgrade.md, shared/token-counting.md, shared/api-version-migration.md, shared/error-codes.md and parts of shared/model-migration.md. The live docs were not fetched and no SDK source is installed on this machine, so SDK internals are marked unconfirmed where I rely on memory.

Paths: L = /home/user/paper-trading-platform/paper_platform/agent_launcher.py, W = /home/user/paper-trading-platform/.github/workflows/agent_run.yml, R = /home/user/paper-trading-platform/paper_platform/requirements-agents.txt.

================================================================
FINDINGS
================================================================

1. L:30-35, L:79-85, L:172-174, L:185. A clock stop or run stop can reach the phone as "failure: APIConnectionError".
Does: `BudgetStop` and `RunStop` subclass `Exception`, and the signal handler raises them inside whatever the main thread is doing, after turning the timer off.
Why it matters: from memory of the 0.x SDK source (`_base_client.py`), the request send is wrapped in `except Exception` and re-raised as `APIConnectionError`. If 2.x still does that, a stop that lands inside `count_tokens` or while the stream is opening is recorded and sent as a failure, then re-raised at L:185. Unconfirmed for 2.13.0. The fix holds either way.
Should: stops cannot be absorbed by a library handler, and the handler's own reason outranks any error.
Replace L:30-35:
```python
class BudgetStop(BaseException):
    """The run met an authorized limit. Not an Exception, so no library handler can absorb it."""


class RunStop(BaseException):
    """The runner was told to stop. Not an Exception, for the same reason."""


STOP = []  # the reason of the one stop signal, written by its handler before it raises
```
Replace L:79-85:
```python
    def clock(*_):
        disarm()
        STOP.append(f"{BUDGET_STOP}: the {seconds}-second clock limit")
        raise BudgetStop(STOP[0])

    def stopped(*_):
        disarm()
        STOP.append("run stopped")
        raise RunStop
```
Insert before L:182:
```python
    if STOP:
        # A library may have turned the stop into its own error. The stop is the reason.
        outcome, failure = STOP[0], None
```
Walk of L:145-187 after the change: L:168 and L:170 still catch the stops, L:172 no longer does (intended), L:177-181 unchanged, and `failure` is cleared so L:185 does not re-raise a library error caused by the stop.

2. L:93-109 and session.py:23-24. The phone notice waits behind three git commands that have no time limit.
Does: `finish` writes the record, runs `git add`, `git commit`, `git push` through `session.git` (no timeout), and only then calls `notify`. `disarm` has set SIGTERM and SIGINT to ignored, and git and ssh inherit that.
Why it matters: a stalled push means no phone notice at all until the job is killed. On a cancel the runner allows roughly 10 seconds, and the push is spent first. A stop that lands before L:148 leaves no folder, so L:98 raises `FileNotFoundError` and no record is written. The notice is tried once. The commit message lacks `[skip ci]` (journal_publication.py:123 has it).
Should: notice first ("at once"), git steps time-limited (run.py:80 uses 25 s), folder created if missing, one more notice attempt carrying anything the first could not.
Replace L:93-109:
```python
def publish(root, *args):
    """One markets-data git step with a time limit, so a stalled push cannot hold the stop path."""
    subprocess.run(["git", "-C", str(root), *args], check=True, timeout=25, stdout=subprocess.DEVNULL)


def tell(reason, run):
    """Send one phone notice. Returns None when delivered, or the reason it was not."""
    try:
        notify(reason, run, activity="agent run")
    except (requests.RequestException, RuntimeError, KeyError) as error:
        return "phone notice not delivered: " + type(error).__name__
    return None


def finish(data_root, folder, record, outcome):
    """The one stop path. The phone notice goes first. Each of notice and record goes even when the other fails."""
    record["outcome"] = outcome
    unheard = tell(outcome, record["run"])
    record["phone_notice"] = unheard or "delivered"
    unpublished = None
    try:
        folder.mkdir(parents=True, exist_ok=True)
        record["files"] = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(folder.iterdir()) if path.is_file()
        }
        (folder / "record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        publish(data_root, "add", "--", folder.relative_to(data_root).as_posix())
        publish(data_root, "-c", "user.name=NG agent run", "-c", "user.email=paper@users.noreply.github.com",
                "commit", "-qm", "Record agent run " + record["run"] + " [skip ci]")
        publish(data_root, "push", "origin", "HEAD:refs/heads/agent-runs/" + record["run"])
    except (OSError, subprocess.SubprocessError) as error:
        unpublished = "record not published: " + type(error).__name__
    if unheard or unpublished:
        parts = [outcome]
        if unpublished:
            parts.append(unpublished)
        unheard = tell(". ".join(parts), record["run"])
    errors = []
    if unpublished:
        errors.append(unpublished)
    if unheard:
        errors.append(unheard)
    return errors
```
(`subprocess.SubprocessError` is the shared base of `CalledProcessError` and `TimeoutExpired`. No new import is needed. Not checkable by reading: whether a push from the depth-1, blob-filtered checkout succeeds.)

3. L:160-166, L:182. A call that was sent but did not finish is recorded as zero tokens spent.
Does: `usage` and `budget.charge` are only reached after `get_final_message()` returns. On a clock stop, run stop or API error mid-stream, the record shows `usage: null`, `tokens_spent: 0`, although the input was billed and output was being generated. No partial answer is kept.
Should: the record says a call went out, keeps whatever usage the stream reported, and states the ceiling.
Replace L:160-161:
```python
            record["call_sent"] = True
            seen = {}
            record["usage_seen_in_stream"] = seen
            with client.messages.stream(model=args.model, max_tokens=args.output_reserve, messages=messages) as stream:
                for event in stream:
                    if event.type == "message_start":
                        reported = event.message.usage
                    elif event.type == "message_delta":
                        reported = event.usage
                    else:
                        continue
                    for key in USAGE:
                        value = getattr(reported, key, None)
                        if value is not None:
                            seen[key] = value
                message = stream.get_final_message()
```
Add `call_sent=False` to the record at L:139-143, and insert before L:182:
```python
    if record["call_sent"] and record["usage"] is None:
        # The API reports output only at the end of a stream, so this is a ceiling, not a count.
        record["tokens_spent_at_most"] = record["input_tokens_counted"] + args.output_reserve
```
Confirmed by the skill: `for event in stream` then `get_final_message()`, and `event.usage.output_tokens` on `message_delta`. Unconfirmed: `event.message.usage` on `message_start`, and any `message_delta` usage field other than `output_tokens`.

4. L:162-167. Reported usage is recorded but never compared with the budget.
Does: `budget.charge(usage)` adds the API's figures to `spent`; nothing checks `spent` against `tokens`, so an overrun still ends as "completed".
Should: compare after the call and report an overrun as a budget stop. Insert after L:166:
```python
            if budget.spent > budget.tokens:
                raise BudgetStop(f"{BUDGET_STOP}: the call used {budget.spent} tokens, the limit is {budget.tokens}")
```
Unconfirmed (not in the skill text I read; from memory of the public token-counting page): the count is an estimate and billed input can differ slightly. The gate at L:46 admits a total equal to the budget, so any difference would pass it.

5. L:124-136. Every refusal to start exits with no record and no phone notice.
Does: `p.error(...)` (exit 2) for no go, bad run id, non-positive budget, missing credential, wrong remote. L:134 calls `git` outside any `try`, so a `--data` that is not a checkout ends in an uncaught `CalledProcessError`. This holds even when both Pushover values are present (for example only `ANTHROPIC_API_KEY` is missing).
Should: send a notice when the two Pushover values exist. Insert after L:123 and change each `p.error(` on L:125-136 to `refuse(`:
```python
    def refuse(reason):
        if os.environ.get("PUSHOVER_APP_TOKEN") and os.environ.get("PUSHOVER_USER_KEY"):
            label = args.run if re.fullmatch("[0-9a-f]{32}", args.run) else "preflight"
            tell("not started: " + reason, label)
        p.error(reason)
```
(`tell` is from finding 2. "preflight" is the label run.py:372 uses.) Argparse's own failures (missing or non-integer argument) still exit 2 silently.

6. L:134-136. Only the fetch URL is checked; the push destination is not.
Does: `git remote get-url origin` returns the https fetch URL that action.yml:28 always sets. The push URL is only set when the deploy key is present (action.yml:35, :51). run.py:42-52 checks the push URL; the launcher does not.
Why it matters: a missing or unusable deploy key is discovered after the model call is paid for, and `answer.txt` then exists only on the runner.
Replace L:134-136:
```python
    try:
        remote = git(data_root, "remote", "get-url", "origin").lower().removesuffix(".git")
        push = git(data_root, "remote", "get-url", "--push", "--all", "origin").splitlines()
    except subprocess.CalledProcessError:
        refuse("--data must be a DavisAI1974/markets-data checkout")
    if remote not in ("https://github.com/davisai1974/markets-data", "git@github.com:davisai1974/markets-data"):
        refuse("agent run records belong in DavisAI1974/markets-data")
    if [url.lower().removesuffix(".git") for url in push] != ["git@github.com:davisai1974/markets-data"]:
        refuse("the markets-data checkout has no SSH push destination: the deploy key is missing")
```
Insert after L:151 (before any API request), as verify_paper_platform.yml:77 does:
```python
            publish(data_root, "push", "--dry-run", "origin", "HEAD:refs/heads/agent-runs/" + args.run)
```

7. L:116-117, L:59-60, W:9-16, W:69. The brief and attachments can be any path on the runner, and are sent to the model and published.
Does: `--brief` and `--attach` are read with `path.read_bytes()` with no confinement. The step's environment holds the API key and both Pushover values (W:64-66), so a path such as `/proc/self/environ` would go to the API and into `request.txt` on a markets-data branch. `for path in $ATTACHMENTS` also glob-expands.
Should: only files committed in the platform repository. Insert before L:137:
```python
    platform = Path(__file__).resolve().parents[1]
    for path in [args.brief, *args.attach]:
        inside = path.resolve()
        if not inside.is_relative_to(platform):
            refuse("the brief and its files must be inside the platform repository: " + path.as_posix())
        try:
            git(platform, "ls-files", "--error-unmatch", "--", inside.relative_to(platform).as_posix())
        except subprocess.CalledProcessError:
            refuse("the brief and its files must be committed in the platform repository: " + path.as_posix())
```
Replace W:68-71:
```bash
          read -r -a paths <<< "$ATTACHMENTS"
          attach_args=()
          for path in "${paths[@]}"; do
            attach_args+=(--attach "$path")
          done
```

8. W:38, W:73. No job time limit, and the launcher is a child of bash.
Does: there is no `timeout-minutes` (GitHub's default is 360 minutes; the other workflows set 355 or 365). The seconds budget has no upper bound, so a large value is cut off by the job limit instead of the launcher's timer. Python runs as a child of the step's bash script.
Unconfirmed by reading: whether the runner's cancel or timeout signal reaches a child of the script shell. record_ng_mbo.yml:71 traps and forwards it by hand. `exec` removes the question.
Replace W:38:
```yaml
    runs-on: ubuntu-latest
    timeout-minutes: 355
```
Replace W:73 (same line with `exec` in front):
```bash
          exec python -m paper_platform.agent_launcher --data agent-output --run "$run_id" --brief "$BRIEF" "${attach_args[@]}" --model "$MODEL" --output-reserve "$OUTPUT_RESERVE" --token-budget "$TOKEN_BUDGET" --seconds-budget "$SECONDS_BUDGET" --greg-go
```
Fact for item 4, no replacement proposed: the clock starts at L:147, after checkout, pip install and module imports, and it does not cover `finish`. A seconds budget above about 5.75 hours cannot be kept by the job; `run_clock.LIMIT_SECONDS` is the existing constant if a cap is wanted.

9. L:139-143, L:164. The record has no time fields and no call identifier.
Does: fields are run, activity, model, platform_commit, budget (tokens, seconds, output_reserve), sources (path and sha256 of brief and each attachment), input_tokens_counted, usage (four counts), served_model, stop_reason, outcome, tokens_spent. There is no start time, end time or elapsed time, no API message id, no Actions run id, no fingerprint of `request.txt` or `answer.txt`.
Add at L:12-19 (alphabetical): `import time`. Replace L:139-143:
```python
    began = time.monotonic()
    record = dict(
        run=args.run, activity="agent run", model=args.model, platform_commit=None,
        actions_run=os.environ.get("GITHUB_RUN_ID"), started_ns=time.time_ns(), ended_ns=None, elapsed_seconds=None,
        budget=dict(tokens=args.token_budget, seconds=args.seconds_budget, output_reserve=args.output_reserve),
        sources=None, input_tokens_counted=None, call_sent=False, usage=None, served_model=None,
        stop_reason=None, message_id=None,
    )
```
Replace L:164:
```python
            record.update(usage=usage, served_model=message.model, stop_reason=message.stop_reason, message_id=message.id)
```
Insert before L:183:
```python
    record["ended_ns"] = time.time_ns()
    record["elapsed_seconds"] = round(time.monotonic() - began, 3)
```
(File fingerprints are in the finding 2 replacement. `started_ns` follows `recorded_ns` at session.py:156.)

10. L:151, L:166, L:99-102, action.yml:2 and :28. The brief, every attached file and the answer are published in full.
Does: `request.txt` (brief plus numbered attachment text) and `answer.txt` are written beside `record.json` in `paper-trading/agent-runs/<run>/` and pushed on branch `agent-runs/<run>` of markets-data, which action.yml fetches anonymously and calls public. `record.json` itself holds neither text. No replacement lines: whether brief and answer belong on that branch is Greg's decision.

11. R:2. `anthropic==2.13.0` is not confirmed.
The skill establishes 2.0.0 as the first Python release that sends API version 2026-10-21; it does not establish 2.13.0. I did not query PyPI. Also unverified: that it resolves alongside nautilus_trader==1.231.0, databento==0.81.0, fastapi==0.115.0. Because L:23 imports `notify` from run.py, the launcher needs the whole platform stack installed and importable (fastapi, pydantic, databento_dbn, nautilus_trader, root, crypto_ng) before `main` starts; a failure there happens before the launcher can notify. Check to make (not run): `pip index versions anthropic`.

12. W whole file, run_end_notice.yml:3-9. Both depend on the default branch.
`git branch -a` shows only `codex/strategy-trades-and-mbo-capture`; the checkout cannot show the default branch. The wishlist (lines 3, 133) says "implemented on main" and that the run-end notice "takes effect after merge". Until agent_run.yml is on the default branch it cannot be dispatched from the Actions page, and until run_end_notice.yml is there, nothing reports a job that dies before or outside the launcher.

================================================================
ITEM 5: EVERY EXIT PATH, AS DRAFTED
================================================================
- Completed (`end_turn`): record, request, answer pushed; notice "completed"; exit 0.
- Model stopped otherwise (`max_tokens`, `refusal`, other): record with usage; notice "the model stopped: X"; exit 1.
- Token budget stop at the gate: count request only, no model call; record with the count, `usage: null`; notice with the three figures; exit 1.
- Clock stop while reading the stream or outside the SDK: notice "budget reached: the N-second clock limit"; record shows zero tokens spent (finding 3); exit 1.
- Clock stop inside an SDK send: possibly "failure: APIConnectionError" (finding 1, unconfirmed).
- Run stop (SIGTERM or SIGINT reaching Python): "run stopped", same record gap; may never reach Python (finding 8); about 10 seconds before the kill, spent on the push first (finding 2).
- API error (401, 404 unknown model, 400, 429, 5xx, connection): no retry; notice "failure: <class>"; record pushed; traceback; exit 1. Mid-stream: usage not recorded.
- Brief or attachment unreadable or not UTF-8, or `import anthropic` fails: failure path, record and notice.
- Missing secret, no go, bad run id, non-positive budget, wrong remote: exit 2, no record, no notice (finding 5).
- Bad arguments at argparse: exit 2, no record, no notice.
- `--data` not a checkout: uncaught error at L:134, no record, no notice.
- Publish failure: notice carries "record not published: CalledProcessError"; answer lost with the runner; exit 1. Publish hang: no notice.
- Notice failure: record already pushed, one attempt only, exit 1.
- Both fail: exit 1, job log only.
- Signal before `arm`, or failure in checkout, deploy-key step, setup-python, pip install, module import: no launcher notice; run_end_notice.yml only, once on the default branch.
- Job skipped (not Greg, no go, re-run attempt): nothing, as run_end_notice.yml:14 intends.
Every non-completed outcome exits non-zero, so after merge Greg gets a second notice from run_end_notice.yml (wishlist line 133 says so).

================================================================
READ AND FOUND MATCHING
================================================================
Python (item 1): no syntax fault found by reading. All names defined; imports present for every name used. `notify(reason, run, *, activity=)` at run.py:28 matches the call at L:106. `git(root, *args)` at session.py:23 matches every call. `git -C <root> -c k=v commit -qm` is a valid order. The nested try at L:145-181 is valid. journal_publication.py and run_clock.py are not used by the launcher.
SDK (item 2), against the skill: `anthropic.Anthropic(max_retries=0)` (0 disables retries); `client.messages.count_tokens(model=, messages=).input_tokens`; `client.messages.stream(model=, max_tokens=, messages=)` with `stream.get_final_message()`; `message.usage` fields `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`; `message.model`; `message.stop_reason`; text blocks via `block.type == "text"` / `block.text`; stop reasons `end_turn`, `max_tokens`, `refusal`, `pause_turn`, `stop_sequence` (and `model_context_window_exceeded` in the migration guide) all fall into "completed" or "the model stopped: X". No sampling parameter is sent, which API version 2026-10-21 requires. Python 3.13 meets the SDK's 3.10 floor. No model ID is hard-coded: it is free text from the workflow input, so there is none to confirm; an unknown one fails at the count request with no model call. The skill's current IDs carry no date suffix (for example `claude-opus-5-5`, `claude-fable-5-2`, `claude-sonnet-5-5`, `claude-haiku-5-5`).
Token budget (item 3): the refusal at L:159 comes before the model call at L:160. `max_tokens` equals the output reserve, and the skill states `max_tokens` is a hard limit on thinking plus response. One call only, no retry, no `fallbacks`, so no second model run outside the gate. On models with always-on thinking, a small reserve can end as "the model stopped: max_tokens" with little or no answer text.
Clock (item 4): `setitimer(ITIMER_REAL)` with a handler that raises in the main thread; the stop path at L:182-183 still runs after it. The process does not just die.
Workflow (item 6): the gate at W:37 is identical to purchased_mbo_paper.yml:46, live_ng_paper.yml:32 and record_ng_mbo.yml:28 (go checkbox, actor and triggering actor both DavisAI1974, first attempt only). There is no typed confirmation here or in any other workflow. Secret names `PUSHOVER_APP_TOKEN`, `PUSHOVER_USER_KEY`, `MARKETS_DATA_DEPLOY_KEY` match the other workflows; `ANTHROPIC_API_KEY` is new and Greg's to add (wishlist line 117). No `vars` are read. Platform checkout matches record_ng_mbo.yml:39-43. The markets-data checkout and SSH push use the same composite action and key as the others; the run folder is inside the sparse cone. setup-python pin and version match. Nested `-r requirements.txt` resolves relative to the file. Inputs reach the shell through `env`, not interpolation. `permissions: contents: read` matches. The workflow name matches run_end_notice.yml:8. No `concurrency` group: two runs can overlap, each under its own budget.
Secrets (item 7): keys are read from the environment only; none is written to the record, the request file, a commit or a print by the launcher. Errors are reported by class name only. The deploy key goes to ssh-agent from stdin (action.yml:43-44). The one route found is finding 7.

Not checkable by reading: the push from the shallow blob-filtered checkout, runner signal delivery, dependency resolution, whether markets-data runs CI on push, receipt of a notice on the phone.
