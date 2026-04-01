# Rival One — Protocol Reference

> **Source:** [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) · [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) · [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)

---

## Message Envelope

All messages are JSON. Client-to-server:

```json
{
    "RequestType": <number>,
    "RequestData": <payload>
}
```

Server-to-client:

```json
{
    "ResponseType": <number>,
    "ResponseData": <payload>
}
```

**Always route and dispatch on the numeric type.** Do not parse string labels for control flow. `_responseTypeName` / `_responseTypeLabel` may be added to a copy for readability, but routing stays on the number.

---

## One WebSocket for Everything

- **One authorized connection** handles both market data and orders.
- Do not open a second WebSocket for market data subscriptions.
- Implement a **single receive loop** that demuxes on `ResponseType`.
- **Serialize all sends**: subscriptions, pings, and orders must go through a single sender / queue. Concurrent sends on a WebSocket are not safe in most libraries.

---

## Connection Requirements

| Requirement | Detail |
|---|---|
| Transport | `wss://` (TLS) |
| Auth header on connect | `Authorization: Bearer <jwt>` — required, connection terminated without it |
| Heartbeat | Ping (Type 26) at least every **5 minutes** — server disconnects on timeout |
| Data types | All prices and quantities **must be floating-point**. Integer types cause server exceptions. |
| Case sensitivity | All field names and values are **case-sensitive** unless explicitly noted |
| Timestamps | All timestamps are **UTC epoch seconds** unless noted |

---

## Endpoints

| Environment | URL |
|---|---|
| Simulation | `wss://sim-api.rivalsystems.cloud:50443` |
| Production | `wss://prod-api.rivalsystems.cloud:60443` |

---

## CME Sub-Exchange Identifiers

| Sub-Exchange | Use this string |
|---|---|
| Globex | `CME` |
| Nymex | `CME-NYMEX` |
| Comex | `CME-COMEX` |
| CBOT | `CME-CBOT` |
| MGE | `CME-MGE` |

All ICE sub-exchanges use `ICE`.

---

## Complete Message Type Reference

> **NOTE:** Some type numbers are shared between requests and responses with different meanings (e.g. Type 2 is both "Book" response and "Send Order" request). Always check direction.

| Type | Request Name | Response Name | Category |
|------|-------------|---------------|----------|
| 0 | Market Data (subscribe) | Market Data Subscription Result | Market Data |
| 1 | — | Instrument Definition | Market Data |
| 2 | Send Order | Book (depth of market) | Orders / Market Data |
| 3 | Cancel Order(s) | Error Message | Orders / Errors |
| 4 | Revise Order | — | Orders |
| 5 | Cancel All Orders | Trade Price | Orders / Market Data |
| 6 | Cancel Buy Orders | Statistics | Orders / Market Data |
| 7 | Cancel Sell Orders | — | Orders |
| 8 | Get All Orders | Order Status | Orders |
| 9 | — | Authorize Response | Authentication |
| 13 | Update Trade Settings | User Settings Response | Settings |
| 14 | Update User Settings | Trade Settings Response | Settings |
| 15 | — | Accounts Response | Authentication |
| 20 | — | Position Summary | Risk |
| 21 | Delete Trade Settings | Not Entitled Error | Settings / Errors |
| 22 | Get Positions | — | Risk |
| 23 | — | Security Not Found Error | Errors |
| 26 | Ping | Pong | Connection |
| 31 | — | Volume at Level | Market Data |
| 33 | Instrument Search | Search Results | Search |
| 34 | Get Options Description | Options Descriptions | Options |
| 35 | — | Top-of-Book | Market Data |
| 37 | Get Spread Combinations | Trade (login replay) | Options / Orders |
| 38 | Send RFQ / Create Spread | Broker Routes Response | Options / Authentication |
| 39 | Get Theos and Greeks | Variable Tick Size Response | Options |
| 40 | Term-Market Data for Options | Spread Classification Response | Options |
| 41 | Get Options Strategies | Tick Size Response | Options |
| 42 | Market Data for Strategies | RFQ Failed Response | Options |
| 43 | Get Margin | Available Strategies Response | Risk / Options |
| 44 | — | Spreads Response | Options |
| 45 | Authorize | Margin Error Response | Authentication / Risk |
| 46 | — | Margin Response | Risk |
| 49 | Enter/Edit/Delete Manual Trade | — | Trades |
| 53 | Get Theos and Greeks (specific) | — | Options |
| 58 | Depth Data | — | Market Data |
| 61 | — | Participant Market Data | Market Data |

---

## Connection Sequence (canonical)

```
Client                                  Server
  |                                        |
  |-- WSS connect (Bearer: <jwt>) -------> |
  |-- { RequestType: 45, RequestData: jwt }|
  |                                        |
  |<-- { ResponseType: 9, IsAuthorized }---|  Authorize result
  |<-- { ResponseType: 13 } ---------------|  User settings (auto-pushed)
  |<-- { ResponseType: 14 } ---------------|  Trade settings (auto-pushed)
  |<-- { ResponseType: 15 } ---------------|  Accounts (auto-pushed)
  |<-- { ResponseType: 38 } ---------------|  Broker routes (auto-pushed)
  |                                        |
  |-- { RequestType: 33, searchVal: "ES" } |  Instrument search
  |<-- { ResponseType: 33, results }-------|
  |                                        |
  |-- { RequestType: 0, symbol: "ESZ5" }   |  Subscribe market data
  |<-- { ResponseType: 1 } ----------------|  Instrument definition
  |<-- { ResponseType: 2 } ----------------|  Book (streaming)
  |<-- { ResponseType: 5 } ----------------|  Trade (streaming)
  |<-- { ResponseType: 6 } ----------------|  Statistics (streaming)
  |                                        |
  |-- { RequestType: 26 } (every 240s) --> |  Ping / heartbeat
  |<-- { ResponseType: 26 } ---------------|  Pong
```

---

## Safety Rules

- **`GroupName` is immutable.** Rival assigns it. Do not set or change it in client messages; strip any user attempt to override it.
- **Never embed secrets in source code.** Use `RIVAL_ONE_*` environment variables or a secret manager.
- **`UserTicketSourceCode`:** Use `13` for manual/click orders, `26` for automated orders. Required on every Send Order (Type 2) request.
- **`ApiUserOrderId`:** Optional but recommended — max 10 bytes — reflected back in order `Tag` for correlation.
