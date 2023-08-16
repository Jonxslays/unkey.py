# Changelog

## v0.4.1 (Aug 2023) 

### Changes

- `UNDEFINED` is now guaranteed to be a singleton, preventing `id(obj)` mismatches.

### Bugfixes

- `Client.start()` now correctly initializes a new client session if called
  after closing the client previously.

### Additions

- Tests :).

---

## v0.4.0 (Jul 2023)

### Additions

- Add `UNDEFINED`, `UndefinedOr`, and `UndefinedNoneOr` types.
- Add `update_key` method to key service.
- Add `name` parameter to the `create_key` method.

### Changes

- Refactor existing methods to use the new `UNDEFINED` type.

---

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
