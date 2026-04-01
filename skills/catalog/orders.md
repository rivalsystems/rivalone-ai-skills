# Bundle: orders — send and revise

## Rules

- **`Quantity` and `Price`** must be JSON **numbers** (floating point at the boundary). Integers can trigger server errors.
- **Never** set or override **`GroupName`** in client payloads; it is assigned by Rival One.
- **Send order** typically **`RequestType` 2**; **Revise order** (cancel-replace) **`RequestType` 4** — confirm in [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w).

## Side values (example wire mapping)

Many integrations map human-readable sides to string codes:

| Input | Wire `Side` |
|-------|-------------|
| buy / b | `"1"` |
| sell / s | `"2"` |
| short / ss | `"3"` |

Confirm against the official doc if your product uses different enumerations.

## Example: limit order (`RequestType` 2)

`RequestData` fields below match a common **Send order** shape; **validate every field** with Client Requests before production.

```json
{
  "RequestType": 2,
  "RequestData": {
    "Quantity": 1.0,
    "Price": 123.45,
    "GenericMarketDataSymbol": "ES",
    "Side": "1",
    "OrdType": 2,
    "TIF": 1,
    "UserTicketSourceCode": 13
  }
}
```

Add `Account` when your registration requires a default account string.

## Python

```python
import json

def side_to_wire(side: str) -> str:
    s = side.strip().lower()
    if s in ("buy", "b"):
        return "1"
    if s in ("sell", "s"):
        return "2"
    if s in ("short", "shortsell", "ss"):
        return "3"
    return side

async def send_limit_order(ws, *, symbol: str, side: str, quantity: float, price: float, account: str | None = None):
    rd = {
        "Quantity": float(quantity),
        "Price": float(price),
        "GenericMarketDataSymbol": symbol,
        "Side": side_to_wire(side),
        "OrdType": 2,
        "TIF": 1,
        "UserTicketSourceCode": 13,
    }
    if account:
        rd["Account"] = account.strip()
    await ws.send(json.dumps({"RequestType": 2, "RequestData": rd}))
```

## TypeScript

```typescript
function sideToWire(side: string): string {
  const s = side.trim().toLowerCase();
  if (s === "buy" || s === "b") return "1";
  if (s === "sell" || s === "s") return "2";
  if (s === "short" || s === "shortsell" || s === "ss") return "3";
  return side;
}

export function sendLimitOrder(
  ws: { send(data: string): void },
  p: { symbol: string; side: string; quantity: number; price: number; account?: string },
) {
  const rd: Record<string, unknown> = {
    Quantity: Number(p.quantity),
    Price: Number(p.price),
    GenericMarketDataSymbol: p.symbol,
    Side: sideToWire(p.side),
    OrdType: 2,
    TIF: 1,
    UserTicketSourceCode: 13,
  };
  if (p.account?.trim()) rd.Account = p.account.trim();
  ws.send(JSON.stringify({ RequestType: 2, RequestData: rd }));
}
```

## C#

Coerce with `Convert.ToDouble` or `(double)` before serializing so JSON emits numbers, not strings.

## Revise order (`RequestType` 4)

Build `RequestData` per Client Requests for cancel-replace. Do **not** invent `GroupName`; use identifiers the vendor specifies for the order to revise.

## See also

- [../references/protocol.md#single-websocket-for-market-data-and-orders](../references/protocol.md#single-websocket-for-market-data-and-orders) — same connection as market data
- [../references/workflows.md](../references/workflows.md)
- [../rival-one-core.md](../rival-one-core.md) — safety checklist
