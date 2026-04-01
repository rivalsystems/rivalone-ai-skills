# Bundle: errors-troubleshooting

## TLS connected but “not really” logged in

The WebSocket **TLS handshake can succeed** even when credentials are wrong or the user is not registered. Always treat **authorize / login responses** from the server as the source of truth, not merely “socket is open.”

## TLS certificate verification failed (`unable to get issuer certificate`)

If connect fails with **certificate verify failed**, **unable to get issuer certificate**, or similar, the server chain often looks invalid to your process because **SSL inspection** replaced the public chain with one signed by a **corporate CA**.

- **Fix:** Trust that CA—install it into the OS/runtime store your app uses, or point your TLS/WebSocket client at a **custom CA bundle** (implementation-specific; see your language’s TLS and WebSocket docs).
- **Do not** rely on disabling verification for production; use it only if IT explicitly allows short-lived diagnostics.

Details and vendor reference: [connection.md — TLS trust and corporate SSL inspection](connection.md#tls-trust-and-corporate-ssl-inspection) · [Outline — Python example](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/python-example-qlh5BEqaQV) (illustrative optional settings).

## Group / user mismatch

Message like `API user not registered with the system | Grp=[...], User=[...]` usually means JWT **`group`** or **`user`** claims do not match what Rival has on file (typo, wrong environment, or stale copy-paste).

- Compare values to the portal / onboarding exactly (including punctuation).
- See [Overview — Common Errors](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/overview-MeKFxBVURU) and [docs/troubleshooting.md](../../docs/troubleshooting.md).

## .NET HS512 secret length

If JWT signing fails with **`IDX10720`**, the HMAC key is shorter than the library minimum for HS512. Use a longer secret (≥ 64 bytes) or confirm algorithm requirements with your security standards.

## Numeric JSON

If orders fail with server exceptions, verify **`Quantity`** and **`Price`** are serialized as JSON **numbers**, not quoted strings.

## `GroupName` in payloads

If you or the model adds **`GroupName`** to outgoing JSON, **remove it** unless the vendor doc explicitly requires it for a specific request. Default stance: **do not set** — see [rival-one-core.md](../rival-one-core.md).

## Where to read next

- [Rival WebSocket API](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/rival-websocket-api-kFEIQKQvp0)
- [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)
- [../references/protocol.md](../references/protocol.md)
- [auth-basics.md](auth-basics.md) · [connection.md](connection.md)
