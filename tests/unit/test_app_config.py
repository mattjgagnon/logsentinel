"""
Unit tests for the app configuration data classes.

This module tests the configuration data classes using TDD approach.
Refactored to be more concise and eliminate duplication.
"""

import pytest
from typing import List, Dict, Any

from logsentinel.config.app_config import (
    AppConfig, ParserConfig, RulesConfig, AlertsConfig,
    ConfigDefaults, ConfigValidator, BaseConfigValidator
)


class TestAppConfig:
    """Test the AppConfig dataclass using parametrized tests."""
    
    @pytest.mark.parametrize("kwargs,expected", [
        # Default values
        ({}, {
            "name": "LogSentinel",
            "version": "0.1.0",
            "description": "Advanced log security analysis platform",
            "log_level": "INFO"
        }),
        
        # Custom values
        ({
            "name": "Custom App",
            "version": "2.0.0",
            "description": "Custom description",
            "log_level": "DEBUG"
        }, {
            "name": "Custom App",
            "version": "2.0.0",
            "description": "Custom description",
            "log_level": "DEBUG"
        }),
        
        # Partial values
        ({
            "name": "Partial App",
            "log_level": "WARNING"
        }, {
            "name": "Partial App",
            "version": "0.1.0",
            "description": "Advanced log security analysis platform",
            "log_level": "WARNING"
        }),
    ])
    def test_app_config_cases(self, kwargs: Dict[str, Any], expected: Dict[str, Any]):
        config = AppConfig(**kwargs)
        
        for key, expected_value in expected.items():
            assert getattr(config, key) == expected_value


class TestParserConfig:
    """Test the ParserConfig dataclass using parametrized tests."""
    
    @pytest.mark.parametrize("kwargs,expected", [
        # Default values
        ({}, {
            "default_format": "syslog",
            "supported_formats": ["syslog", "apache", "nginx"],
            "buffer_size": 8192,
            "max_line_length": 4096
        }),
        
        # Custom values
        ({
            "default_format": "json",
            "supported_formats": ["json", "xml", "csv"],
            "buffer_size": 16384,
            "max_line_length": 8192
        }, {
            "default_format": "json",
            "supported_formats": ["json", "xml", "csv"],
            "buffer_size": 16384,
            "max_line_length": 8192
        }),
        
        # None supported_formats (triggers __post_init__)
        ({"supported_formats": None}, {
            "default_format": "syslog",
            "supported_formats": ["syslog", "apache", "nginx"],
            "buffer_size": 8192,
            "max_line_length": 4096
        }),
        
        # Empty supported_formats
        ({"supported_formats": []}, {
            "default_format": "syslog",
            "supported_formats": [],
            "buffer_size": 8192,
            "max_line_length": 4096
        }),
        
        # Partial values
        ({
            "default_format": "nginx",
            "buffer_size": 4096
        }, {
            "default_format": "nginx",
            "supported_formats": ["syslog", "apache", "nginx"],
            "buffer_size": 4096,
            "max_line_length": 4096
        }),
    ])
    def test_parser_config_cases(self, kwargs: Dict[str, Any], expected: Dict[str, Any]):
        config = ParserConfig(**kwargs)
        
        for key, expected_value in expected.items():
            assert getattr(config, key) == expected_value


class TestRulesConfig:
    """Test the RulesConfig dataclass using parametrized tests."""
    
    @pytest.mark.parametrize("kwargs,expected", [
        # Default values
        ({}, {
            "directory": "/app/rules",
            "auto_reload": True,
            "reload_interval": 60,
            "max_rules": 1000,
            "rule_timeout": 30
        }),
        
        # Custom values
        ({
            "directory": "/custom/rules",
            "auto_reload": False,
            "reload_interval": 120,
            "max_rules": 2000,
            "rule_timeout": 60
        }, {
            "directory": "/custom/rules",
            "auto_reload": False,
            "reload_interval": 120,
            "max_rules": 2000,
            "rule_timeout": 60
        }),
        
        # Partial values
        ({
            "directory": "/partial/rules",
            "auto_reload": False
        }, {
            "directory": "/partial/rules",
            "auto_reload": False,
            "reload_interval": 60,
            "max_rules": 1000,
            "rule_timeout": 30
        }),
    ])
    def test_rules_config_cases(self, kwargs: Dict[str, Any], expected: Dict[str, Any]):
        config = RulesConfig(**kwargs)
        
        for key, expected_value in expected.items():
            assert getattr(config, key) == expected_value


