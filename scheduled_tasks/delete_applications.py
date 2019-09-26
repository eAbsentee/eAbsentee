import os
import glob

os.chdir('..')
files = glob.glob('applications/*')
for f in files:
    os.remove(f)
