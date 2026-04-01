# Bundle: connection — Connect, Authorize, Heartbeat

> **Source:** [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) · [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)

## Endpoints

| Environment | URL |
|-------------|-----|
| **Simulation** | `wss://sim-api.rivalsystems.cloud:50443` |
| **Production** | `wss://prod-api.rivalsystems.cloud:60443` |

## Connection Requirements

- **Bearer token required on connect** — include the JWT as `Authorization: Bearer <jwt>` in the WebSocket upgrade headers. Connections without this header are terminated immediately.
- **Heartbeat required** — send a Ping (Type 26) at least every **5 minutes** or the server will disconnect you. A 240-second interval is a safe default.
- **One WebSocket for everything** — market data and orders share the same connection. Do not open separate sockets per feature. See [../references/protocol.md](../references/protocol.md).
- **All field names and values are case-sensitive** unless the docs explicitly note otherwise.
- **All prices and quantities are floating-point.** Using integer/long parsing will cause server-side exceptions.

## Connection + Auth Flow

```
1. Build JWT  (see auth-basics.md)
2. Open WSS   with header: Authorization: Bearer <jwt>
3. Send       { "RequestType": 45, "RequestData": "<jwt>" }
4. Receive    Type 9  (Authorize response — IsAuthorized: true/false)
              Type 13 (User settings — auto-pushed on success)
              Type 14 (Trade settings — auto-pushed on success)
              Type 15 (Accounts — auto-pushed on success)
              Type 38 (Broker routes — auto-pushed on success)
5. Start      heartbeat loop: Ping (Type 26) every 240 s
```

## Ping / Pong (Type 26)

Send to keep the connection alive. The optional `RequestData` is a request ID reflected back in the pong — useful for latency measurement.

```json
{ "RequestType": 26, "RequestData": "123456789" }
```

Pong response:
```json
{ "ResponseType": 26, "ResponseData": "123456789" }
```

## Python Example

```python
import asyncio
import os
import jwt
import websockets

async def connect():
    token = build_jwt(
        api_key=os.environ["RIVAL_ONE_API_KEY"],
        secret_key=os.environ["RIVAL_ONE_SECRET_KEY"],
        group=os.environ["RIVAL_ONE_GROUP"],
        user=os.environ["RIVAL_ONE_USER"],
    )
    url = os.environ.get("RIVAL_ONE_WSS_URL", "wss://sim-api.rivalsystems.cloud:50443")
    headers = {"Authorization": f"Bearer {token}"}

    async with websockets.connect(url, additional_headers=headers) as ws:
        # Authorize
        await ws.send(json.dumps({"RequestType": 45, "RequestData": token}))

        # Heartbeat task
        async def heartbeat():
            while True:
                await asyncio.sleep(240)
                await ws.send(json.dumps({"RequestType": 26, "RequestData": "hb"}))

        asyncio.create_task(heartbeat())

        # Receive loop
        async for raw in ws:
            msg = json.loads(raw)
            await handle(msg)
```

## TypeScript / Node Example

```typescript
import WebSocket from "ws";

async function connect(token: string, url: string) {
  const ws = new WebSocket(url, {
    headers: { Authorization: `Bearer ${token}` },
  });

  ws.on("open", () => {
    // Authorize
    ws.send(JSON.stringify({ RequestType: 45, RequestData: token }));

    // Heartbeat
    setInterval(() => {
      ws.send(JSON.stringify({ RequestType: 26, RequestData: Date.now() }));
    }, 240_000);
  });

  ws.on("message", (data) => {
    const msg = JSON.parse(data.toString());
    handle(msg);
  });
}
```

## C# Example

```csharp
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

var token = BuildJwt(apiKey, secretKey, group, user);
var uri = new Uri("wss://sim-api.rivalsystems.cloud:50443");

using var ws = new ClientWebSocket();
ws.Options.SetRequestHeader("Authorization", $"Bearer {token}");
await ws.ConnectAsync(uri, CancellationToken.None);

// Authorize
await SendAsync(ws, new { RequestType = 45, RequestData = token });

// Heartbeat
_ = Task.Run(async () => {
    while (ws.State == WebSocketState.Open) {
        await Task.Delay(240_000);
        await SendAsync(ws, new { RequestType = 26, RequestData = DateTimeOffset.UtcNow.ToUnixTimeSeconds() });
    }
});

// Receive loop
var buffer = new byte[65536];
while (ws.State == WebSocketState.Open) {
    var result = await ws.ReceiveAsync(buffer, CancellationToken.None);
    var json = Encoding.UTF8.GetString(buffer, 0, result.Count);
    Handle(JsonSerializer.Deserialize<JsonElement>(json));
}
```

## TLS Trust and Corporate SSL Inspection

If `wss://` fails with certificate or issuer errors on your network, your organization may be performing TLS inspection. Options:

- **Python (websockets/aiohttp):** pass `ssl=ctx` where `ctx` is an `ssl.SSLContext` loaded with your corp CA bundle via `ctx.load_verify_locations(cafile="/path/to/corp-ca.pem")`
- **Node.js:** set `ca` in the WebSocket options or set `NODE_EXTRA_CA_CERTS=/path/to/corp-ca.pem`
- **C#:** install the corp CA into the Windows/system certificate store, or pass a custom `HttpClientHandler` with `ServerCertificateCustomValidationCallback`

## See also

- [auth-basics.md](auth-basics.md) — JWT construction
- [../references/protocol.md](../references/protocol.md) — message envelope + one-socket rule
- [errors-troubleshooting.md](errors-troubleshooting.md) — connection failures
