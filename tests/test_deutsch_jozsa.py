import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "exercices"))

from deutsch_jozsa import (
    deutsch_jozsa,
    oracle_constant,
    oracle_balanced,
    oracle_constant_random,
    oracle_balanced_random,
)


@pytest.fixture
def deutsch_jozsa_func():
    return deutsch_jozsa


def test_deutsch_jozsa_oracle_constant(deutsch_jozsa_func):
    counts = deutsch_jozsa_func(oracle_constant)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    p000 = counts.get("000", 0) / 1
    assert p000 == total, "expected all outputs to be zero for constant oracle"


def test_deutsch_jozsa_oracle_balanced(deutsch_jozsa_func):
    counts = deutsch_jozsa_func(oracle_balanced)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    p111 = counts.get("111", 0)
    assert p111 == total, "expected all outputs to be one for balanced oracle"


def test_deutsch_jozsa_oracle_constant_random(deutsch_jozsa_func):
    counts = deutsch_jozsa_func(oracle_constant_random)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    p000 = counts.get("000", 0)
    assert p000 == total, "expected all outputs to be zero for constant oracle"


def test_deutsch_jozsa_oracle_balanced_random(deutsch_jozsa_func):
    counts = deutsch_jozsa_func(oracle_balanced_random)
    assert counts, "no counts returned"
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    p111 = counts.get("111", 0)
    assert p111 == total, "expected all outputs to be one for balanced oracle"
