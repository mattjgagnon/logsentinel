"""
Pattern-based security rule implementation.

This module provides pattern matching for security rules.
"""

from typing import Optional, List
from datetime import datetime

from .base import Rule, RuleResult
from ..parsers import LogEntry


class PatternRule(Rule):
    """
    Rule that matches log entries using multiple patterns.
    
    This class follows the Single Responsibility Principle by focusing solely on
    pattern-based matching with multiple conditions.
    """
    
    def __init__(self, rule_id: str, name: str, patterns: List[str], 
                 severity: str, match_all: bool = True, enabled: bool = True):
        """
        Initialize the pattern rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Human-readable rule name
            patterns: List of patterns to match
            severity: Rule severity level
            match_all: Whether all patterns must match (AND) or any pattern (OR)
            enabled: Whether the rule is enabled
        """
        super().__init__(rule_id, name, severity, enabled)
        self.patterns = patterns
        self.match_all = match_all
    
    def evaluate(self, log_entry: LogEntry) -> Optional[RuleResult]:
        """
        Evaluate the pattern rule against a log entry.
        
        Args:
            log_entry: Log entry to evaluate
            
        Returns:
            Rule result if patterns match, None otherwise
        """
        if not self.is_enabled():
            return None
        
        matches = []
        for pattern in self.patterns:
            if pattern.lower() in log_entry.message.lower():
                matches.append(pattern)
        
        # Check if conditions are met
        if self.match_all:
            # All patterns must match
            if len(matches) == len(self.patterns):
                return RuleResult(
                    rule_id=self.rule_id,
                    matched=True,
                    severity=self.severity,
                    message=f"All patterns matched: {', '.join(matches)}",
                    timestamp=datetime.now(),
                    log_entry=log_entry,
                    metadata={
                        "patterns": self.patterns,
                        "matched_patterns": matches,
                        "match_all": self.match_all
                    }
                )
        else:
            # Any pattern can match
            if matches:
                return RuleResult(
                    rule_id=self.rule_id,
                    matched=True,
                    severity=self.severity,
                    message=f"Patterns matched: {', '.join(matches)}",
                    timestamp=datetime.now(),
                    log_entry=log_entry,
                    metadata={
                        "patterns": self.patterns,
                        "matched_patterns": matches,
                        "match_all": self.match_all
                    }
                )
        
        return None
