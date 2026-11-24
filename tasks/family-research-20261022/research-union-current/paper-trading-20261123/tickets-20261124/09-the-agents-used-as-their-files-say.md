# 09: The agents used as their files say

**What to build:** The scout locates and reads, the builder shows its diff before writing, the reviewer reads every final diff.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] The reviewer has read everything built in Markets today and the platform change as it stands; each finding is fixed with its commit or listed as open
- [ ] From here every builder returns its diff and writes only on the main session's go
- [ ] Locating and reading goes to the scout; what it returns is written to the graph by the main session
- [ ] Missing pieces covered: B12, B13, B14, B15
