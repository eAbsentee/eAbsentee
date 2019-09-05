import os
import glob

files = glob.glob('../applications/*')
for f in files:
    os.remove(f)
