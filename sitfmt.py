#!/usr/bin/env python3
"""sitfmt - standalone CLI entry for the assignment-report-formatter skill.

Works from a repo clone (scripts/ next to this file) or a pip/pipx install
(scripts shipped to <prefix>/share/sit-formatter/):

    sitfmt --spec spec.json --format pdf --out report.pdf
"""
import os
import sys

import site

_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPT_DIRS = [
    os.path.join(_HERE, "scripts"),
    os.path.join(sys.prefix, "share", "sit-formatter", "scripts"),
    os.path.join(site.USER_BASE, "share", "sit-formatter", "scripts"),
]
for _d in _SCRIPT_DIRS:
    if os.path.exists(os.path.join(_d, "make_report.py")):
        sys.path.insert(0, _d)
        break
else:
    sys.exit("sitfmt: make_report.py not found (cloned repo or pip install required)")

from make_report import main  # noqa: E402

if __name__ == "__main__":
    main()
