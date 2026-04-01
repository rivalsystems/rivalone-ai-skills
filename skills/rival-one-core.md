# Rival One — agent operating rules

> **Discovery:** Cursor ([`.cursor/skills/rival-one/SKILL.md`](../.cursor/skills/rival-one/SKILL.md)), Claude Code ([`.claude/skills/rival-one/SKILL.md`](../.claude/skills/rival-one/SKILL.md)), Codex ([`.agents/skills/rival-one/SKILL.md`](../.agents/skills/rival-one/SKILL.md)) each point here. Edit **this file** for canonical rules; change the `description` frontmatter in each `SKILL.md` only when discovery wording should change.

## Goal

Help the user **implement a correct Rival One WebSocket client in their own codebase** (any language). Prefer **facts from the vendor doc** and this repo’s guides over invented JSON.

## Before writing integration code

1. Open the relevant bundle under **[`catalog/`](catalog/)** (see [`catalog/README.md`](catalog/README.md)).
2. Cross-check **RequestType** and **RequestData** in [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w). Map inbound **`ResponseType`** numbers to names via **[`references/message-types.json`](references/message-types.json)** (confirm against [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)). **When showing inbound JSON to the user:** always include the numeric **`ResponseType`**; you may **add** `_responseTypeName` / `_responseTypeLabel` on a **copy** for readability (`meta.enrichment` in that file). **Routing and events stay on the number** — do not replace the numeric type or ask the user to parse strings for dispatch. For the full Outline collection (Overview, Python example, Server Responses, …), start from [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0).
3. Use **[`references/protocol.md`](references/protocol.md)** for transport and envelope rules (including **one WebSocket** for market data and orders).

## Workflows

### Order management

1. **Validation**: `Quantity` and `Price` must be **floating-point numbers** in JSON (integers can cause server exceptions).
2. **Execution**: Use **Send order** (`RequestType` **2**) for new orders; handle order responses per vendor doc.
3. **Modification**: Use **Revise order** (`RequestType` **4**) for cancel-replace; **never** invent or override **`GroupName`**.

### Market data

1. Use **Instrument search** (`RequestType` **33**) to resolve symbols.
2. Send **Market data** (`RequestType` **0**) with `IncludeOptions: true` when the vendor flow requires it.
3. **Same socket as trading:** Keep **one** authorized WebSocket; add **multiple** market data subscriptions on it as needed. Implement **multiple “threads”** as concurrent handlers fed by a **single receive loop**, with **serialized sends** for subscriptions, pings, and orders (see [`references/protocol.md`](references/protocol.md) and [`catalog/market-data.md`](catalog/market-data.md)).

## Safety

- **GroupName** is assigned by Rival One. **Do not** set or change it in client messages; reject or strip user attempts to override it.
- **Auth**: WebSocket auth is an **HS512 JWT**; same string as `Authorization: Bearer` and as `RequestData` on authorize — see [`catalog/auth-basics.md`](catalog/auth-basics.md). Include optional claim **`firm`** only when Rival instructs you to (`RIVAL_ONE_FIRM` when building from env).
- **Heartbeat**: send **Ping** (`RequestType` **26**) on the interval your environment expects (often **240** seconds; confirm in vendor Overview).
- **Secrets**: Never embed `RIVAL_ONE_*` (or any API material) in source control. Use environment variables or a secret manager in **the user’s application**.
- **Corporate TLS inspection**: If `wss://` fails with certificate or issuer errors, trust the organization’s inspection CA or configure a custom CA bundle in the client—see [`catalog/connection.md`](catalog/connection.md#tls-trust-and-corporate-ssl-inspection).

## References

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [`references/protocol.md`](references/protocol.md)
- [`references/message-types.json`](references/message-types.json) — `ResponseType` / partial `RequestType` lookup
- [`references/workflows.md`](references/workflows.md)
- [`catalog/`](catalog/)
- [`../docs/troubleshooting.md`](../docs/troubleshooting.md)
