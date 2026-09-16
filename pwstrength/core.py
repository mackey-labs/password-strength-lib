"""Heuristic password strength scoring.

Not a substitute for a real cracking-time model (zxcvbn does that properly).
This gives a cheap 0-4 score plus the reasons behind it, good enough for a
signup form hint or a bulk audit of a leaked-password dump.
"""

from dataclasses import dataclass, field
import re

_LABELS = ["very weak", "weak", "fair", "strong", "very strong"]


@dataclass
class Strength:
    score: int
    label: str
    reasons: list = field(default_factory=list)


def analyze(password, common_passwords=frozenset()):
    """Score a single password.

    common_passwords is an optional set of lowercase strings (see
    load_wordlist) checked as an exact-match denylist. A hit forces the
    score to 0 regardless of how "complex" the password otherwise looks,
    since attackers try known-leaked passwords before anything else.
    """
    if not password:
        return Strength(0, _LABELS[0], ["empty password"])

    reasons = []
    points = 0

    length = len(password)
    if length >= 16:
        points += 2
    elif length >= 12:
        points += 1
    elif length < 8:
        reasons.append("shorter than 8 characters")

    classes = 0
    for pattern in (r"[a-z]", r"[A-Z]", r"[0-9]", r"[^a-zA-Z0-9]"):
        if re.search(pattern, password):
            classes += 1
    if classes <= 1:
        reasons.append("uses only one character type")
    points += max(0, classes - 1)

    if re.search(r"(.)\1\1", password):
        reasons.append("contains a repeated character run")
        points -= 1

    if _has_sequential_run(password, run_length=4):
        reasons.append("contains a sequential run (e.g. abcd, 1234)")
        points -= 1

    if password.lower() in common_passwords:
        reasons.append("matches a known common password")
        points = 0

    score = max(0, min(4, points))
    return Strength(score=score, label=_LABELS[score], reasons=reasons)


def _has_sequential_run(password, run_length):
    lowered = password.lower()
    for start in range(len(lowered) - run_length + 1):
        window = lowered[start:start + run_length]
        if not window.isalnum():
            continue
        codes = [ord(c) for c in window]
        steps = [b - a for a, b in zip(codes, codes[1:])]
        if all(step == 1 for step in steps) or all(step == -1 for step in steps):
            return True
    return False
