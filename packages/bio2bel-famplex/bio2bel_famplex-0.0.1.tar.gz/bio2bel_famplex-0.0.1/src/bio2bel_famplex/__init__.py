# -*- coding: utf-8 -*-

"""Bio2BEL FamPlex.

This repository contains utilities for downloading, parsing, and serializing
`FamPlex <http://github.com/sorgerlab/famplex>`_ to BEL.
"""

from .constants import get_version
from .manager import Manager
from .relations import *
