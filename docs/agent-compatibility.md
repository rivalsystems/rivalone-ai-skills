# Agent compatibility (Cursor, Claude, Codex)

## Shared source of truth

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- Login / group / user issues: [`troubleshooting.md`](troubleshooting.md)
- Canonical workflow and safety rules: [`../skills/rival-one-core.md`](../skills/rival-one-core.md)
- Protocol tables and caveats: [`../skills/references/protocol.md`](../skills/references/protocol.md)
- Implementation examples: [`../skills/catalog/`](../skills/catalog/)

## Platform-native skills (same `name`: `rival-one`)

Each product loads **Agent Skills**–style `SKILL.md` from its own folder. All three wrap the same canonical docs under `skills/`; keep discovery text and entrypoint links aligned when you edit.

| Platform | Skill path | How it loads |
|----------|------------|----------------|
| **Cursor** | [`.cursor/skills/rival-one/SKILL.md`](../.cursor/skills/rival-one/SKILL.md) | Project skills under `.cursor/skills/<name>/`; `description` drives when the agent applies it |
| **Claude Code** | [`.claude/skills/rival-one/SKILL.md`](../.claude/skills/rival-one/SKILL.md) | Project skills under `.claude/skills/<name>/`; optional `/rival-one`; `/skills` in CLI lists skills |
| **Codex** | [`.agents/skills/rival-one/SKILL.md`](../.agents/skills/rival-one/SKILL.md) | Repo skills under `.agents/skills/<name>/` (Codex customization) |

## Always-loaded project docs

| Platform | File | Role |
|----------|------|------|
| Claude (incl. Claude Code) | [`../CLAUDE.md`](../CLAUDE.md) | Loaded every session; points at `.claude/skills/` and `skills/` |
| Codex / generic agents | [`../AGENTS.md`](../AGENTS.md) | Loaded from repo root; points at `.agents/skills/` and `skills/` |

Security and secrets for **your application**: [`../SECURITY.md`](../SECURITY.md).

End-user install steps: [`../README.md`](../README.md#add-this-skill-to-your-ai).

## Keeping parity

When you change protocol behavior or examples, update:

1. [`skills/references/protocol.md`](../skills/references/protocol.md) (if the rule is protocol-wide)
2. The relevant file under [`skills/catalog/`](../skills/catalog/)
3. If you change skill **discovery** (`description`) or **entrypoint links**, update all three: `.cursor/skills/rival-one/SKILL.md`, `.claude/skills/rival-one/SKILL.md`, `.agents/skills/rival-one/SKILL.md`

Do not duplicate long tables inside every wrapper; link to `skills/catalog/` and `references/` instead.
