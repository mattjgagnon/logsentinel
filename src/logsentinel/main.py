"""
Main application module for LogSentinel.

This module provides the main application class that orchestrates the entire analysis workflow.
"""

import logging
from typing import Optional

from .config import ConfigManager
from .parsers import LogParser
from .rules import RulesEngine
from .alerts import AlertSystem


class LogSentinelApp:
    """
    Main application class for LogSentinel.
    
    This class follows the Single Responsibility Principle by focusing solely on
    orchestrating the log analysis workflow.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize LogSentinel.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_manager = ConfigManager(config_path)
        self.log_parser: Optional[LogParser] = None
        self.rules_engine: Optional[RulesEngine] = None
        self.alert_system: Optional[AlertSystem] = None
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        config = self.config_manager.get_app_config()
        logging.basicConfig(
            level=getattr(logging, config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize(self) -> None:
        """
        Initialize all components of the application.
        
        This method follows the Dependency Inversion Principle by depending on
        abstractions rather than concrete implementations.
        """
        self.logger.info("Initializing LogSentinel")
        
        # Initialize components (will be implemented in TDD phases)
        # self.log_parser = LogParserFactory.create(self.config_manager)
        # self.rules_engine = RulesEngine(self.config_manager)
        # self.alert_system = AlertSystem(self.config_manager)
        
        self.logger.info("Application initialized successfully")
    
    def analyze_logs(self, log_file_path: str) -> None:
        """
        Analyze log files for security threats.
        
        Args:
            log_file_path: Path to the log file to analyze
        """
        self.logger.info(f"Starting analysis of log file: {log_file_path}")
        
        # This will be implemented in TDD phases
        # 1. Parse log file
        # 2. Apply rules
        # 3. Generate alerts
        
        self.logger.info("Log analysis completed")
    
    def run(self) -> None:
        """Run the main application loop."""
        self.logger.info("Starting LogSentinel")
        
        try:
            self.initialize()
            # Main application loop will be implemented here
            self.logger.info("Application running")
        except KeyboardInterrupt:
            self.logger.info("Application stopped by user")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            raise


def main():
    """Main entry point for LogSentinel."""
    app = LogSentinelApp()
    app.run()


if __name__ == "__main__":
    main()
