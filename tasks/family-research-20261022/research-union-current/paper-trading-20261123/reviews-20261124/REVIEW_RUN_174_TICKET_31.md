# Reviewer run 174 (Opus): ticket 31, the first read of the manifest check

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 174 (Opus): ticket 31, the first read of the manifest check

Working copy: /home/user/wt/r174 at Markets 5a9579d. The change is exactly two new files: /home/user/wt/r174/tools/kgraph/manifest_check.py (143 lines) and /home/user/wt/r174/tests/agent_program/test_manifest_check.py (211 lines). Both were read whole. markets-data B was fixed at db095e0 for every real-history read.

## 1. The checks
`MARKETS_DATA=/home/user/markets-data python3 -m pytest tests/agent_program/test_manifest_check.py -q -rs -p no:cacheprovider --basetemp=/home/user/tmp-pytest/r174`
- Result: 10 run, 0 skipped, 0 failing (2.46 s).
- I deleted /home/user/tmp-pytest/r174 after every run. Three other folders are in /home/user/tmp-pytest (main, r168s, r170). They are not mine and I did not touch them.

## 2. Put-backs
Each one changes a single line of manifest_check.py. I ran the checks after each and restored with `git checkout -- .`. `git status --porcelain` showed 0 changed paths after every restore and is empty at the end.

| # | line | change | checks |
|---|---|---|---|
| M1 file gone at B | 122 | `if blob is None:` -> `if False:` | 1 failed |
| M2 unknown shape skipped silently | 66 | `not_read.append(p)` -> `pass` | 2 failed |
| M3 bytes compared where not carried | 83 | `if "bytes" in entry:` -> `if True:` | 1 failed |
| M3b | 84 | `entry["bytes"]` -> `entry.get("bytes")` | 0 failed. This change cannot alter output while line 83 guards it, so no check could notice it. |
| M4 sha256 compared where not carried | 87 | `if "sha256" in entry:` -> `if True:` | 1 failed |
| M5 manifest text read from the working folder | 60 | `_blob(data, b, p)` -> `(data / p).read_bytes()` | 1 failed |
| M6 manifest list taken at HEAD, not B | 55 | `ls-tree ... b` -> `ls-tree ... "HEAD"` | **0 failed** |
| M7 exit 2, bad checkout | 104 | `return 2` -> `return 0` | 1 failed |
| M8 exit 2, bad range | 116 | `return 2` -> `return 0` | 1 failed |
| M9 file blob read at HEAD, not B | 121 | `_blob(data, b, p)` -> `_blob(data, "HEAD", p)` | 1 failed |
| M10 rename detection on | 73 | `--no-renames` removed | **0 failed** |
| M11 manifest name matched by case | 57 | `.lower()` removed | 6 failed |

Why M6 goes unnoticed: no check uses a range whose B has a different set of manifest paths from the checkout's HEAD. test_42614ca (test file lines 68-91) does not assert `manifests_read` or `manifests_shape_not_read`. test_d70527a (lines 49-65) asserts 13 and 1, but markets-data has the same 14 manifest paths at d70527a and at HEAD.

Why M10 goes unnoticed: no check holds a rename.

## 3. The command on the real history (read-only)
**557a3b0..db095e0 (11 commits, this session), exit 0:**
- COUNTS: added=57, with_entry=0, no_entry=57, gone_at_B=0, manifests_read=13, manifests_shape_not_read=1.
- The manifest named as not read is paper-rules/20261109/machine/PAPER_UNIVERSE_MANIFEST.json. Its top keys are schema, all_paper_included and so on; it has no list of entries.
- All 57 files are under tasks/family-research-20261022/research-union-current/paper-trading-20261123/: transcripts 26, run-plans 22, scout-20261124 4, audits-20261124 3, reviews-20261124 1, builder-20261124 1.
- Second route: I searched the text of all 14 manifests at db095e0 for each file's basename and found 0 hits. So the relative-path gap in section 4 does not change the answer for this range: none of the 57 has a manifest entry, and all 57 are named.

