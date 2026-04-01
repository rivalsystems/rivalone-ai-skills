---
name: rival-one
description: Use when building or debugging a client for the Rival One WebSocket API (JWT HS512 auth, orders, market data, SIM or production). Implementation patterns and safety rules live in skills/.
---

# Rival One (Claude Code)

## Canonical instructions

Read **[`skills/rival-one-core.md`](../../../skills/rival-one-core.md)** first.

## Guides under `skills/catalog/`

- [`skills/catalog/README.md`](../../../skills/catalog/README.md) — index
- [`auth-basics.md`](../../../skills/catalog/auth-basics.md), [`connection.md`](../../../skills/catalog/connection.md), [`market-data.md`](../../../skills/catalog/market-data.md), [`orders.md`](../../../skills/catalog/orders.md), [`errors-troubleshooting.md`](../../../skills/catalog/errors-troubleshooting.md)

## References

- [`skills/references/protocol.md`](../../../skills/references/protocol.md) — includes **one WebSocket** for market data + orders
- [`skills/references/message-types.json`](../../../skills/references/message-types.json) — `ResponseType` / partial `RequestType` → name + label
- [`skills/references/workflows.md`](../../../skills/references/workflows.md)
- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) (message-level API)
- [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB) (`ResponseType` reference)
- [Python example](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/python-example-qlh5BEqaQV) — optional TLS / CA bundle settings (see universal notes in [`connection.md`](../../../skills/catalog/connection.md))

Invoke explicitly with `/rival-one` if needed; confirm with `/skills`.
