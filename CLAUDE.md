# Rival One (Claude / Claude Code)

This repository is a **skills pack** for building a Rival One WebSocket client: agent instructions, implementation guides, and protocol references.

## Skill

Claude Code loads **`rival-one`** from [`.claude/skills/rival-one/SKILL.md`](.claude/skills/rival-one/SKILL.md). Use `/rival-one` or rely on automatic loading. Run `/skills` to confirm it appears.

## Canonical content

- Rules: [`skills/rival-one-core.md`](skills/rival-one-core.md)
- Implementation bundles: [`skills/catalog/`](skills/catalog/)
- Protocol: [`skills/references/protocol.md`](skills/references/protocol.md)
- Message type lookup: [`skills/references/message-types.json`](skills/references/message-types.json) (`ResponseType` / partial `RequestType`)

## Vendor documentation

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) (Outline) for message shapes

## Other docs

- [`docs/example-ai-prompt.md`](docs/example-ai-prompt.md) — JSON credential template + copy-paste prompt to scaffold an app
- [`docs/troubleshooting.md`](docs/troubleshooting.md)
- [`docs/agent-compatibility.md`](docs/agent-compatibility.md)
- Secrets in **your app**: [`SECURITY.md`](SECURITY.md), [`.env.example`](.env.example)

## How to add this skill to another project

Copy the folder [`.claude/skills/rival-one/`](.claude/skills/rival-one/) into your app repository (or symlink it), and copy or symlink [`skills/`](skills/) so the relative links in `SKILL.md` resolve. See [README — Add this skill to your AI](README.md#add-this-skill-to-your-ai).
