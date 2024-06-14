import os
from pathlib import Path

total = 0

for r, d, f in os.walk("cheeze"):
    to_remove = []
    for x in d:
        if x.startswith("__"):
            to_remove.append(x)

    for x in to_remove:
        d.remove(x)

    for x in f:
        if not x.endswith(".py"):
            continue
        with open(Path(r)/x) as fp:
            lines = len(fp.readlines())
            print(f"{r}\\{x}".ljust(50), f"{lines}".rjust(4))
            total += lines

print("Total lines: ", total)