# Run 59: item 32, credential handling: every place a key or token could reach a file, a print, a commit or a process listing

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of checklist item 32 ("Keys and tokens never in any file, print or commit"), branch codex/strategy-trades-and-mbo-capture at e12bfde. Everything below comes from reading files. I ran no code, test, workflow or network call, and changed no file. I looked only at this repository and did not look for the set-aside markets-data sandbox credential.

**How much I read:**
- **Read in full, line by line:** all 8 workflows; .github/actions/markets-data/action.yml; run.py, journal_publication.py, run_live.py, capture_backup.py, record_mbo.py, relay.py, restore_view.py, agent_launcher.py, agent_budget_hook.py; render.yaml and the three requirements files.
- **Read in part:** session.py lines 1-160 and 300-409. Lines 160-300 were only searched for env, url, token, header, print and raise.
- **Searched for credential words only, not read line by line:** capture.py, views.py, api.py, live_contract.py, feed.py, monitor.html, docs/platform/previews/ng-paper.html, all of docs/, README.md, AGENTS.md, and paper_platform/README.md (that one partly read, lines 30-40 and 50-60).

## Table (question 1): each credential, where it is read, where its value goes

| Name (kind) | Where it is read | Where the value goes |
|---|---|---|
| MARKETS_DATA_DEPLOY_KEY (Actions secret) | Passed as `deploy-key:` at agent_run.yml:52, live_ng_paper.yml:56 and 62, purchased_mbo_paper.yml:68, record_ng_mbo.yml:48, verify_paper_platform.yml:73. The action reads it at action.yml:38 (env DEPLOY_KEY). | Step environment, then the ssh-add here-string at action.yml:44, then ssh-agent memory. The agent's own environment drops DEPLOY_KEY (`env -u`, line 43). Only the socket path goes into $GITHUB_ENV (line 48), so every later step in the job can sign with the key. Not written to argv, the URL, .git/config or a print. |
| MARKETS_DATA_TOKEN (Actions secret) | purchased_mbo_paper.yml:128; run.py:48 and 66 | run.py:66-70 puts it base64-encoded in GIT_CONFIG_VALUE_0, an environment variable of every git child, and only when the push URL is HTTPS. run.py:64 copies the whole environment, so every git and ssh child gets the raw value as well. Not in argv, URL, disk or print. run_live.py:256 allows it into the `run` child. |
| PAPER_CAPTURE_KEY (Actions secret) | Job-level env at live_ng_paper.yml:41 and record_ng_mbo.yml:35; step env at purchased_mbo_paper.yml:114; read at capture_backup.py:30 | Held in os.environ and the Fernet object for the whole process, and inherited by every git child through session.py:24. At job level it is in the env of every step, including `pip install` and setup-python. run_live.py:239 gives it only to the backup child. |
| DATABENTO_API_KEY (Actions secret) | live_ng_paper.yml:75, record_ng_mbo.yml:63. record_mbo.py:130 checks it is present; the SDK reads it from env at record_mbo.py:133 (`db.Live(...)` takes no key argument). | In-process SDK use. In record_ng_mbo.yml it also reaches the `capture_backup follow` process, which does not need it. run_live.py:242 gives it only to the recorder. |
| PAPER_RELAY_TOKEN (Actions secret; Render env) | Actions: live_ng_paper.yml:74, purchased_mbo_paper.yml:130, restore_phone_dashboard.yml:41. Code: run.py:63, restore_view.py:84, relay.py:35. Render: render.yaml:12 (`sync: false`, no value in the file). | HTTP `Authorization: Bearer` header on POSTs with allow_redirects=False (run.py:88, 116, 147; restore_view.py:52). Compared on the relay at relay.py:80. Also in the env of git children (run.py:64). Not in URL, print or journal. |
| PAPER_VIEW_PASSWORD (Render env) | relay.py:34; render.yaml:10 (`sync: false`) | Held in memory as the expected `Basic base64("greg:"+pw)` string (relay.py:38) and compared at relay.py:68. Not logged. |
| PUSHOVER_APP_TOKEN, PUSHOVER_USER_KEY (Actions secrets) | agent_run.yml:66-67, live_ng_paper.yml:76-77, purchased_mbo_paper.yml:131-132, record_ng_mbo.yml:64-65, run_end_notice.yml:22-23. Code: run.py:32-33, agent_budget_hook.py:68, agent_launcher.py:150 and 158, record_mbo.py:217 | POST form body (run.py:29-37, agent_budget_hook.py:71-73). **curl command-line arguments** at run_end_notice.yml:30-31. Env of git children. On failure the code publishes only error type names. |
| ANTHROPIC_API_KEY (Actions secret) | agent_run.yml:65; presence check at agent_launcher.py:158; the SDK reads it from env at agent_launcher.py:200 | SDK request header. Also in the env of the git children at agent_launcher.py:99. Not in record.json or any print. |
| PAPER_RELAY_URL (Actions variable, not a secret, so not masked in logs) | live_ng_paper.yml:73, purchased_mbo_paper.yml:129, restore_phone_dashboard.yml:40; run.py:228, restore_view.py:79 | Request URLs. The text of a requests exception includes it (run.py:245 `raise_for_status`). See finding 6. |
| GITHUB_TOKEN | Not read anywhere. Every checkout is `git init` plus an anonymous HTTPS fetch, so nothing persists it into .git/config. | none |

