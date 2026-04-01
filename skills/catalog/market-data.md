# Bundle: market-data — search and subscribe

Always confirm **`RequestData` shape** in [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w). Broader context: [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0) (Outline). Default request numbers below match common Rival One usage; verify before production.

## One WebSocket: many market-data consumers + trading

You normally maintain **a single** authorized WebSocket and multiplex everything on it:

1. **Subscriptions:** Issue multiple **Market data** requests (`RequestType` **0**) on that socket—one per instrument/stream your app needs (exact payload per Client Requests). That is how you “run several market data threads”: not several sockets, but several subscriptions (and several in-app workers reading from a shared inbound demux).
2. **Trading:** Send **orders** (`RequestType` **2** / **4** / …) on the **same** socket between or alongside subscription traffic.
3. **Concurrency:** Use one **receive** loop and route messages to per-symbol or per-topic handlers (async tasks, channels, callbacks). Use **one serialized send path** (lock or queue) so ping, market-data requests, and orders never call `send` concurrently on a non-thread-safe client.

See [protocol — one WebSocket](../references/protocol.md#single-websocket-for-market-data-and-orders) and [orders.md](orders.md).

| RequestType | Purpose |
|-------------|---------|
| **33** | Instrument search |
| **0** | Market data subscription |

Use **Instrument search** first to resolve symbols, then **Market data** with the fields your vendor doc requires. When options chains matter, set **`IncludeOptions: true`** if the API expects it (see [workflows](../references/workflows.md)).

## Pattern

```json
{ "RequestType": 33, "RequestData": { /* per Client Requests — Instrument Search */ } }
```

```json
{ "RequestType": 0, "RequestData": { /* per Client Requests — Market Data */ } }
```

## Python

```python
import json

async def instrument_search(ws, request_data: dict) -> None:
    await ws.send(json.dumps({"RequestType": 33, "RequestData": request_data}))

async def market_data_subscribe(ws, request_data: dict) -> None:
    request_data = {**request_data, "IncludeOptions": True}  # only if your doc requires it
    await ws.send(json.dumps({"RequestType": 0, "RequestData": request_data}))
```

## TypeScript

```typescript
export function instrumentSearch(ws: { send(data: string): void }, requestData: Record<string, unknown>) {
  ws.send(JSON.stringify({ RequestType: 33, RequestData: requestData }));
}

export function marketDataSubscribe(ws: { send(data: string): void }, requestData: Record<string, unknown>) {
  ws.send(JSON.stringify({ RequestType: 0, RequestData: { ...requestData, IncludeOptions: true } }));
}
```

Replace `requestData` keys with the exact names and types from the vendor document.

## See also

- [../references/protocol.md](../references/protocol.md)
- [orders.md](orders.md)
