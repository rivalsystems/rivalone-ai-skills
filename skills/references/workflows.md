# Rival One — workflows

## Connect

1. Build or load the **HS512 JWT** (Bearer token) per [Client Requests — Authorize](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w).
2. Open WebSocket with `Authorization: Bearer <JWT>`.
3. Send **Authorize** (`RequestType` **45**, `RequestData` = same JWT string).
4. Start **Ping** loop (`RequestType` **26**) on the configured interval.

Step-by-step code: [`../catalog/connection.md`](../catalog/connection.md).

## Place limit order

1. Validate symbol and side (map Buy/Sell to wire values per vendor doc — examples in [`../catalog/orders.md`](../catalog/orders.md)).
2. Coerce `Quantity` and `Price` to floats.
3. Build **Send order** (`RequestType` **2**, `RequestData` object per Client Requests).
4. Send JSON over the socket; handle responses per your subscriptions.

## Market data

1. **Instrument search** (`RequestType` **33**) to confirm symbol.
2. **Market data** (`RequestType` **0**) subscription with `IncludeOptions: true` when needed.
3. **One WebSocket:** Add as many market data subscriptions as required on the **same** connection you use for **orders** and **ping**. Demux inbound messages in one receive path; serialize outbound `send` calls.

See [`../catalog/market-data.md`](../catalog/market-data.md) and [protocol — one WebSocket](protocol.md#single-websocket-for-market-data-and-orders).

Vendor WebSocket docs: [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0).

## Safety checklist

- [ ] No unauthorized `GroupName` changes.
- [ ] Heartbeat task running after authorize.
- [ ] Floats used for numeric trading fields.
- [ ] Request shapes verified against Client Requests (not guessed).
