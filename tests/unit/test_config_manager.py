"""
Unit tests for the ConfigManager class.

This module tests the configuration management functionality using TDD approach.
Refactored to be more concise and eliminate duplication.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from typing import Dict, Any, List, Tuple

from logsentinel.config.config_manager import ConfigManager, simple_yaml_load


class TestSimpleYamlLoad:
    """Test the simple_yaml_load function using parametrized tests."""
    
    @pytest.mark.parametrize("config_content,expected", [
        # Empty file
        ("", {}),
        
        # Comments only
        ("# This is a comment\n# Another comment\n# Yet another comment\n", {}),
        
        # Valid configuration with all sections
        ("""# Test configuration
app:
  name: "Test App"
  version: "1.0.0"
  log_level: "DEBUG"

parsers:
  default_format: "syslog"
  - "apache"
  - "nginx"
  - "syslog"

rules:
  directory: "/app/rules"
  auto_reload: "true"

alerts:
  handlers: "console,file"
  output_file: "/app/logs/alerts.log"
""", {
            "app": {
                "name": "Test App",
                "version": "1.0.0",
                "log_level": "DEBUG"
            },
            "parsers": {
                "default_format": "syslog",
                "supported_formats": ["apache", "nginx", "syslog"]
            },
            "rules": {
                "directory": "/app/rules",
                "auto_reload": "true"
            },
            "alerts": {
                "handlers": "console,file",
                "output_file": "/app/logs/alerts.log"
            }
        }),
        
        # Configuration with empty lines and whitespace
        ("""
app:
  name: "Test App"

# Comment here

parsers:
  default_format: "syslog"

""", {
            "app": {"name": "Test App"},
            "parsers": {"default_format": "syslog"}
        }),
        
        # Configuration with list items
        ("""parsers:
  - "apache"
  - "nginx"
  - "syslog"
  - "json"

alerts:
  handlers: "console"
  - "email"
  - "slack"
""", {
            "parsers": {
                "supported_formats": ["apache", "nginx", "syslog", "json"]
            },
            "alerts": {
                "handlers": "console",
                "supported_formats": ["email", "slack"]
            }
        }),
    ])
    def test_simple_yaml_load_cases(self, temp_dir: Path, config_content: str, expected: Dict[str, Any]):
        """Test various YAML loading scenarios."""
        # Arrange
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text(config_content)
        
        # Act
        result = simple_yaml_load(str(config_file))
        
        # Assert
        assert result == expected


class TestConfigManager:
    """Test the ConfigManager class with refactored, data-driven tests."""
    
    @pytest.mark.parametrize("config_path,expected_path", [
        (None, "config/app_config.yaml"),
        ("/custom/path/config.yaml", "/custom/path/config.yaml"),
        ("relative/path.yaml", "relative/path.yaml"),
    ])
    def test_initialization(self, config_path: str, expected_path: str):
        """Test ConfigManager initialization with various paths."""
        manager = ConfigManager(config_path)
        assert manager.config_path == expected_path
        assert manager._config is None
    
    def test_load_config_with_nonexistent_file(self):
        """Test loading configuration from a non-existent file."""
        manager = ConfigManager("/nonexistent/path/config.yaml")
        
        with pytest.raises(FileNotFoundError) as exc_info:
            manager.load_config()
        
        assert "Configuration file not found: /nonexistent/path/config.yaml" in str(exc_info.value)
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_load_config_with_file_permission_error(self, mock_file, mock_exists):
        """Test loading config when file access is denied."""
        manager = ConfigManager("/some/path/config.yaml")
        
        with pytest.raises(IOError) as exc_info:
            manager.load_config()
        
        assert "Permission denied" in str(exc_info.value)
    
    @pytest.mark.parametrize("config_content,expected_config", [
        # Basic configuration
        ("""app:
  name: "Test App"
  version: "1.0.0"

parsers:
  default_format: "syslog"
""", {
            "app": {"name": "Test App", "version": "1.0.0"},
            "parsers": {"default_format": "syslog"}
        }),
        
        # Configuration with all sections
        ("""app:
  name: "Test App"
  version: "1.0.0"
  log_level: "DEBUG"

parsers:
  default_format: "syslog"
  buffer_size: "8192"
  - "apache"
  - "nginx"

rules:
  directory: "/app/rules"
  auto_reload: "true"
  reload_interval: "60"

alerts:
  handlers: "console,file"
  output_file: "/app/logs/alerts.log"
  max_alerts_per_minute: "100"
""", {
            "app": {"name": "Test App", "version": "1.0.0", "log_level": "DEBUG"},
            "parsers": {
                "default_format": "syslog",
                "buffer_size": "8192",
                "supported_formats": ["apache", "nginx"]
            },
            "rules": {
                "directory": "/app/rules",
                "auto_reload": "true",
                "reload_interval": "60"
            },
            "alerts": {
                "handlers": "console,file",
                "output_file": "/app/logs/alerts.log",
                "max_alerts_per_minute": "100"
            }
        }),
    ])
    def test_load_config_with_existing_file(self, temp_dir: Path, config_content: str, expected_config: Dict[str, Any]):
        """Test loading configuration from existing files."""
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text(config_content)
        
        manager = ConfigManager(str(config_file))
        result = manager.load_config()
        
        assert result == expected_config
        assert manager._config == expected_config
    
    @pytest.mark.parametrize("section,config_content,expected_result", [
        # App section tests
        ("app", """app:
  name: "Test App"
  version: "1.0.0"
  log_level: "DEBUG"

