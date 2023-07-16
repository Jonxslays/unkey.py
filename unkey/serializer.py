from __future__ import annotations

import typing as t
from datetime import datetime

from unkey import models

__all__ = ("Serializer",)

T = t.TypeVar("T")
DictT = t.Dict[str, t.Any]
TransformT = t.Optional[t.Callable[[t.Any], t.Any]]


class Serializer:
    """Deserializes JSON data into wom.py model classes."""

    __slots__ = ()

    def _dt_from_iso(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.rstrip("Z"))

    def _dt_from_iso_maybe(self, timestamp: t.Optional[str]) -> t.Optional[datetime]:
        return self._dt_from_iso(timestamp) if timestamp else None

    def to_camel_case(self, attr: str) -> str:
        first, *rest = attr.split("_")
        return "".join((first.lower(), *map(str.title, rest)))

    def _set_attrs(
        self,
        model: t.Any,
        data: DictT,
        *attrs: str,
        transform: TransformT = None,
        camel_case: bool = False,
        maybe: bool = False,
    ) -> None:
        if transform and maybe:
            raise RuntimeError("Only one of 'maybe' and 'transform' may be used.")

        for attr in attrs:
            cased_attr = self.to_camel_case(attr) if camel_case else attr

            if transform:
                setattr(
                    model,
                    attr,
                    transform(data.get(cased_attr, None) if maybe else data[cased_attr]),
                )
            else:
                setattr(model, attr, data.get(cased_attr, None) if maybe else data[cased_attr])

    def _set_attrs_cased(
        self,
        model: t.Any,
        data: DictT,
        *attrs: str,
        transform: TransformT = None,
        maybe: bool = False,
    ) -> None:
        self._set_attrs(model, data, *attrs, transform=transform, camel_case=True, maybe=maybe)

    def to_api_key(self, data: DictT) -> models.ApiKey:
        model = models.ApiKey()
        self._set_attrs_cased(model, data, "key", "key_id")
        return model

    def to_api_key_verification(self, data: DictT) -> models.ApiKeyVerification:
        model = models.ApiKeyVerification()
        model.code = models.ErrorCode.from_str_maybe(data.get("code", ""))
        self._set_attrs_cased(
            model, data, "valid", "owner_id", "meta", "remaining", "error", maybe=True
        )

        return model

    def to_api(self, data: DictT) -> models.Api:
        model = models.Api()
        self._set_attrs_cased(model, data, "id", "name", "workspace_id")
        return model

    def to_ratelimit(self, data: DictT) -> models.Ratelimit:
        return models.Ratelimit(
            limit=data["limit"],
            refill_rate=data["refillRate"],
            refill_interval=data["refillInterval"],
            type=models.RatelimitType.from_str(data["type"]),
        )

    def to_api_key_meta(self, data: DictT) -> models.ApiKeyMeta:
        model = models.ApiKeyMeta()
        ratelimit = data.get("ratelimit")
        model.ratelimit = self.to_ratelimit(ratelimit) if ratelimit else ratelimit
        self._set_attrs_cased(
            model,
            data,
            "id",
            "meta",
            "start",
            "api_id",
            "expires",
            "remaining",
            "owner_id",
            "created_at",
            "workspace_id",
            maybe=True,
        )

        return model

    def to_api_key_list(self, data: DictT) -> models.ApiKeyList:
        model = models.ApiKeyList()
        model.total = data["total"]
        model.keys = [self.to_api_key_meta(key) for key in data["keys"]]
        return model
