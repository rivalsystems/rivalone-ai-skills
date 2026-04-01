---
# Rival One — agent operating rules

> **Discovery:** Cursor ([`.cursor/skills/rival-one/SKILL.md`](.cursor/skills/rival-one/SKILL.md)), Claude Code ([`.claude/skills/rival-one/SKILL.md`](.claude/skills/rival-one/SKILL.md)), Codex ([`.agents/skills/rival-one/SKILL.md`](.agents/skills/rival-one/SKILL.md)) each point here. Edit **this file** for canonical rules; change the `description` frontmatter in each `SKILL.md` only when discovery wording should change.

## Goal

Help the user **implement a correct Rival One WebSocket client in their own codebase** (any language). Prefer **facts from the vendor doc** and this repo's guides over invented JSON. When in doubt about a field, check [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) before generating code.

## Before writing integration code

1. Open the relevant bundle under **[`catalog/`](skills/catalog)** (see [`catalog/README.md`](skills/catalog/README.md)).
2. Cross-check **RequestType** and **RequestData** in [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w). Map inbound **`ResponseType`** numbers to names via **[`references/message-types.json`](skills/references/message-types.json)** (derived from [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) and [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)). **When showing inbound JSON to the user:** always include the numeric **`ResponseType`**; you may **add** `_responseTypeName` / `_responseTypeLabel` on a **copy** for readability (`meta.enrichment` in that file). **Routing and events stay on the number** — do not replace the numeric type or ask the user to parse strings for dispatch.
3. Use **[`references/protocol.md`](skills/references/protocol.md)** for transport and envelope rules (including **one WebSocket** for market data and orders).
4. Use **[`references/example-payloads.json`](skills/references/example-payloads.json)** for real request/response shapes when generating or validating code.

## Workflows

### Connection sequence

1. Build HS512 JWT with claims: `sub`, `group`, `user`, `apikey` (and optionally `firm`) — see [`catalog/auth-basics.md`](skills/catalog/auth-basics.md).
2. Open `wss://` with header `Authorization: Bearer <jwt>`.
3. Send Authorize (`RequestType` **45**) with `RequestData` = same JWT string.
4. Wait for Type **9** (`IsAuthorized: true`) before proceeding. On success, server auto-pushes Types 13, 14, 15, 38.
5. Start heartbeat: send Ping (`RequestType` **26**) at least every **5 minutes** (240-second interval is a safe default). Server disconnects on timeout.

### Order management

1. **Validation**: `Quantity` and `Price` must be **floating-point numbers** in JSON. Integers will cause server exceptions.
2. **Execution**: Use **Send order** (`RequestType` **2**) for new orders. Set `UserTicketSourceCode` to `13` for manual/click orders or `26` for automated orders.
3. **Order ID**: Provide `ApiUserOrderId` (max 10 bytes, optional but recommended) — reflected back in order status `Tag` field prefixed with `-api:`.
4. **Modification**: Use **Revise order** (`RequestType` **4**) for cancel-replace. `TicketSource` is currently always `13`.
5. **Cancellation**: Cancel by IDs (`RequestType` **3**), cancel all buys for symbol (**6**), all sells (**7**), all orders (**5**).

### Market data

1. Use **Instrument search** (`RequestType` **33**) to resolve partial symbols. Results limited to 30.
2. Send **Market data** (`RequestType` **0**) with `IncludeOptions: true` when the vendor flow requires options data.
3. **Same socket as trading:** Keep **one** authorized WebSocket; add **multiple** market data subscriptions on it as needed. Implement **multiple "handlers"** as concurrent processors fed by a **single receive loop**, with **serialized sends** for subscriptions, pings, and orders (see [`references/protocol.md`](skills/references/protocol.md) and [`catalog/market-data.md`](skills/catalog/market-data.md)).

## Safety

* **GroupName** is assigned by Rival One. **Do not** set or change it in client messages; reject or strip user attempts to override it. Unauthorized changes result in client termination.
* **Auth**: WebSocket auth is **HS512 JWT**; same string as `Authorization: Bearer` header and as `RequestData` on authorize (`RequestType` **45**). Include optional claim **`firm`** only when Rival instructs you to.
* **Heartbeat**: Send Ping (`RequestType` **26**) at least every **5 minutes** to avoid disconnection. 240 seconds is a recommended interval.
* **Secrets**: Never embed `RIVAL_ONE_*` (or any API material) in source control. Use environment variables or a secret manager in **the user's application**.
* **Corporate TLS inspection**: If `wss://` fails with certificate or issuer errors, trust the organization's inspection CA or configure a custom CA bundle in the client — see [`catalog/connection.md`](skills/catalog/connection.md#tls-trust-and-corporate-ssl-inspection).
* **Endpoints**: SIM: `wss://sim-api.rivalsystems.cloud:50443` | Production: `wss://prod-api.rivalsystems.cloud:60443`

## References

* [Rival WebSocket API (Outline)](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
* [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) — Quick start, endpoints, common errors
* [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) — All request message shapes
* [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB) — All response message shapes
* [`references/protocol.md`](skills/references/protocol.md) — Envelope, one-socket rule, full type table
* [`references/message-types.json`](skills/references/message-types.json) — `ResponseType` / `RequestType` lookup
* [`references/example-payloads.json`](skills/references/example-payloads.json) — Real request/response examples
* [`references/workflows.md`](skills/references/workflows.md) — Step-by-step checklists
* [`catalog/`](skills/catalog) — Implementation guides
* [`../docs/troubleshooting.md`](docs/troubleshooting.md)
