# Bundle: market-data — Instrument Search, Subscriptions, Market Data Messages

> **Source:** [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) · [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB) · [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU)

## One Socket Rule

Market data and orders share the **same authorized WebSocket**. Never open a second connection for market data. Implement a single receive loop that demuxes on `ResponseType`; serialize all sends (subscriptions, pings, orders) through one sender. See [../references/protocol.md](../references/protocol.md).

---

## Step 1 — Instrument Search (Type 33)

Resolve a partial symbol to its `GenericMarketDataSymbol` before subscribing. Results are limited to 30 per search.

**Request:**
```json
{
    "RequestType": 33,
    "RequestData": {
        "searchId": "d798b02a-8c3e-42f8-919c-c04ec16cf0de",
        "searchVal": "ESH",
        "selectedVals": []
    }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `searchId` | String | Yes | Unique GUID — returned in response for correlation |
| `searchVal` | String | Yes | Partial symbol string (e.g. `"ES"` returns all ES futures) |
| `selectedVals` | SearchOption[] | No | Additional search filters |

**Response (Type 33):**
```json
{
    "ResponseType": 33,
    "ResponseData": {
        "SearchId": "d798b02a-8c3e-42f8-919c-c04ec16cf0de",
        "SearchResults": [
            {
                "name": "ESZ5",
                "longName": "E-mini Standard and Poor's 500 Stock Price Index Futures",
                "exchange": "CME",
                "category": "Symbols",
                "secType": 3
            }
        ]
    }
}
```

Use the `name` field as your `GenericMarketDataSymbol` in subsequent requests.

---

## Step 2 — Subscribe to Market Data (Type 0)

Subscribe to book, trade, and statistics messages for an instrument.

**Request:**
```json
{
    "RequestType": 0,
    "RequestData": {
        "GenericMarketDataSymbol": "ESZ5",
        "IncludeOptions": false
    }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `GenericMarketDataSymbol` | String | Yes | Market data symbol from instrument search |
| `FeedSpecificID` | String | Yes* | Required for certain feeds (e.g. ICE) — the `MdAuxilliaryUserInfo` value |
| `IsSpreaderInst` | Boolean | No | `true` if synthetic user-defined spread |
| `IncludeOptions` | Boolean | No | `true` to also receive associated options data |

**Subscription result response (Type 0):**
```json
{
    "ResponseType": 0,
    "ResponseData": {
        "SubscriptionResults": [
            {
                "Success": true,
                "Username": "rival_123",
                "GenericMarketDataSymbol": "ESZ5"
            }
        ]
    }
}
```

On success, the server streams the following message types automatically:

| ResponseType | Name | Typical Use |
|-------------|------|-------------|
| `1` | Instrument Definition | Contract metadata (tick size, expiry, contract size) |
| `2` | Book | Depth of market — bid/ask levels (futures/spreads) |
| `35` | Top-of-Book | Best bid/offer L1 (options/option spreads) |
| `5` | Trade Price | Last trade price and size |
| `31` | Volume at Level | Cumulative volume by price level for session |
| `6` | Statistics | Settlement, open, daily high/low |

---

## Market Data Messages Reference

### Instrument Definition (Type 1)
Contract metadata. Always arrives after a successful subscription.
```json
{
    "ResponseType": 1,
    "ResponseData": {
        "SecurityInfo": {
            "SecurityType": "F",
            "BaseSymbol": "ES",
            "Ticker": "ESZ5",
            "Exchange": "CME",
            "Strike": 0,
            "Expiration": "2025-12-19",
            "ContractSize": 50,
            "TickSize": 0.25,
            "GenericMdSymbol": "ESZ5",
            "CurrencyCode": "USD",
            "LongName": "E-mini Standard and Poor's 500 Stock Price Index Futures",
            "RoninSymbol": "F:ES:251201:CME",
            "ExpirationTime": "1766154600",
            "ExpYear": 2025,
            "ExpMonth": 12,
            "ExpDay": 19,
            "DecimalPrecision": 0
        }
    }
}
```

### Book (Type 2) — Futures & Spreads
Depth of market. Bids descending, asks ascending.
```json
{
    "ResponseType": 2,
    "ResponseData": {
        "Symbol": "ESZ5",
        "Feed": "CME",
        "Bids": [
            { "Price": 5900.25, "Size": 100 },
            { "Price": 5900.00, "Size": 150 }
        ],
        "Asks": [
            { "Price": 5900.50, "Size": 100 },
            { "Price": 5900.75, "Size": 150 }
        ]
    }
}
```

### Top-of-Book (Type 35) — Options & Option Spreads
Best bid/offer (L1) only.
```json
{
    "ResponseType": 35,
    "ResponseData": {
        "Symbol": "ESZ5",
        "Exchange": "CME",
        "TopBid": { "Price": 5900.25, "Size": 100 },
        "TopAsk": { "Price": 5900.50, "Size": 100 }
    }
}
```

### Trade Price (Type 5)
Last trade details.
```json
{
    "ResponseType": 5,
    "ResponseData": {
        "Symbol": "ESZ5",
        "Feed": "CME",
        "LastPrice": 5900.25,
        "LastSize": 150,
        "CumulativeTradeQuantity": 750,
        "ExchangeTime": 1704920400,
        "IsOTC": false,
        "IsLeg": false,
        "VolumeAtLevel": 200
    }
}
```

### Volume at Level (Type 31)
All price levels traded during the session with cumulative volume.
```json
{
    "ResponseType": 31,
    "ResponseData": {
        "Symbol": "ESZ5",
        "Feed": "CME",
        "MaxVolume": 1596,
        "PriceToVolume": {
            "5900.0": 15,
            "5900.25": 1596,
            "5900.5": 220
        }
    }
}
```

### Statistics (Type 6)
Settlement and session price data.
```json
{
    "ResponseType": 6,
    "ResponseData": {
        "Symbol": "ESZ5",
        "Feed": "CME",
        "SettlementPrice": 5900.0,
        "OpeningPrice": 5895.50,
        "DailyLowPrice": 5880.0,
        "DailyHighPrice": 5915.0,
        "ExchangeTime": 1704920400
    }
}
```

---

## Options Market Data

### For an Options Series

1. Send Market Data (Type 0) with `IncludeOptions: true`
2. Send Term-Market Data (Type 40) immediately after for the specific series

**Term-Market Data Request (Type 40):**
```json
{
    "RequestType": 40,
    "RequestData": {
        "OptionSymbol": "EW",
        "Exchange": "CME",
        "ExpTime": "1704920400",
        "IsSubscribeRequest": true
    }
}
```

To unsubscribe set `IsSubscribeRequest: false`.

> **NOTE:** Options market data requires additional entitlements.

### Get Option Descriptions (Type 34)
Fetch available strikes/expiries for an options series:
```json
{
    "RequestType": 34,
    "RequestData": {
        "RequestData": [
            {
                "Exchange": "CME",
                "Category": "Options",
                "BaseSymbol": "ES.CME",
                "BaseSymbolExchange": "CME",
                "SecType": 4
            }
        ]
    }
}
```

---

## CME Sub-Exchange Names

Use these exact strings in `Exchange` fields:

| Sub-Exchange | Value |
|---|---|
| Globex | `CME` |
| Nymex | `CME-NYMEX` |
| Comex | `CME-COMEX` |
| CBOT | `CME-CBOT` |
| MGE | `CME-MGE` |

> Note: ICE sub-exchanges are all simply `ICE` (ICE LIFFE, ICE US, etc. all use the same value).

---

## Python Pattern — Single Socket with Market Data

```python
import asyncio
import json
import websockets

async def run(token: str, url: str):
    async with websockets.connect(url, additional_headers={"Authorization": f"Bearer {token}"}) as ws:
        # Auth
        await ws.send(json.dumps({"RequestType": 45, "RequestData": token}))

        # Heartbeat
        async def ping():
            while True:
                await asyncio.sleep(240)
                await ws.send(json.dumps({"RequestType": 26}))
        asyncio.create_task(ping())

        # Wait for auth confirmation before subscribing
        authorized = False
        async for raw in ws:
            msg = json.loads(raw)
            rt = msg.get("ResponseType")

            if rt == 9:  # Authorize response
                if msg["ResponseData"]["IsAuthorized"]:
                    authorized = True
                    # Now subscribe
                    await ws.send(json.dumps({
                        "RequestType": 33,
                        "RequestData": {"searchId": "s1", "searchVal": "ESZ5", "selectedVals": []}
                    }))
            elif rt == 33 and authorized:  # Search results
                symbol = msg["ResponseData"]["SearchResults"][0]["name"]
                await ws.send(json.dumps({
                    "RequestType": 0,
                    "RequestData": {"GenericMarketDataSymbol": symbol}
                }))
            elif rt == 1:   # Instrument definition
                pass
            elif rt == 2:   # Book update
                pass
            elif rt == 5:   # Trade
                pass
            elif rt == 6:   # Statistics
                pass
```

## See also

- [connection.md](connection.md) — connect and authorize
- [orders.md](orders.md) — trading on the same socket
- [../references/protocol.md](../references/protocol.md)
