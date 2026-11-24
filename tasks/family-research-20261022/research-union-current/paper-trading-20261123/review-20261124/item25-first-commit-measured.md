# Item 25: the run branch's first commit, measured (2026-11-24)

The reviewer of items 24 and 25 (run 55, finding 1) read that the first commit of a run's markets-data branch is
built on the data checkout's pinned commit, in a checkout fetched one commit deep with no file contents, and marked
it as depending on git. This is what git did. Only git was run, on a throwaway copy in the session's scratch
folder. No platform code ran. Nothing was pushed. git version 2.43.0.

## The copy

Made with the same commands as `.github/actions/markets-data/action.yml`:

```
git init; git remote add origin https://github.com/DavisAI1974/markets-data.git
git config remote.origin.promisor true; git config remote.origin.partialclonefilter blob:none
git sparse-checkout init --cone; git sparse-checkout set paper-trading/agent-runs
git fetch --depth=1 --filter=blob:none origin 46199c5f4af03fde341535a7aff6a0396300cc73
git checkout --detach FETCH_HEAD
```

The sparse folder was one that holds nothing at that commit, so the copy began with no file contents at all. The
live workflow's sparse folder is the purchased tape, `data/nymex_mbo/ng_v0_oct2023`, so a real runner already holds
those files and has less to fetch than this copy did.

| What | Figure |
| --- | --- |
| Objects in the copy after the fetch | 53 (the commit and its folders; no file) |
| Size of `.git` after the fetch | 276 KB |
| Files in the tree at `46199c5` | 508 |
| Branches of markets-data whose tip is `46199c5` | 0 (it is inside two branches, the tip of none) |

## The publisher's first commit, step by step

`journal_publication.py` did: `read-tree <the checkout's commit>`, add the run's files to that index, `write-tree`,
`commit-tree -p <the checkout's commit>`, push.

| Step | What happened |
| --- | --- |
| `read-tree HEAD`, one small file added, then `write-tree` | 13.2 seconds. Objects 53 to 557: git fetched 504 files it did not hold. `.git` 276 KB to 405 MB. The publisher allows each git step 25 seconds. |
| The pack a first push would send, parent `46199c5` (`git pack-objects --revs --thin --stdout --shallow`, the new commit given, no remote tip held locally to leave out) | 423,340,066 bytes |
| The same for a branch with no parent that holds only the run folder (`read-tree --empty`, the file, `write-tree`, `commit-tree` with no `-p`) | 347 bytes, nothing fetched |

The pack size is what `pack-objects` wrote locally; no push was made, so what GitHub would do with a 423 MB push
inside 25 seconds was not seen. The publisher tries a push three times.

## What was changed

Platform branch, item 25: the run branch now starts with no parent and holds only the run's own folder. In draft;
the platform code was not run.
