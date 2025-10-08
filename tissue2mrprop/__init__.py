import os
from pathlib import Path

version_file = Path(__file__).parent / "version.txt"
with open(version_file, 'r') as f:
    __version__ = f.read().rstrip()