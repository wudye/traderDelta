import os
from pathlib import Path

_version_file = Path(__file__).parent.parent / "VERSION"
if _version_file.exists():
    __version__ = _version_file.read_text().strip()
else:
    __version__ = "0.1.0"


__author__ = "mwu"
__email__ = "<EMAIL>"


from . import core
from . import data
from . import strategy
from . import backtest
from . import indicators
from . import trader
from . import live
from .te import this_test
__all__ = [
    "core",
    "data",
    "strategy",
    "backtest",
    "indicators",
    "trader",
    "live",
    "this_test"
]

