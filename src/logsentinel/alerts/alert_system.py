"""
Alert system for managing security alerts.

This module provides the main alert system for handling security alerts.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from .base import Alert, AlertHandler
from ..rules import RuleResult


class AlertSystem:
    """
    System for managing and handling security alerts.
    
    This class follows the Single Responsibility Principle by focusing solely on
    alert management and routing.
    """
    
    def __init__(self, handlers: Optional[List[AlertHandler]] = None):
        """
        Initialize the alert system.
        
        Args:
            handlers: Optional list of alert handlers
        """
        self.handlers = handlers or []
        self.alert_count = 0
    
    def add_handler(self, handler: AlertHandler) -> None:
        """
        Add an alert handler to the system.
        
        Args:
            handler: Handler to add
        """
        self.handlers.append(handler)
    
    def remove_handler(self, handler: AlertHandler) -> bool:
        """
        Remove an alert handler from the system.
        
        Args:
            handler: Handler to remove
            
        Returns:
            True if handler was removed, False if not found
        """
        try:
            self.handlers.remove(handler)
            return True
        except ValueError:
            return False
    
    def create_alert_from_rule_result(self, rule_result: RuleResult) -> Alert:
        """
        Create an alert from a rule result.
        
        Args:
            rule_result: Rule result to create alert from
            
        Returns:
            Created alert
        """
        self.alert_count += 1
        alert_id = f"alert_{self.alert_count:06d}_{uuid.uuid4().hex[:8]}"
        
        return Alert(
            id=alert_id,
            timestamp=rule_result.timestamp,
            rule_id=rule_result.rule_id,
            rule_name=rule_result.log_entry.source,  # This should be rule name
            severity=rule_result.severity,
            message=rule_result.message,
            log_entry=rule_result.log_entry.raw_line,
            source=rule_result.log_entry.source,
            metadata=rule_result.metadata
        )
    
    def process_rule_result(self, rule_result: RuleResult) -> bool:
        """
        Process a rule result and create/handle alerts.
        
        Args:
            rule_result: Rule result to process
            
        Returns:
            True if alert was processed successfully
        """
        if not rule_result.matched:
            return False
        
        # Create alert from rule result
        alert = self.create_alert_from_rule_result(rule_result)
        
        # Handle alert with all applicable handlers
        success = True
        for handler in self.handlers:
            if handler.can_handle(alert):
                if not handler.handle_alert(alert):
                    success = False
        
        return success
    
    def process_rule_results(self, rule_results: List[RuleResult]) -> int:
        """
        Process multiple rule results and create/handle alerts.
        
        Args:
            rule_results: List of rule results to process
            
        Returns:
            Number of alerts processed successfully
        """
        processed_count = 0
        
        for rule_result in rule_results:
            if self.process_rule_result(rule_result):
                processed_count += 1
        
        return processed_count
    
    def get_handler_count(self) -> int:
        """
        Get the number of alert handlers.
        
        Returns:
            Number of handlers
        """
        return len(self.handlers)
    
    def get_alert_count(self) -> int:
        """
        Get the total number of alerts created.
        
        Returns:
            Number of alerts
        """
        return self.alert_count
