from . import processing, plotting
from .io import api as io
from .processing import diagnostics, conversions
from .plotting import plot
from .io.api import open_product, save_product, select, info, report

__all__ = [
    # modules
    "api",
    "io",
    "processing",
    "plotting",
    # core functions
    "open_product",
    "save_product",
    "info",
    "select",
    "conversions",
    "diagnostics",
    "plot",
    "report",
]