**What goes into $GITHUB_ENV:**
- action.yml:48-49: `SSH_AUTH_SOCK=<socket path>` and `GIT_SSH_COMMAND=ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=$RUNNER_TEMP/markets-data-known-hosts`.
- PAPER_RUN_STARTED_NS (live_ng_paper.yml:44, purchased_mbo_paper.yml:53).
- PLATFORM_ROOT (purchased_mbo_paper.yml:101).
- RECORDED_CAPTURE and CAPTURE_COMMIT (purchased_mbo_paper.yml:118-119).

None of these is a secret value. The socket path does let any later process in the job use the key.

## Findings

**1. run_end_notice.yml:30-31: both Pushover values are curl command-line arguments.**
- What the code does: it passes `--form-string "token=$PUSHOVER_APP_TOKEN"` and `--form-string "user=$PUSHOVER_USER_KEY"` as arguments to the external curl process, so both values sit in /proc/<pid>/cmdline while curl runs.
- What item 32 requires: no key reaches a process listing.
- Replacement for lines 29-33 (printf is a bash builtin, so the values never appear in an argument list):
```
          printf 'form-string = "token=%s"\nform-string = "user=%s"\n' "$PUSHOVER_APP_TOKEN" "$PUSHOVER_USER_KEY" |
            curl --fail --silent --show-error --max-time 5 --retry 3 --retry-delay 2 --config - \
              --form-string "message=NG Actions run $WORKFLOW #$RUN_NUMBER ended: $CONCLUSION" \
              https://api.pushover.net/1/messages.json > /dev/null
```
- Certain from the code that the values are in argv. Who can list processes on a hosted runner depends on the runner image.

**2. action.yml:44: the deploy key is fed to ssh-add through a here-string.**
- What the code does: `ssh-add -q - <<< "$DEPLOY_KEY"`. Bash before 5.1 always backs a here-string with a temporary file in $TMPDIR. Bash 5.1 and later uses a pipe only when the text fits the pipe buffer.
- What item 32 requires: the key never in a file. The item's own status says the key goes "directly to an SSH agent".
- Replacement for line 44:
```
          printf '%s\n' "$DEPLOY_KEY" | ssh-add -q -
```
- Depends on behaviour not readable here: the bash version on ubuntu-latest and the key's size. If a temp file is used, bash unlinks it, but it does exist on disk while ssh-add reads it.

