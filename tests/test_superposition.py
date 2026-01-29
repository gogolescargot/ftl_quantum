import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "exercices"))

from superposition import superposition


@pytest.fixture
def superposition_func():
    return superposition


def test_superposition_approximately_half(superposition_func):
    counts = superposition_func()
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p0 = counts.get("0", 0) / total
    p1 = counts.get("1", 0) / total
    assert 0.4 <= p0 <= 0.6 and 0.4 <= p1 <= 0.6, (
        f"expected approximately half '0' and half '1', got p0={p0:.2f}, p1={p1:.2f}"
    )
