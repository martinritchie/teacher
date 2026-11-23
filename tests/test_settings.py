"""Settings (settings.py): per-model profiles."""

import pytest

from teacher.settings import (
    profile,
)


def test_a_model_with_no_profile_is_an_error():
    """Settings are looked up by model family; an unknown family says where to add one."""
    with pytest.raises(ValueError, match="PROFILES"):
        profile("gemma-4-12b")
