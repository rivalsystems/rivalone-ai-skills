# Bundle: orders — Send, Revise, Cancel Orders

> **Source:** [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) · [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)

> **NOTE:** Order execution requires additional entitlements baked into your API key.

## Critical: Numeric Types

**All `Quantity` and `Price` fields must be floating-point numbers in JSON.** Using integer or long types will cause server-side exceptions. Always serialize as `5.0` not `5`, or as a quoted decimal string where the API accepts it (e.g. `"5500.25"`).

---

## Send Order (Type 2)

```json
{
    "RequestType": 2,
    "RequestData": {
        "GenericMarketDataSymbol": "ESZ5",
        "Quantity": 5.0,
        "Price": "5500.25",
        "Side": "1",
        "Account": "RIVAL_12345",
        "TIF": "1",
        "OrdType": "2",
        "UserTicketSourceCode": 13,
        "ApiUserOrderId": "my_order_001"
    }
}
```

### Send Order Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `GenericMarketDataSymbol` | String | Yes | Market data symbol (from instrument search) |
| `Quantity` | Number | Yes | Order quantity — **must be float** |
| `Price` | Number | Yes | Order price — **must be float** |
| `Side` | Enum | Yes | `1=Buy`, `2=Sell`, `3=ShortSell` |
| `Account` | String | Yes | Account identifier |
| `TIF` | Enum | Yes | Time-in-force (see table below) |
| `OrdType` | Enum | Yes | Order type (see table below) |
| `UserTicketSourceCode` | Number | Yes | `13` for manual/click orders; `26` for automated orders |
| `ApiUserOrderId` | String | No | Your own order ID — reflected back in order status `Tag` field (max 10 bytes, recommended) |
| `StopPrice` | Number | No | Stop price for Stop/StopLimit orders |
| `ShowQty` | Number | No | Max-show (iceberg) quantity |
| `ShortSellOverride` | Enum | Yes* | Required for `Side=3`: `0=Auto`, `1=OnOrder`, `2=Off` |
| `ExchangeRoute` | Enum | No | Destination code for broker routing |
| `autoHedge` | Boolean | No | `true` to auto-hedge option orders |
| `IsSpreaderOrder` | Boolean | No | `true` if synthetic user-defined spread (default: `false`) |

### TIF Values

| Value | Name |
|-------|------|
| `1` | Day |
| `2` | GoodTillCancel |
| `3` | ImmediateOrCancel |
| `4` | GoodTillCrossing |
| `5` | DayGoodTillCrossing |
| `6` | MarketOnClose |

### Order Type Values

| Value | Name |
|-------|------|
| `1` | Market |
| `2` | Limit |
| `3` | Stop |
| `4` | StopLimit |

---

## Revise Order (Type 4) — Cancel-Replace

```json
{
    "RequestType": 4,
    "RequestData": {
        "Tag": "test-TEST-40040-1764686958",
        "GenericMarketDataSymbol": "ESZ5",
        "Price": 5900.25,
        "Quantity": 2.0,
        "ShowQty": 0.0,
        "Side": 1,
        "StopPrice": 0.0,
        "IsSpreaderOrder": false,
        "TicketSource": 13
    }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Tag` | String | Yes | Order ID to revise (from Order Status response) |
| `GenericMarketDataSymbol` | String | Yes | Market data symbol |
| `Quantity` | Number | Yes | New quantity — **must be float** |
| `Price` | Number | Yes | New price — **must be float** |
| `Side` | Enum | Yes | `1=Buy`, `2=Sell`, `3=ShortSell` |
| `TicketSource` | Enum | Yes | Currently only `13` supported |
| `ShowQty` | Number | No | New max-show quantity |
| `StopPrice` | Number | No | New stop price |
| `IsSpreaderOrder` | Boolean | No | `true` if synthetic spread |

> **Never** invent or override `GroupName` — it is assigned by Rival and immutable.

---

## Cancel Orders (Type 3) — Cancel by ID

