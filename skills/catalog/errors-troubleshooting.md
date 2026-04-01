# Bundle: errors-troubleshooting — Auth, Connection, and Order Errors

> **Source:** [Overview — Common Errors](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) · [Server Responses](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/server-responses-2ZB81dxqCB)

---

## Auth & Login Errors

### "API user not registered with the system"

```
API user not registered with the system | Grp=[SOMETHING.JSMITH], User=[jsmith]
```

This is the most common login failure. Causes:

- `group` claim does not exactly match what Rival registered for your account (case-sensitive, must match character-for-character)
- `user` claim does not match registration
- `apikey` claim is wrong or has extra whitespace
- JWT was built with the wrong secret (signature invalid — server may reject silently or with a generic error)

**Fix:** Confirm `group`, `user`, and `apikey` values directly with Rival support (`rivalapisupport@rivalsystems.com`). Trim all whitespace before encoding claims.

### Connection terminated immediately on connect

- Missing or malformed `Authorization: Bearer <jwt>` header on the WebSocket upgrade request
- JWT header does not specify `alg: HS512` (some libraries default to HS256)
- Secret key too short for HS512 in your JWT library (C# `IDX10720`: minimum 64 bytes)

### Authorize Response `IsAuthorized: false`

```json
{
    "ResponseType": 9,
    "ResponseData": {
        "IsAuthorized": false,
        "ErrorMessage": "API user not registered with the system | Grp=[...], User=[...]"
    }
}
```

Read `ErrorMessage` for details. The server still returns a Type 9 on failure — do not proceed to subscribe or trade if `IsAuthorized` is `false`.

---

## Server Error Message Types

### Generic Error (Type 3)

Critical error resulting from a request or system issue.

```json
{
    "ResponseType": 3,
    "ResponseData": "Ran into an issue"
}
```

### Not Entitled Error (Type 21)

Your API key does not have entitlements for the requested data or action.

```json
{
    "ResponseType": 21,
    "ResponseData": {
        "ErrorMessage": "Ran into an issue because user is not entitled",
        "Symbol": "ESZ5"
    }
}
```

Common causes: market data for an exchange you're not entitled to, options data without the options entitlement, order submission without trading entitlement.

### Security Not Found (Type 23)

Symbol was not found — the contract has likely expired or the symbol is malformed.

```json
{
    "ResponseType": 23,
    "ResponseData": {
        "ErrorMessage": "This contract is either expired or your request symbol is malformed",
        "Symbol": "ESZ3"
    }
}
```

**Fix:** Run an Instrument Search (Type 33) to verify the current active contract symbol before subscribing.

---

## Order Errors

### Order Rejected

Rejections arrive as Order Status (Type 8) messages. Check `Text` for the rejection reason:

```json
{
    "ResponseType": 8,
    "ResponseData": {
        "Tag": "ngen01-32122-...",
        "OrderStatus": -1,
        "Text": "Account not authorized for this instrument",
        "LeaveShares": 0.0
    }
}
```

Common rejection reasons:
- Account not valid for the symbol's exchange
- Price/quantity numeric type error (integer instead of float — fix: always use `5.0` not `5`)
- TIF or OrdType not supported for the instrument
- Position limits exceeded

### Numeric Type Errors

If `Quantity` or `Price` are sent as integers, the server will throw an exception. Always ensure these are serialized as floating-point in your JSON payload:

```json
// WRONG
{ "Quantity": 5, "Price": 5500 }

// CORRECT
{ "Quantity": 5.0, "Price": 5500.25 }
```

---

## Market Data Errors

### Subscription Failure (Type 0 response)

```json
{
    "ResponseType": 0,
    "ResponseData": {
        "SubscriptionResults": [
            {
                "Success": false,
                "Username": "rival_123",
                "GenericMarketDataSymbol": "ESZ3",
                "Message": "Symbol not found",
                "ExceptionError": ""
            }
        ]
    }
}
```

Always check `SubscriptionResults[n].Success` before assuming market data will arrive.

---

## Diagnostics Checklist

1. **Auth fails:** Confirm `group`, `user`, `apikey` values with Rival. Check for extra whitespace. Verify `alg: HS512` in JWT header.
2. **Connection drops immediately:** Verify Bearer token header is present on WebSocket upgrade. Test with `wscat` or equivalent.
3. **No market data after subscribe:** Check Type 0 response `SubscriptionResults[0].Success`. Check for Type 21 (not entitled). Verify symbol using Instrument Search (Type 33) first.
4. **Order rejected:** Read `Text` field in Type 8 response. Verify float types on `Quantity` and `Price`. Confirm `Account` is in your Accounts list (Type 15 response after login).
5. **Disconnected after ~5 min idle:** Heartbeat Ping (Type 26) must be sent at least every 5 minutes.

---

## Contact

For API issues: `rivalapisupport@rivalsystems.com`

## See also

- [auth-basics.md](auth-basics.md) — JWT construction
- [connection.md](connection.md) — connect flow
- [orders.md](orders.md) — order field requirements
