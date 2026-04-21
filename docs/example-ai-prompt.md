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
Build me a minimal [Python / TypeScript / C# — pick one] application for Rival One WebSocket API integration.

## Requirements

1. **Configuration from environment variables** (no secrets in source code)
   - Create a `.env.example` template with these placeholder variable names:
     - RIVAL_ONE_API_KEY=your_api_key_here
     - RIVAL_ONE_SECRET_KEY=your_secret_key_here
     - RIVAL_ONE_GROUP=HUNTER
     - RIVAL_ONE_USER=jdoe
     - RIVAL_ONE_JWT_SUB=Rival-Websocket-API-Client
     - RIVAL_ONE_DISPLAY_NAME=John Doe
     - RIVAL_ONE_WSS_URL=wss://sim-api.rivalsystems.cloud:50443
     - RIVAL_ONE_FIRM=#Only use if Rival JSON contained a firm field.
   - Load from a `.env` file (gitignored) at runtime using your language's standard dotenv library/package
   - Include a config module that validates all required variables are present
   - Do not hardcode secrets in source files or README

2. **HS512 JWT authentication**
   - Build a JWT with claims: sub, group, user, apikey, [firm if present]
   - Sign with RIVAL_ONE_SECRET_KEY using HS512 algorithm
   - Use your language's standard JWT library

3. **WebSocket connection with Authorization header**
   - Connect to RIVAL_ONE_WSS_URL
   - Include Authorization header: "Bearer <jwt>"
   - Use your language's native WebSocket library

4. **Authorize handshake**
   - After connect, send RequestType 45 (Authorize)
   - Set RequestData equal to the JWT string itself

5. **Heartbeat loop**
   - Send Ping (RequestType 26) every 240 seconds
   - Run as a background task

6. **Single WebSocket for all traffic**
   - One connection for all market data and order traffic
   - One receive loop that demuxes and logs all incoming JSON messages
   - Serialize all sends (no concurrent writes to the socket)
   - Log all incoming messages as formatted JSON to stdout with clear arrows (→ sent, ← received)

7. **Clean shutdown**
   - Handle graceful shutdown on Ctrl+C / SIGINT
   - Cancel background tasks
   - Close WebSocket cleanly

8. **Logging**
   - Use your language's standard logging library
   - Include timestamps
   - Log connection state, Ping sends, and all incoming/outgoing messages

## Structure

- `config.[ext]` — environment loading and validation (returns validated config object)
- `rival_one_client.[ext]` — main client class with async/await or equivalent
- `.env.example` — template for users to copy to `.env` and fill with their credentials
- `.gitignore` — ignore .env, build artifacts, dependencies, OS files
- `requirements.txt` / `package.json` / `*.csproj` — dependency manifest
- `README.md` — instructions to create `.env` from their Rival credential JSON using the env var mapping above

Use your language's native async/await patterns (or equivalent). Include docstrings/comments. Keep code minimal but readable.

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

- [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)
- **`name`:** Include in the JWT only if required by the vendor; otherwise your app can use it for logging or UI only.
- **After it runs:** Extend with instrument search (33) and market data (0) using [`skills/catalog/market-data.md`](../skills/catalog/market-data.md), or orders using [`skills/catalog/orders.md`](../skills/catalog/orders.md).

## Related

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [README — Environment variables](../README.md#environment-variables-your-app)
- [`skills/catalog/auth-basics.md`](../skills/catalog/auth-basics.md)
- [`docs/troubleshooting.md`](troubleshooting.md)


## Disclaimer
The AI Agent Skill Repository is provided to assist with connectivity and authentication to the Rival One WebSocket API. Rival Systems is responsible solely for ensuring proper API connectivity and login functionality. Any applications, tools, or solutions built using this repository , including those generated through AI-assisted or automated coding methods are the sole responsibility of the developer or end user. Rival Systems makes no warranties and assumes no liability for the functionality, accuracy, or performance of third-party applications built on top of this repository.
