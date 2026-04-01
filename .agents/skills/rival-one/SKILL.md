---
name: rival-one
description: Use this skill whenever the user is building, debugging, testing, or extending any integration with the Rival One WebSocket API — including JWT HS512 auth setup, instrument search, market data subscriptions, order send/revise/cancel, heartbeat, or SIM/production environment setup. Also use when the user mentions Rival One, rival-one, RIVAL_ONE env vars, or is working with a WebSocket client that uses RequestType/ResponseType message envelopes. Implementation patterns and safety rules (GroupName immutability, secret handling) live in skills/.
---

# Rival One (OpenAI Codex / generic agents)

## Canonical instructions

Read **[`skills/rival-one-core.md`](skills/rival-one-core.md)** first.

## Guides under `skills/catalog/`

* [`skills/catalog/README.md`](skills/catalog/README.md) — index
* [`auth-basics.md`](skills/catalog/auth-basics.md) — JWT HS512, claims, authorize request/response
* [`connection.md`](skills/catalog/connection.md) — endpoints, connect flow, heartbeat, TLS
* [`market-data.md`](skills/catalog/market-data.md) — instrument search (33), subscriptions (0), all market data message types
* [`orders.md`](skills/catalog/orders.md) — send (2), revise (4), cancel (3/5/6/7), order status (8)
* [`errors-troubleshooting.md`](skills/catalog/errors-troubleshooting.md) — auth failures, error types (3/21/23), diagnostics

## References

* [`skills/references/protocol.md`](skills/references/protocol.md) — envelope format, one WebSocket rule, full type reference table
* [`skills/references/message-types.json`](skills/references/message-types.json) — complete `ResponseType` / `RequestType` → name lookup
* [`skills/references/example-payloads.json`](skills/references/example-payloads.json) — real request/response examples
* [`skills/references/workflows.md`](skills/references/workflows.md)
* [Rival WebSocket API (Outline)](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
* [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU)
* [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)
* [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)
