# Builder run 195 (Sonnet): the depth fetch that made the data checkout shallow

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Builder run 195 (Sonnet): the depth fetch that made the data checkout shallow

Tickets 44 and 43. Branch wt-b195 at /home/user/wt/b195. Pushed to ccr-144315dd-pta2ze. The first push was refused, so I merged FETCH_HEAD (merge commit 0abcb7d) and pushed again. The remote warned "approaching its size quota".

## Point 1: both fetches take the branch whole
- Commit 564d8c9. Files: /home/user/wt/b195/tools/kgraph/ingest_platform.py and /home/user/wt/b195/tools/kgraph/live.py.
- ingest_platform.py line 91: `"fetch", "--depth", "1", "origin"` is now `"fetch", "--no-tags", "origin"`. The docstring on line 86 now says "fetched whole (no depth limit, no tags)".
- live.py line 201: `"fetch", "--depth", "1000000", "origin"` is now `"fetch", "--no-tags", "origin"`.
- Nothing else in either file changed.

## Point 2: the check
- Commit 9b301c1. File: /home/user/wt/b195/tests/agent_program/test_stage7d_platform.py. This is the shorter of the two files that name ingest_platform (143 lines against 295 in test_live_platform.py).
- The check is `test_fetching_a_real_run_branch_leaves_the_checkout_not_shallow`. Its module-scoped fixture is `scratch_checkout`. I also added `import subprocess` and the helper `_g`.
- The fixture clones the real checkout with `git clone --no-hardlinks --single-branch --branch ccr-144315dd-pta2ze file:///home/user/markets-data <scratch>` under the basetemp folder. It then calls `ipf.ensure_run(copy, "036ed57524584afdaeb0bc60be6aaa71")`.
- The check asserts that the copy is not shallow before the call. It asserts that the run ref is absent before the call and present after. It asserts `rev-parse --is-shallow-repository` prints false and `.git/shallow` does not exist.
- **Deviation from your brief.** The scratch `origin` is not file:///home/user/markets-data itself.
  - The real checkout holds the run branches only as `refs/remotes/paper-runs/<run>` and `refs/remotes/origin/paper-runs/<run>`.
  - It holds no `refs/heads/paper-runs/<run>`, which is the ref the function fetches. A fetch straight from the real checkout therefore fails.
  - The fixture makes a bare repository in the scratch folder. It fetches `refs/remotes/paper-runs/<run>` from the real checkout into it, as `refs/heads/paper-runs/<run>`, whole and with no tags. It points the copy's `origin` at that bare repository.
  - Nothing is written into the real checkout.
- With `--depth 1` as it was, the check failed: `assert 'true' == 'false'` on the is-shallow line. This was run before the code change, with `-k not_shallow`. 1 failed, 5 deselected, 93 s.
- With the fix, the whole file passed.
- The scratch clone took well under 300 s. The file takes about 130 s in total.

## Counts of the check file
`MARKETS_DATA=/home/user/markets-data python3 -m pytest tests/agent_program/test_stage7d_platform.py -q -rs -p no:cacheprovider --basetemp=/home/user/tmp-pytest/run195b`: 6 passed, 0 skipped, 0 failed, in 129.52 s. There are no skips, so no skip reasons. The scratch folder was deleted afterwards.

## Point 3: other git writers under tools/ and tests/
Command: `grep -rn '"fetch"\|"gc"\|"prune"\|update-ref\|"checkout"\|"reset"' tools tests --include=*.py`. I changed none of these.

- tools/exp_dag.py:283 and :314. "fetch" is an argparse verb of the experiment record, not a git command. It writes nothing through git.
- tools/kgraph/ingest_platform.py:91 (`ensure_run`). It runs `git fetch --no-tags origin +refs/heads/paper-runs/<run>:refs/remotes/paper-runs/<run>` in `data`, the checkout passed in. This is the point-1 line. It writes the ref and the objects of the branch into that checkout.
- tools/kgraph/live.py:201 (`watch`, when `fetch=True`). It runs the same kind of fetch into `store.data_root`, with the target ref being `ref` or `candidate_refs(run)[0]`. This is the point-1 line. It writes the ref and objects.
- tools/ratchet/loop.py, all on `wt`/`worktree`, the ratchet's own worktree:
  - Line 91: `reset -q --hard HEAD` (rewrites the worktree and index).
  - Lines 317 and 404: `update-ref ref(n) commit` (writes the ratchet ref).
  - Lines 318, 324 and 330: `reset -q --hard anchor` or `HEAD` (moves the worktree branch and rewrites files).
  - Line 334: `update-ref ref(0) head` (writes a ref).
  - Line 421: `reset -q --hard HEAD`.
  - Whether `wt` can ever be the real data checkout depends on the caller; I did not trace that. The docstring says the proposer works on a worktree on the branch `ratchet/<loop>`.
- tests/agent_program/test_run_plan.py:382, 386, 463, 466: `checkout -q -b side` and `checkout -q -`. These run in `d` from `_repo(tmp_path)`, a new repository made under tmp_path. They switch the HEAD and files of that scratch repository. They copy files from the real checkout and write nothing into it.
- tests/agent_program/test_stage3_proposer.py:249: `checkout -q base` in `clone`. `clone` is a copy of the platform repository (the `PLATFORM` constant in test_stage3_ratchet.py's `clone` fixture) made under tmp_path. It writes HEAD and files of that copy.
- tests/agent_program/test_stage3_ratchet.py:55: `checkout -q BASE` in `dest`, a clone of `PLATFORM` under tmp_path. It writes HEAD and files of that copy.
- No "gc" or "prune" match anywhere.
- The grep only sees the quoted-argument forms you gave. I did not search for fetches written in other ways, for example inside `sh(..., "git", "fetch")` strings.

## Final state
`git -C /home/user/markets-data rev-parse --is-shallow-repository` prints `false` (run after the push).

## Open and not done
- Nothing is open for points 1 to 3.
- The merge of FETCH_HEAD brought in 4 files, including tools/kgraph/consolidate.py. I did not run their checks.

## Tool calls by name (hand-back apart)
Read 1, Bash 8 (plus 1 background-wait Bash), Edit 0, Write 0. The `advisor` tool was not called.
