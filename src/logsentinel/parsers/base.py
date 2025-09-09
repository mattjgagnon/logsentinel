"""
Base classes for log parsers.

This module provides the abstract base classes for log parsing functionality.
"""

from abc import ABC, abstractmethod
from typing import Optional, Iterator
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    """
    Represents a parsed log entry.
    
    This class follows the Single Responsibility Principle by focusing solely on
    representing log entry data.
    """
    
    timestamp: datetime
    level: str
    message: str
    source: str
    raw_line: str
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class LogParser(ABC):
    """
    Abstract base class for log parsers.
    
    This class follows the Open/Closed Principle by providing a stable interface
    that can be extended for different log formats without modification.
    """
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the log parser.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
    
    @abstractmethod
    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Parse a single log line.
        
        Args:
            line: Raw log line to parse
            
        Returns:
            Parsed log entry or None if parsing fails
        """
        pass
    
    @abstractmethod
    def parse_file(self, file_path: str) -> Iterator[LogEntry]:
        """
        Parse a log file.
        
        Args:
            file_path: Path to the log file
            
        Yields:
            Parsed log entries
        """
        pass
    
    @abstractmethod
    def can_parse(self, line: str) -> bool:
        """
        Check if this parser can handle the given log line.
        
        Args:
            line: Log line to check
            
        Returns:
            True if this parser can handle the line
        """
        pass
