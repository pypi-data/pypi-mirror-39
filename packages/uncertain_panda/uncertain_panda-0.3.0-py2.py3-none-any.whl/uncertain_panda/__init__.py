"""Pandas with uncertainties"""
__version__ = "0.3.0"

from .utils.pandas_utils import add_uncertainty_accessors
add_uncertainty_accessors()

from .uncertainties.calculation import UncertaintyMode
from .uncertainties.bootstrap_result import BootstrapResult

import pandas
