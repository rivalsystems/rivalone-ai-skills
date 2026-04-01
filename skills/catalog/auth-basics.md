# Bundle: auth-basics — JWT (HS512)

> **Source:** [Client Requests — Authorize (Type 45)](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)

Rival One uses the **same JWT string** for two things:

1. The WebSocket handshake connection header: `Authorization: Bearer <JWT>`
2. The first application message after connect: `{ "RequestType": 45, "RequestData": "<JWT>" }`

> **WARNING:** You must pass the bearer token in the connection header. Connections without this will be terminated.

Algorithm: **HS512**. Header must specify `alg: HS512`, `typ: JWT`.

## JWT Header

```json
{
  "alg": "HS512",
  "typ": "JWT"
}
```

## JWT Payload Claims

| Claim | Required | Description |
|-------|----------|-------------|
| `sub` | No | Subject identifier (e.g. `"Rival API user Authentication"`) |
| `group` | **Yes** | Rival-assigned trading group — must match registration exactly |
| `user` | **Yes** | Rival-assigned API user — must match registration exactly |
| `apikey` | **Yes** | Your Rival API key |
| `firm` | No | **Optional.** Include only when Rival instructs you to send firm scoping (maps to `RIVAL_ONE_FIRM`). |

> **Secrets:** Treat all `RIVAL_ONE_*` env vars as confidential. Never commit them to source control. `group` and `user` are still sensitive identifiers even without the secret.

## Authorize Request (Type 45) — After Connect

Send immediately after the WebSocket connection is established. `RequestData` is the full JWT string (identical to the Bearer token):

```json
{
    "RequestType": 45,
    "RequestData": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9..."
}
```

## Authorize Response (Type 9) — Success

On successful authorization, the server sends a Type 9 response **and automatically pushes**:
- User settings (Type 13)
- Trade settings (Type 14)  
- Accounts (Type 15)
- Broker routes (Type 38)

```json
{
    "ResponseType": 9,
    "ResponseData": {
        "IsAuthorized": true,
        "ErrorMessage": "",
        "Role": "API User"
    }
}
```

On failure, `IsAuthorized` will be `false` and `ErrorMessage` will contain the reason. See [errors-troubleshooting.md](errors-troubleshooting.md) for common auth errors.

## Python (PyJWT)

```python
import jwt

def build_jwt(
    *,
    api_key: str,
    secret_key: str,
    group: str,
    user: str,
    sub: str = "Rival API user Authentication",
    firm: str | None = None,
) -> str:
    payload = {
        "sub": sub,
        "group": group.strip(),
        "user": user.strip(),
        "apikey": api_key.strip(),
    }
    if firm is not None and firm.strip():
        payload["firm"] = firm.strip()
    return jwt.encode(
        payload,
        secret_key.strip(),
        algorithm="HS512",
        headers={"typ": "JWT"},
    )
```

Install: `pip install PyJWT`

## TypeScript / Node (jose)

```typescript
import * as jose from "jose";

export async function buildJwt(params: {
  apiKey: string;
  secretKey: string;
  group: string;
  user: string;
  sub?: string;
  /** Optional — include only when Rival instructs firm scoping */
  firm?: string;
}): Promise<string> {
  const key = new TextEncoder().encode(params.secretKey.trim());
  const body: Record<string, string> = {
    group: params.group.trim(),
    user: params.user.trim(),
    apikey: params.apiKey.trim(),
  };
  if (params.firm?.trim()) {
    body["firm"] = params.firm.trim();
  }
  return await new jose.SignJWT(body)
    .setProtectedHeader({ alg: "HS512", typ: "JWT" })
    .setSubject(params.sub ?? "Rival API user Authentication")
    .sign(key);
}
```

Install: `npm install jose`

## C# (.NET)

`System.IdentityModel.Tokens.Jwt` enforces a **minimum 64-byte secret** for HS512 (`IDX10720` if the secret is too short). Other stacks may only warn.

```csharp
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

static string BuildJwt(
    string apiKey, string secretKey, string group, string user,
    string sub = "Rival API user Authentication", string? firm = null)
{
    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey.Trim()));
    var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha512);
    var claimList = new List<Claim>
    {
        new Claim(JwtRegisteredClaimNames.Sub, sub),
        new Claim("group", group.Trim()),
        new Claim("user", user.Trim()),
        new Claim("apikey", apiKey.Trim()),
    };
    if (!string.IsNullOrWhiteSpace(firm))
        claimList.Add(new Claim("firm", firm.Trim()));
    var token = new JwtSecurityToken(claims: claimList, signingCredentials: creds);
    return new JwtSecurityTokenHandler().WriteToken(token);
}
```

Packages: `System.IdentityModel.Tokens.Jwt`, `Microsoft.IdentityModel.Tokens`

## See also

- [connection.md](connection.md) — using the JWT on the socket + full connect/authorize flow
- [errors-troubleshooting.md](errors-troubleshooting.md) — auth failure messages
- [../references/protocol.md](../references/protocol.md) — envelope format