**Earlier range 2405fe0..2fcfbb1 (desktop-peak-lives, the range that adds files a manifest holds):** added=13, with_entry=12, no_entry=1 (the MANIFEST.json itself), manifests_read=6.

**Earlier range 2fab819..a8a6738 (carry-forward):** added=26, with_entry=0, no_entry=26. Section 4 shows this is wrong for files the manifest does list.

**Five lines checked by another route:**
1. run-plans/run-0174.json. Command: exists, 942 bytes, no entry. `git ls-tree -l db095e0`: blob 3e3b3aec, 942 bytes. Added in 6ae8503. Basename found in no manifest.
2. transcripts/run-0173.json. Command: 311 bytes, no entry. ls-tree: 311 bytes. Added in 9264ddc. Found in no manifest.
3. desktop-peak-lives-on-clock-20261117/load.py. Command: 505 bytes, bytes equal, sha256 equal. ls-tree: 505 bytes. `git show | sha256sum` gives 6a7a281a...b01114. The manifest entry at db095e0 has bytes 505 and the same sha256.
4. .../peak-lives-20231002.parquet. Command: 2336143 bytes, manifest entry. ls-tree: 2336143 bytes. sha256 7e3103c0...efb7, the same as the entry.
5. carry-forward/20261109/FINDINGS_REGISTER.json. Command: 19808 bytes, "no manifest holds an entry for it". But carry-forward/20261109/FILE_MANIFEST.json at db095e0 holds `{'path': 'FINDINGS_REGISTER.json', 'bytes': 19808, 'sha256': '9e641327...383c', 'git_blob_sha': 'a6401877...'}`, and both values equal the blob at B (ls-tree 19808, sha256sum 9e641327...383c). This output line does not match the manifest.

## 4. Paths that can flip "has an entry" and "has none"
- **Entry paths relative to the manifest's own folder (real, in the current history).** manifest_check.py:127 compares `e.get(k) == p` against the repo-root path only. Three manifests at db095e0 store every path relative to their own folder, so each of these entries prints as "no manifest holds an entry":
  - carry-forward/20261109/FILE_MANIFEST.json: 25 of 25 entries
  - paper-rules/20261109/FILE_MANIFEST.json: 124 of 124
  - tasks/.../field-rebuild-20261113/STATIC_CONTENT_MANIFEST.json: 72 of 72

  The concrete case is item 5 above. The plan the builder was handed does not say how relative paths resolve, so this gap is in the plan as well as the code.
- **Leading "./".** Line 127 is an exact string compare. Scratch probe (built from the real 42614ca manifest and trials.jsonl, then deleted): with the entry path written `./experiments/trials2.jsonl`, the file printed "no manifest holds an entry". At db095e0 no manifest path starts with "./" (survey: dot=0 in every manifest).
- **Entry naming a folder.** Line 127, exact compare. Probe: with the entry `experiments/`, the file under it printed "no entry". At db095e0 the root MANIFEST.json holds three such entries: tasks/family-research-20261022/replay-artifacts/{20231002,20231003,20231017}/root-frames/. Each folder has 0 files at db095e0, so there is no case of this in the current history.
- **Same path in two manifests.** Lines 125-128 loop over every manifest. Probe: both manifests were listed on the one line, and with_entry counted the file once (line 131).
- **Upper-case manifest name.** Line 57 lower-cases the basename before the "manifest" and ".json" tests. Probe: `other/Data_Manifest.JSON` was read. The ".json" test is also case-insensitive (".JSON" accepted); the plan says ends ".json".
- **Renamed file.** Line 73 uses `--diff-filter=A --no-renames`. With rename detection off, git reports a rename as a delete plus an add, so the filter keeps the new path as "added". Probe: a `git mv` in the range listed experiments/trials2.jsonl as added. If a file is added and then renamed inside the same range, the old path is also listed and prints "gone at B" (I reasoned this from lines 121-123; I did not probe it). With rename detection on (M10), the new path of a file renamed in the range would not be listed. No check covers this.
- **Manifests counted as read whose entries can never match.** Line 127 skips non-dict entries and entries that have neither "path" nor "markets_data_path", and says nothing. These manifests are counted in `manifests_read` and are not named:
  - data/nymex_mbo/ng_v0_oct2023/MANIFEST.json: 7 of 7 entries keyed "file"
  - data/outside/ng_oct2023/MANIFEST.json: 142 of 142 keyed "address"
  - tasks/.../claude-independent-research-20261113/SOURCE_MANIFEST.json: 239 of 239 keyed package_path / published_path / repository_path
  - paper-rules/20261109/recovery/model_source_audit/SOURCE_MANIFEST.json: 10 of 15 without a path key

  The plan names only a manifest of another shape; it says nothing about entries of another shape.
