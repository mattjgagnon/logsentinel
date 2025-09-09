"""
Regex-based security rule implementation.

This module provides regex pattern matching for security rules.
"""

import re
from typing import Optional
from datetime import datetime

from .base import Rule, RuleResult
from ..parsers import LogEntry


class RegexRule(Rule):
    """
    Rule that matches log entries using regular expressions.
    
    This class follows the Single Responsibility Principle by focusing solely on
    regex-based pattern matching.
    """
    
    def __init__(self, rule_id: str, name: str, pattern: str, severity: str, 
                 enabled: bool = True, case_sensitive: bool = False):
        """
        Initialize the regex rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Human-readable rule name
            pattern: Regex pattern to match
            severity: Rule severity level
            enabled: Whether the rule is enabled
            case_sensitive: Whether pattern matching is case sensitive
        """
        super().__init__(rule_id, name, severity, enabled)
        self.pattern = pattern
        self.case_sensitive = case_sensitive
        
        # Compile regex pattern
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            self.compiled_pattern = re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
    
    def evaluate(self, log_entry: LogEntry) -> Optional[RuleResult]:
        """
        Evaluate the regex rule against a log entry.
        
        Args:
            log_entry: Log entry to evaluate
            
        Returns:
            Rule result if pattern matches, None otherwise
        """
        if not self.is_enabled():
            return None
        
        # Search in the log message
        if self.compiled_pattern.search(log_entry.message):
            return RuleResult(
                rule_id=self.rule_id,
                matched=True,
                severity=self.severity,
                message=f"Regex pattern '{self.pattern}' matched in log message",
                timestamp=datetime.now(),
                log_entry=log_entry,
                metadata={
                    "pattern": self.pattern,
                    "case_sensitive": self.case_sensitive
                }
            )
        
        return None
