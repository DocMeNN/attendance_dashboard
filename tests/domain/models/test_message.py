# tests/domain/models/test_message.py

"""
Tests for the Message Domain Model.
"""

from datetime import datetime

import pytest

from src.domain.models.message import Message


@pytest.fixture
def message() -> Message:
    """Return a valid Message instance."""
    return Message(
        timestamp=datetime(2026, 7, 22, 10, 30, 45),
        sender=" John Doe ",
        content="  Hello   Bible Study  ",
        line_number=42,
    )


def test_creates_valid_message(message: Message) -> None:
    """A valid message should be created successfully."""
    assert message.timestamp == datetime(2026, 7, 22, 10, 30, 45)
    assert message.sender == "John Doe"
    assert message.content == "Hello   Bible Study"
    assert message.line_number == 42


def test_sender_is_trimmed() -> None:
    """Sender whitespace should be removed."""
    message = Message(
        timestamp=datetime(2026, 7, 22, 10, 30),
        sender="  John Doe  ",
        content="Hello",
        line_number=1,
    )

    assert message.sender == "John Doe"


def test_content_is_trimmed() -> None:
    """Content leading and trailing whitespace should be removed."""
    message = Message(
        timestamp=datetime(2026, 7, 22, 10, 30),
        sender="John Doe",
        content="  Hello World  ",
        line_number=1,
    )

    assert message.content == "Hello World"


def test_invalid_timestamp_is_rejected() -> None:
    """A non-datetime timestamp should be rejected."""
    with pytest.raises(ValueError):
        Message(
            timestamp="2026-07-22",  # type: ignore[arg-type]
            sender="John Doe",
            content="Hello",
            line_number=1,
        )


def test_invalid_sender_type_is_rejected() -> None:
    """A non-string sender should be rejected."""
    with pytest.raises(ValueError):
        Message(
            timestamp=datetime(2026, 7, 22, 10, 30),
            sender=123,  # type: ignore[arg-type]
            content="Hello",
            line_number=1,
        )


def test_empty_sender_is_rejected() -> None:
    """An empty sender should be rejected."""
    with pytest.raises(ValueError):
        Message(
            timestamp=datetime(2026, 7, 22, 10, 30),
            sender="   ",
            content="Hello",
            line_number=1,
        )


def test_invalid_content_type_is_rejected() -> None:
    """A non-string content value should be rejected."""
    with pytest.raises(ValueError):
        Message(
            timestamp=datetime(2026, 7, 22, 10, 30),
            sender="John Doe",
            content=123,  # type: ignore[arg-type]
            line_number=1,
        )


@pytest.mark.parametrize("line_number", [0, -1])
def test_invalid_line_number_is_rejected(line_number: int) -> None:
    """Line numbers must be greater than zero."""
    with pytest.raises(ValueError):
        Message(
            timestamp=datetime(2026, 7, 22, 10, 30),
            sender="John Doe",
            content="Hello",
            line_number=line_number,
        )


def test_excessive_line_number_is_rejected() -> None:
    """Line numbers above the allowed maximum should be rejected."""
    with pytest.raises(ValueError):
        Message(
            timestamp=datetime(2026, 7, 22, 10, 30),
            sender="John Doe",
            content="Hello",
            line_number=10_000_001,
        )


def test_date_and_time_properties(message: Message) -> None:
    """Date and time properties should be derived from timestamp."""
    assert message.message_date.isoformat() == "2026-07-22"
    assert message.message_time.isoformat() == "10:30:45"


def test_normalized_content(message: Message) -> None:
    """Multiple internal spaces should be normalized."""
    assert message.normalized_content == "Hello Bible Study"


def test_lowercase_content(message: Message) -> None:
    """Lowercase content should be returned."""
    assert message.lowercase_content == "hello bible study"


def test_stripped_content(message: Message) -> None:
    """Stripped content should be returned."""
    assert message.stripped_content == "Hello   Bible Study"


def test_character_count(message: Message) -> None:
    """Character count should match the stored content."""
    assert message.character_count == len("Hello   Bible Study")


def test_word_count(message: Message) -> None:
    """Word count should be calculated correctly."""
    assert message.word_count == 3


def test_blank_message() -> None:
    """A whitespace-only content message should be recognized as blank."""
    message = Message(
        timestamp=datetime(2026, 7, 22, 10, 30),
        sender="John Doe",
        content="   ",
        line_number=1,
    )

    assert message.is_blank is True
    assert message.word_count == 0


def test_single_word_message() -> None:
    """A one-word message should be recognized."""
    message = Message(
        timestamp=datetime(2026, 7, 22, 10, 30),
        sender="John Doe",
        content="Done",
        line_number=1,
    )

    assert message.is_single_word is True
    assert message.is_multi_word is False


def test_multi_word_message(message: Message) -> None:
    """A multi-word message should be recognized."""
    assert message.is_multi_word is True
    assert message.is_single_word is False


def test_content_inspection(message: Message) -> None:
    """Content inspection properties should work correctly."""
    assert message.has_letters is True
    assert message.has_numbers is False
    assert message.has_uppercase is True
    assert message.has_lowercase is True
    assert message.starts_with_alpha is True


def test_contains_is_case_insensitive_by_default(
    message: Message,
) -> None:
    """Contains should be case-insensitive by default."""
    assert message.contains("BIBLE") is True


def test_contains_can_be_case_sensitive(
    message: Message,
) -> None:
    """Contains should support case-sensitive searches."""
    assert message.contains("Bible", case_sensitive=True) is True
    assert message.contains("BIBLE", case_sensitive=True) is False


def test_starts_with(message: Message) -> None:
    """Starts-with should support case-insensitive matching."""
    assert message.starts_with("hello") is True


def test_ends_with(message: Message) -> None:
    """Ends-with should support case-insensitive matching."""
    assert message.ends_with("STUDY") is True


def test_to_dict_returns_message_data(message: Message) -> None:
    """to_dict should return the message data."""
    result = message.to_dict()

    assert result == {
        "timestamp": message.timestamp,
        "sender": message.sender,
        "content": message.content,
        "line_number": message.line_number,
    }


def test_message_is_immutable(message: Message) -> None:
    """Message should be immutable."""
    with pytest.raises(AttributeError):
        message.sender = "Another Person"  # type: ignore[misc]


def test_message_length_returns_character_count(
    message: Message,
) -> None:
    """len(message) should return the character count."""
    assert len(message) == message.character_count