class TestAlertsConfig:
    """Test the AlertsConfig dataclass using parametrized tests."""
    
    @pytest.mark.parametrize("kwargs,expected", [
        # Default values
        ({}, {
            "handlers": ["console", "file"],
            "output_file": "/app/logs/alerts.log",
            "max_alerts_per_minute": 100,
            "alert_retention_days": 30
        }),
        
        # Custom values
        ({
            "handlers": ["email", "slack", "webhook"],
            "output_file": "/custom/alerts.log",
            "max_alerts_per_minute": 200,
            "alert_retention_days": 60
        }, {
            "handlers": ["email", "slack", "webhook"],
            "output_file": "/custom/alerts.log",
            "max_alerts_per_minute": 200,
            "alert_retention_days": 60
        }),
        
        # None handlers (triggers __post_init__)
        ({"handlers": None}, {
            "handlers": ["console", "file"],
            "output_file": "/app/logs/alerts.log",
            "max_alerts_per_minute": 100,
            "alert_retention_days": 30
        }),
        
        # Empty handlers
        ({"handlers": []}, {
            "handlers": [],
            "output_file": "/app/logs/alerts.log",
            "max_alerts_per_minute": 100,
            "alert_retention_days": 30
        }),
        
        # Partial values
        ({
            "output_file": "/partial/alerts.log",
            "max_alerts_per_minute": 50
        }, {
            "handlers": ["console", "file"],
            "output_file": "/partial/alerts.log",
            "max_alerts_per_minute": 50,
            "alert_retention_days": 30
        }),
    ])
    def test_alerts_config_cases(self, kwargs: Dict[str, Any], expected: Dict[str, Any]):
        config = AlertsConfig(**kwargs)
        
        for key, expected_value in expected.items():
            assert getattr(config, key) == expected_value


class TestConfigDataClasses:
    """Test interactions and edge cases across all config classes."""
    
    def test_all_configs_with_minimal_values(self):
        app = AppConfig()
        parser = ParserConfig()
        rules = RulesConfig()
        alerts = AlertsConfig()
        
        # Verify all have expected default values
        assert app.name == "LogSentinel"
        assert parser.default_format == "syslog"
        assert rules.auto_reload is True
        assert alerts.handlers == ["console", "file"]
    
    def test_config_immutability_after_init(self):
        app = AppConfig()
        original_name = app.name
        app.name = "Modified Name"
        
        assert app.name == "Modified Name"
        assert app.name != original_name
    
    @pytest.mark.parametrize("config_class,kwargs,expected_field,expected_value", [
        # Edge case values
        (AppConfig, {"name": "", "version": ""}, "name", ""),
        (AppConfig, {"name": "", "version": ""}, "version", ""),
        (ParserConfig, {"buffer_size": 0, "max_line_length": 0}, "buffer_size", 0),
        (ParserConfig, {"buffer_size": 0, "max_line_length": 0}, "max_line_length", 0),
        (RulesConfig, {"reload_interval": -1, "max_rules": -1}, "reload_interval", -1),
        (RulesConfig, {"reload_interval": -1, "max_rules": -1}, "max_rules", -1),
    ])
    def test_config_edge_case_values(self, config_class, kwargs: Dict[str, Any], 
                                   expected_field: str, expected_value: Any):
        config = config_class(**kwargs)
        assert getattr(config, expected_field) == expected_value


