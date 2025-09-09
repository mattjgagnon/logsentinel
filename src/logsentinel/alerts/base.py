"""
Base classes for alert system.

This module provides the abstract base classes for alert functionality.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Alert:
    """
    Represents a security alert.
    
    This class follows the Single Responsibility Principle by focusing solely on
    representing alert data.
    """
    
    id: str
    timestamp: datetime
    rule_id: str
    rule_name: str
    severity: str
    message: str
    log_entry: str
    source: str
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class AlertHandler(ABC):
    """
    Abstract base class for alert handlers.
    
    This class follows the Open/Closed Principle by providing a stable interface
    that can be extended for different alert output formats without modification.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the alert handler.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
    
    @abstractmethod
    def handle_alert(self, alert: Alert) -> bool:
        """
        Handle a security alert.
        
        Args:
            alert: Alert to handle
            
        Returns:
            True if alert was handled successfully
        """
        pass
    
    @abstractmethod
    def can_handle(self, alert: Alert) -> bool:
        """
        Check if this handler can handle the given alert.
        
        Args:
            alert: Alert to check
            
        Returns:
            True if this handler can handle the alert
        """
        pass
