"""Loading denylists of known-bad passwords.

The one requirement that shapes this whole module: callers should be able
to point at a file on disk *or* pipe a list in, without caring which. A CLI
built on top of this library (not included here) would default its
--wordlist argument to "-" and hand it straight to load_wordlist.
"""

import sys
from pathlib import Path


def load_wordlist(source=None):
    """Return a frozenset of lowercase, stripped words from source.

    source may be:
      - None or "-": read from sys.stdin
      - a path (str or os.PathLike): read that file
      - an open file-like object (anything with .read()): read it directly

    Blank lines are dropped. Comparison in analyze() is case-insensitive,
    so words are lowercased here once rather than on every lookup.
    """
    if source is None or source == "-":
        text = sys.stdin.read()
    elif hasattr(source, "read"):
        text = source.read()
    else:
        text = Path(source).read_text(encoding="utf-8", errors="ignore")

    return frozenset(
        line.strip().lower()
        for line in text.splitlines()
        if line.strip()
    )
