"""
Unit tests for LogEntry data class.

This module tests the LogEntry data class which represents a parsed log entry.
Following TDD principles - tests are written before implementation.
"""

import pytest
from datetime import datetime
from logsentinel.parsers.base import LogEntry


class TestLogEntry:
    """Test cases for LogEntry data class."""

    def test_log_entry_creation_with_required_fields(self):
        """Test that LogEntry can be created with required fields."""
        # Arrange
        timestamp = datetime(2023, 12, 1, 10, 0, 0)
        level = "INFO"
        message = "User login successful"
        source = "auth"
        raw_line = "2023-12-01 10:00:00 INFO User login successful"

        # Act
        log_entry = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line
        )

        # Assert
        assert log_entry.timestamp == timestamp
        assert log_entry.level == level
        assert log_entry.message == message
        assert log_entry.source == source
        assert log_entry.raw_line == raw_line
        assert log_entry.metadata == {}

    def test_log_entry_creation_with_metadata(self):
        """Test that LogEntry can be created with custom metadata."""
        # Arrange
        timestamp = datetime(2023, 12, 1, 10, 0, 0)
        level = "WARN"
        message = "Failed login attempt"
        source = "auth"
        raw_line = "2023-12-01 10:00:00 WARN Failed login attempt"
        metadata = {"ip": "192.168.1.100", "user": "admin"}

        # Act
        log_entry = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line,
            metadata=metadata
        )

        # Assert
        assert log_entry.timestamp == timestamp
        assert log_entry.level == level
        assert log_entry.message == message
        assert log_entry.source == source
        assert log_entry.raw_line == raw_line
        assert log_entry.metadata == metadata

    def test_log_entry_creation_without_metadata_defaults_to_empty_dict(self):
        """Test that LogEntry defaults metadata to empty dict when not provided."""
        # Arrange
        timestamp = datetime(2023, 12, 1, 10, 0, 0)
        level = "ERROR"
        message = "Database connection failed"
        source = "database"
        raw_line = "2023-12-01 10:00:00 ERROR Database connection failed"

        # Act
        log_entry = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line
        )

        # Assert
        assert log_entry.metadata == {}

    def test_log_entry_equality(self):
        """Test that LogEntry instances with same data are equal."""
        # Arrange
        timestamp = datetime(2023, 12, 1, 10, 0, 0)
        level = "INFO"
        message = "User login successful"
        source = "auth"
        raw_line = "2023-12-01 10:00:00 INFO User login successful"
        metadata = {"ip": "192.168.1.100"}

        # Act
        log_entry1 = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line,
            metadata=metadata
        )
        
        log_entry2 = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line,
            metadata=metadata
        )

        # Assert
        assert log_entry1 == log_entry2

    def test_log_entry_inequality(self):
        """Test that LogEntry instances with different data are not equal."""
        # Arrange
        timestamp1 = datetime(2023, 12, 1, 10, 0, 0)
        timestamp2 = datetime(2023, 12, 1, 10, 1, 0)
        level = "INFO"
        message = "User login successful"
        source = "auth"
        raw_line = "2023-12-01 10:00:00 INFO User login successful"

        # Act
        log_entry1 = LogEntry(
            timestamp=timestamp1,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line
        )
        
        log_entry2 = LogEntry(
            timestamp=timestamp2,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line
        )

        # Assert
        assert log_entry1 != log_entry2

    def test_log_entry_string_representation(self):
        """Test that LogEntry has a meaningful string representation."""
        # Arrange
        timestamp = datetime(2023, 12, 1, 10, 0, 0)
        level = "INFO"
        message = "User login successful"
        source = "auth"
        raw_line = "2023-12-01 10:00:00 INFO User login successful"

        # Act
        log_entry = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line
        )

        # Assert
        str_repr = str(log_entry)
        assert "LogEntry" in str_repr
        assert "INFO" in str_repr
        assert "User login successful" in str_repr
        assert "auth" in str_repr

    def test_log_entry_with_different_log_levels(self):
        """Test that LogEntry works with different log levels."""
        # Arrange
        timestamp = datetime(2023, 12, 1, 10, 0, 0)
        source = "system"
        raw_line = "2023-12-01 10:00:00 DEBUG System check completed"
        log_levels = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

        for level in log_levels:
            # Act
            log_entry = LogEntry(
                timestamp=timestamp,
                level=level,
                message=f"Test message for {level}",
                source=source,
                raw_line=raw_line
            )

            # Assert
            assert log_entry.level == level
            assert log_entry.message == f"Test message for {level}"

    def test_log_entry_metadata_modification(self):
        """Test that LogEntry metadata can be modified after creation."""
        # Arrange
        timestamp = datetime(2023, 12, 1, 10, 0, 0)
        level = "INFO"
        message = "User login successful"
        source = "auth"
        raw_line = "2023-12-01 10:00:00 INFO User login successful"

        # Act
        log_entry = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line
        )

        # Assert - initial state
        assert log_entry.metadata == {}

        # Act - modify metadata
        log_entry.metadata["ip"] = "192.168.1.100"
        log_entry.metadata["user"] = "admin"

        # Assert - modified state
        assert log_entry.metadata["ip"] == "192.168.1.100"
        assert log_entry.metadata["user"] == "admin"
        assert len(log_entry.metadata) == 2
