"""
Configuration manager for the log security analysis application.

This module provides configuration management following the Single Responsibility Principle.
"""

from typing import Optional, Dict, Any, Tuple
from pathlib import Path

class SimpleYamlParser:
    """Simple YAML-like parser for basic configuration files.
    
    Parses YAML-like configuration files with sections, key-value pairs,
    and list items. Designed with SOLID principles for maintainability.
    """
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.current_section: Optional[str] = None
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a YAML-like configuration file."""
        self.config = {}
        self.current_section = None
        
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                self._process_line(line, line_num)
        
        return self.config
    
    def _process_line(self, line: str, line_num: int) -> None:
        """Process a single line of the configuration file."""
        original_line = line
        stripped_line = line.strip()
        
        if self._should_skip_line(stripped_line):
            return
        
        # Route to appropriate processor based on line type
        if self._is_section_header(stripped_line, original_line):
            self._process_section_header(stripped_line)
        elif self._is_list_item(stripped_line):
            self._process_list_item(stripped_line)
        elif self._is_key_value_pair(stripped_line):
            self._process_key_value_pair(stripped_line)
    
    def _should_skip_line(self, line: str) -> bool:
        return not line or line.startswith('#')
    
    def _is_section_header(self, stripped_line: str, original_line: str) -> bool:
        return ':' in stripped_line and not original_line.startswith(' ')
    
    def _is_list_item(self, line: str) -> bool:
        return line.startswith('- ') and self.current_section is not None
    
    def _is_key_value_pair(self, line: str) -> bool:
        return ':' in line and self.current_section is not None
    
    def _process_section_header(self, line: str) -> None:
        section_name = line.split(':')[0].strip()
        self.current_section = section_name
        self.config[section_name] = {}
    
    def _process_list_item(self, line: str) -> None:
        item_value = self._extract_list_item_value(line)
        # TODO: Make list key configurable instead of hardcoded
        self._add_to_section_list('supported_formats', item_value)
    
    def _process_key_value_pair(self, line: str) -> None:
        key, value = self._extract_key_value(line)
        self.config[self.current_section][key] = value
    
    def _extract_list_item_value(self, line: str) -> str:
        return line[2:].strip().strip('"')
    
    def _extract_key_value(self, line: str) -> Tuple[str, str]:
        key, value = line.split(':', 1)
        return key.strip(), value.strip().strip('"')
    
    def _add_to_section_list(self, list_key: str, item: str) -> None:
        if list_key not in self.config[self.current_section]:
            self.config[self.current_section][list_key] = []
        self.config[self.current_section][list_key].append(item)


def simple_yaml_load(file_path: str) -> Dict[str, Any]:
    """Simple YAML parser for basic configuration files.
    
    Maintains backward compatibility with existing code.
    """
    parser = SimpleYamlParser()
    return parser.parse_file(file_path)


class ConfigManager:
    """
    Manages application configuration.
    
    This class follows the Single Responsibility Principle by focusing solely on
    configuration management.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/app_config.yaml"
        self._config: Optional[Dict[str, Any]] = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Raises:
            FileNotFoundError: If config file doesn't exist
        """
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        self._config = simple_yaml_load(config_file)
        
        return self._config
    
    def get_app_config(self) -> Dict[str, Any]:
        if self._config is None:
            self.load_config()
        
        return self._config.get('app', {})
    
    def get_parser_config(self) -> Dict[str, Any]:
        if self._config is None:
            self.load_config()
        
        return self._config.get('parsers', {})
    
    def get_rules_config(self) -> Dict[str, Any]:
        if self._config is None:
            self.load_config()
        
        return self._config.get('rules', {})
    
    def get_alerts_config(self) -> Dict[str, Any]:
        if self._config is None:
            self.load_config()
        
        return self._config.get('alerts', {})
