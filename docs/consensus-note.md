# Consensus note

This repository packages **agent skills** and **implementation guides** for the Rival One WebSocket API. It does not ship vendor-certified API documentation.

The layout is:

- Shared [`skills/`](../skills/) (rules, protocol summary, catalog of code patterns)
- Per-platform skill wrappers: [`.cursor/skills/`](../.cursor/skills/), [`.claude/skills/`](../.claude/skills/), [`.agents/skills/`](../.agents/skills/)

See [`assumptions-and-consensus.md`](assumptions-and-consensus.md) for technical assumptions and [`agent-compatibility.md`](agent-compatibility.md) for how agents load the content.
