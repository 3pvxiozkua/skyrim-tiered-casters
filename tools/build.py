#!/usr/bin/env python3
"""Regenerate the configs, validate them, and build the distributable archive.

    python3 tools/build.py

Output: dist/skyrim-tiered-casters-<version>.zip
The archive is laid out the way MO2 and Vortex expect: fomod/ at the root, the
candidate ini files in folders the installer copies to Data, docs alongside.
"""

import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import generate  # noqa: E402
import validate_distr  # noqa: E402

DIST = os.path.join(ROOT, "dist")


def stage():
    staging = os.path.join(ROOT, ".build", "skyrim-tiered-casters")
    if os.path.isdir(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)

    shutil.copytree(os.path.join(ROOT, "fomod"), os.path.join(staging, "fomod"))
    shutil.copytree(os.path.join(ROOT, "src", "Presets"), os.path.join(staging, "Presets"))
    shutil.copytree(os.path.join(ROOT, "src", "Modules"), os.path.join(staging, "Modules"))

    docs = os.path.join(staging, "docs")
    os.makedirs(docs)
    for name in ("README.md", "CHANGELOG.md"):
        source = os.path.join(ROOT, name)
        if os.path.isfile(source):
            shutil.copy2(source, os.path.join(docs, name))
    return staging


def main():
    generate.main()

    failures = 0
    for sub in ("src/Presets", "src/Modules"):
        for name in sorted(os.listdir(os.path.join(ROOT, sub))):
            if not name.endswith("_DISTR.ini"):
                continue
            _, errors = validate_distr.check_file(os.path.join(ROOT, sub, name))
            for error in errors:
                print("! %s" % error)
            failures += len(errors)
    if failures:
        print("refusing to package: %d validation problems" % failures)
        return 1

    staging = stage()
    os.makedirs(DIST, exist_ok=True)
    archive = os.path.join(DIST, "skyrim-tiered-casters-%s.zip" % generate.VERSION)
    if os.path.isfile(archive):
        os.remove(archive)

    # Fixed timestamp: reproducible archive, and it sidesteps filesystems that
    # report an epoch mtime (zip cannot store anything before 1980).
    stamp = (2026, 11, 19, 0, 0, 0)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder, _, names in os.walk(staging):
            for name in sorted(names):
                full = os.path.join(folder, name)
                rel = os.path.relpath(full, staging).replace(os.sep, "/")
                info = zipfile.ZipInfo(rel, date_time=stamp)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                with open(full, "rb") as fh:
                    zf.writestr(info, fh.read())

    with zipfile.ZipFile(archive) as zf:
        entries = zf.namelist()
    print("\n%s" % archive)
    print("%d entries, %.1f KB" % (len(entries), os.path.getsize(archive) / 1024.0))
    for entry in entries:
        print("  %s" % entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