- **Paths outside the repo.** consolidation/20261109/MANIFEST.json has 2437 entries; entry 0 is `path: acquire.py` with `asset: research-union-001.zip`. These paths are inside archive assets, none exists at B, and none will match.
- The root MANIFEST.json has 58 entries, of which 18 carry a `markets_data_path` that differs from `path`. Line 127 matches either key, as the plan says.

## 5. Standing rules
- **Dropped without being named:**
  - line 127 (entries without a path key or not a dict, as above)
  - line 39 (any `git show` failure becomes None, which lines 122-123 then count as "gone at B", so a read error looks the same as a deleted file)
  - line 76 (`strip("\n")` changes any path that begins or ends with a newline; none seen)
- **Verdict words:** the output uses "equal" and "not equal" and none was seen. test_output_gives_no_verdict_words (test lines 107-112) looks only for "pass" and "fail", on one range.
- **Made-up data in checks:** the scratch section (test lines 115-211) uses real 42614ca texts. The only scaffolding is a `README.md` containing "scratch". test lines 189-192 re-serialize the manifest with `json.dumps(indent=1)`, which also changes the whitespace beyond the named change. Its `# change:` comment names only the removed keys.
- **Nothing written:** the command only calls git read commands. `git -C /home/user/markets-data status --porcelain` was empty when I checked it twice, last at the end. Scratch repos were kept under the session scratchpad and deleted.
- **AWS:** no new dependency on S3, EC2, SSM, Bedrock, SageMaker, boto3 or aws-mcp.

## Speculation (labelled)
- Merges: `git log --diff-filter=A` without `-m` shows no diff for merge commits, so a file that appears only in a merge resolution would not be listed. I did not check whether markets-data has merges inside these ranges.
- M6 would matter for a B older than a manifest's first commit or older than its deletion. Such a manifest's line 60 read at B returns None and it would be named "shape was not read" rather than left out.

## Open after this read
**For the builder:**
- manifest_check.py:127: resolve entry paths against the manifest's own folder. This is the real case of carry-forward/20261109/FILE_MANIFEST.json, paper-rules/20261109/FILE_MANIFEST.json and STATIC_CONTENT_MANIFEST.json, shown by item 5 in range 2fab819..a8a6738. Also decide how "./" and folder entries are handled (this needs the plan's word, see below).
- manifest_check.py:127 with lines 65-68: name manifests whose entries carry no path key, giving counts per manifest, instead of counting them as read.
- manifest_check.py:37-39 with 122-123: separate "absent at B" from "git show failed".
- test_manifest_check.py: add checks that notice M6 (assert the manifest counts on a range whose B differs from HEAD) and M10 (a rename case). test_42614ca (lines 68-91) asserts no manifest counts.

**For the main session:**
- The ticket's answer at db095e0: all 57 files added in 557a3b0..db095e0 have no MANIFEST entry, and all 57 are named. The basename search of all 14 manifests confirms it.
- The plan's definition of an entry needs a rule for paths relative to the manifest folder, for folder entries, and for entries keyed "file", "address" or "package_path". This is Greg's or the plan-writer's call.
- Whether run-plans, transcripts and reports count as "data" under the MANIFEST.json rule is not settled by the code.

**What code cannot hold:** whether a manifest entry naming a file means the same file in intent (for example, archive-internal paths in consolidation/20261109/MANIFEST.json).

Tool calls: 7 of 16, including this handback. No sub-agents. I stopped because the task was done, not because of a limit.
