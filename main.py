#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the output directory.

Stdlib only. Deterministic: reads entry.png from the repo dir, writes it to
$MAKEFUN_OUTPUT_DIR (or /output/entry.png), verifies the sha256, prints it,
and exits 0.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "8ba35cf1d082f855f13153ffebe55a83158e2eafe194a464a59c8fe6c93d9294"


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(repo_dir, "entry.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    shutil.copyfile(src, dst)

    with open(dst, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()

    if digest != EXPECTED_SHA256:
        print("sha256 mismatch", digest, file=sys.stderr)
        sys.exit(1)

    print(digest)
    sys.exit(0)


if __name__ == "__main__":
    main()