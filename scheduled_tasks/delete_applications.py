import os
from glob import glob
from Typing import List

files: List[str] = glob('../applications/*')
for f in files:
    os.remove(f)
