# Run 52: the documented facts on hooks inside a subagent, the subagent transcript and the built-in caps

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is under the item's number in the platform checklist and in agent-runs.jsonl.

---

Answers from the official Claude Code docs (code.claude.com). Where a point is not in the fetched pages I say "not documented". The hooks reference was read in sections, so each claim notes its page.

**1. Hooks inside a subagent**
- Yes. Tool events fire inside subagents. The hooks reference says: "When a subagent calls a tool, tool events such as PreToolUse and PostToolUse fire the same configured hooks as in the main conversation, and the input carries the agent_id and agent_type common input fields that identify the subagent." (https://code.claude.com/docs/en/hooks.md, Common input fields). The subagents page confirms hooks from settings, managed policy and plugins all apply inside subagents (https://code.claude.com/docs/en/sub-agents.md).
- Common stdin fields, from the hooks reference: session_id, prompt_id, transcript_path, cwd, scratchpad_dir, permission_mode, effort (object with level), hook_event_name, agent_id, agent_type. model is only sent to SessionStart hooks. (hooks.md, Common input fields)
- Event fields: PreToolUse gets tool_name, tool_input, tool_use_id, plus mcp_server for MCP tools (hooks.md, PreToolUse). No subagent-specific field appears on PreToolUse/PostToolUse.
- Inside vs. outside: agent_id is "Unique identifier for the subagent or in-process teammate the hook fires in." agent_type is the agent name, and is "present when the session uses --agent or the hook fires inside a subagent." (hooks.md). A main-thread call's agent_id is not documented in the pages I read, so treat its absence as the "main thread" signal only after testing.
- agent_transcript_path is NOT a common field. It appears only on SubagentStop input (see 4).

**2. Transcript location and usage**
- Path pattern: `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`, with `agent-{agentId}.meta.json` alongside (https://code.claude.com/docs/en/sub-agents.md, Transcript storage). The SubagentStop example uses `.../<session>/subagents/agent-def456.jsonl` (hooks.md).
- Per-line `usage` in that JSONL: NOT documented. The Agent SDK cost-tracking page documents usage on assistant messages (message.usage, with per-step output_tokens as a placeholder; read the real output count from the result message) (https://code.claude.com/docs/en/agent-sdk/cost-tracking.md). Do not rely on the on-disk file layout without testing it.
- Live token signal that IS documented: OpenTelemetry metrics `claude_code.token.usage` (type = input, output, cacheRead, cacheCreation) and `claude_code.cost.usage`, each "Incremented after each API request," with attributes query_source (value "subagent" documented) and agent.name. Export interval default OTEL_METRIC_EXPORT_INTERVAL=60000 ms, so values lag up to about a minute (https://code.claude.com/docs/en/monitoring-usage.md). This is the only documented per-request counter I found; it is not a hook.
- The Agent tool's PostToolUse tool_response carries totalTokens and usage, but the docs say these cover "the final request only", and point to the token counters for subagent rollups (hooks.md, PostToolUse). So it is not a mid-run signal.

**3. Stopping a subagent from a PreToolUse hook**
- Exit code 2: blocks that tool call; stderr is the message given to Claude. A block stays even if JSON says allow (hooks.md, Exit code behavior).
- JSON hookSpecificOutput.permissionDecision: "allow" | "deny" | "ask" | "defer", with permissionDecisionReason (hooks.md, PreToolUse decision control). "deny" blocks that one call; the agent keeps running.
- "continue": false: "Claude stops processing entirely after the hook runs. It doesn't block a PreToolUse tool call, so to do that, also return permissionDecision: 'deny'." stopReason is shown to the user and stays in the conversation (hooks.md, JSON output).
- Scope of continue:false inside a subagent (subagent only vs whole session) and what the parent agent receives: NOT documented in the pages I read.
- Recommended for a budget stop: return permissionDecision "deny" with a reason (blocks further calls), and separately exit/stop. Whether a denied subagent then ends cleanly is not documented.

**4. SubagentStart / SubagentStop**
- Both exist (hooks.md). SubagentStart input: agent_id, agent_type; it can inject additionalContext; exit 2 only shows stderr and does not block.
- SubagentStop fires when a subagent finishes. Input: stop_hook_active, agent_id, agent_type, agent_transcript_path (the subagent's own transcript in the nested subagents/ folder), last_assistant_message, background_tasks, session_crons (hooks.md, SubagentStop input; example shows permission_mode too). It CAN block: exit 2 or decision "block" with reason prevents the subagent from stopping; hookSpecificOutput.additionalContext continues the conversation. The docs say that for SubagentStop, continue:false takes precedence over exit 2 so the subagent ends its turn.
- Hook that fires per model request: NONE documented. Closest are Stop/SubagentStop (per turn), StopFailure (API error), MessageDisplay (per streamed text batch, no usage). Use OpenTelemetry for per-request counts.
- Notification hook types: permission_prompt, idle_prompt (hooks.md, Notification). Usable for a phone alert on idle or permission prompts; no budget event exists.

**5. Built-in caps**
- Frontmatter `maxTurns` in agent definitions: "Maximum number of agentic turns before the subagent stops. When the subagent reaches the limit, Claude Code returns its output marked as partial, and Claude can resume it" (https://code.claude.com/docs/en/sub-agents.md). Applies to subagents, in any mode.
- CLI `--max-turns N`: print mode (-p) only, no limit by default (https://code.claude.com/docs/en/cli-reference.md).
- Spend cap in headless: `--max-budget-usd`. The headless page says that when the run reaches the --max-budget-usd cap, Claude Code stops the remaining background work, including background subagents (https://code.claude.com/docs/en/headless.md, Background tasks at exit). Its exact CLI flag row was not visible in my fetch, so confirm in cli-reference.md.
- Agent SDK: `max_budget_usd` (Python) / `maxBudgetUsd` (TypeScript) counts the call's own spend, including subagents, and a result with subtype error_max_budget_usd is returned (https://code.claude.com/docs/en/agent-sdk/cost-tracking.md). The SDK also has a "cap subagent depth, concurrency, and spend" section (https://code.claude.com/docs/en/agent-sdk/subagents.md), which I did not fetch.
- Env vars for subagents: CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH and CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS (sub-agents.md summary). These limit depth and concurrency, not tokens.
- Stop-hook continuation cap: CLAUDE_CODE_STOP_HOOK_BLOCK_CAP, default 8 (hooks.md, Stop).
- Token budget in frontmatter or as a task budget: NOT documented. `autoCompactWindow` is a compaction setting, not a cap.
- None of these caps is a mid-run token count. maxTurns and --max-budget-usd are enforced by the harness and cover cost and turns, not a live token figure the user can read.

**6. Hooks in .claude/settings.json**
- Shape (hooks.md, Configuration):
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/x.sh" } ] }
    ]
  }
}
```
  Optional per-handler `if` (e.g. "Bash(rm *)") and `args` (exec form, no shell). Three levels: event, matcher group, handler array.
- Timeout: per handler `timeout` in seconds. Defaults: 600 for command, http, mcp_tool; 30 for prompt; 60 for agent. Lowered to 30 for command/http/mcp_tool on UserPromptSubmit, PreModelSwitch, PostModelSwitch, and 10 on MessageDisplay. Not enforced on async:true command hooks (hooks.md, timeout section; cloud-environments.md confirms the 600 s default for SessionStart command hooks).
- Cloud sessions (https://code.claude.com/docs/en/cloud-environments.md, "What carries over from your setup"; https://code.claude.com/docs/en/settings.md, Settings in cloud sessions): in an Anthropic-hosted session with ONE repository, the repo's committed .claude/settings.json hooks and permission rules do apply. In a project thread, they do not. User-level ~/.claude/settings.json hooks do not reach cloud sessions. Server-managed settings hooks run, except in Claude Tag sessions. Self-hosted environments can also run hooks seeded from the runner host.

**7. Headless stream-json usage**
- Yes, events stream during the run. `--output-format stream-json --verbose --include-partial-messages` emits partial messages as they are generated (https://code.claude.com/docs/en/headless.md, Stream responses). Subagent messages appear as assistant and user messages with parent_tool_use_id set; text/thinking of subagents needs --forward-subagent-text (headless.md).
- Assistant messages carry usage (SDK cost-tracking), but output_tokens on them is a placeholder; the true output count arrives in the result message. The docs do not state explicitly that every streamed line carries a usage object in the CLI stream, so verify with a test run.
- The stream is output only. The docs document no inbound token-budget command for an outside process. Stopping options documented: SIGINT or the SDK interrupt() ends the turn cleanly; SIGTERM exits 143 with no result for the turn (headless.md, Stop a run with SIGTERM). Passing --max-budget-usd or --max-turns is the documented harness cap.
- Hooks do run in headless -p mode unless --bare is passed (headless.md, Start faster with bare mode).

**Practical implication for the phone-notice design**
- No documented mid-run token count is pushed to a hook. The documented options are: (a) a PreToolUse hook that reads the subagent's own transcript file (path above; per-line usage format not documented, test first) and returns permissionDecision "deny" once a budget is crossed; (b) OpenTelemetry claude_code.token.usage filtered on query_source=subagent for a live counter with about a 60 s lag; (c) maxTurns or --max-budget-usd as a hard harness stop; (d) SubagentStop, which fires after the subagent ends, for the phone notice.

Sources (all code.claude.com/docs/en/): hooks.md; sub-agents.md; headless.md; settings.md; cli-reference.md; cloud-environments.md; monitoring-usage.md; agent-sdk/cost-tracking.md; agent-sdk/subagents.md (not fetched).
