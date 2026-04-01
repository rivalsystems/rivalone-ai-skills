# Rival One integration — assumptions and consensus

This repository does not ship vendor Rival One API documentation. The scaffold below reflects **best-effort consensus** from the product prompt and internal review, not certified behavior.

## Treated as specified in vendor documentation

- WebSocket transport to a configurable URL (default SIM: `wss://sim-api.rivalsystems.cloud:50443`).
- Connection uses `Authorization: Bearer <JWT>` on the WebSocket handshake (**HS512 JWT** per [Client Requests — Authorize](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)).
- After connect, an **Authorize** message with **RequestType 45** and **`RequestData`** set to the **same JWT string** as the Bearer token.
- Client messages use the **`RequestType` / `RequestData`** envelope (not legacy top-level `Type` for new work).
- **Ping** uses **RequestType 26** on a periodic cadence (default **240 seconds**) to keep the session alive.
- **Send order** uses **RequestType 2** with `RequestData` containing order fields; `Quantity` and `Price` as JSON numbers.
- **GroupName** is assigned by the platform; agents must **not** invent or overwrite it in outgoing messages.

## Explicitly configurable / verify with vendor docs

- Exact numeric **Type** values for every operation (search, market data, revise order, order status, etc.).
- Full JSON schemas for each message type, including required and optional fields.
- Whether any numeric fields must be serialized as decimals/strings instead of JSON numbers.
- Token lifetime, refresh, and error responses from the Authorize step.
- Reconnection, backoff, and session idempotency rules.

## Implementation note

Example code in [`../skills/catalog/`](../skills/catalog/) uses common defaults (request types, ping interval, field names). When official docs disagree, update the **catalog** markdown and [`../skills/references/protocol.md`](../skills/references/protocol.md) so agents and humans see one consistent story.
