"""
Nginx log parser implementation.

This module provides Nginx access log parsing functionality.
"""

from typing import Optional, Iterator
from datetime import datetime
import re

from .base import LogParser, LogEntry


class NginxParser(LogParser):
    """
    Parser for Nginx access log format.
    
    This class follows the Single Responsibility Principle by focusing solely on
    Nginx log parsing functionality.
    """
    
    # Nginx Common Log Format pattern (similar to Apache)
    NGINX_PATTERN = re.compile(
        r'^(\S+)\s+(\S+)\s+(\S+)\s+\[([^\]]+)\]\s+"([^"]*)"\s+(\d+)\s+(\S+)\s+"([^"]*)"\s+"([^"]*)"$'
    )
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the Nginx parser.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
    
    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Parse a single Nginx log line.
        
        Args:
            line: Raw Nginx log line to parse
            
        Returns:
            Parsed log entry or None if parsing fails
        """
        match = self.NGINX_PATTERN.match(line.strip())
        if not match:
            return None
        
        ip, identity, user, timestamp_str, request, status, size, referer, user_agent = match.groups()
        
        # Parse timestamp
        try:
            timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
        except ValueError:
            try:
                timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")
            except ValueError:
                timestamp = datetime.now()
        
        # Determine log level based on status code
        status_code = int(status)
        if status_code >= 500:
            level = "ERROR"
        elif status_code >= 400:
            level = "WARN"
        else:
            level = "INFO"
        
        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=f"{request} - {status}",
            source="nginx",
            raw_line=line,
            metadata={
                "ip": ip,
                "identity": identity,
                "user": user,
                "status_code": status_code,
                "size": size,
                "request": request,
                "referer": referer,
                "user_agent": user_agent
            }
        )
    
    def parse_file(self, file_path: str) -> Iterator[LogEntry]:
        """
        Parse an Nginx log file.
        
        Args:
            file_path: Path to the Nginx log file
            
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
        return self.NGINX_PATTERN.match(line.strip()) is not None
