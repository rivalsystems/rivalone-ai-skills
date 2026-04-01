# Example prompt — bootstrap a Rival One client with AI

**Start here when you want one chat to generate your first client.** Use this when you already have **login credentials** from Rival (API key, HMAC secret, group, user, WebSocket URL). Paste a **sanitized** JSON template into your assistant, then ask it to generate an application that loads configuration from environment variables or a local config file—**never** commit real secrets.

**Official WebSocket API docs (Outline):** [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0). Message-level reference: [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w).

## Credential template (placeholders only)

Replace `${MYRIVALKEY}` and `${MYRIVALSECRET}` with your real values only in a private shell or secret store, not in shared chats or git history.

```json
{
  "logincredentials": {
    "sub": "Rival-Websocket-API-Client",
    "name": "John Doe",
    "group": "HUNTER",
    "user": "jdoe",
    "apikey": "${MYRIVALKEY}"
  },
  "secret": "${MYRIVALSECRET}",
  "server_url": "wss://sim-api.rivalsystems.cloud:50443"
}
```

If Rival asked you to send **firm** scoping on the login JWT, add an optional claim alongside the others:

```json
"firm": "YOUR_FIRM_ID"
```

inside `logincredentials` (and map it to something like `RIVAL_ONE_FIRM` in your app). See [`skills/catalog/auth-basics.md`](../skills/catalog/auth-basics.md).

## Example message to paste into Cursor, Claude, Codex, etc.

Copy everything in the block below into a **new** chat in the project where the **rival-one** skill (or this repo’s `skills/`) is available. Swap the language, features, and placeholder names to match what you want.

```text
I am integrating with the Rival One WebSocket API. Use the rival-one skill / the repo’s skills/catalog guides and the official Client Requests doc for message shapes.

Build me a minimal [Python / TypeScript / C# — pick one] application that:

1. Loads configuration from environment variables (no secrets in source code). **Create a `.env` file** in the project (gitignored) and set `RIVAL_ONE_*` variables using **the values from the JSON I provide below**—map each field explicitly, for example:
   - `logincredentials.apikey` → `RIVAL_ONE_API_KEY`
   - `secret` → `RIVAL_ONE_SECRET_KEY`
   - `logincredentials.group` → `RIVAL_ONE_GROUP`
   - `logincredentials.user` → `RIVAL_ONE_USER`
   - `server_url` → `RIVAL_ONE_WSS_URL`
   - `logincredentials.sub` → `RIVAL_ONE_JWT_SUB` (if present)
   - `logincredentials.name` → `RIVAL_ONE_DISPLAY_NAME` for display/logging only unless Client Requests requires `name` in the JWT (it does not in the Authorize payload table—confirm if your onboarding differs)
   - optional `logincredentials.firm` or top-level firm field → `RIVAL_ONE_FIRM` when I use firm scoping
   Do not paste my real secrets into source files or the README; the app should read from `.env` via the environment (e.g. `python-dotenv` or your stack’s equivalent). JWT payload claims: `sub`, `group`, `user`, `apikey` (and `firm` when applicable)—see Client Requests.

2. Builds an HS512 JWT and opens a WebSocket to server_url with header Authorization: Bearer <jwt>.

3. After connect, sends Authorize (RequestType 45) with RequestData equal to the same JWT string.

4. Starts a heartbeat loop sending Ping (RequestType 26) every 240 seconds (or the interval in skills/references/protocol.md / vendor Overview).

5. Logs incoming JSON messages to stdout so I can verify the session, and shuts down cleanly on Ctrl+C.

6. Uses **one** WebSocket for everything: structure the app so multiple market-data subscriptions and future order traffic share that single connection (one receive loop demuxing messages; serialized sends). Follow skills/references/protocol.md section on one WebSocket for market data and orders.

Here is my credential JSON—use it to **fill `.env`** with the mapped `RIVAL_ONE_*` keys (placeholders here; I will replace with real values locally):

{
  "logincredentials": {
    "sub": "Rival-Websocket-API-Client",
    "name": "John Doe",
    "group": "HUNTER",
    "user": "jdoe",
    "apikey": "${MYRIVALKEY}"
  },
  "secret": "${MYRIVALSECRET}",
  "server_url": "wss://sim-api.rivalsystems.cloud:50443"
}

Also add a short README in the project listing the same `RIVAL_ONE_*` env vars and stating that users should **create `.env` from their Rival credential JSON** using that mapping; reference the repo’s `.env.example` or a `config.template` shipped with the app.
```

## Tips

- **Sub claim:** Your template uses `"sub": "Rival-Websocket-API-Client"`. Some docs use `Rival API user Authentication`. Match whatever Rival gave you or what [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) specifies for your environment.
- **`name`:** Include in the JWT only if required by the vendor; otherwise your app can use it for logging or UI only.
- **After it runs:** Extend with instrument search (33) and market data (0) using [`skills/catalog/market-data.md`](../skills/catalog/market-data.md), or orders using [`skills/catalog/orders.md`](../skills/catalog/orders.md).

## Related

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [README — Environment variables](../README.md#environment-variables-your-app)
- [`skills/catalog/auth-basics.md`](../skills/catalog/auth-basics.md)
- [`docs/troubleshooting.md`](troubleshooting.md)
