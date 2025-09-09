"""
Pytest configuration and shared fixtures for the log security analysis app.

This module provides common fixtures and configuration for all tests.
"""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Generator, Dict, Any


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_log_file(temp_dir: Path) -> Path:
    """Create a sample log file for testing."""
    log_file = temp_dir / "sample.log"
    log_content = """2023-12-01 10:00:00 INFO User login successful
2023-12-01 10:01:00 WARN Failed login attempt
2023-12-01 10:02:00 ERROR Database connection failed
2023-12-01 10:03:00 INFO User logout successful"""
    
    log_file.write_text(log_content)
    return log_file


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Sample configuration for testing."""
    return {
        "app": {
            "name": "Log Security Analysis",
            "version": "0.1.0",
            "log_level": "INFO"
        },
        "parsers": {
            "default_format": "syslog",
            "supported_formats": ["syslog", "apache", "nginx"]
        },
        "rules": {
            "directory": "/app/rules",
            "auto_reload": True,
            "reload_interval": 60
        },
        "alerts": {
            "handlers": ["console", "file"],
            "output_file": "/app/logs/alerts.log"
        }
    }


@pytest.fixture
def sample_rule_config() -> Dict[str, Any]:
    """Sample rule configuration for testing."""
    return {
        "rules": [
            {
                "id": "failed_login",
                "name": "Failed Login Attempts",
                "type": "regex",
                "pattern": r"Failed login attempt",
                "severity": "medium",
                "enabled": True
            },
            {
                "id": "database_error",
                "name": "Database Connection Errors",
                "type": "regex", 
                "pattern": r"Database connection failed",
                "severity": "high",
                "enabled": True
            }
        ]
    }


@pytest.fixture
def mock_log_entry():
    """Mock log entry for testing."""
    from datetime import datetime
    
    return {
        "timestamp": datetime(2023, 12, 1, 10, 0, 0),
        "level": "INFO",
        "message": "User login successful",
        "source": "auth",
        "raw_line": "2023-12-01 10:00:00 INFO User login successful"
    }


@pytest.fixture
def mock_alert():
    """Mock alert for testing."""
    from datetime import datetime
    
    return {
        "id": "alert_001",
        "timestamp": datetime(2023, 12, 1, 10, 0, 0),
        "rule_id": "failed_login",
        "rule_name": "Failed Login Attempts",
        "severity": "medium",
        "message": "Failed login attempt detected",
        "log_entry": "2023-12-01 10:01:00 WARN Failed login attempt",
        "source": "auth"
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "security: mark test as security-related"
    )
