"""
Syslog parser implementation.

This module provides syslog parsing functionality.
"""

from typing import Optional, Iterator
from datetime import datetime
import re

from .base import LogParser, LogEntry


class SyslogParser(LogParser):
    """
    Parser for syslog format logs.
    
    This class follows the Single Responsibility Principle by focusing solely on
    syslog parsing functionality.
    """
    
    # Syslog pattern: timestamp hostname service: message
    SYSLOG_PATTERN = re.compile(
        r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+):\s*(.*)$'
    )
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the syslog parser.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
    
    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Parse a single syslog line.
        
        Args:
            line: Raw syslog line to parse
            
        Returns:
            Parsed log entry or None if parsing fails
        """
        match = self.SYSLOG_PATTERN.match(line.strip())
        if not match:
            return None
        
        timestamp_str, hostname, service, message = match.groups()
        
        # Parse timestamp (simplified - assumes current year)
        try:
            timestamp = datetime.strptime(f"{datetime.now().year} {timestamp_str}", "%Y %b %d %H:%M:%S")
        except ValueError:
            # If parsing fails, use current time
            timestamp = datetime.now()
        
        return LogEntry(
            timestamp=timestamp,
            level="INFO",  # Syslog doesn't always include level
            message=message,
            source=f"{hostname}:{service}",
            raw_line=line,
            metadata={"hostname": hostname, "service": service}
        )
    
    def parse_file(self, file_path: str) -> Iterator[LogEntry]:
        """
        Parse a syslog file.
        
        Args:
            file_path: Path to the syslog file
            
        Yields:
            Parsed log entries
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        entry = self.parse_line(line)
                        if entry:
                            entry.metadata["line_number"] = line_num
                            yield entry
        except FileNotFoundError:
            raise FileNotFoundError(f"Log file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error parsing log file {file_path}: {e}")
    
    def can_parse(self, line: str) -> bool:
        """
        Check if this parser can handle the given log line.
        
        Args:
            line: Log line to check
            
        Returns:
            True if this parser can handle the line
        """
        return self.SYSLOG_PATTERN.match(line.strip()) is not None
