"""
Alert handlers for different output formats.

This module provides various alert handlers for different output destinations.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import json

from .base import Alert, AlertHandler


class ConsoleHandler(AlertHandler):
    """
    Handler for outputting alerts to the console.
    
    This class follows the Single Responsibility Principle by focusing solely on
    console output functionality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the console handler.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self.format = self.config.get('format', 'simple')  # simple, json, detailed
    
    def handle_alert(self, alert: Alert) -> bool:
        """
        Handle an alert by outputting to console.
        
        Args:
            alert: Alert to handle
            
        Returns:
            True if alert was handled successfully
        """
        try:
            if self.format == 'json':
                self._output_json(alert)
            elif self.format == 'detailed':
                self._output_detailed(alert)
            else:
                self._output_simple(alert)
            return True
        except Exception:
            return False
    
    def can_handle(self, alert: Alert) -> bool:
        """
        Check if this handler can handle the given alert.
        
        Args:
            alert: Alert to check
            
        Returns:
            True (console can handle all alerts)
        """
        return True
    
    def _output_simple(self, alert: Alert) -> None:
        """Output alert in simple format."""
        print(f"[{alert.severity.upper()}] {alert.timestamp} - {alert.message}")
    
    def _output_detailed(self, alert: Alert) -> None:
        """Output alert in detailed format."""
        print(f"""
ALERT: {alert.id}
Time: {alert.timestamp}
Rule: {alert.rule_name} ({alert.rule_id})
Severity: {alert.severity.upper()}
Message: {alert.message}
Source: {alert.source}
Log Entry: {alert.log_entry}
""")
    
    def _output_json(self, alert: Alert) -> None:
        """Output alert in JSON format."""
        alert_data = {
            'id': alert.id,
            'timestamp': alert.timestamp.isoformat(),
            'rule_id': alert.rule_id,
            'rule_name': alert.rule_name,
            'severity': alert.severity,
            'message': alert.message,
            'source': alert.source,
            'log_entry': alert.log_entry,
            'metadata': alert.metadata
        }
        print(json.dumps(alert_data, indent=2))


class FileHandler(AlertHandler):
    """
    Handler for outputting alerts to a file.
    
    This class follows the Single Responsibility Principle by focusing solely on
    file output functionality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the file handler.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self.file_path = self.config.get('file_path', 'alerts.log')
        self.format = self.config.get('format', 'simple')
    
    def handle_alert(self, alert: Alert) -> bool:
        """
        Handle an alert by writing to file.
        
        Args:
            alert: Alert to handle
            
        Returns:
            True if alert was handled successfully
        """
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                if self.format == 'json':
                    self._write_json(f, alert)
                else:
                    self._write_simple(f, alert)
            return True
        except Exception:
            return False
    
    def can_handle(self, alert: Alert) -> bool:
        """
        Check if this handler can handle the given alert.
        
        Args:
            alert: Alert to check
            
        Returns:
            True (file can handle all alerts)
        """
        return True
    
    def _write_simple(self, file, alert: Alert) -> None:
        """Write alert in simple format to file."""
        file.write(f"[{alert.severity.upper()}] {alert.timestamp} - {alert.message}\n")
    
    def _write_json(self, file, alert: Alert) -> None:
        """Write alert in JSON format to file."""
        alert_data = {
            'id': alert.id,
            'timestamp': alert.timestamp.isoformat(),
            'rule_id': alert.rule_id,
            'rule_name': alert.rule_name,
            'severity': alert.severity,
            'message': alert.message,
            'source': alert.source,
            'log_entry': alert.log_entry,
            'metadata': alert.metadata
        }
        file.write(json.dumps(alert_data) + '\n')


class WebhookHandler(AlertHandler):
    """
    Handler for sending alerts via webhook.
    
    This class follows the Single Responsibility Principle by focusing solely on
    webhook functionality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the webhook handler.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self.webhook_url = self.config.get('webhook_url')
        self.timeout = self.config.get('timeout', 30)
    
    def handle_alert(self, alert: Alert) -> bool:
        """
        Handle an alert by sending webhook.
        
        Args:
            alert: Alert to handle
            
        Returns:
            True if alert was handled successfully
        """
        if not self.webhook_url:
            return False
        
        try:
            # This would use requests library in a real implementation
            # For now, just simulate success
            alert_data = {
                'id': alert.id,
                'timestamp': alert.timestamp.isoformat(),
                'rule_id': alert.rule_id,
                'rule_name': alert.rule_name,
                'severity': alert.severity,
                'message': alert.message,
                'source': alert.source,
                'log_entry': alert.log_entry,
                'metadata': alert.metadata
            }
            
            # Simulate webhook call
            print(f"Webhook sent to {self.webhook_url}: {alert_data}")
            return True
        except Exception:
            return False
    
    def can_handle(self, alert: Alert) -> bool:
        """
        Check if this handler can handle the given alert.
        
        Args:
            alert: Alert to check
            
        Returns:
            True if webhook URL is configured
        """
        return self.webhook_url is not None
