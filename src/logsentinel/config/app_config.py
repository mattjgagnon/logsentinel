"""
Application configuration data classes.

This module provides configuration data classes following SOLID principles.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


class ConfigDefaults:
    """Default configuration values following Open/Closed Principle."""
    
    # App defaults
    APP_NAME = "LogSentinel"
    APP_VERSION = "0.1.0"
    APP_DESCRIPTION = "Advanced log security analysis platform"
    DEFAULT_LOG_LEVEL = "INFO"
    
    # Parser defaults
    DEFAULT_FORMAT = "syslog"
    SUPPORTED_FORMATS = ["syslog", "apache", "nginx"]
    BUFFER_SIZE = 8192
    MAX_LINE_LENGTH = 4096
    
    # Rules defaults
    RULES_DIRECTORY = "/app/rules"
    AUTO_RELOAD = True
    RELOAD_INTERVAL = 60
    MAX_RULES = 1000
    RULE_TIMEOUT = 30
    
    # Alerts defaults
    DEFAULT_HANDLERS = ["console", "file"]
    OUTPUT_FILE = "/app/logs/alerts.log"
    MAX_ALERTS_PER_MINUTE = 100
    ALERT_RETENTION_DAYS = 30


class BaseConfigValidator(ABC):
    """Abstract validator following Interface Segregation Principle."""
    
    @abstractmethod
    def validate(self, config: Any) -> None:
        pass


class ConfigValidator(BaseConfigValidator):
    """Configuration validator following Single Responsibility Principle."""
    
    @staticmethod
    def validate_positive_int(value: int, field_name: str) -> None:
        """Validate that an integer value is positive."""
        if value < 0:
            raise ValueError(f"{field_name} must be positive, got {value}")
    
    @staticmethod
    def validate_non_empty_string(value: str, field_name: str) -> None:
        """Validate that a string value is not empty."""
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
    
    @staticmethod
    def validate_non_empty_list(value: List[str], field_name: str) -> None:
        """Validate that a list contains non-empty strings."""
        if not value:
            raise ValueError(f"{field_name} cannot be empty")
        if any(not item.strip() for item in value):
            raise ValueError(f"{field_name} cannot contain empty strings")
    
    def validate(self, config: Any) -> None:
        if isinstance(config, ParserConfig):
            self._validate_parser_config(config)
        elif isinstance(config, AlertsConfig):
            self._validate_alerts_config(config)
        elif isinstance(config, RulesConfig):
            self._validate_rules_config(config)
        elif isinstance(config, AppConfig):
            self._validate_app_config(config)
    
    def _validate_parser_config(self, config: 'ParserConfig') -> None:
        self.validate_non_empty_string(config.default_format, "default_format")
        self.validate_positive_int(config.buffer_size, "buffer_size")
        self.validate_positive_int(config.max_line_length, "max_line_length")
        # Note: supported_formats can be empty, so we don't validate it
    
    def _validate_alerts_config(self, config: 'AlertsConfig') -> None:
        self.validate_positive_int(config.max_alerts_per_minute, "max_alerts_per_minute")
        self.validate_positive_int(config.alert_retention_days, "alert_retention_days")
        self.validate_non_empty_string(config.output_file, "output_file")
        # Note: handlers can be empty, so we don't validate it
    
    def _validate_rules_config(self, config: 'RulesConfig') -> None:
        self.validate_non_empty_string(config.directory, "directory")
        self.validate_positive_int(config.reload_interval, "reload_interval")
        self.validate_positive_int(config.max_rules, "max_rules")
        self.validate_positive_int(config.rule_timeout, "rule_timeout")
    
    def _validate_app_config(self, config: 'AppConfig') -> None:
        self.validate_non_empty_string(config.name, "name")
        self.validate_non_empty_string(config.version, "version")
        if config.description:
            self.validate_non_empty_string(config.description, "description")
        self.validate_non_empty_string(config.log_level, "log_level")


@dataclass
class AppConfig:
    """Application configuration model following Single Responsibility Principle."""
    
    name: str = ConfigDefaults.APP_NAME
    version: str = ConfigDefaults.APP_VERSION
    description: Optional[str] = ConfigDefaults.APP_DESCRIPTION
    log_level: str = ConfigDefaults.DEFAULT_LOG_LEVEL
    
    def validate(self) -> None:
        ConfigValidator()._validate_app_config(self)


@dataclass
class ParserConfig:
    """Parser configuration model following Single Responsibility Principle."""
    
    default_format: str = ConfigDefaults.DEFAULT_FORMAT
    supported_formats: List[str] = field(default_factory=lambda: ConfigDefaults.SUPPORTED_FORMATS.copy())
    buffer_size: int = ConfigDefaults.BUFFER_SIZE
    max_line_length: int = ConfigDefaults.MAX_LINE_LENGTH
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ConfigDefaults.SUPPORTED_FORMATS.copy()
    
    def validate(self) -> None:
        ConfigValidator()._validate_parser_config(self)


@dataclass
class RulesConfig:
    """Rules configuration model following Single Responsibility Principle."""
    
    directory: str = ConfigDefaults.RULES_DIRECTORY
    auto_reload: bool = ConfigDefaults.AUTO_RELOAD
    reload_interval: int = ConfigDefaults.RELOAD_INTERVAL
    max_rules: int = ConfigDefaults.MAX_RULES
    rule_timeout: int = ConfigDefaults.RULE_TIMEOUT
    
    def validate(self) -> None:
        ConfigValidator()._validate_rules_config(self)


@dataclass
class AlertsConfig:
    """Alerts configuration model following Single Responsibility Principle."""
    
    handlers: List[str] = field(default_factory=lambda: ConfigDefaults.DEFAULT_HANDLERS.copy())
    output_file: str = ConfigDefaults.OUTPUT_FILE
    max_alerts_per_minute: int = ConfigDefaults.MAX_ALERTS_PER_MINUTE
    alert_retention_days: int = ConfigDefaults.ALERT_RETENTION_DAYS
    
    def __post_init__(self):
        if self.handlers is None:
            self.handlers = ConfigDefaults.DEFAULT_HANDLERS.copy()
    
    def validate(self) -> None:
        ConfigValidator()._validate_alerts_config(self)