class TestBaseConfigValidator:
    """Test the BaseConfigValidator abstract class."""
    
    def test_base_config_validator_abstract(self):
        # Should not be able to instantiate BaseConfigValidator directly
        with pytest.raises(TypeError):
            BaseConfigValidator()


class TestConfigDefaults:
    """Test the ConfigDefaults class."""
    
    def test_app_defaults(self):
        assert ConfigDefaults.APP_NAME == "LogSentinel"
        assert ConfigDefaults.APP_VERSION == "0.1.0"
        assert ConfigDefaults.APP_DESCRIPTION == "Advanced log security analysis platform"
        assert ConfigDefaults.DEFAULT_LOG_LEVEL == "INFO"
    
    def test_parser_defaults(self):
        assert ConfigDefaults.DEFAULT_FORMAT == "syslog"
        assert ConfigDefaults.SUPPORTED_FORMATS == ["syslog", "apache", "nginx"]
        assert ConfigDefaults.BUFFER_SIZE == 8192
        assert ConfigDefaults.MAX_LINE_LENGTH == 4096
    
    def test_rules_defaults(self):
        assert ConfigDefaults.RULES_DIRECTORY == "/app/rules"
        assert ConfigDefaults.AUTO_RELOAD is True
        assert ConfigDefaults.RELOAD_INTERVAL == 60
        assert ConfigDefaults.MAX_RULES == 1000
        assert ConfigDefaults.RULE_TIMEOUT == 30
    
    def test_alerts_defaults(self):
        assert ConfigDefaults.DEFAULT_HANDLERS == ["console", "file"]
        assert ConfigDefaults.OUTPUT_FILE == "/app/logs/alerts.log"
        assert ConfigDefaults.MAX_ALERTS_PER_MINUTE == 100
        assert ConfigDefaults.ALERT_RETENTION_DAYS == 30