**3. live_ng_paper.yml:41 and record_ng_mbo.yml:35: PAPER_CAPTURE_KEY is set at job level.**
- What the code does: the key is in the environment of every step. That includes the composite action, setup-python, and `pip install` (live_ng_paper.yml:66, record_ng_mbo.yml:57), where package build code can run with it.
- What item 32 requires: the key goes only to the processes that use it.
- Fix: delete the job-level line and add `PAPER_CAPTURE_KEY: ${{ secrets.PAPER_CAPTURE_KEY }}` under `env:` in only these steps:
  - live_ng_paper.yml: "Restore the last published capture checkpoint" (67), "Run the recorder and paper session together" (70), "Persist the final committed deliveries" (81).
  - record_ng_mbo.yml: the steps at lines 58, 61 and 84.
- Certain from the code. Whether pip actually runs build code depends on which wheels resolve: requirements.txt:5 and :7 are ranges, transitive dependencies are not pinned, and nothing uses `--require-hashes`.

**4. The SSH agent socket reaches `pip install` in every publishing workflow.**
- What the code does: the deploy-key checkout puts SSH_AUTH_SOCK into $GITHUB_ENV before `pip install` runs: agent_run.yml:48→56, live_ng_paper.yml:52→66, record_ng_mbo.yml:44→57, purchased_mbo_paper.yml:61→103. Any process in those steps can push to markets-data with the deploy key.
- What item 32 requires: a credential reaches only the process that needs it.
- Smallest fix: move the `uses: actions/setup-python` and `pip install` steps above the first `uses: ./.github/actions/markets-data` that passes `deploy-key`. In agent_run.yml, live_ng_paper.yml and record_ng_mbo.yml these steps do not depend on that checkout. In purchased_mbo_paper.yml, move the block at lines 61-68 to just after line 103 ("Restore the recorded week" is the first step that uses purchased-inputs).
- Certain from the code. Exposure depends on the same pip behaviour as finding 3.

**5. record_ng_mbo.yml:61-69: both background processes inherit the whole step environment.**
- What the code does: `capture_backup follow` gets DATABENTO_API_KEY and both Pushover values, which it does not use. `record_mbo` gets PAPER_CAPTURE_KEY (job level) and the agent socket, which it does not use. This path does not go through run_live.launch.
- What item 32 requires: each child gets only its own credentials.
- Replacement for lines 67 and 69 (`env` replaces itself with python, so `$!` is still the python pid):
```
          env -u DATABENTO_API_KEY -u PUSHOVER_APP_TOKEN -u PUSHOVER_USER_KEY python -m paper_platform.capture_backup follow --data purchased-inputs --checkout checkpoint --trade-day "$TRADE_DAY" --source "$SOURCE" &
          env -u PAPER_CAPTURE_KEY -u SSH_AUTH_SOCK python -m paper_platform.record_mbo --data purchased-inputs --trade-day "$TRADE_DAY" --source "$SOURCE" --message-budget "$DELIVERY_BUDGET" --greg-go &
```
- Certain from the code.

**6. run.py:229 and restore_view.py:81: the URL check misses a password with an empty user name.**
- What the code does: both reject PAPER_RELAY_URL only when `urlsplit(url).username` is truthy. The stdlib `_userinfo` (I read /usr/lib/python3.11/urllib/parse.py:194-203) returns username `''` for `https://:secret@host`, so that URL passes. run.py also does not reject a query string, so `?token=` passes as well. The value would then appear in requests exception text, for example from `raise_for_status` at run.py:245, and in the Actions log, where variables are not masked.
- What item 32 requires: no key in a URL or a print.
- Replacement for run.py:229:
```
    if urlsplit(url).scheme != "https" or not urlsplit(url).hostname or "@" in urlsplit(url).netloc or urlsplit(url).query:
```
- Replacement for restore_view.py:81:
```
    if target.scheme != "https" or not target.hostname or "@" in target.netloc or target.query or target.fragment:
```
- Certain for Python 3.11. That 3.13 (the version the workflows use) has the same `_userinfo` is depends-on, not read.

