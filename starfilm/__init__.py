__version__ = "0.1.0"

import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .swapi import swapi
from .cli.cli import CliApp