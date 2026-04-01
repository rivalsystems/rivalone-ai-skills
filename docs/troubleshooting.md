# Rival WebSocket API — troubleshooting

Official references (read these alongside this repo):

- **[Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)** — Outline index (Overview, Client Requests, Server Responses, …).
- **[Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU)** — connection flow, endpoints, heartbeat, message-type reference, **common errors**.
- **[Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)** — JSON envelope (`RequestType` / `RequestData`), **JWT (HS512)** for Authorize.

## Endpoints (from Overview)

| Environment | Host (TLS) |
|-------------|------------|
| Simulation | `sim-api.rivalsystems.cloud:50443` |
| Production | `prod-api.rivalsystems.cloud:60443` |

Set `RIVAL_ONE_WSS_URL` to `wss://<host>:<port>` for the environment you use.

## TLS errors behind corporate SSL inspection

If you see messages like **`certificate verify failed`** or **`unable to get issuer certificate`** when opening `wss://`, your network may be **inspecting TLS** and presenting a certificate signed by an **internal CA** your runtime does not trust yet.

1. Obtain the **corporate root/intermediate CA** from IT (or export from your browser after trusting the proxy chain, if policy allows).
2. **Add it to the trust store** your application uses (OS-level, language runtime, or explicit CA path in your WebSocket/TLS client—see your stack’s documentation).
3. Avoid **disabling TLS verification** except for tightly controlled diagnostics; Rival’s docs describe that option as **not recommended for production**. The [Python example](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/python-example-qlh5BEqaQV) on Outline shows optional `ca_cert_file` / `disable_ssl_verification` style settings as a reference pattern.

Language-neutral guidance in this repo: [`skills/catalog/connection.md`](../skills/catalog/connection.md) (TLS trust section) and [`skills/catalog/errors-troubleshooting.md`](../skills/catalog/errors-troubleshooting.md).

## JWT claims: `group`, `user`, and optional `firm`

The Authorize JWT payload must include Rival-assigned **`group`** and **`user`** claims (see Client Requests). In this repository:

| JWT claim | Environment variables |
|-----------|------------------------|
| `group` | `RIVAL_ONE_GROUP` (must match the trading group Rival registered for your API user) |
| `user` | `RIVAL_ONE_USER` **or** `RIVAL_ONE_USERNAME` (same claim; use whichever matches your portal / docs naming) |
| `firm` (optional) | `RIVAL_ONE_FIRM` — only if Rival instructed you to include firm scoping in the login JWT |

If `RIVAL_ONE_USER` is empty, **`RIVAL_ONE_USERNAME`** is used so values like portal `username` map cleanly to the JWT `user` claim.

## Common errors (from Overview)

When logging in, you may see:

```text
API user not registered with the system | Grp=[SOMETHING.JSMITH], User=[jsmith]
```

The [Overview](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) states this **typically indicates an issue with your login credentials, most likely with the group name** you are passing. Verify:

1. **`RIVAL_ONE_GROUP`** exactly matches the **Rival-assigned** group string (case-sensitive unless noted otherwise in vendor docs).
2. **`RIVAL_ONE_USER`** / **`RIVAL_ONE_USERNAME`** matches the **Rival-assigned** API user name for that group.
3. **`RIVAL_ONE_API_KEY`** and **`RIVAL_ONE_SECRET_KEY`** belong to that same API user / entitlement set.

`GroupName` in other messages is **server-assigned** and must not be set by clients (see Overview — User Setup).

## Heartbeat

Send **Ping** (`RequestType` **26**) at least every **5 minutes** to avoid disconnection (examples in [`skills/catalog/connection.md`](../skills/catalog/connection.md) often use **240** seconds). See Overview — Connection Requirements.

## Support

For API questions, the Overview lists: `rivalapisupport@rivalsystems.com`.