**7. run_live.py:182-183: launch removes a fixed list of names, which is incomplete.**
- What the code does: any name not on the list is passed to all three children. Missing today: ANTHROPIC_API_KEY, PAPER_VIEW_PASSWORD, and SSH_AUTH_SOCK. The recorder (`record_mbo`) never pushes but can still use the deploy key. No missing secret name is in live_ng_paper.yml's env today, so nothing reaches a child now. This finding is about the next name to be added.
- What item 32 requires: no process holds a credential it does not need.
- Replacement for lines 182-183:
```
    for key in ("DATABENTO_API_KEY", "PAPER_CAPTURE_KEY", "PAPER_RELAY_TOKEN", "PUSHOVER_APP_TOKEN",
                "PUSHOVER_USER_KEY", "MARKETS_DATA_TOKEN", "ANTHROPIC_API_KEY", "PAPER_VIEW_PASSWORD", "SSH_AUTH_SOCK"):
```
- Also change line 239 to `{"PAPER_CAPTURE_KEY", "SSH_AUTH_SOCK"})` and line 256 to `notices | {"PAPER_RELAY_TOKEN", "MARKETS_DATA_TOKEN", "SSH_AUTH_SOCK"})`.
- Certain from the code.

**8. purchased_mbo_paper.yml:128: MARKETS_DATA_TOKEN is passed but never used.**
- What the code does: the same job gives `deploy-key` at line 68, so action.yml:51 sets an SSH push URL. writer_remote (run.py:50-52) then returns the SSH URL and the HTTPS branch at run.py:65 never runs. The token still enters run.py's environment and, through run.py:64, every git and ssh child.
- What item 32 requires: no credential where it is not needed. The item 32 status says the in-memory key work is still in draft.
- Fix: delete line 128.
- Certain from the code.

**9. Git children inherit the full environment, including secrets they do not need.**
- Where:
  - run.py:64: `self.env = dict(os.environ, ...)`.
  - session.py:24: `git()` passes no env.
  - agent_launcher.py:99: no env.
- Effect: every git child, and the ssh it starts, carries PAPER_RELAY_TOKEN, both Pushover values, ANTHROPIC_API_KEY (agent run), and PAPER_CAPTURE_KEY (capture_backup through session.git). The values are only in /proc/<pid>/environ, which only the same user can read. Never argv, URL or disk.
- Smallest fix for the key with the widest reach, capture_backup.py:30:
```
        self.cipher = Fernet(os.environ.pop("PAPER_CAPTURE_KEY").encode())
```
- For run.py:64:
```
        self.env = {k: v for k, v in os.environ.items() if k not in ("PAPER_RELAY_TOKEN", "PUSHOVER_APP_TOKEN", "PUSHOVER_USER_KEY", "MARKETS_DATA_TOKEN", "DATABENTO_API_KEY", "PAPER_CAPTURE_KEY", "ANTHROPIC_API_KEY")}
        self.env["GIT_TERMINAL_PROMPT"] = "0"
```
- Certain from the code. How far this reaches depends on runner user isolation.

**10. agent_launcher.py:243 and record_mbo.py (uncaught non-CaptureFailure errors) send SDK exceptions to the Actions log as full tracebacks.**
- The code puts only `type(error).__name__` into record.json and the phone notices. The re-raised exception's text is whatever the anthropic or databento SDK puts there.
- No replacement proposed.
- Depends on SDK behaviour not readable here. I found no code path that formats a key into a message.

