---
name: rival-one
description: Use when building or debugging a client for the Rival One WebSocket API (JWT HS512 auth, orders, market data, SIM or production). Implementation patterns and safety rules live in skills/.
---

# Rival One (Cursor)

## Canonical instructions

Load and follow **[`skills/rival-one-core.md`](../../../skills/rival-one-core.md)** for operating rules.

## Implementation guides (read the relevant file)

| Topic | Path |
|-------|------|
| Catalog index | [`skills/catalog/README.md`](../../../skills/catalog/README.md) |
| JWT auth | [`skills/catalog/auth-basics.md`](../../../skills/catalog/auth-basics.md) |
| WebSocket + heartbeat | [`skills/catalog/connection.md`](../../../skills/catalog/connection.md) |
| Market data | [`skills/catalog/market-data.md`](../../../skills/catalog/market-data.md) |
| Orders | [`skills/catalog/orders.md`](../../../skills/catalog/orders.md) |
| Errors | [`skills/catalog/errors-troubleshooting.md`](../../../skills/catalog/errors-troubleshooting.md) |
| Protocol tables | [`skills/references/protocol.md`](../../../skills/references/protocol.md) |
| ResponseType / RequestType names (JSON) | [`skills/references/message-types.json`](../../../skills/references/message-types.json) |
| Workflows | [`skills/references/workflows.md`](../../../skills/references/workflows.md) |

| External | Link |
|----------|------|
| Rival WebSocket API (Outline) | [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0) |
| Client Requests (message API) | [Outline — Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) |
| Server Responses (`ResponseType`) | [Outline — Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB) |
| Python example (incl. optional TLS / CA settings) | [Outline — Python example](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/python-example-qlh5BEqaQV) |

Do not invent `RequestType` or `RequestData` shapes; copy from the catalog + Client Requests. Use **one WebSocket** for market data subscriptions and orders unless vendor docs say otherwise ([protocol](../../../skills/references/protocol.md#single-websocket-for-market-data-and-orders)).
