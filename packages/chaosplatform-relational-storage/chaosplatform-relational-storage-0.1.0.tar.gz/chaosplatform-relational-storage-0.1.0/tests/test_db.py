from typing import Any, Dict

from chaosplt_relational_storage.db import get_engine


def test_get_engine(config: Dict[str, Any]):
    engine = get_engine(config)
    assert engine is not None


def test_get_engine_returns_same(config: Dict[str, Any]):
    engine = get_engine(config)
    assert engine is not None

    engine2 = get_engine(config)
    assert engine2 is engine
