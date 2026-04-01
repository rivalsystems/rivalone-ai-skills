---
name: rival-one
description: Rival One WebSocket API integration — JWT HS512, orders, market data. Use when the user implements or debugs a Rival One client in any language.
---

# Rival One (OpenAI Codex)

## Start here

**[`skills/rival-one-core.md`](../../../skills/rival-one-core.md)** — rules and checklists.

## Implementation catalog

| File | Topic |
|------|--------|
| [`skills/catalog/README.md`](../../../skills/catalog/README.md) | Index |
| [`auth-basics.md`](../../../skills/catalog/auth-basics.md) | JWT |
| [`connection.md`](../../../skills/catalog/connection.md) | WSS + ping |
| [`market-data.md`](../../../skills/catalog/market-data.md) | Search + subscribe |
| [`orders.md`](../../../skills/catalog/orders.md) | Send / revise |
| [`errors-troubleshooting.md`](../../../skills/catalog/errors-troubleshooting.md) | Common issues |

## References

[`protocol.md`](../../../skills/references/protocol.md) (one WebSocket for market data + orders) · [`message-types.json`](../../../skills/references/message-types.json) (`ResponseType` / partial `RequestType` lookup) · [`workflows.md`](../../../skills/references/workflows.md)

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)
- [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)
- [Python example](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/python-example-qlh5BEqaQV) — optional TLS / CA settings; universal guidance in [`connection.md`](../../../skills/catalog/connection.md)

Codex discovers repo skills per [OpenAI customization docs](https://developers.openai.com/codex/concepts/customization/).