parsers:
  default_format: "syslog"
""", {"name": "Test App", "version": "1.0.0", "log_level": "DEBUG"}),
        
        # Parser section tests
        ("parser", """app:
  name: "Test App"

parsers:
  default_format: "syslog"
  buffer_size: "8192"
  - "apache"
  - "nginx"

rules:
  directory: "/app/rules"
""", {
            "default_format": "syslog",
            "buffer_size": "8192",
            "supported_formats": ["apache", "nginx"]
        }),
        
        # Rules section tests
        ("rules", """app:
  name: "Test App"

parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"
  auto_reload: "true"
  reload_interval: "60"
""", {
            "directory": "/app/rules",
            "auto_reload": "true",
            "reload_interval": "60"
        }),
        
        # Alerts section tests
        ("alerts", """app:
  name: "Test App"

parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"

alerts:
  handlers: "console,file"
  output_file: "/app/logs/alerts.log"
  max_alerts_per_minute: "100"
""", {
            "handlers": "console,file",
            "output_file": "/app/logs/alerts.log",
            "max_alerts_per_minute": "100"
        }),
    ])
    def test_get_section_config_with_loaded_config(self, temp_dir: Path, section: str, config_content: str, expected_result: Dict[str, Any]):
        """Test getting section configuration after loading config."""
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text(config_content)
        
        manager = ConfigManager(str(config_file))
        manager.load_config()
        
        # Get the appropriate method based on section
        method_map = {
            "app": manager.get_app_config,
            "parser": manager.get_parser_config,
            "rules": manager.get_rules_config,
            "alerts": manager.get_alerts_config,
        }
        
        result = method_map[section]()
        assert result == expected_result
    
    @pytest.mark.parametrize("section,config_content,expected_result", [
        # App section tests
        ("app", """app:
  name: "Test App"
  version: "1.0.0"

parsers:
  default_format: "syslog"
""", {"name": "Test App", "version": "1.0.0"}),
        
        # Parser section tests
        ("parser", """app:
  name: "Test App"

parsers:
  default_format: "syslog"
  buffer_size: "8192"

rules:
  directory: "/app/rules"
""", {"default_format": "syslog", "buffer_size": "8192"}),
        
        # Rules section tests
        ("rules", """app:
  name: "Test App"

parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"
  auto_reload: "true"
""", {"directory": "/app/rules", "auto_reload": "true"}),
        
        # Alerts section tests
        ("alerts", """app:
  name: "Test App"

parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"

alerts:
  handlers: "console"
  output_file: "/app/logs/alerts.log"
""", {"handlers": "console", "output_file": "/app/logs/alerts.log"}),
    ])
    def test_get_section_config_without_loaded_config(self, temp_dir: Path, section: str, config_content: str, expected_result: Dict[str, Any]):
        """Test getting section configuration when config hasn't been loaded yet."""
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text(config_content)
        
        manager = ConfigManager(str(config_file))
        
        # Get the appropriate method based on section
        method_map = {
            "app": manager.get_app_config,
            "parser": manager.get_parser_config,
            "rules": manager.get_rules_config,
            "alerts": manager.get_alerts_config,
        }
        
        result = method_map[section]()
        assert result == expected_result
        assert manager._config is not None  # Should be loaded automatically
    
    @pytest.mark.parametrize("section", ["app", "parser", "rules", "alerts"])
    def test_get_section_config_with_no_section(self, temp_dir: Path, section: str):
        """Test getting section configuration when the section doesn't exist."""
        config_content = """app:
  name: "Test App"

parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"

alerts:
  handlers: "console"
"""
        
        # Remove the target section from config
        if section == "app":
            config_content = """parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"

alerts:
  handlers: "console"
"""
        elif section == "parser":
            config_content = """app:
  name: "Test App"

rules:
  directory: "/app/rules"

alerts:
  handlers: "console"
"""
        elif section == "rules":
            config_content = """app:
  name: "Test App"

parsers:
  default_format: "syslog"

alerts:
  handlers: "console"
"""
        elif section == "alerts":
            config_content = """app:
  name: "Test App"

parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"
"""
        
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text(config_content)
        
        manager = ConfigManager(str(config_file))
        
        # Get the appropriate method based on section
        method_map = {
            "app": manager.get_app_config,
            "parser": manager.get_parser_config,
            "rules": manager.get_rules_config,
            "alerts": manager.get_alerts_config,
        }
        
        result = method_map[section]()
        assert result == {}
    
    def test_multiple_config_access_without_reloading(self, temp_dir: Path):
        """Test that config is not reloaded when accessing multiple sections."""
        config_content = """app:
  name: "Test App"

parsers:
  default_format: "syslog"

rules:
  directory: "/app/rules"

alerts:
  handlers: "console"
"""
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text(config_content)
        
        manager = ConfigManager(str(config_file))
        
        # Load config first
        manager.load_config()
        
        # Access multiple sections
        app_config = manager.get_app_config()
        parser_config = manager.get_parser_config()
        rules_config = manager.get_rules_config()
        alerts_config = manager.get_alerts_config()
        
        # Assert
        assert app_config == {"name": "Test App"}
        assert parser_config == {"default_format": "syslog"}
        assert rules_config == {"directory": "/app/rules"}
        assert alerts_config == {"handlers": "console"}
        
        # Verify config was only loaded once
        assert manager._config is not None