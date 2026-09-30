import io

from pwstrength import load_wordlist


def test_file_like_object():
    words = load_wordlist(io.StringIO("Password\n  Letmein  \n\nQWERTY\n"))
    assert words == frozenset({"password", "letmein", "qwerty"})
    assert isinstance(words, frozenset)


def test_path_as_str_and_pathlib(tmp_path):
    path = tmp_path / "words.txt"
    path.write_text("one\nTwo\n", encoding="utf-8")
    expected = frozenset({"one", "two"})
    assert load_wordlist(path) == expected
    assert load_wordlist(str(path)) == expected


def test_none_reads_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("Alpha\nBeta\n"))
    assert load_wordlist() == frozenset({"alpha", "beta"})


def test_dash_reads_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("Gamma\n"))
    assert load_wordlist("-") == frozenset({"gamma"})


def test_crlf_line_endings(tmp_path):
    path = tmp_path / "words.txt"
    path.write_bytes(b"first\r\nsecond\r\n")
    assert load_wordlist(path) == frozenset({"first", "second"})


def test_invalid_utf8_bytes_are_dropped_not_fatal(tmp_path):
    path = tmp_path / "words.txt"
    path.write_bytes(b"good\n\xff\xfebad\n")
    assert load_wordlist(path) == frozenset({"good", "bad"})


def test_empty_source_gives_empty_set():
    assert load_wordlist(io.StringIO("")) == frozenset()
