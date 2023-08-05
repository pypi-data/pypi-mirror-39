# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

"""
This subpackage is used for reading and writing sequencing data
using the popular FASTQ format.

This package contains the `FastqFile`, which provides a dictionary
like interface to FASTQ files, with the sequence identifer strings being
the keys and the sequences and quality scores being the values.
"""

__author__ = "Patrick Kunzmann"

from .file import *