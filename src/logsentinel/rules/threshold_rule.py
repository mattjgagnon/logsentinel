"""
Threshold-based security rule implementation.

This module provides threshold-based pattern matching for security rules.
"""

from typing import Optional, Dict, List
from datetime import datetime, timedelta
from collections import defaultdict

from .base import Rule, RuleResult
from ..parsers import LogEntry


class ThresholdRule(Rule):
    """
    Rule that matches log entries based on occurrence thresholds.
    
    This class follows the Single Responsibility Principle by focusing solely on
    threshold-based pattern matching.
    """
    
    def __init__(self, rule_id: str, name: str, pattern: str, threshold: int, 
                 time_window: int, severity: str, enabled: bool = True):
        """
        Initialize the threshold rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Human-readable rule name
            pattern: Pattern to match (can be regex or simple string)
            threshold: Number of occurrences to trigger the rule
            time_window: Time window in seconds
            severity: Rule severity level
            enabled: Whether the rule is enabled
        """
        super().__init__(rule_id, name, severity, enabled)
        self.pattern = pattern
        self.threshold = threshold
        self.time_window = time_window
        
        # Track occurrences by source (IP, user, etc.)
        self.occurrences: Dict[str, List[datetime]] = defaultdict(list)
    
    def evaluate(self, log_entry: LogEntry) -> Optional[RuleResult]:
        """
        Evaluate the threshold rule against a log entry.
        
        Args:
            log_entry: Log entry to evaluate
            
        Returns:
            Rule result if threshold is exceeded, None otherwise
        """
        if not self.is_enabled():
            return None
        
        # Check if the pattern matches
        if self.pattern.lower() not in log_entry.message.lower():
            return None
        
        # Get source identifier (IP, user, etc.)
        source = self._get_source_identifier(log_entry)
        
        # Add current occurrence
        now = datetime.now()
        self.occurrences[source].append(now)
        
        # Clean old occurrences outside time window
        cutoff_time = now - timedelta(seconds=self.time_window)
        self.occurrences[source] = [
            ts for ts in self.occurrences[source] if ts > cutoff_time
        ]
        
        # Check if threshold is exceeded
        if len(self.occurrences[source]) >= self.threshold:
            return RuleResult(
                rule_id=self.rule_id,
                matched=True,
                severity=self.severity,
                message=f"Threshold exceeded: {len(self.occurrences[source])} occurrences in {self.time_window}s",
                timestamp=now,
                log_entry=log_entry,
                metadata={
                    "pattern": self.pattern,
                    "threshold": self.threshold,
                    "time_window": self.time_window,
                    "occurrences": len(self.occurrences[source]),
                    "source": source
                }
            )
        
        return None
    
    def _get_source_identifier(self, log_entry: LogEntry) -> str:
        """
        Get a source identifier for the log entry.
        
        Args:
            log_entry: Log entry to get source from
            
        Returns:
            Source identifier string
        """
        # Try to get IP from metadata first
        if "ip" in log_entry.metadata:
            return log_entry.metadata["ip"]
        
        # Fall back to source field
        return log_entry.source
