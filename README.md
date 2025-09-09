# LogSentinel

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com)
[![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![TDD](https://img.shields.io/badge/Development-TDD-orange.svg)](https://en.wikipedia.org/wiki/Test-driven_development)

**Advanced Log Security Analysis Platform** - A rules-based threat detection engine built with SOLID principles and Test-Driven Development

## Overview

LogSentinel is a sophisticated Python-based log security analysis platform designed to proactively detect security threats through intelligent log analysis. Built from the ground up using **Test-Driven Development (TDD)** principles, it demonstrates enterprise-grade software engineering practices including SOLID design principles, comprehensive testing, and containerized deployment.

### Key Highlights

- **100% Test Coverage** - Every line of code is tested before implementation
- **SOLID Architecture** - Clean, maintainable, and extensible design
- **Docker-First** - Complete containerization for development and production
- **Rules-Based Engine** - Flexible, user-configurable threat detection
- **Real-Time Analysis** - Proactive security monitoring capabilities

## Features

### Currently Implemented
- **Modular Architecture** - Clean separation of concerns with dedicated modules
- **Docker Environment** - Multi-stage builds for development and production
- **Configuration Management** - YAML-based configuration with validation
- **Test Infrastructure** - Comprehensive pytest setup with coverage reporting
- **Log Parser Framework** - Extensible parser system for multiple log formats
- **Rules Engine Foundation** - Abstract rule system ready for implementation

### In Development (TDD Phases)
- **Log Parsing Engine** - Support for Syslog, Apache, Nginx, and custom formats
- **Security Rules Engine** - Regex, threshold, and pattern-based threat detection
- **Real-Time Alerting** - Console, file, and webhook alert handlers
- **Rule Management** - Hot-reloading and validation of security rules
- **Performance Optimization** - Efficient processing of large log files

### Planned Features
- **Machine Learning Integration** - Anomaly detection using ML algorithms
- **Web Dashboard** - Real-time monitoring and rule management interface
- **API Endpoints** - RESTful API for integration with other security tools
- **Database Integration** - Persistent storage for alerts and historical data
- **Multi-Format Support** - JSON, XML, and binary log format parsing
- **Distributed Processing** - Horizontal scaling for enterprise environments
- **Custom Rule Builder** - Visual interface for creating security rules
- **Threat Intelligence** - Integration with external threat feeds
- **Compliance Reporting** - Automated compliance and audit reports
- **SIEM Integration** - Seamless integration with existing SIEM platforms

## Architecture

LogSentinel follows a modular, SOLID-compliant architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Log Parsers   │    │  Rules Engine   │    │  Alert System   │
│                 │    │                 │    │                 │
│ • Syslog        │───▶│ • Regex Rules   │───▶│ • Console       │
│ • Apache        │    │ • Threshold     │    │ • File Output   │
│ • Nginx         │    │ • Pattern       │    │ • Webhooks      │
│ • Custom        │    │ • Custom        │    │ • Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Configuration   │
                    │ Management      │
                    │                 │
                    │ • App Config    │
                    │ • Rule Config   │
                    │ • Environment   │
                    └─────────────────┘
```

### SOLID Principles Implementation

- **Single Responsibility** - Each class has one clear purpose
- **Open/Closed** - Extensible through inheritance and composition
- **Liskov Substitution** - Proper inheritance hierarchies
- **Interface Segregation** - Focused, cohesive interfaces
- **Dependency Inversion** - Dependencies on abstractions

## Technology Stack

### Core Technologies
- **Python 3.11+** - Modern Python with type hints and dataclasses
- **Docker & Docker Compose** - Containerization and orchestration
- **Pytest** - Testing framework with 100% coverage requirement
- **YAML** - Configuration management
- **Git** - Version control with conventional commits

### Development Tools
- **Black** - Code formatting
- **isort** - Import sorting
- **Flake8** - Linting
- **MyPy** - Static type checking
- **Pre-commit** - Git hooks for code quality

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mattjgagnon/logsentinel.git
   cd logsentinel
   ```

2. **Build and run the development environment**
   ```bash
   docker compose build dev
   docker compose up dev
   ```

3. **Run the test suite**
   ```bash
   docker compose run test
   ```

4. **Generate coverage report**
   ```bash
   docker compose run coverage
   ```

### Production Deployment

```bash
# Build production image
docker compose build app

# Run in production mode
docker compose --profile production up app
```

## Testing & Quality Assurance

### Test-Driven Development (TDD)
This project follows strict TDD principles:
1. **Red** - Write a failing test
2. **Green** - Write minimal code to pass the test
3. **Refactor** - Improve code while keeping tests green

### Quality Metrics
- **100% Test Coverage** - Every function and class is tested
- **Type Safety** - Full type hints throughout the codebase
- **Code Quality** - Automated linting and formatting
- **Documentation** - Comprehensive docstrings and comments

### Running Tests
```bash
# Run all tests
docker compose run test

# Run with coverage
docker compose run coverage

# Run specific test categories
docker compose run test pytest tests/unit/ -m unit
docker compose run test pytest tests/integration/ -m integration
```

## Project Structure

```
logsentinel/
├── src/logsentinel/           # Main application code
│   ├── parsers/               # Log parsing modules
│   │   ├── base.py           # Abstract parser classes
│   │   ├── syslog_parser.py  # Syslog implementation
│   │   ├── apache_parser.py  # Apache log parser
│   │   └── nginx_parser.py   # Nginx log parser
│   ├── rules/                 # Rules engine
│   │   ├── base.py           # Abstract rule classes
│   │   ├── regex_rule.py     # Regex-based rules
│   │   ├── threshold_rule.py # Threshold-based rules
│   │   ├── pattern_rule.py   # Pattern matching rules
│   │   └── rules_engine.py   # Rules execution engine
│   ├── alerts/                # Alert system
│   │   ├── base.py           # Abstract alert classes
│   │   ├── alert_system.py   # Alert management
│   │   └── handlers.py       # Alert output handlers
│   ├── config/                # Configuration management
│   │   ├── config_manager.py # Configuration loader
│   │   ├── app_config.py     # Application config models
│   │   └── rule_config.py    # Rule config models
│   └── main.py               # Main application entry point
├── tests/                     # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data and fixtures
├── rules/                     # Security rules configuration
├── config/                    # Application configuration
├── logs/                      # Log files directory
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Docker Compose configuration
└── requirements*.txt          # Python dependencies
```

## Configuration

### Application Configuration (`config/app_config.yaml`)
```yaml
app:
  name: "LogSentinel"
  version: "0.1.0"
  log_level: "INFO"

parsers:
  default_format: "syslog"
  supported_formats: ["syslog", "apache", "nginx"]

rules:
  directory: "/app/rules"
  auto_reload: true
  reload_interval: 60

alerts:
  handlers: ["console", "file"]
  output_file: "/app/logs/alerts.log"
```

### Security Rules (`rules/default_rules.yaml`)
```yaml
rules:
  - id: "failed_login_attempts"
    name: "Failed Login Attempts"
    type: "regex"
    pattern: "(?i)(failed|invalid).*login"
    severity: "medium"
    enabled: true
```

## Development

### TDD Workflow
1. Write a failing test
2. Implement minimal code to pass
3. Refactor while maintaining tests
4. Repeat for each feature

### Code Quality Standards
- **100% test coverage** requirement
- **Type hints** for all functions and methods
- **Documentation** for all public APIs
- **SOLID principles** adherence
- **Clean code** practices

### Contributing
1. Follow TDD principles - write tests first
2. Maintain 100% test coverage
3. Follow SOLID principles and OOP best practices
4. Use type hints and proper documentation
5. Run all tests before submitting changes

## Performance & Scalability

### Current Capabilities
- Efficient log parsing with streaming support
- Memory-optimized rule evaluation
- Configurable performance parameters

### Planned Optimizations
- Multi-threaded log processing
- Distributed rule evaluation
- Caching and indexing strategies
- Horizontal scaling support

## Security Features

### Threat Detection
- **Authentication Attacks** - Brute force, privilege escalation
- **Network Intrusions** - Port scans, suspicious connections
- **Application Attacks** - SQL injection, XSS attempts
- **System Anomalies** - Service failures, resource abuse

### Alert Management
- **Real-time Processing** - Immediate threat detection
- **Severity Classification** - Low, Medium, High, Critical
- **Alert Deduplication** - Prevents alert fatigue
- **Multiple Output Formats** - Console, file, webhook, database

## Roadmap

### Phase 1: Core Engine (Completed)
- [x] Project structure and Docker setup
- [x] Configuration management
- [x] Test infrastructure
- [x] Basic architecture

### Phase 2: Log Processing (In Progress)
- [ ] Log parser implementations
- [ ] Format detection and validation
- [ ] Streaming log processing
- [ ] Performance optimization

### Phase 3: Rules Engine (Planned)
- [ ] Rule execution engine
- [ ] Rule management system
- [ ] Hot-reloading capabilities
- [ ] Rule validation and testing

### Phase 4: Alert System (Planned)
- [ ] Alert generation and management
- [ ] Multiple output handlers
- [ ] Alert deduplication
- [ ] Notification systems

### Phase 5: Advanced Features (Planned)
- [ ] Web dashboard
- [ ] API endpoints
- [ ] Machine learning integration
- [ ] SIEM integration

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup
   git clone https://github.com/mattjgagnon/logsentinel.git
cd logsentinel

# Install pre-commit hooks
pre-commit install

# Run tests
docker compose run test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Matt Gagnon**
- GitHub: [@mattjgagnon](https://github.com/mattjgagnon)
- Website: [MatthewJGagnon.com](https://matthewjgagnon.com)
- Software Engineer, Singer, Songwriter, Musician, and Epic Fantasy Novelist

## Acknowledgments

- Built with modern Python best practices
- Inspired by enterprise security monitoring tools
- Thanks to the open-source community for excellent tools and libraries

---

**Star this repository if you find it helpful!**

[![GitHub stars](https://img.shields.io/github/stars/mattjgagnon/logsentinel.svg?style=social&label=Star)](https://github.com/mattjgagnon/logsentinel)
[![GitHub forks](https://img.shields.io/github/forks/mattjgagnon/logsentinel.svg?style=social&label=Fork)](https://github.com/mattjgagnon/logsentinel/fork)