**11. capture_backup.py:77-81 (this answers question 8; it is not a key leak).**
- What the encryption covers: each 4 MiB block of the SQLite snapshot is gzip-compressed and then Fernet-encrypted (AES-128-CBC plus HMAC-SHA256). The block list (the manifest, `checkpoint.enc`) is also encrypted. This protects the captured DBN frames, receive nanoseconds and connection records in markets-data. paper_platform/README.md:35 says that repository is public.
- What it does not hide: each block's file name is the SHA-256 of the unencrypted block. A guessed block can therefore be confirmed. Block count, which blocks change from one checkpoint to the next, and commit timing are also visible.
- Where the key is while in use: Actions secret, then env (job level, finding 3), then os.environ plus the Fernet object for the life of the process, then the git children (finding 9). No code line writes it to disk, prints it or commits it. The restored database is unencrypted on the runner disk by design (capture_backup.py:54).
- If the names should be opaque, replace line 77 with `digest = hmac.new(self.cipher_key, block, "sha256").hexdigest()` and change the check at line 59 to match. That is a format change: existing checkpoints would no longer restore.
- Certain from the code.

**12. Relay (question 6). Nothing here conflicts with item 32.**
- Both credentials are compared with `secrets.compare_digest` (relay.py:68 and 80), which is constant time for equal lengths.
- Neither has a default: `os.environ[...]` fails if unset, empty values are refused, and the two must differ (relay.py:34-37).
- The dashboard user name is fixed as "greg" (relay.py:38).
- No route takes a credential in the query string, so uvicorn access logs (render.yaml:7) carry none.
- Error bodies are fixed (401 and 403 with no detail).
- render.yaml holds names only (`sync: false`).

Separate from item 32: there is no limit on repeated password attempts, and /health and /static need no login.

## Committed material (question 7)
- Tracked tree: no private-key block, no `sk-`, `ghp_`, `github_pat_` or `AKIA` string, and no `Bearer`, `password` or `token` set to a literal.
- History (72 commits, all refs): every long added string is one of these:
  - a separator line;
  - an identifier, a path or a commit hash;
  - the published GitHub SSH host public key (action.yml:47, commit 9ed49ef).
- No path was ever deleted from history.
- No `.env`, `.pem` or key file is tracked or was ever added.
- Tests create random values (test_viewer.py:24, `secrets.token_urlsafe()`) or use the placeholder "verification" (test_ledger.py:123, :130).

## What already keeps secrets out of files, prints and commits
- Every secret enters a step through `env:` or an action input. None is written as `${{ secrets.X }}` inside a script, and there is no `set -x`, `echo` of a secret or `::add-mask` needed.
- No checkout persists a token in .git/config. The markets-data push URL is plain SSH (action.yml:51).
- The deploy key goes only to ssh-agent, whose own environment is stripped of it (action.yml:43). Host-key checking is strict against a pinned host key.
- HTTPS publication puts its token in environment-only git config, never in the URL or on disk (run.py:65-71).
- Git and HTTP failures publish only fixed messages or exception type names: run.py:83, 104, 124, 150, 316; journal_publication.py:77; agent_launcher.py:107, 125, 226; restore_view.py:62. The git calls in run.py send stderr to /dev/null (run.py:78).
- Where a subprocess error message can appear (CalledProcessError, TimeoutExpired), the command line holds only `remote`/`push` arguments and the plain push URL.
- start.json, the receipt, the journal and the agent record.json hold no environment value, URL or header (session.py:124-147, 377-386; agent_launcher.py:180-186).
- Relay requests do not follow redirects, so the bearer header cannot be forwarded to another host.

## Outside item 32
verify_paper_platform.yml:70 has an empty `path:`. Whether `git init ""` and the later `git remote add origin` in the workspace fail, which would stop the verify-writer job before the deploy key loads, depends on git behaviour I did not run.

Files: /home/user/paper-trading-platform/.github/actions/markets-data/action.yml, /home/user/paper-trading-platform/.github/workflows/{run_end_notice,live_ng_paper,record_ng_mbo,purchased_mbo_paper,agent_run,verify_paper_platform}.yml, /home/user/paper-trading-platform/paper_platform/{run.py,run_live.py,capture_backup.py,restore_view.py,relay.py,session.py,agent_launcher.py,record_mbo.py}.
