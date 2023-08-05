# -*- coding: utf-8 -*-

"""Top-level package for Fourier-filtered Relative Entropy Minimization."""

__author__ = """Carl Simon Adorf"""
__email__ = 'csadorf@umich.edu'
__version__ = '0.1.0'

__all__ = ['FFREM', 'calc_rdf']

from .ffrem import FFREM
from .util import calc_rdf
