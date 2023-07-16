from __future__ import annotations

from unkey import BaseModel
from unkey import Ratelimit
from unkey import RatelimitType


def test_base_to_dict() -> None:
    assert BaseModel().to_dict() == {}


def test_ratelimit() -> None:
    model = Ratelimit(
        RatelimitType.Fast,
        limit=10,
        refill_rate=9,
        refill_interval=1000,
    )

    assert model.limit == 10
    assert model.refill_rate == 9
    assert model.refill_interval == 1000
    assert model.type == RatelimitType.Fast
    assert model.to_dict() == {
        "limit": 10,
        "refill_rate": 9,
        "refill_interval": 1000,
        "type": RatelimitType.Fast,
    }
