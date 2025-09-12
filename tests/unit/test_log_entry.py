"""
Unit tests for LogEntry data class.

This module tests the LogEntry data class which represents a parsed log entry.
Refactored to be more concise and eliminate duplication.
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Iterator
from logsentinel.parsers.base import LogEntry, LogLevel, LogEntryValidator, BaseLogParser


class TestLogEntry:
    """Test cases for LogEntry data class using parametrized tests."""
    
    @pytest.fixture
    def base_timestamp(self):
        """Base timestamp for test data."""
        return datetime(2023, 12, 1, 10, 0, 0)
    
    @pytest.fixture
    def base_log_data(self, base_timestamp):
        """Base log data for test cases."""
        return {
            "timestamp": base_timestamp,
            "level": "INFO",
            "message": "User login successful",
            "source": "auth",
            "raw_line": "2023-12-01 10:00:00 INFO User login successful"
        }
    
    @pytest.mark.parametrize("kwargs,expected_metadata", [
        # No metadata provided (defaults to None, then becomes {})
        ({}, {}),
        
        # Explicit None metadata
        ({"metadata": None}, {}),
        
        # Custom metadata
        ({"metadata": {"ip": "192.168.1.100", "user": "admin"}}, {"ip": "192.168.1.100", "user": "admin"}),
        
        # Empty metadata dict
        ({"metadata": {}}, {}),
    ])
    def test_log_entry_creation_scenarios(self, base_log_data, kwargs, expected_metadata):
        """Test LogEntry creation with various metadata scenarios."""
        # Act
        log_entry = LogEntry(**base_log_data, **kwargs)
        
        # Assert
        assert log_entry.timestamp == base_log_data["timestamp"]
        assert log_entry.level == base_log_data["level"]
        assert log_entry.message == base_log_data["message"]
        assert log_entry.source == base_log_data["source"]
        assert log_entry.raw_line == base_log_data["raw_line"]
        assert log_entry.metadata == expected_metadata
        assert isinstance(log_entry.metadata, dict)
    
    @pytest.mark.parametrize("level,message,source", [
        ("DEBUG", "Debug message", "app"),
        ("INFO", "Info message", "system"),
        ("WARN", "Warning message", "security"),
        ("ERROR", "Error message", "database"),
        ("CRITICAL", "Critical message", "core"),
    ])
    def test_log_entry_with_different_levels(self, base_timestamp, level, message, source):
        """Test LogEntry with different log levels and sources."""
        raw_line = f"2023-12-01 10:00:00 {level} {message}"
        
        # Act
        log_entry = LogEntry(
            timestamp=base_timestamp,
            level=level,
            message=message,
            source=source,
            raw_line=raw_line
        )
        
        # Assert
        assert log_entry.level == level
        assert log_entry.message == message
        assert log_entry.source == source
        assert log_entry.raw_line == raw_line
    
    @pytest.mark.parametrize("entry1_data,entry2_data,should_be_equal", [
        # Same data - should be equal
        (
            {"level": "INFO", "message": "Test", "source": "test"},
            {"level": "INFO", "message": "Test", "source": "test"},
            True
        ),
        
        # Different timestamp - should not be equal
        (
            {"timestamp": datetime(2023, 12, 1, 10, 0, 0), "level": "INFO", "message": "Test", "source": "test"},
            {"timestamp": datetime(2023, 12, 1, 10, 1, 0), "level": "INFO", "message": "Test", "source": "test"},
            False
        ),
        
        # Different level - should not be equal
        (
            {"level": "INFO", "message": "Test", "source": "test"},
            {"level": "WARN", "message": "Test", "source": "test"},
            False
        ),
        
        # Different message - should not be equal
        (
            {"level": "INFO", "message": "Test 1", "source": "test"},
            {"level": "INFO", "message": "Test 2", "source": "test"},
            False
        ),
        
        # Different source - should not be equal
        (
            {"level": "INFO", "message": "Test", "source": "test1"},
            {"level": "INFO", "message": "Test", "source": "test2"},
            False
        ),
        
        # Different metadata - should not be equal
        (
            {"level": "INFO", "message": "Test", "source": "test", "metadata": {"key1": "value1"}},
            {"level": "INFO", "message": "Test", "source": "test", "metadata": {"key2": "value2"}},
            False
        ),
    ])
    def test_log_entry_equality_scenarios(self, base_timestamp, entry1_data, entry2_data, should_be_equal):
        """Test LogEntry equality with various data combinations."""
        # Arrange
        base_data = {
            "raw_line": "2023-12-01 10:00:00 INFO Test"
        }
        
        # Use base_timestamp only if timestamp is not in entry data
        if "timestamp" not in entry1_data:
            entry1_data = {**entry1_data, "timestamp": base_timestamp}
        if "timestamp" not in entry2_data:
            entry2_data = {**entry2_data, "timestamp": base_timestamp}
        
        log_entry1 = LogEntry(**base_data, **entry1_data)
        log_entry2 = LogEntry(**base_data, **entry2_data)
        
        # Act & Assert
        if should_be_equal:
            assert log_entry1 == log_entry2
        else:
            assert log_entry1 != log_entry2
    
    def test_log_entry_string_representation(self, base_log_data):
        """Test that LogEntry has a meaningful string representation."""
        # Act
        log_entry = LogEntry(**base_log_data)
        str_repr = str(log_entry)
        
        # Assert
        assert "LogEntry" in str_repr
        assert base_log_data["level"] in str_repr
        assert base_log_data["message"] in str_repr
        assert base_log_data["source"] in str_repr
    
    def test_log_entry_metadata_modification(self, base_log_data):
        """Test that LogEntry metadata can be modified after creation."""
        # Act
        log_entry = LogEntry(**base_log_data)
        
        # Assert - initial state
        assert log_entry.metadata == {}
        
        # Act - modify metadata
        log_entry.metadata["ip"] = "192.168.1.100"
        log_entry.metadata["user"] = "admin"
        
        # Assert - modified state
        assert log_entry.metadata["ip"] == "192.168.1.100"
        assert log_entry.metadata["user"] == "admin"
        assert len(log_entry.metadata) == 2
    
    @pytest.mark.parametrize("metadata_updates,expected_result", [
        # Single update
        ({"ip": "192.168.1.100"}, {"ip": "192.168.1.100"}),
        
        # Multiple updates
        ({"ip": "192.168.1.100", "user": "admin"}, {"ip": "192.168.1.100", "user": "admin"}),
        
        # Update existing key
        ({"ip": "10.0.0.1"}, {"ip": "10.0.0.1"}),
        
        # Mixed types
        ({"count": 42, "active": True, "name": "test"}, {"count": 42, "active": True, "name": "test"}),
    ])
    def test_log_entry_metadata_modification_scenarios(self, base_log_data, metadata_updates, expected_result):
        """Test various metadata modification scenarios."""
        # Act
        log_entry = LogEntry(**base_log_data)
        
        # Apply updates
        for key, value in metadata_updates.items():
            log_entry.metadata[key] = value
        
        # Assert
        assert log_entry.metadata == expected_result
        assert len(log_entry.metadata) == len(expected_result)
    
    def test_log_entry_immutability_of_core_fields(self, base_log_data):
        """Test that core LogEntry fields can be modified (dataclass behavior)."""
        # Act
        log_entry = LogEntry(**base_log_data)
        original_timestamp = log_entry.timestamp
        original_level = log_entry.level
        
        # Modify fields
        log_entry.timestamp = datetime(2024, 1, 1, 12, 0, 0)
        log_entry.level = "ERROR"
        
        # Assert - fields can be modified
        assert log_entry.timestamp != original_timestamp
        assert log_entry.level != original_level
        assert log_entry.timestamp == datetime(2024, 1, 1, 12, 0, 0)
        assert log_entry.level == "ERROR"
    
    @pytest.mark.parametrize("level,expected_error", [
        ("ERROR", True),
        ("CRITICAL", True),
        ("error", True),  # Case insensitive
        ("critical", True),
        ("INFO", False),
        ("DEBUG", False),
        ("WARN", False),
    ])
    def test_log_entry_is_error_level(self, base_log_data, level, expected_error):
        """Test LogEntry.is_error_level() method."""
        # Act
        log_data = base_log_data.copy()
        log_data["level"] = level
        log_entry = LogEntry(**log_data)
        
        # Assert
        assert log_entry.is_error_level() == expected_error
    
    @pytest.mark.parametrize("level,expected_warning", [
        ("WARN", True),
        ("warn", True),  # Case insensitive
        ("ERROR", False),
        ("INFO", False),
        ("DEBUG", False),
        ("CRITICAL", False),
    ])
    def test_log_entry_is_warning_level(self, base_log_data, level, expected_warning):
        """Test LogEntry.is_warning_level() method."""
        # Act
        log_data = base_log_data.copy()
        log_data["level"] = level
        log_entry = LogEntry(**log_data)
        
        # Assert
        assert log_entry.is_warning_level() == expected_warning
    
    @pytest.mark.parametrize("level,expected_priority", [
        ("DEBUG", 1),
        ("debug", 1),  # Case insensitive
        ("INFO", 2),
        ("WARN", 3),
        ("ERROR", 4),
        ("CRITICAL", 5),
    ])
    def test_log_entry_get_level_priority(self, base_log_data, level, expected_priority):
        """Test LogEntry.get_level_priority() method."""
        # Act
        log_data = base_log_data.copy()
        log_data["level"] = level
        log_entry = LogEntry(**log_data)
        
        # Assert
        assert log_entry.get_level_priority() == expected_priority
    
    def test_log_entry_get_level_priority_unknown_level(self, base_log_data):
        """Test LogEntry.get_level_priority() method with unknown level."""
        # Act - create with valid level first, then modify to bypass validation
        log_entry = LogEntry(**base_log_data)
        log_entry.level = "UNKNOWN"  # Direct assignment bypasses validation
        
        # Assert
        assert log_entry.get_level_priority() == 0
    
    def test_log_entry_add_metadata(self, base_log_data):
        """Test LogEntry.add_metadata() method."""
        # Act
        log_entry = LogEntry(**base_log_data)
        log_entry.add_metadata("ip", "192.168.1.100")
        log_entry.add_metadata("user", "admin")
        
        # Assert
        assert log_entry.metadata["ip"] == "192.168.1.100"
        assert log_entry.metadata["user"] == "admin"
        assert len(log_entry.metadata) == 2
    
    def test_log_entry_add_metadata_invalid_key(self, base_log_data):
        """Test LogEntry.add_metadata() with invalid key."""
        # Act
        log_entry = LogEntry(**base_log_data)
        
        # Assert - empty key
        with pytest.raises(ValueError, match="Metadata key must be a non-empty string"):
            log_entry.add_metadata("", "value")
        
        # Assert - whitespace key
        with pytest.raises(ValueError, match="Metadata key must be a non-empty string"):
            log_entry.add_metadata("   ", "value")
        
        # Assert - non-string key
        with pytest.raises(ValueError, match="Metadata key must be a non-empty string"):
            log_entry.add_metadata(123, "value")
    
    def test_log_entry_get_metadata(self, base_log_data):
        """Test LogEntry.get_metadata() method."""
        # Act
        log_entry = LogEntry(**base_log_data, metadata={"ip": "192.168.1.100", "user": "admin"})
        
        # Assert
        assert log_entry.get_metadata("ip") == "192.168.1.100"
        assert log_entry.get_metadata("user") == "admin"
        assert log_entry.get_metadata("nonexistent") is None
        assert log_entry.get_metadata("nonexistent", "default") == "default"
    
    def test_log_entry_has_metadata(self, base_log_data):
        """Test LogEntry.has_metadata() method."""
        # Act
        log_entry = LogEntry(**base_log_data, metadata={"ip": "192.168.1.100"})
        
        # Assert
        assert log_entry.has_metadata("ip") is True
        assert log_entry.has_metadata("user") is False
    
    def test_log_entry_to_dict(self, base_log_data):
        """Test LogEntry.to_dict() method."""
        # Act
        log_entry = LogEntry(**base_log_data, metadata={"ip": "192.168.1.100"})
        result = log_entry.to_dict()
        
        # Assert
        assert result["timestamp"] == base_log_data["timestamp"].isoformat()
        assert result["level"] == base_log_data["level"]
        assert result["message"] == base_log_data["message"]
        assert result["source"] == base_log_data["source"]
        assert result["raw_line"] == base_log_data["raw_line"]
        assert result["metadata"] == {"ip": "192.168.1.100"}
        assert isinstance(result["metadata"], dict)
        assert result["metadata"] is not log_entry.metadata  # Should be a copy


class TestLogLevel:
    """Test cases for LogLevel enum."""
    
    def test_log_level_values(self):
        """Test LogLevel enum values."""
        assert LogLevel.DEBUG.value == "DEBUG"
        assert LogLevel.INFO.value == "INFO"
        assert LogLevel.WARN.value == "WARN"
        assert LogLevel.ERROR.value == "ERROR"
        assert LogLevel.CRITICAL.value == "CRITICAL"
    
    def test_log_level_membership(self):
        """Test LogLevel enum membership."""
        assert "DEBUG" in [level.value for level in LogLevel]
        assert "INFO" in [level.value for level in LogLevel]
        assert "WARN" in [level.value for level in LogLevel]
        assert "ERROR" in [level.value for level in LogLevel]
        assert "CRITICAL" in [level.value for level in LogLevel]


class TestLogEntryValidator:
    """Test cases for LogEntryValidator class."""
    
    def test_validate_timestamp_valid(self):
        """Test timestamp validation with valid timestamp."""
        # Act & Assert - should not raise
        LogEntryValidator.validate_timestamp(datetime.now())
        LogEntryValidator.validate_timestamp(datetime.now() - timedelta(hours=1))
    
    def test_validate_timestamp_future(self):
        """Test timestamp validation with future timestamp."""
        # Act & Assert
        with pytest.raises(ValueError, match="Log timestamp cannot be in the future"):
            LogEntryValidator.validate_timestamp(datetime.now() + timedelta(hours=1))
    
    @pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"])
    def test_validate_level_valid(self, level):
        """Test level validation with valid levels."""
        # Act & Assert - should not raise
        LogEntryValidator.validate_level(level)
        LogEntryValidator.validate_level(level.lower())  # Case insensitive
    
    def test_validate_level_invalid(self):
        """Test level validation with invalid level."""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid log level: INVALID"):
            LogEntryValidator.validate_level("INVALID")
    
    def test_validate_message_valid(self):
        """Test message validation with valid messages."""
        # Act & Assert - should not raise
        LogEntryValidator.validate_message("Valid message")
        LogEntryValidator.validate_message("Another valid message")
    
    def test_validate_message_invalid(self):
        """Test message validation with invalid messages."""
        # Act & Assert - empty message
        with pytest.raises(ValueError, match="Log message cannot be empty"):
            LogEntryValidator.validate_message("")
        
        # Act & Assert - whitespace message
        with pytest.raises(ValueError, match="Log message cannot be empty"):
            LogEntryValidator.validate_message("   ")
    
    def test_validate_source_valid(self):
        """Test source validation with valid sources."""
        # Act & Assert - should not raise
        LogEntryValidator.validate_source("auth")
        LogEntryValidator.validate_source("database")
    
    def test_validate_source_invalid(self):
        """Test source validation with invalid sources."""
        # Act & Assert - empty source
        with pytest.raises(ValueError, match="Log source cannot be empty"):
            LogEntryValidator.validate_source("")
        
        # Act & Assert - whitespace source
        with pytest.raises(ValueError, match="Log source cannot be empty"):
            LogEntryValidator.validate_source("   ")
    
    def test_validate_raw_line_valid(self):
        """Test raw line validation with valid lines."""
        # Act & Assert - should not raise
        LogEntryValidator.validate_raw_line("2023-12-01 10:00:00 INFO Test message")
        LogEntryValidator.validate_raw_line("Another valid line")
    
    def test_validate_raw_line_invalid(self):
        """Test raw line validation with invalid lines."""
        # Act & Assert - empty line
        with pytest.raises(ValueError, match="Raw log line cannot be empty"):
            LogEntryValidator.validate_raw_line("")
        
        # Act & Assert - whitespace line
        with pytest.raises(ValueError, match="Raw log line cannot be empty"):
            LogEntryValidator.validate_raw_line("   ")
    
    def test_validate_metadata_valid(self):
        """Test metadata validation with valid metadata."""
        # Act & Assert - should not raise
        LogEntryValidator.validate_metadata({})
        LogEntryValidator.validate_metadata({"ip": "192.168.1.100", "user": "admin"})
        LogEntryValidator.validate_metadata({"key1": "value1", "key2": 123, "key3": True})
    
    def test_validate_metadata_invalid_type(self):
        """Test metadata validation with invalid type."""
        # Act & Assert
        with pytest.raises(TypeError, match="Metadata must be a dictionary"):
            LogEntryValidator.validate_metadata("not a dict")
        
        with pytest.raises(TypeError, match="Metadata must be a dictionary"):
            LogEntryValidator.validate_metadata(123)
    
    def test_validate_metadata_invalid_keys(self):
        """Test metadata validation with invalid keys."""
        # Act & Assert - non-string key
        with pytest.raises(TypeError, match="Metadata keys must be strings"):
            LogEntryValidator.validate_metadata({123: "value"})
        
        # Act & Assert - empty key
        with pytest.raises(ValueError, match="Metadata keys cannot be empty"):
            LogEntryValidator.validate_metadata({"": "value"})
        
        # Act & Assert - whitespace key
        with pytest.raises(ValueError, match="Metadata keys cannot be empty"):
            LogEntryValidator.validate_metadata({"   ": "value"})


class ConcreteLogParser(BaseLogParser):
    """Concrete implementation of BaseLogParser for testing."""
    
    def parse_line(self, line: str) -> Optional[LogEntry]:
        """Parse a single log line."""
        return LogEntry(
            timestamp=datetime.now(),
            level="INFO",
            message="Test message",
            source="test",
            raw_line=line
        )
    
    def parse_file(self, file_path: str) -> Iterator[LogEntry]:
        """Parse a log file."""
        yield self.parse_line("test line")
    
    def can_parse(self, line: str) -> bool:
        """Check if this parser can handle the given log line."""
        return True


class TestBaseLogParser:
    """Test cases for BaseLogParser class."""
    
    def test_base_log_parser_initialization_with_config(self):
        """Test BaseLogParser initialization with config."""
        # Arrange
        config = {"format": "syslog", "timezone": "UTC"}
        
        # Act
        parser = ConcreteLogParser(config)
        
        # Assert
        assert parser.config == config
        assert parser.get_config_value("format") == "syslog"
        assert parser.get_config_value("timezone") == "UTC"
        assert parser.has_config_key("format") is True
        assert parser.has_config_key("nonexistent") is False
    
    def test_base_log_parser_initialization_without_config(self):
        """Test BaseLogParser initialization without config."""
        # Act
        parser = ConcreteLogParser()
        
        # Assert
        assert parser.config == {}
        assert parser.get_config_value("nonexistent") is None
        assert parser.get_config_value("nonexistent", "default") == "default"
        assert parser.has_config_key("nonexistent") is False
    
    def test_base_log_parser_config_read_only(self):
        """Test that BaseLogParser config is read-only."""
        # Act
        parser = ConcreteLogParser({"key": "value"})
        config = parser.config
        
        # Assert - modifying returned config should not affect original
        config["new_key"] = "new_value"
        assert parser.config == {"key": "value"}
        assert "new_key" not in parser.config
    
    def test_base_log_parser_invalid_config_type(self):
        """Test BaseLogParser with invalid config type."""
        # Act & Assert
        with pytest.raises(TypeError, match="Parser config must be a dictionary"):
            ConcreteLogParser("not a dict")
        
        with pytest.raises(TypeError, match="Parser config must be a dictionary"):
            ConcreteLogParser(123)
    
    def test_base_log_parser_abstract_methods(self):
        """Test that BaseLogParser has required abstract methods."""
        # Assert
        assert hasattr(BaseLogParser, 'parse_line')
        assert hasattr(BaseLogParser, 'parse_file')
        assert hasattr(BaseLogParser, 'can_parse')
        
        # Check that methods are abstract
        assert 'parse_line' in BaseLogParser.__abstractmethods__
        assert 'parse_file' in BaseLogParser.__abstractmethods__
        assert 'can_parse' in BaseLogParser.__abstractmethods__
    
    def test_base_log_parser_cannot_be_instantiated_directly(self):
        """Test that BaseLogParser cannot be instantiated directly."""
        # Act & Assert
        with pytest.raises(TypeError):
            BaseLogParser()