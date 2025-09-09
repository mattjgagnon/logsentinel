"""
Unit tests for LogParser abstract base class.

This module tests the LogParser abstract base class and its concrete implementations.
Following TDD principles - tests are written before implementation.
"""

import pytest
from abc import ABC
from unittest.mock import Mock, patch
from logsentinel.parsers.base import LogParser, LogEntry
from datetime import datetime


class ConcreteLogParser(LogParser):
    """Concrete implementation of LogParser for testing."""
    
    def parse_line(self, line: str) -> LogEntry:
        """Parse a single log line."""
        return LogEntry(
            timestamp=datetime.now(),
            level="INFO",
            message=line,
            source="test",
            raw_line=line
        )
    
    def parse_file(self, file_path: str):
        """Parse a log file."""
        yield self.parse_line("test line")
    
    def can_parse(self, line: str) -> bool:
        """Check if this parser can handle the given log line."""
        return True


class TestLogParser:
    """Test cases for LogParser abstract base class."""

    def test_log_parser_is_abstract_base_class(self):
        """Test that LogParser is an abstract base class."""
        # Assert
        assert issubclass(LogParser, ABC)
        assert hasattr(LogParser, '__abstractmethods__')

    def test_log_parser_cannot_be_instantiated_directly(self):
        """Test that LogParser cannot be instantiated directly."""
        # Act & Assert
        with pytest.raises(TypeError):
            LogParser()

    def test_concrete_log_parser_can_be_instantiated(self):
        """Test that concrete LogParser implementations can be instantiated."""
        # Act
        parser = ConcreteLogParser()
        
        # Assert
        assert isinstance(parser, LogParser)
        assert parser.config == {}

    def test_log_parser_initialization_with_config(self):
        """Test that LogParser can be initialized with configuration."""
        # Arrange
        config = {"format": "syslog", "timezone": "UTC"}
        
        # Act
        parser = ConcreteLogParser(config)
        
        # Assert
        assert parser.config == config

    def test_log_parser_initialization_without_config_defaults_to_empty_dict(self):
        """Test that LogParser defaults config to empty dict when not provided."""
        # Act
        parser = ConcreteLogParser()
        
        # Assert
        assert parser.config == {}

    def test_concrete_log_parser_parse_line_returns_log_entry(self):
        """Test that concrete LogParser parse_line returns LogEntry."""
        # Arrange
        parser = ConcreteLogParser()
        test_line = "2023-12-01 10:00:00 INFO Test message"
        
        # Act
        result = parser.parse_line(test_line)
        
        # Assert
        assert isinstance(result, LogEntry)
        assert result.message == test_line
        assert result.raw_line == test_line
        assert result.source == "test"

    def test_concrete_log_parser_parse_file_yields_log_entries(self):
        """Test that concrete LogParser parse_file yields LogEntry objects."""
        # Arrange
        parser = ConcreteLogParser()
        
        # Act
        results = list(parser.parse_file("test.log"))
        
        # Assert
        assert len(results) == 1
        assert isinstance(results[0], LogEntry)
        assert results[0].message == "test line"

    def test_concrete_log_parser_can_parse_returns_boolean(self):
        """Test that concrete LogParser can_parse returns boolean."""
        # Arrange
        parser = ConcreteLogParser()
        
        # Act
        result = parser.can_parse("any line")
        
        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_log_parser_abstract_methods_are_defined(self):
        """Test that LogParser defines all required abstract methods."""
        # Assert
        assert hasattr(LogParser, 'parse_line')
        assert hasattr(LogParser, 'parse_file')
        assert hasattr(LogParser, 'can_parse')
        
        # Check that methods are abstract
        assert 'parse_line' in LogParser.__abstractmethods__
        assert 'parse_file' in LogParser.__abstractmethods__
        assert 'can_parse' in LogParser.__abstractmethods__

    def test_log_parser_method_signatures(self):
        """Test that LogParser methods have correct signatures."""
        # Arrange
        parser = ConcreteLogParser()
        
        # Act & Assert - These should not raise exceptions
        parser.parse_line("test")
        list(parser.parse_file("test.log"))
        parser.can_parse("test")
