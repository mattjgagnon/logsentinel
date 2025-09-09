"""
Configuration manager for the log security analysis application.

This module provides configuration management following the Single Responsibility Principle.
"""

from typing import Optional, Dict, Any
from pathlib import Path

# Simple YAML-like parser for basic config files
def simple_yaml_load(file_path: str) -> Dict[str, Any]:
    """Simple YAML parser for basic configuration files."""
    config = {}
    with open(file_path, 'r') as f:
        current_section = None
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line and not line.startswith(' '):
                # Section header
                current_section = line.split(':')[0].strip()
                config[current_section] = {}
            elif line.startswith('- ') and current_section:
                # List item
                if 'supported_formats' not in config[current_section]:
                    config[current_section]['supported_formats'] = []
                config[current_section]['supported_formats'].append(line[2:].strip().strip('"'))
            elif ':' in line and current_section:
                # Key-value pair
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"')
                config[current_section][key] = value
    return config


class ConfigManager:
    """
    Manages application configuration.
    
    This class follows the Single Responsibility Principle by focusing solely on
    configuration management.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path or "config/app_config.yaml"
        self._config: Optional[Dict[str, Any]] = None
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
        """
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        self._config = simple_yaml_load(config_file)
        
        return self._config
    
    def get_app_config(self) -> Dict[str, Any]:
        """
        Get application configuration.
        
        Returns:
            Application configuration dictionary
        """
        if self._config is None:
            self.load_config()
        
        return self._config.get('app', {})
    
    def get_parser_config(self) -> Dict[str, Any]:
        """
        Get parser configuration.
        
        Returns:
            Parser configuration dictionary
        """
        if self._config is None:
            self.load_config()
        
        return self._config.get('parsers', {})
    
    def get_rules_config(self) -> Dict[str, Any]:
        """
        Get rules configuration.
        
        Returns:
            Rules configuration dictionary
        """
        if self._config is None:
            self.load_config()
        
        return self._config.get('rules', {})
    
    def get_alerts_config(self) -> Dict[str, Any]:
        """
        Get alerts configuration.
        
        Returns:
            Alerts configuration dictionary
        """
        if self._config is None:
            self.load_config()
        
        return self._config.get('alerts', {})
