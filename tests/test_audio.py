"""Tests for TTS text chunking."""

from teacher.speak.audio import chunk_text


def test_short_text_single_chunk():
    text = "One sentence. Two sentences."
    assert chunk_text(text, max_chars=1000) == [text]


def test_splits_at_sentence_boundary():
    # Two ~10-char sentences, max 15 forces one sentence per chunk.
    chunks = chunk_text("Hello there. Goodbye now.", max_chars=15)
    assert chunks == ["Hello there.", "Goodbye now."]


def test_every_chunk_within_limit():
    text = " ".join(f"Sentence number {i}." for i in range(50))
    chunks = chunk_text(text, max_chars=80)
    assert all(len(c) <= 80 for c in chunks)
    # Reassembling recovers the original word sequence (whitespace aside).
    assert " ".join(chunks).split() == text.split()


def test_oversized_single_sentence_is_hard_split():
    # One "sentence" with no boundary, well over the limit: chunk_text must
    # hard-split it so no chunk exceeds max_chars and no content is lost.
    text = "x" * 100
    chunks = chunk_text(text, max_chars=40)
    assert all(len(c) <= 40 for c in chunks)
    assert "".join(chunks) == text
