"""
Application configuration data classes.

This module provides configuration data classes for the application.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Application configuration model."""
    
    name: str = "LogSentinel"
    version: str = "0.1.0"
    description: Optional[str] = "Advanced log security analysis platform"
    log_level: str = "INFO"


@dataclass
class ParserConfig:
    """Parser configuration model."""
    
    default_format: str = "syslog"
    supported_formats: List[str] = None
    buffer_size: int = 8192
    max_line_length: int = 4096
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ["syslog", "apache", "nginx"]


@dataclass
class RulesConfig:
    """Rules configuration model."""
    
    directory: str = "/app/rules"
    auto_reload: bool = True
    reload_interval: int = 60
    max_rules: int = 1000
    rule_timeout: int = 30


@dataclass
class AlertsConfig:
    """Alerts configuration model."""
    
    handlers: List[str] = None
    output_file: str = "/app/logs/alerts.log"
    max_alerts_per_minute: int = 100
    alert_retention_days: int = 30
    
    def __post_init__(self):
        if self.handlers is None:
            self.handlers = ["console", "file"]
