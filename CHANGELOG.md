# Changelog

## v0.7.2 (May 2024)

### Fixes

- Fix race condition for concurrent requests using the `protected` decorator.

### Additions

- The `Client` can now be used as an async context manager which starts
  and closes the client automatically.

### Changes

- The `InvalidKeyHandlerT` and `ExcHandlerT` types no longer include `Optional`,
  and instead are wrapped in `Optional` in the function signature.

---

## v0.7.1 (Feb 2024)

### Fixes

- Fix invalid docs link.

---

## v0.7.0 (Feb 2024)

### Additions

- Add `protected` decorator for verifying keys easily in web frameworks.

### Changes

- `Client` constructor parameter `api_key` is now optional.

---

## v0.6.1 (Dec 2023)

### Changes

- Inner return type of `KeyService.update_remaining` is now correctly
  `Optional`.

---

## v0.6.0 (Dec 2023)

### Additions

- Add `Refill`, `RefillInterval`, and `UpdateOp` models/enums.
- Add `id` property onto `ApiKeyVerification`.
- Add `refill` property onto `ApiKeyMeta` and `ApiKeyVerification`.
- Add serialization methods for new properties and models.
- Add support for `refill` when creating and updating a key.
- Add `update_remaining` method to `KeyService` and corresponding `Route`.

---

## v0.5.0 (Dec 2023)

### Breaking Changes

- `verify_key` now requires an `api_id` parameter.
- `list_keys` no longer accepts the `offset` parameter.

### Additions

- Add `Conflict` variant to `ErrorCode`.
- Add `get_key` method to `KeyService`.
- Add `cursor` parameter to `list_keys`.

### Bugfixes

- Fix invalid default used when ratelimit was not passed in `create_key`.

### Changes

- Refactor internal routes to use new API endpoints.

---

## v0.4.3 (Sep 2023)

### Additions

- Add `NotUnique` and `InvalidKeyType` variants to `ErrorCode`.

### Changes

- Rename `UsageExceeded` error code to `KeyUsageExceeded`.

---

## v0.4.2 (Aug 2023)

### Additions

- Add `RatelimitState` model.
- Add `ratelimit` and `expires` fields to `ApiKeyVerification`.

---

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
