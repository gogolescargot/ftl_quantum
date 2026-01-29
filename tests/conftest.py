import sys
import matplotlib
import matplotlib.pyplot as plt
import builtins
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

matplotlib.use("Agg")

plt.show = lambda *a, **k: None
plt.pause = lambda *a, **k: None

_original_print = builtins.print


def _noop_print(*args, **kwargs):
    pass


def pytest_configure(config):
    builtins.print = _noop_print


def pytest_unconfigure(config):
    builtins.print = _original_print
