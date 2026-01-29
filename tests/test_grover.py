import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "exercices"))

from grover import (
    grover,
    grover_oracle,
    grover_oracle_1,
    grover_oracle_2,
    grover_oracle_3,
    grover_oracle_4,
    grover_oracle_5,
)


@pytest.fixture
def grover_func():
    return grover


def test_grover_oracle_majority_111(grover_func):
    counts = grover_func(3, grover_oracle)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p111 = counts.get("111", 0) / total
    assert p111 > 0.5, f"expected majority '111', got {p111:.2f}"


def test_grover_oracle_1_majority_01(grover_func):
    counts = grover_func(2, grover_oracle_1)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p01 = counts.get("01", 0) / total
    assert p01 > 0.5, f"expected majority '01', got {p01:.2f}"


def test_grover_oracle_2_majority_111(grover_func):
    counts = grover_func(3, grover_oracle_2)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p111 = counts.get("111", 0) / total
    assert p111 > 0.5, f"expected majority '111', got {p111:.2f}"


def test_grover_oracle_3_majority_110(grover_func):
    counts = grover_func(3, grover_oracle_3)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p110 = counts.get("110", 0) / total
    assert p110 > 0.5, f"expected majority '110', got {p110:.2f}"


def test_grover_oracle_4_majority_1111(grover_func):
    counts = grover_func(4, grover_oracle_4)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p1111 = counts.get("1111", 0) / total
    assert p1111 > 0.5, f"expected majority '1111', got {p1111:.2f}"


def test_grover_oracle_5_majority_01111_and_11111(grover_func):
    counts = grover_func(5, grover_oracle_5)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    assert total > 0
    p01111 = counts.get("01111", 0) / total
    p11111 = counts.get("11111", 0) / total
    assert p01111 + p11111 > 0.5, (
        f"expected majority '01111' and '11111', got {p01111 + p11111:.2f}"
    )
