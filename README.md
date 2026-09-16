# pwstrength

A small library for scoring password strength, with no dependencies beyond
the Python standard library.

Most strength checkers either do nothing (length >= 8, one number, done) or
pull in a large model like zxcvbn's frequency tables. This sits in between:
a handful of cheap heuristics (length, character variety, repeated or
sequential runs) plus an optional denylist check against a wordlist of
known-leaked passwords. Good enough for a signup form hint or a quick audit
of a password dump, without adding a dependency to your project.

## Install

There's no package published yet. Vendor the `pwstrength/` directory or
add this repo as a path dependency until it lands on PyPI.

## Usage

```python
from pwstrength import analyze

result = analyze("correcthorsebatterystaple")
print(result.score)    # 0-4
print(result.label)    # "very weak" .. "very strong"
print(result.reasons)  # why it scored the way it did
```

### Checking against a wordlist

`analyze` takes an optional `common_passwords` set. Use `load_wordlist` to
build one from a file:

```python
from pwstrength import analyze, load_wordlist

common = load_wordlist("rockyou-top10k.txt")
result = analyze("password1", common_passwords=common)
# result.score == 0, result.reasons includes "matches a known common password"
```

The same function reads from stdin when no source is given, or when the
source is `"-"`. That makes it easy to wire up a script that accepts either
a file argument or a pipe:

```python
import sys
from pwstrength import analyze, load_wordlist

# python check.py rockyou.txt   -> reads the file
# cat rockyou.txt | python check.py -> reads stdin
wordlist_arg = sys.argv[1] if len(sys.argv) > 1 else "-"
common = load_wordlist(wordlist_arg)

for line in sys.stdin if wordlist_arg != "-" else []:
    print(analyze(line.strip(), common_passwords=common))
```

`load_wordlist` also accepts any already-open file object, so tests can
pass an `io.StringIO` instead of touching the filesystem.

## Scope

This is a library, not a CLI. It doesn't estimate crack time in seconds or
model keyboard-walk patterns beyond simple ascending/descending runs — see
the roadmap in commit history for what's planned next.

## License

MIT, see LICENSE.
