"""Zip an Advanced Slides export folder into <repo>/presentation/export/<name>.zip (entries at the zip root)."""
import os, sys, zipfile, pathlib
src = pathlib.Path(sys.argv[1]); dst = pathlib.Path(sys.argv[2])
n = 0
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(src.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(src).as_posix()); n += 1
print(f'{dst.name}: {n} files, {dst.stat().st_size/1048576:.1f} MB')
