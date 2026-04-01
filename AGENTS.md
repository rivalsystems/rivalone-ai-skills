# Rival One (Codex / generic agents)

This repository ships **agent skills and implementation guides** for the Rival One WebSocket API so you can implement a client in whatever language you choose.

## Skill (Codex)

Codex discovers repo skills under [`.agents/skills/<name>/`](https://developers.openai.com/codex/concepts/customization/). This repo provides **`rival-one`** at [`.agents/skills/rival-one/SKILL.md`](.agents/skills/rival-one/SKILL.md).

## Canonical content

- [`skills/rival-one-core.md`](skills/rival-one-core.md)
- [`skills/catalog/`](skills/catalog/)
- [`skills/references/protocol.md`](skills/references/protocol.md)
- [`skills/references/message-types.json`](skills/references/message-types.json) (`ResponseType` / partial `RequestType`)

## Vendor API

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)

## Docs

- [`docs/example-ai-prompt.md`](docs/example-ai-prompt.md) — starter JSON + example AI prompt
- [`docs/troubleshooting.md`](docs/troubleshooting.md)
- [`docs/agent-compatibility.md`](docs/agent-compatibility.md)
- [`SECURITY.md`](SECURITY.md)

## Add skill to another repo

Copy [`.agents/skills/rival-one/`](.agents/skills/rival-one/) and [`skills/`](skills/) (or use a submodule). Details: [README](README.md#add-this-skill-to-your-ai).
