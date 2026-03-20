# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## Context Manager Check

- Run session_status to check current context usage
- If context > 60%, consider saving memory and preparing for session switch
- Check ~/proactivity/session-state.md for active tasks
- Update ~/proactivity/memory/working-buffer.md if needed

## Self-Improving Check

- Read ./skills/self-improving/heartbeat-rules.md
- Use ~/self-improving/heartbeat-state.md for last-run markers and action notes
- If no file inside ~/self-improving/ changed since the last reviewed change, return HEARTBEAT_OK

## Proactivity Check

- Read ~/proactivity/heartbeat.md
- Re-check active blockers, promised follow-ups, stale work, and missing decisions
- Ask what useful check-in or next move would help right now
- Message the user only when something changed or needs a decision
- Update ~/proactivity/session-state.md after meaningful follow-through
