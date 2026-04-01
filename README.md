# Rival One — AI skills for client development

---

## Start here

### [Example AI prompt and credential template → `docs/example-ai-prompt.md`](docs/example-ai-prompt.md)

**Use this first.** One page with a **ready-to-paste chat message** and **placeholder JSON** (`logincredentials`, `secret`, `server_url`) so your assistant can scaffold a working WebSocket client in a single conversation. Add the [rival-one skill](#add-this-skill-to-your-ai) to your project so it follows [`skills/catalog/`](skills/catalog/).

---

This repository helps you and your coding assistant **write a correct Rival One WebSocket client** in **any language**. It ships **agent skills** (Cursor, Claude Code, OpenAI Codex) and an **implementation catalog** you use inside your own project: JWT auth, connection/heartbeat, market data, orders, and troubleshooting.

| Documentation | Link |
|----------------|------|
| **Rival WebSocket API** (Outline — Overview, Client Requests, …) | [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0) |
| **Client Requests** (message-level API reference, Outline) | [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) |

**License:** [Apache License 2.0](LICENSE); [NOTICE](NOTICE).

## Contents

- [Start here](#start-here)
- [Add this skill to your AI](#add-this-skill-to-your-ai)
- [What is in the repo](#what-is-in-the-repo)
- [Environment variables (your app)](#environment-variables-your-app)
- [Project layout](#project-layout)
- [Validate the catalog](#validate-the-catalog)
- [Protocol and safety](#protocol-and-safety)
- [Further reading](#further-reading)

## Add this skill to your AI

### Cursor

**Option A — Use this repo as your workspace (simplest)**  
Clone or open this repository in Cursor. Project skills under [`.cursor/skills/rival-one/`](.cursor/skills/rival-one/) load automatically with the matching `description` for discovery.

**Option B — Install as a user (global) skill**  
Copy the folder `rival-one` from [`.cursor/skills/`](.cursor/skills/rival-one/) into your **user skills** directory so it is available in every project. Cursor resolves user skills from a fixed path on your machine; see the current Cursor documentation for **Agent Skills** and the exact directory for your OS (Linux, macOS, or Windows). You must also make [`skills/`](skills/) available—either copy `skills/` next to your project’s skill layout or open a workspace that includes both your app and this repo.

**Option C — Use in another app repo only**  
Copy into your application repository:

- `.cursor/skills/rival-one/` (entire folder)
- `skills/` (entire folder, so links in `SKILL.md` and `rival-one-core.md` resolve)

Or add this repo as a **git submodule** at a path like `vendor/rival-one-skill` and symlink `skills` and `.cursor/skills/rival-one` into your tree.

### Claude Code

Copy [`.claude/skills/rival-one/`](.claude/skills/rival-one/) and [`skills/`](skills/) into your project (or symlink/submodule). In the CLI, run `/skills` to confirm **`rival-one`** appears; invoke with `/rival-one` when you want it explicitly.

### OpenAI Codex

Copy [`.agents/skills/rival-one/`](.agents/skills/rival-one/) and [`skills/`](skills/) per [Codex customization](https://developers.openai.com/codex/concepts/customization/) (repo skills under `.agents/skills/<name>/`).

### Other tools

Copy **`skills/`** and point your agent at [`skills/rival-one-core.md`](skills/rival-one-core.md). If the product supports a skill manifest, adapt the frontmatter from one of the existing `SKILL.md` files.

### Sparse checkout (only skill files from this repo)

If you want to vendor files without cloning everything:

```bash
git clone --filter=blob:none --sparse https://github.com/YOUR_ORG/rivalone-mcp-skill.git rival-one-skill
cd rival-one-skill
git sparse-checkout set skills .cursor/skills/rival-one .claude/skills/rival-one .agents/skills/rival-one
```

Adjust the remote URL to your fork or upstream. Then copy or symlink those paths into your app.

## What is in the repo

| Area | Purpose |
|------|---------|
| [`skills/rival-one-core.md`](skills/rival-one-core.md) | Agent operating rules (safety, workflows) |
| [`skills/catalog/`](skills/catalog/) | Implementation bundles (Python / TypeScript / C# examples + prose) |
| [`skills/references/protocol.md`](skills/references/protocol.md) | Protocol summary (confirm against vendor) |
| [`skills/references/workflows.md`](skills/references/workflows.md) | Connect / trade / market-data checklist |
| [`.cursor/skills/rival-one/`](.cursor/skills/rival-one/) | Cursor skill entry |
| [`.claude/skills/rival-one/`](.claude/skills/rival-one/) | Claude Code skill entry |
| [`.agents/skills/rival-one/`](.agents/skills/rival-one/) | Codex skill entry |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | Common errors |
| [`docs/agent-compatibility.md`](docs/agent-compatibility.md) | How agents load these files |

Start with [`skills/catalog/README.md`](skills/catalog/README.md) for a topic index.

## Environment variables (your app)

When **your** program builds or loads a JWT, you will typically use environment variables or a secret store. Copy [`.env.example`](.env.example) as a template for **local development** only; never commit real values.

Authentication is **HS512 JWT** per [Client Requests — Authorize](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w): the same JWT is the WebSocket **Bearer** token and the **`RequestData`** string on authorize (`RequestType` **45**).

> **All `RIVAL_ONE_*` values are secrets**, including `RIVAL_ONE_GROUP` and `RIVAL_ONE_USER` (JWT claims tied to registration). See [`SECURITY.md`](SECURITY.md).

| Variable | Required | Purpose |
|----------|----------|---------|
| `RIVAL_ONE_API_TOKEN` | One of two modes† | Pre-built JWT (three segments) |
| `RIVAL_ONE_API_KEY` | † | `apikey` claim when building JWT locally |
| `RIVAL_ONE_SECRET_KEY` | † | HMAC secret for HS512 |
| `RIVAL_ONE_GROUP` | † | `group` claim |
| `RIVAL_ONE_USER` or `RIVAL_ONE_USERNAME` | † | `user` claim |
| `RIVAL_ONE_JWT_SUB` | No | JWT `sub` (default in examples: `Rival API user Authentication`) |
| `RIVAL_ONE_FIRM` | No | Optional JWT claim **`firm`** on login credentials when Rival asks you to send firm scoping |
| `RIVAL_ONE_DEFAULT_ACCOUNT` | No | Default `Account` on send-order payloads if your flow needs it |
| `RIVAL_ONE_WSS_URL` | No | WebSocket URL (SIM default in `.env.example`) |
| `RIVAL_ONE_PING_INTERVAL_SECONDS` | No | Ping interval (often `240`) |

† Either set `RIVAL_ONE_API_TOKEN` **or** the four builder fields above.

If login fails with `API user not registered with the system | Grp=[...], User=[...]`, see [Overview — Common Errors](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) and [`docs/troubleshooting.md`](docs/troubleshooting.md).

## Project layout

```
.
├── README.md
├── LICENSE
├── NOTICE
├── SECURITY.md
├── .env.example
├── skills/
│   ├── rival-one-core.md
│   ├── catalog/           # implementation guides + catalog.json
│   └── references/        # protocol + workflows
├── .cursor/skills/rival-one/
├── .claude/skills/rival-one/
├── .agents/skills/rival-one/
├── docs/
├── scripts/
│   └── validate_catalog.py
└── .github/workflows/     # optional CI
```

## Validate the catalog

After editing `skills/catalog/`, run:

```bash
python3 scripts/validate_catalog.py
```

Ensures `catalog.json` lists only bundles whose markdown files exist and required bundle ids are present.

## Protocol and safety

- Vendor WebSocket docs: [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0) (Outline). Message envelopes and JWT auth: [`skills/references/protocol.md`](skills/references/protocol.md) and **Client Requests**.
- Never commit API tokens. Use environment variables or your platform’s secret manager in **your** application.
- See [`docs/assumptions-and-consensus.md`](docs/assumptions-and-consensus.md) for scope and caveats.

## Further reading

- [`CLAUDE.md`](CLAUDE.md) — Claude Code entry
- [`AGENTS.md`](AGENTS.md) — Codex / generic agents entry
- [`docs/consensus-note.md`](docs/consensus-note.md)
