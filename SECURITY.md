# Security

## Reporting vulnerabilities

If you believe you have found a security issue in **this repository** (skills, catalog markdown, or supporting docs), report it through the channel your Rival One account team or support portal provides for security-sensitive issues.

Do not open a public GitHub issue for undisclosed vulnerabilities.

## Secrets

- **All `RIVAL_ONE_*` variables are secrets** — including `RIVAL_ONE_GROUP` and `RIVAL_ONE_USER` (they are JWT claims tied to your Rival One registration). If you use optional firm scoping, `RIVAL_ONE_FIRM` is likewise sensitive. Never commit API tokens, passwords, HMAC secrets, group names, usernames, or private URLs. Use environment variables in **your application** as documented in [`.env.example`](.env.example). Authentication uses an **HS512 JWT**: either **`RIVAL_ONE_API_TOKEN`** (full JWT) or **`RIVAL_ONE_API_KEY`** + **`RIVAL_ONE_SECRET_KEY`** + **`RIVAL_ONE_GROUP`** + **`RIVAL_ONE_USER`** to build the JWT locally (see [Client Requests](https://rivalsystems.getoutline.com/s/3a1c668b-79be-48b3-83a1-859ecf82a4d0/doc/client-requests-OKFTPUQJ6w)).
- Add `.env` to local ignore rules (included in [`.gitignore`](.gitignore)); verify with `git status` before pushing.

## Scope

This project is **documentation and agent guidance** for integrating with the Rival One WebSocket API. Token handling, transport security, and API behavior are governed by Rival One’s platform and your agreement with them. Confirm message types and fields against **official Rival One API documentation** for production use.
