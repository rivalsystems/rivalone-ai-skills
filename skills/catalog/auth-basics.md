# Bundle: auth-basics — JWT (HS512)

Rival One uses the **same JWT string** for:

1. The WebSocket handshake: header `Authorization: Bearer <JWT>`
2. The first application message: `{ "RequestType": 45, "RequestData": "<JWT>" }` (authorize; confirm number in [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w))

Algorithm: **HS512**. Header typically includes `alg: HS512`, `typ: JWT`.

## Claims (typical)

| Claim | Meaning |
|-------|---------|
| `sub` | Subject (often a fixed string from the vendor doc) |
| `group` | Rival-assigned trading group — must match registration |
| `user` | Rival-assigned API user — must match registration |
| `apikey` | Your API key |
| `firm` | **Optional.** Rival may ask you to include this login-credentials claim when your entitlement uses firm scoping—omit unless your onboarding or [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w) says to set it. |

Use **either** a pre-built JWT from your portal **or** build it in your app from key + secret + claims.

> **Secrets:** Treat `RIVAL_ONE_*` (or your own env names) as confidential. Never commit them. `group` and `user` are still sensitive identifiers.

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
  /** Optional login claim when Rival instructs you to send firm scoping */
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

`System.IdentityModel.Tokens.Jwt` enforces a **minimum 64-byte secret** for HS512 (`IDX10720` if too short). Other stacks may only warn.

```csharp
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

static string BuildJwt(string apiKey, string secretKey, string group, string user, string sub = "Rival API user Authentication", string? firm = null)
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

Packages: `System.IdentityModel.Tokens.Jwt`, `Microsoft.IdentityModel.Tokens`.

## See also

- [connection.md](connection.md) — use the JWT on the socket
- [../references/protocol.md](../references/protocol.md)
