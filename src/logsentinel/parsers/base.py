"""
Base classes for log parsers.

This module provides the abstract base classes for log parsing functionality
following SOLID principles and Pythonic design patterns.
"""

from abc import ABC, abstractmethod
from typing import Optional, Iterator, Dict, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """Enumeration of standard log levels following RFC 5424."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntryValidator:
    """Validator for LogEntry data following Single Responsibility Principle."""
    
    @staticmethod
    def validate_timestamp(timestamp: datetime) -> None:
        """Validate timestamp is not in the future."""
        if timestamp > datetime.now():
            raise ValueError("Log timestamp cannot be in the future")
    
    @staticmethod
    def validate_level(level: str) -> None:
        """Validate log level is a standard level."""
        valid_levels = [log_level.value for log_level in LogLevel]
        if level.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}")
    
    @staticmethod
    def validate_message(message: str) -> None:
        """Validate message is not empty."""
        if not message or not message.strip():
            raise ValueError("Log message cannot be empty")
    
    @staticmethod
    def validate_source(source: str) -> None:
        """Validate source is not empty."""
        if not source or not source.strip():
            raise ValueError("Log source cannot be empty")
    
    @staticmethod
    def validate_raw_line(raw_line: str) -> None:
        """Validate raw line is not empty."""
        if not raw_line or not raw_line.strip():
            raise ValueError("Raw log line cannot be empty")
    
    @staticmethod
    def validate_metadata(metadata: Dict[str, Any]) -> None:
        """Validate metadata structure."""
        if not isinstance(metadata, dict):
            raise TypeError("Metadata must be a dictionary")
        
        for key, value in metadata.items():
            if not isinstance(key, str):
                raise TypeError("Metadata keys must be strings")
            if not key.strip():
                raise ValueError("Metadata keys cannot be empty")


@dataclass
class LogEntry:
    """
    Represents a parsed log entry following SOLID principles.
    
    This class follows the Single Responsibility Principle by focusing solely on
    representing log entry data with validation and utility methods.
    """
    
    timestamp: datetime
    level: str
    message: str
    source: str
    raw_line: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize and validate log entry data."""
        self._initialize_metadata()
        self._validate_entry()
    
    def _initialize_metadata(self) -> None:
        """Initialize metadata to empty dict if None."""
        if self.metadata is None:
            self.metadata = {}
    
    def _validate_entry(self) -> None:
        """Validate all log entry fields."""
        LogEntryValidator.validate_timestamp(self.timestamp)
        LogEntryValidator.validate_level(self.level)
        LogEntryValidator.validate_message(self.message)
        LogEntryValidator.validate_source(self.source)
        LogEntryValidator.validate_raw_line(self.raw_line)
        LogEntryValidator.validate_metadata(self.metadata)
    
    def is_error_level(self) -> bool:
        """Check if log level indicates an error."""
        return self.level.upper() in [LogLevel.ERROR.value, LogLevel.CRITICAL.value]
    
    def is_warning_level(self) -> bool:
        """Check if log level indicates a warning."""
        return self.level.upper() == LogLevel.WARN.value
    
    def get_level_priority(self) -> int:
        """Get numeric priority for log level (higher = more important)."""
        level_priorities = {
            LogLevel.DEBUG.value: 1,
            LogLevel.INFO.value: 2,
            LogLevel.WARN.value: 3,
            LogLevel.ERROR.value: 4,
            LogLevel.CRITICAL.value: 5,
        }
        return level_priorities.get(self.level.upper(), 0)
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata key-value pair with validation."""
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Metadata key must be a non-empty string")
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value with default fallback."""
        return self.metadata.get(key, default)
    
    def has_metadata(self, key: str) -> bool:
        """Check if metadata contains a specific key."""
        return key in self.metadata
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert log entry to dictionary representation."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "source": self.source,
            "raw_line": self.raw_line,
            "metadata": self.metadata.copy()
        }


class BaseLogParser(ABC):
    """
    Abstract base class for log parsers following SOLID principles.
    
    This class follows the Open/Closed Principle by providing a stable interface
    that can be extended for different log formats without modification.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the log parser with configuration."""
        self._config = self._initialize_config(config)
        self._validate_config()
    
    def _initialize_config(self, config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Initialize configuration with defaults."""
        return config or {}
    
    def _validate_config(self) -> None:
        """Validate parser configuration."""
        if not isinstance(self._config, dict):
            raise TypeError("Parser config must be a dictionary")
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get parser configuration (read-only)."""
        return self._config.copy()
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value with default fallback."""
        return self._config.get(key, default)
    
    def has_config_key(self, key: str) -> bool:
        """Check if configuration contains a specific key."""
        return key in self._config
    
    @abstractmethod
    def parse_line(self, line: str) -> Optional[LogEntry]:
        """Parse a single log line."""
        pass
    
    @abstractmethod
    def parse_file(self, file_path: str) -> Iterator[LogEntry]:
        """Parse a log file."""
        pass
    
    @abstractmethod
    def can_parse(self, line: str) -> bool:
        """Check if this parser can handle the given log line."""
        pass


# Backward compatibility alias
LogParser = BaseLogParser
