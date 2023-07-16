# Changelog

## v0.3.0 (Jul 2023)

### Bugfixes

- Remove debug print statement in `list_keys`.

### Additions

- Add `ErrorCode` enum.
- Add `remaining` parameter to `create_key`.
- Add `remaining` field to `ApiKeyVerification` and `ApiKeyMeta` models.
- Add `code` field to `ApiKeyVerification` model.
- Add `code` field to `HttpResponse` model.

### Changes

- Update status code for `revoke_key` to 200 OK.

---

## v0.2.0 (Jun 2023)

### Additions

- Add `Client`, `KeyService` and `ApiService`.
- Add `Serializer`, and other necessary base services.
- Add relevant models.
- Add support for all publicly documented endpoints:
  - Get API
  - List Keys
  - Create Key
  - Verify Key
  - Revoke Key

---

## v0.1.0 (Jun 2023)

- Initial release!