"""
Rule configuration data classes.

This module provides rule configuration data classes for the application.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class SeverityLevel(str, Enum):
    """Severity levels for security rules."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "critical"


class RuleType(str, Enum):
    """Types of security rules."""
    
    REGEX = "regex"
    THRESHOLD = "threshold"
    PATTERN = "pattern"


@dataclass
class RuleConfig:
    """Individual rule configuration model."""
    
    id: str
    name: str
    description: Optional[str] = None
    type: RuleType = RuleType.REGEX
    pattern: str = ""
    severity: SeverityLevel = SeverityLevel.MEDIUM
    enabled: bool = True
    category: Optional[str] = None
    
    # Optional fields for threshold rules
    threshold: Optional[int] = None
    time_window: Optional[int] = None
    
    # Additional metadata
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RuleCategory:
    """Rule category configuration model."""
    
    name: str
    description: str
    color: Optional[str] = None


@dataclass
class RulesFileConfig:
    """Complete rules file configuration model."""
    
    rules: List[RuleConfig] = None
    categories: Dict[str, RuleCategory] = None
    
    def __post_init__(self):
        if self.rules is None:
            self.rules = []
        if self.categories is None:
            self.categories = {}
