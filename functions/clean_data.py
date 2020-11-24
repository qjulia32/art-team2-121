from pathlib import Path
import os

data_dir = "..\data"

for root, dirs, files in os.walk(data_dir):
    num = len(files)
    if num < 6:
        print(root + ": " + str(num))
    for f in files:
        size = Path(os.path.join(root, f)).stat().st_size
        # if size > 1000000:
        #     print(f)
        #     os.remove(os.path.join(root, f))
        #
