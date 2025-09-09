"""
Base classes for security rules.

This module provides the abstract base classes for rule functionality.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from ..parsers import LogEntry


@dataclass
class RuleResult:
    """
    Represents the result of a rule evaluation.
    
    This class follows the Single Responsibility Principle by focusing solely on
    representing rule evaluation results.
    """
    
    rule_id: str
    matched: bool
    severity: str
    message: str
    timestamp: datetime
    log_entry: LogEntry
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Rule(ABC):
    """
    Abstract base class for security rules.
    
    This class follows the Open/Closed Principle by providing a stable interface
    that can be extended for different rule types without modification.
    """
    
    def __init__(self, rule_id: str, name: str, severity: str, enabled: bool = True):
        """
        Initialize the rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Human-readable rule name
            severity: Rule severity level
            enabled: Whether the rule is enabled
        """
        self.rule_id = rule_id
        self.name = name
        self.severity = severity
        self.enabled = enabled
    
    @abstractmethod
    def evaluate(self, log_entry: LogEntry) -> Optional[RuleResult]:
        """
        Evaluate the rule against a log entry.
        
        Args:
            log_entry: Log entry to evaluate
            
        Returns:
            Rule result if rule matches, None otherwise
        """
        pass
    
    def is_enabled(self) -> bool:
        """
        Check if the rule is enabled.
        
        Returns:
            True if the rule is enabled
        """
        return self.enabled
