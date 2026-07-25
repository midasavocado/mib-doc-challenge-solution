#!/usr/bin/env python3
"""MIB challenge entrypoint."""

from __future__ import annotations

import sys

from mib_pipeline import main


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: solution.py <input_pdf_dir> <output_path>")
    main(sys.argv[1], sys.argv[2])
