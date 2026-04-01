# Rival One — implementation catalog

Hands-on guides for **your** application code. Each bundle is one markdown file with multi-language examples.

| ID | File | Topic |
|----|------|--------|
| `auth-basics` | [auth-basics.md](auth-basics.md) | HS512 JWT, claims, authorize request/response (Type 45/9) |
| `connection` | [connection.md](connection.md) | Endpoints, connect flow, heartbeat (5 min), TLS/corp CA |
| `market-data` | [market-data.md](market-data.md) | Search (33), subscriptions (0), all 6 market data types |
| `orders` | [orders.md](orders.md) | Send (2), revise (4), cancel (3/5/6/7), order status (8) |
| `errors-troubleshooting` | [errors-troubleshooting.md](errors-troubleshooting.md) | Auth failures, error types (3/21/23), diagnostics |

Machine-readable index: [catalog.json](catalog.json).

**References:**
- [../references/protocol.md](../references/protocol.md) — envelope format, one-socket rule, complete type table
- [../references/message-types.json](../references/message-types.json) — complete ResponseType/RequestType lookup
- [../references/example-payloads.json](../references/example-payloads.json) — real sanitized request/response examples
- [../references/workflows.md](../references/workflows.md) — step-by-step checklists

**Vendor WebSocket docs:** [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0) · [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) · [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) · [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)

**New to the flow?** See [`../../docs/example-ai-prompt.md`](../../docs/example-ai-prompt.md) for a credential JSON template and a ready-made prompt to bootstrap an app with your AI.
