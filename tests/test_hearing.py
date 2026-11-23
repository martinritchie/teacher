"""Checking spoken clips by machine (hearing.py)."""


def test_word_error_rate_ignores_case_and_punctuation():
    """The speech check's word error rate: edits over the script's length, without case or punctuation."""
    from teacher.hearing import word_error_rate

    assert (
        word_error_rate("The encoder, then the loss.", "the encoder then the loss") == 0
    )
    assert word_error_rate("one two three four", "one too three") == 0.5
