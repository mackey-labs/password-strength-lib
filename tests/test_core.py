from pwstrength import Strength, analyze
from pwstrength.core import _has_sequential_run


def test_empty_password_scores_zero():
    result = analyze("")
    assert result == Strength(0, "very weak", ["empty password"])


def test_short_single_class_is_very_weak():
    result = analyze("abc")
    assert result.score == 0
    assert "shorter than 8 characters" in result.reasons
    assert "uses only one character type" in result.reasons


def test_mixed_medium_length_is_fair():
    result = analyze("kqzmvxjw3p7t")
    assert result.score == 2
    assert result.label == "fair"
    assert result.reasons == []


def test_score_is_capped_at_four():
    result = analyze("Xk9#mPq2$vLw7!zR")
    assert result.score == 4
    assert result.label == "very strong"


def test_repeated_run_is_penalised():
    result = analyze("aaaa1111")
    assert result.score == 0
    assert "contains a repeated character run" in result.reasons


def test_two_repeats_in_a_row_are_not_a_run():
    result = analyze("aab1ccd2")
    assert "contains a repeated character run" not in result.reasons


def test_sequential_run_is_penalised():
    result = analyze("abcd1234")
    assert any("sequential" in r for r in result.reasons)
    assert result.score == 0


def test_denylist_forces_zero_even_when_complex():
    common = frozenset({"tr0ub4dor&3xyz"})
    assert analyze("Tr0ub4dor&3xyz").score == 4
    result = analyze("Tr0ub4dor&3xyz", common)
    assert result.score == 0
    assert "matches a known common password" in result.reasons


def test_denylist_match_ignores_case():
    result = analyze("PassWord1!", frozenset({"password1!"}))
    assert result.score == 0


def test_sequential_run_ascending_and_descending():
    assert _has_sequential_run("xx1234xx", 4)
    assert _has_sequential_run("xxdcbaxx", 4)


def test_sequential_run_ignores_case():
    assert _has_sequential_run("ABCD", 4)


def test_sequential_run_needs_full_length():
    assert not _has_sequential_run("abc", 4)
    assert not _has_sequential_run("abdc", 4)


def test_sequential_run_skips_non_alphanumeric_windows():
    # ':' follows '9' in ASCII but is not a digit
    assert not _has_sequential_run("789:", 4)