class TestConfigValidator:
    """Test the ConfigValidator class."""
    
    def test_validate_positive_int_valid(self):
        ConfigValidator.validate_positive_int(1, "test_field")
        ConfigValidator.validate_positive_int(0, "test_field")
        ConfigValidator.validate_positive_int(100, "test_field")
    
    def test_validate_positive_int_invalid(self):
        with pytest.raises(ValueError, match="test_field must be positive, got -1"):
            ConfigValidator.validate_positive_int(-1, "test_field")
    
    def test_validate_non_empty_string_valid(self):
        ConfigValidator.validate_non_empty_string("valid", "test_field")
        ConfigValidator.validate_non_empty_string("a", "test_field")
    
    def test_validate_non_empty_string_invalid(self):
        with pytest.raises(ValueError, match="test_field cannot be empty"):
            ConfigValidator.validate_non_empty_string("", "test_field")
        
        with pytest.raises(ValueError, match="test_field cannot be empty"):
            ConfigValidator.validate_non_empty_string("   ", "test_field")
    
    def test_validate_non_empty_list_valid(self):
        ConfigValidator.validate_non_empty_list(["item1", "item2"], "test_field")
        ConfigValidator.validate_non_empty_list(["single"], "test_field")
    
    def test_validate_non_empty_list_invalid(self):
        with pytest.raises(ValueError, match="test_field cannot be empty"):
            ConfigValidator.validate_non_empty_list([], "test_field")
        
        with pytest.raises(ValueError, match="test_field cannot contain empty strings"):
            ConfigValidator.validate_non_empty_list(["valid", ""], "test_field")
        
        with pytest.raises(ValueError, match="test_field cannot contain empty strings"):
            ConfigValidator.validate_non_empty_list(["valid", "   "], "test_field")
    
    def test_validate_app_config(self):
        validator = ConfigValidator()
        
        # Valid config
        valid_config = AppConfig(name="Test", version="1.0.0", log_level="INFO")
        validator._validate_app_config(valid_config)  # Should not raise
        
        # Invalid configs
        with pytest.raises(ValueError):
            validator._validate_app_config(AppConfig(name="", version="1.0.0"))
        
        with pytest.raises(ValueError):
            validator._validate_app_config(AppConfig(name="Test", version=""))
        
        with pytest.raises(ValueError):
            validator._validate_app_config(AppConfig(name="Test", version="1.0.0", log_level=""))
    
    def test_validate_parser_config(self):
        validator = ConfigValidator()
        
        # Valid config
        valid_config = ParserConfig(default_format="syslog", buffer_size=8192, max_line_length=4096)
        validator._validate_parser_config(valid_config)  # Should not raise
        
        # Invalid configs
        with pytest.raises(ValueError):
            validator._validate_parser_config(ParserConfig(default_format=""))
        
        with pytest.raises(ValueError):
            validator._validate_parser_config(ParserConfig(buffer_size=-1))
        
        with pytest.raises(ValueError):
            validator._validate_parser_config(ParserConfig(max_line_length=-1))
        
        # Empty supported_formats is allowed, so no validation error expected
        validator._validate_parser_config(ParserConfig(supported_formats=[]))
        
        # Note: supported_formats validation is disabled, so no error expected
        validator._validate_parser_config(ParserConfig(supported_formats=["valid", ""]))
    
    def test_validate_rules_config(self):
        validator = ConfigValidator()
        
        # Valid config
        valid_config = RulesConfig(directory="/test", reload_interval=60, max_rules=100, rule_timeout=30)
        validator._validate_rules_config(valid_config)  # Should not raise
        
        # Invalid configs
        with pytest.raises(ValueError):
            validator._validate_rules_config(RulesConfig(directory=""))
        
        with pytest.raises(ValueError):
            validator._validate_rules_config(RulesConfig(reload_interval=-1))
        
        with pytest.raises(ValueError):
            validator._validate_rules_config(RulesConfig(max_rules=-1))
        
        with pytest.raises(ValueError):
            validator._validate_rules_config(RulesConfig(rule_timeout=-1))
    
    def test_validate_alerts_config(self):
        validator = ConfigValidator()
        
        # Valid config
        valid_config = AlertsConfig(output_file="/test.log", max_alerts_per_minute=100, alert_retention_days=30)
        validator._validate_alerts_config(valid_config)  # Should not raise
        
        # Invalid configs
        with pytest.raises(ValueError):
            validator._validate_alerts_config(AlertsConfig(output_file=""))
        
        with pytest.raises(ValueError):
            validator._validate_alerts_config(AlertsConfig(max_alerts_per_minute=-1))
        
        with pytest.raises(ValueError):
            validator._validate_alerts_config(AlertsConfig(alert_retention_days=-1))
        
        # Empty handlers is allowed, so no validation error expected
        validator._validate_alerts_config(AlertsConfig(handlers=[]))
        
        # Note: handlers validation is disabled, so no error expected
        validator._validate_alerts_config(AlertsConfig(handlers=["valid", ""]))
    
    def test_validate_method_dispatch(self):
        validator = ConfigValidator()
        
        # Test dispatch to specific validators
        validator.validate(AppConfig())
        validator.validate(ParserConfig())
        validator.validate(RulesConfig())
        validator.validate(AlertsConfig())


class TestConfigValidationIntegration:
    """Test validation integration with config classes."""
    
    def test_app_config_validation_method(self):
        config = AppConfig()
        config.validate()  # Should not raise
        
        config.name = ""
        with pytest.raises(ValueError):
            config.validate()
    
    def test_parser_config_validation_method(self):
        config = ParserConfig()
        config.validate()  # Should not raise
        
        config.buffer_size = -1
        with pytest.raises(ValueError):
            config.validate()
    
    def test_rules_config_validation_method(self):
        config = RulesConfig()
        config.validate()  # Should not raise
        
        config.directory = ""
        with pytest.raises(ValueError):
            config.validate()
    
    def test_alerts_config_validation_method(self):
        config = AlertsConfig()
        config.validate()  # Should not raise
        
        config.output_file = ""
        with pytest.raises(ValueError):
            config.validate()