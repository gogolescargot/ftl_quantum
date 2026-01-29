import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "exercices"))

from noise import noise


@pytest.fixture
def noise_func():
    return noise


def test_noise_has_errors_in_01_10(noise_func):
    counts = noise_func()
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    assert counts.get("01", 0) + counts.get("10", 0) > 0, (
        "expected some errors in '01' and '10'"
    )


# ...existing code...
