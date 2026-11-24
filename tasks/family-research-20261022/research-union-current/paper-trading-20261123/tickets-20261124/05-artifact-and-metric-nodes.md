# 05: Artifact and metric nodes

**What to build:** The graph knows where things are now: every built thing has a node with its authoring run and its version, and the session text shows the current versions.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Plans, control files, decider programs and rule files are Artifact nodes with their authoring run, commit and hash; each repository's working branch and head is one too
- [ ] Measured figures (tokens, wall clock) are Metric nodes tied to their agent run
- [ ] The session text has a section of current artifact versions, each with its date
- [ ] A fresh agent answers from the graph's text which repository and branch the platform work is on
- [ ] Missing pieces covered: D25, D26