```json
{
    "RequestType": 3,
    "RequestData": {
        "Tags": ["order-id-1", "order-id-2"]
    }
}
```

## Cancel Buy Orders (Type 6) — Cancel All Buys for Symbol

```json
{
    "RequestType": 6,
    "RequestData": {
        "GenericMarketDataSymbol": "ESZ5"
    }
}
```

## Cancel Sell Orders (Type 7) — Cancel All Sells for Symbol

```json
{
    "RequestType": 7,
    "RequestData": {
        "GenericMarketDataSymbol": "ESZ5"
    }
}
```

## Cancel All Orders (Type 5)

Cancels all orders. Pass `GenericMarketDataSymbol` to limit to a specific instrument, or omit for all.

```json
{
    "RequestType": 5,
    "RequestData": {
        "GenericMarketDataSymbol": "ESZ5"
    }
}
```

## Get All Orders (Type 8)

Fetches all existing orders (open and closed). No payload required.

```json
{
    "RequestType": 8
}
```

---

## Order Status Response (Type 8)

All order lifecycle events arrive as Type 8 messages. The `Tag` field is a multi-part order ID — if you sent `ApiUserOrderId`, it appears in `Tag` prefixed with `-api:`.

```json
{
    "ResponseType": 8,
    "ResponseData": {
        "TimestampStr": "2024-12-26T18:58:05Z",
        "Tag": "ngen01-32122-1703544077-api:my_order_001",
        "GmdSymbol": "ESZ5",
        "Shares": 5.0,
        "Price": 5500.25,
        "OrderType": 2,
        "Side": 1,
        "TimeInForce": 1,
        "TraderName": "jsmith",
        "OrderStatus": -1,
        "LeaveShares": 5.0,
        "LastShares": 0.0,
        "Text": "",
        "StopPrice": 0.0,
        "ShowQty": 0.0,
        "TickSize": 0.25
    }
}
```

### OrderStatus Values

| Value | Meaning |
|-------|---------|
| `-1` | PendingNew |
| `4` | Cancelled |
| `12` | Open |
| `1` | PartiallyFilled |
| `2` | Filled |

If `OrderStatus` is not one of the above and `Text` is non-empty, the order was **rejected** — read `Text` for the reason.

---

## Python Pattern — Sending an Order

```python
import asyncio, json, websockets

async def send_order(ws, symbol: str, qty: float, price: float, account: str, order_id: str):
    """Send a limit buy order. ws must already be authorized."""
    msg = {
        "RequestType": 2,
        "RequestData": {
            "GenericMarketDataSymbol": symbol,
            "Quantity": qty,
            "Price": price,
            "Side": 1,              # Buy
            "OrdType": 2,           # Limit
            "TIF": 1,               # Day
            "Account": account,
            "UserTicketSourceCode": 13,
            "ApiUserOrderId": order_id[:10],  # max 10 bytes
        }
    }
    await ws.send(json.dumps(msg))

# In your receive loop, handle order updates:
# elif rt == 8:
#     status = msg["ResponseData"]["OrderStatus"]
#     tag = msg["ResponseData"]["Tag"]
```

## TypeScript Pattern — Sending an Order

```typescript
function sendOrder(ws: WebSocket, params: {
  symbol: string; qty: number; price: number;
  account: string; orderId: string;
}) {
  ws.send(JSON.stringify({
    RequestType: 2,
    RequestData: {
      GenericMarketDataSymbol: params.symbol,
      Quantity: params.qty,
      Price: params.price,
      Side: 1,                  // Buy
      OrdType: 2,               // Limit
      TIF: 1,                   // Day
      Account: params.account,
      UserTicketSourceCode: 13,
      ApiUserOrderId: params.orderId.slice(0, 10),
    }
  }));
}
```

## See also

- [connection.md](connection.md) — connect and authorize first
- [market-data.md](market-data.md) — instrument search to get `GenericMarketDataSymbol`
- [errors-troubleshooting.md](errors-troubleshooting.md) — order rejection reasons
- [../references/protocol.md](../references/protocol.md) — serialized sends on one socket
