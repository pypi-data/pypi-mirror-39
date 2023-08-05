# -*- coding: utf-8 -*-
#
#     Copyright (C) 2018 Kevin De Bruycker and Tim Krappitz
#
#     This file is part of pyMacroMS.
#     pyMacroMS allows for high performance quantification of complex high resolution polymer mass spectra.
#
#     pyMacroMS is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     pyMacroMS is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with pyMacroMS.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import absolute_import
import sys
name = "pymacroms"
version = '0.2.0'

if not hasattr(sys, "version_info") or sys.version_info < (3, 4):
    raise RuntimeError("pymacroms requires Python 3.4 or later.")

from . import database
from .single_molecule import Molecule
from .polymer import Polymer
from .spectrum_processing import Spectrum
from .helper_functions import *
del sys
