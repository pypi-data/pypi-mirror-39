from typing import Any, Dict

import pytest


@pytest.fixture
def config() -> Dict[str, Any]:
    return {
        "db": {
            "uri": "sqlite:///:memory:",
            "debug": True
        }
    }