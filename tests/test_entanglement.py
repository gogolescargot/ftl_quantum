import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "exercices"))

from entanglement import entanglement


@pytest.fixture
def entanglement_func():
    return entanglement


def test_entanglement_00_11_approximately_half(entanglement_func):
    counts = entanglement_func()
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p00 = counts.get("00", 0) / total
    p11 = counts.get("11", 0) / total
    p01_count = counts.get("01", 0)
    p10_count = counts.get("10", 0)
    assert (
        0.4 <= p00 <= 0.6
        and 0.4 <= p11 <= 0.6
        and p01_count == 0
        and p10_count == 0
    ), (
        f"expected approximately half '00' and half '11' and no '01' or '10', got p00={p00:.2f}, p11={p11:.2f}"
    )
