# Rival One — protocol reference

> **Source of truth:** [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) (Outline). Confirm message numbers and field shapes there before production.
>
> **Overview & common errors:** [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) — endpoints, heartbeat, and login errors. Repo notes: [`docs/troubleshooting.md`](../../docs/troubleshooting.md).
>
> **WebSocket API (Outline):** [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0) — index to Overview, Client Requests, Server Responses, and related pages.
>
> **Server messages:** [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB) — `ResponseType` numbers and `ResponseData` shapes.

## Message type lookup (JSON)

Inbound frames use `{ "ResponseType": <number>, "ResponseData": ... }`. For quick demux and logging, use **[`message-types.json`](message-types.json)**:

- **`responseTypesById`** — string keys (`"0"`, `"8"`, …) → `{ "name", "label" }` (stable `name` for code branches; `label` matches the vendor doc title where possible).
- **`requestTypesById`** — partial list of outbound types also documented in this file; extend from [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w).

Reconcile any new or changed numbers with Outline before production (`meta` in the JSON points at the canonical pages).

### Enrichment for display (optional)

The server only sends the **numeric** `ResponseType`. **Keep that number** on the object your app uses for routing, events, and `switch`/`match` — users and integrations should **not** depend on parsing a string instead of the number.

For **logs, UI, or assistant-visible copies**, you may **add** optional sidecar keys (see `meta.enrichment` in the JSON), e.g. **`_responseTypeName`** and **`_responseTypeLabel`**, copied from `responseTypesById`. Use a **shallow copy** of the frame so wire-format records stay vendor-pure if you persist them. Leading underscore avoids clashing with fields inside `ResponseData`.

## Transport

- **WebSocket** URL from `RIVAL_ONE_WSS_URL` (default SIM: `wss://sim-api.rivalsystems.cloud:50443`).
- Handshake header: **`Authorization: Bearer <JWT>`** where `<JWT>` is a complete HS512 JWT (see Authorize below).

## Single WebSocket for market data and orders

Use **one** authenticated WebSocket for the whole session unless Rival’s documentation explicitly tells you to open additional connections.

- **Market data “threads” in your app** are usually **concurrent tasks or queues** (per symbol, book, or strategy) that all attach to the **same** socket. You send multiple **Market data** requests (`RequestType` **0**, shapes per Client Requests) on that connection; inbound ticks and book updates arrive on the same socket as order acknowledgements and other responses.
- **Orders** (**Send** `RequestType` **2**, **Revise** **4**, etc.) use the **same** connection. Do not split “data plane” and “order plane” into two sockets unless the product requires it.
- **Implementation pattern:** one **receive** loop that parses JSON and **demultiplexes** to handlers (by `ResponseType`, symbol, correlation id, or fields your vendor doc defines). One **send** path: serialize outbound frames (mutex, single writer task, or outbound queue) because many WebSocket clients are **not** thread-safe for concurrent `send`.
- **Heartbeat** (**Ping**, `RequestType` **26**) also runs on this same connection.

Details and examples: [`../catalog/market-data.md`](../catalog/market-data.md), [`../catalog/orders.md`](../catalog/orders.md).

## Message envelope

All client messages use:

```json
{
  "RequestType": <number>,
  "RequestData": <payload>
}
```

`RequestData` type depends on the request (string JWT for authorize, object for orders, etc.).

## Authorize (RequestType 45)

Per [Client Requests — Authorize Request](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w):

1. Build a **JWT** with **HS512**, header `alg: HS512`, `typ: JWT`.
2. Payload claims include at least: `group`, `user`, `apikey` (and typically `sub`). When your onboarding requires it, add optional login claim **`firm`**—see [`../catalog/auth-basics.md`](../catalog/auth-basics.md).
3. Sign with your **secret key** (HMAC-SHA512).
4. Use the same JWT string for:
   - the WebSocket **Bearer** header, and
   - **`RequestData`** on the authorize message: `{ "RequestType": 45, "RequestData": "<jwt>" }`.

Your application can build that JWT from `RIVAL_ONE_API_KEY`, `RIVAL_ONE_SECRET_KEY`, `RIVAL_ONE_GROUP`, and `RIVAL_ONE_USER`, optionally adding claim **`firm`** from `RIVAL_ONE_FIRM` when Rival instructs you to (or load a pre-built JWT from `RIVAL_ONE_API_TOKEN`). See [`../catalog/auth-basics.md`](../catalog/auth-basics.md) for language examples.

## Session

| RequestType (default) | Name | Notes |
|----------------------|------|--------|
| 45 | Authorize | `RequestData` = JWT string |
| 26 | Ping | `RequestData` optional request id (string) |

## Trading (examples)

| RequestType (default) | Name | Notes |
|----------------------|------|--------|
| 2 | Send order | `RequestData` object; `Quantity` / `Price` as JSON numbers |
| 4 | Revise order | Cancel-replace; do not set `GroupName` in client payloads |
| 8 | Get all orders | Per vendor doc |

## Market data / search (examples)

| RequestType (default) | Name | Notes |
|----------------------|------|--------|
| 0 | Market data | `RequestData` per vendor |
| 33 | Instrument search | `RequestData` per vendor |

## Numeric coercion

At the boundary, coerce `Quantity` and `Price` with `float(...)` (Python) / `Number()` (TS) / `double` (C#) and serialize as JSON numbers where the API expects numbers.
