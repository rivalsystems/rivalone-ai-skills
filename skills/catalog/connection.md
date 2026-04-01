# Bundle: connection — WebSocket and heartbeat

## Steps

1. Build or load the JWT (see [auth-basics.md](auth-basics.md)).
2. Open a **WebSocket** to your environment URL (SIM example: `wss://sim-api.rivalsystems.cloud:50443`).
3. Set request header: `Authorization: Bearer <JWT>`.
4. After `open`, send **Authorize**: `{ "RequestType": 45, "RequestData": "<same JWT string>" }` (confirm `RequestType` in [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)).
5. Start a **timer** to send **Ping** (`RequestType` **26**) every N seconds (often **240**; confirm in [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU)). `RequestData` is often a string id (e.g. UUID).

> TLS succeeding does **not** prove auth. Wait for vendor **authorize response** (e.g. response indicating authorized) before assuming the session is valid.

## TLS trust and corporate SSL inspection

If the client fails **before** the WebSocket upgrade with errors such as **`certificate verify failed`** or **`unable to get issuer certificate`** (exact text depends on OS and TLS stack), the TLS path is often broken by **corporate SSL inspection**: a proxy or gateway terminates TLS and re-encrypts using a certificate signed by an **internal CA** that is not in your runtime’s default trust store.

**Preferred fix (any language):**

1. Get the **root and/or issuing CA** your IT team uses for inspection (usually PEM or a trust bundle they publish).
2. Either **install that CA into the system or runtime trust store** used by your process, **or** configure your WebSocket/TLS client to **load a custom CA file or bundle** when opening `wss://` (the setting name differs by library: trust anchors, `ca_file`, custom `X509Store`, etc.—follow your stack’s docs).

**Avoid in production:** Turning off certificate verification entirely. Rival’s sample Python client documents this only as a last resort; treat it as a temporary diagnostic, not a shipping configuration. For one worked example of optional config keys (`ca_cert_file`, `disable_ssl_verification`), see [Outline — Python example](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/python-example-qlh5BEqaQV).

More symptom-oriented notes: [errors-troubleshooting.md](errors-troubleshooting.md).

## Python (websockets)

Uses `websockets` async client; send authorize immediately after connect.

```python
import asyncio
import json
import uuid
import websockets

async def run(url: str, jwt_token: str, ping_interval: float = 240.0):
    headers = [("Authorization", f"Bearer {jwt_token}")]
    async with websockets.connect(url, additional_headers=headers) as ws:
        await ws.send(json.dumps({"RequestType": 45, "RequestData": jwt_token}))

        async def ping_loop():
            while True:
                await asyncio.sleep(ping_interval)
                await ws.send(json.dumps({"RequestType": 26, "RequestData": str(uuid.uuid4())}))

        ping_task = asyncio.create_task(ping_loop())
        try:
            async for raw in ws:
                msg = json.loads(raw)
                # handle messages
                _ = msg
        finally:
            ping_task.cancel()

# asyncio.run(run(wss_url, token))
```

Install: `pip install websockets`

## TypeScript (ws)

```typescript
import WebSocket from "ws";
import { randomUUID } from "node:crypto";

export function connectRival(url: string, jwtToken: string, pingSeconds = 240): WebSocket {
  const ws = new WebSocket(url, { headers: { Authorization: `Bearer ${jwtToken}` } });
  ws.on("open", () => {
    ws.send(JSON.stringify({ RequestType: 45, RequestData: jwtToken }));
    setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ RequestType: 26, RequestData: randomUUID() }));
      }
    }, Math.max(1000, pingSeconds * 1000));
  });
  return ws;
}
```

Install: `npm install ws`, `@types/ws`

## C# (ClientWebSocket)

```csharp
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

static async Task RunAsync(Uri uri, string jwt, TimeSpan pingInterval, CancellationToken ct)
{
    using var ws = new ClientWebSocket();
    ws.Options.SetRequestHeader("Authorization", $"Bearer {jwt}");
    await ws.ConnectAsync(uri, ct);
    var auth = JsonSerializer.Serialize(new { RequestType = 45, RequestData = jwt });
    await ws.SendAsync(Encoding.UTF8.GetBytes(auth), WebSocketMessageType.Text, true, ct);

    _ = Task.Run(async () =>
    {
        while (!ct.IsCancellationRequested)
        {
            await Task.Delay(pingInterval, ct);
            var ping = JsonSerializer.Serialize(new { RequestType = 26, RequestData = Guid.NewGuid().ToString() });
            await ws.SendAsync(Encoding.UTF8.GetBytes(ping), WebSocketMessageType.Text, true, ct);
        }
    }, ct);

    // receive loop: ReceiveAsync(...)
}
```

## Reconnect guidance

- Back off reconnects; on reconnect, repeat JWT header + authorize + ping loop.
- Do not send trading or market-data messages until the session is authorized per vendor responses.

## See also

- [../references/protocol.md#single-websocket-for-market-data-and-orders](../references/protocol.md#single-websocket-for-market-data-and-orders) — market data and orders on one connection
- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [../references/workflows.md](../references/workflows.md)
- [errors-troubleshooting.md](errors-troubleshooting.md)
