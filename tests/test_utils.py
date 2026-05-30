"""Tests for section-selection parsing."""

from pathlib import Path

import pytest

from teacher.utils import parse_section_selection

# Stand-in section files; only the names matter for selection logic.
FILES = [
    Path("000-abstract.md"),
    Path("001-introduction.md"),
    Path("002-method.md"),
    Path("003-results.md"),
]


def test_none_returns_all():
    assert parse_section_selection(None, FILES) == FILES


def test_single_index():
    assert parse_section_selection("2", FILES) == [Path("002-method.md")]


def test_comma_list():
    assert parse_section_selection("0,3", FILES) == [
        Path("000-abstract.md"),
        Path("003-results.md"),
    ]


def test_range():
    assert parse_section_selection("1-2", FILES) == [
        Path("001-introduction.md"),
        Path("002-method.md"),
    ]


def test_mixed_range_and_index():
    assert parse_section_selection("0-1,3", FILES) == [
        Path("000-abstract.md"),
        Path("001-introduction.md"),
        Path("003-results.md"),
    ]


def test_select_by_name():
    assert parse_section_selection("method", FILES) == [Path("002-method.md")]


def test_unknown_name_raises():
    with pytest.raises(ValueError):
        parse_section_selection("nonexistent", FILES)


def test_no_match_raises():
    with pytest.raises(ValueError):
        parse_section_selection("9", FILES)
