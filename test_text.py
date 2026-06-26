"""
Unit tests for rich/text.py — Text and Span classes.
Part 4a: White-Box Testing — Retake Project
"""
import pytest
from rich.text import Text, Span


# ── Test 1: Text creation and plain property ──────────────────────────────────
def test_text_creation_plain():
    """Text object stores plain string correctly."""
    t = Text("Hello, World!")
    assert t.plain == "Hello, World!"
    assert len(t) == 13


# ── Test 2: Text append ───────────────────────────────────────────────────────
def test_text_append():
    """Appending plain string extends the text correctly."""
    t = Text("Hello")
    t.append(" World")
    assert t.plain == "Hello World"
    assert len(t) == 11


# ── Test 3: truncate — crop overflow ─────────────────────────────────────────
def test_truncate_crop():
    """Truncate crops text to max_width with 'fold' overflow."""
    t = Text("Hello World")
    t.truncate(5, overflow="fold")
    assert len(t.plain) == 5
    assert t.plain == "Hello"


# ── Test 4: truncate — ellipsis overflow ─────────────────────────────────────
def test_truncate_ellipsis():
    """Truncate with ellipsis overflow appends '…' and clips to max_width."""
    t = Text("Hello World")
    t.truncate(6, overflow="ellipsis")
    # result should be 5 visible chars + ellipsis character = 6 total cells
    assert t.plain.endswith("…")
    assert len(t.plain) == 6  # 5 chars + 1 ellipsis


# ── Test 5: pad_left adds characters ─────────────────────────────────────────
def test_pad_left():
    """pad_left prepends the correct number of characters."""
    t = Text("Hi")
    t.pad_left(3, "-")
    assert t.plain == "---Hi"


# ── Test 6: pad_right adds characters ────────────────────────────────────────
def test_pad_right():
    """pad_right appends the correct number of characters."""
    t = Text("Hi")
    t.pad_right(3, ".")
    assert t.plain == "Hi..."


# ── Test 7: remove_suffix removes existing suffix ────────────────────────────
def test_remove_suffix_present():
    """remove_suffix strips the suffix when it exists."""
    t = Text("Hello\n")
    t.remove_suffix("\n")
    assert t.plain == "Hello"


# ── Test 8: remove_suffix no-op when suffix absent ───────────────────────────
def test_remove_suffix_absent():
    """remove_suffix does nothing when suffix is not present."""
    t = Text("Hello")
    t.remove_suffix("\n")
    assert t.plain == "Hello"


# ── Test 9: set_length — extend ──────────────────────────────────────────────
def test_set_length_extend():
    """set_length pads text with spaces when new length is larger."""
    t = Text("Hi")
    t.set_length(5)
    assert len(t) == 5
    assert t.plain == "Hi   "


# ── Test 10: set_length — crop ───────────────────────────────────────────────
def test_set_length_crop():
    """set_length crops text when new length is smaller."""
    t = Text("Hello World")
    t.set_length(5)
    assert len(t) == 5
    assert t.plain == "Hello"


# ── Test 11: Span split — mid-span ───────────────────────────────────────────
def test_span_split_middle():
    """Span.split at middle offset produces two valid spans."""
    s = Span(0, 10, "bold")
    s1, s2 = s.split(5)
    assert s1 == Span(0, 5, "bold")
    assert s2 == Span(5, 10, "bold")


# ── Test 12: Span split — offset before start returns original ────────────────
def test_span_split_before_start():
    """Span.split with offset before start returns original span and None."""
    s = Span(5, 10, "italic")
    s1, s2 = s.split(2)
    assert s1 == s
    assert s2 is None


# ── Test 13: Text __contains__ ───────────────────────────────────────────────
def test_text_contains():
    """'in' operator checks substring membership."""
    t = Text("Hello World")
    assert "World" in t
    assert "xyz" not in t


# ── Test 14: Text copy is independent ────────────────────────────────────────
def test_text_copy_independence():
    """Copying a Text object creates an independent instance."""
    t1 = Text("Hello")
    t2 = t1.copy()
    t2.plain = "World"
    assert t1.plain == "Hello"
    assert t2.plain == "World"


# ── Test 15: align — center ──────────────────────────────────────────────────
def test_align_center():
    """align('center', width) pads text symmetrically."""
    t = Text("Hi")
    t.align("center", 6)
    assert len(t.plain) == 6
    # 'Hi' centered in 6 chars: 2 left, 2 right
    assert t.plain == "  Hi  "


# ── Test 16: align — right ────────────────────────────────────────────────────
def test_align_right():
    """align('right', width) pads text on the left."""
    t = Text("Hi")
    t.align("right", 5)
    assert t.plain == "   Hi"


# ── Test 17: append with style stores span ───────────────────────────────────
def test_append_with_style():
    """Appending text with style creates a Span."""
    t = Text("Hello")
    t.append(" World", style="bold")
    assert len(t._spans) == 1
    span = t._spans[0]
    assert span.style == "bold"
    assert span.start == 5
    assert span.end == 11


# ── Test 18: Text from_markup strips markup tags ─────────────────────────────
def test_from_markup():
    """from_markup parses rich markup and returns plain text without tags."""
    t = Text.from_markup("[bold]Hello[/bold]")
    assert t.plain == "Hello"


# ── Test 19: rstrip removes trailing whitespace ──────────────────────────────
def test_rstrip():
    """rstrip() removes trailing whitespace from the text."""
    t = Text("Hello   ")
    t.rstrip()
    assert t.plain == "Hello"


# ── Test 20: Span __bool__ — empty span is falsy ─────────────────────────────
def test_span_bool_empty():
    """A Span with equal start and end is falsy (zero-length)."""
    s = Span(5, 5, "bold")
    assert not bool(s)


# ── Test 21: Span __bool__ — non-empty is truthy ─────────────────────────────
def test_span_bool_nonempty():
    """A Span with start < end is truthy."""
    s = Span(0, 3, "red")
    assert bool(s)
