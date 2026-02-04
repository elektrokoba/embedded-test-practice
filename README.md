# Systems Verification Assignment - Home Praktice

## Overview
This project is a comprehensive systems verification assignment for an automotive seat comfort module featuring heating and pneumatic massage functionality. The assignment tests key skills in requirements decomposition, test case design, HIL (Hardware-in-the-Loop) testing, automated scripting, and verification reporting.

## Project Structure

```
├── README.md                          # This file
├── requirements/                      # System and functional requirements
│   ├── SYSTEM_REQUIREMENTS.md         # Overall system specifications
│   └── FUNCTIONAL_REQUIREMENTS.md     # Detailed functional specifications
├── test_cases/                        # Test case design and specifications
│   ├── test_cases.csv                 # Test case matrix
│   └── test_coverage_analysis.md      # Coverage and traceability matrix
├── test_scripts/                      # Automated test implementation
│   ├── conftest.py                    # pytest configuration
│   ├── test_heating_system.py         # Heating subsystem tests
│   ├── test_massage_system.py         # Pneumatic massage subsystem tests
│   ├── test_hil_integration.py        # HIL integration tests
│   └── utilities/                     # Test utilities and helpers
│       ├── hil_interface.py           # HIL communication interface
│       ├── data_logger.py             # Test data logging
│       └── signal_generator.py        # Test signal generation
├── hil_config/                        # HIL and Vector configuration
│   ├── CANoe_configuration.xml        # Vector CANoe setup
│   ├── wiring_diagram.md              # HIL wiring documentation
│   └── bus_definitions.dbc            # CAN database file
├── docs/                              # Documentation and technical notes
│   ├── ASSIGNMENT_BRIEF.md            # Assignment overview
│   ├── TEST_STRATEGY.md               # Testing approach and methodology
│   └── HIL_SETUP_GUIDE.md             # HIL environment setup
├── reports/                           # Test execution and verification reports
│   ├── test_execution_log.csv         # Test execution records
│   └── verification_report.md         # Final verification report template
└── config.ini                         # Project configuration

```

## System Under Test: Seat Comfort Module

### Subsystems
1. **Heating System** - Electric heater control with temperature regulation
2. **Pneumatic Massage System** - Air pump and valve control for massage patterns

### Key Features
- Independent control of heating and massage functions
- Safety limits and fault detection
- CAN-based communication interface
- Multiple operational modes and intensity levels

## Getting Started

### Prerequisites
- Python 3.9+
- pytest framework
- Vector tools (CANoe, CANalyzer) - or simulators
- CAN interface hardware (or virtual CAN setup)

### Installation

```bash
# Install Python dependencies
pip install pytest pytest-cov cantools python-can

# Set up project
cd embedded-test-practice
python -m pytest test_scripts/ --collect-only
```

### Running Tests

```bash
# Run all tests
python -m pytest test_scripts/ -v

# Run specific test suite
python -m pytest test_scripts/test_heating_system.py -v

# Generate coverage report
python -m pytest test_scripts/ --cov=test_scripts --cov-report=html
```

## Assignment Scope (4-6 hours)

### Phase 1: Requirements Analysis (1 hour)
- System decomposition
- Functional requirement specification
- Use case identification

### Phase 2: Test Case Design (1.5 hours)
- Test case creation
- Test coverage analysis
- Traceability matrix

### Phase 3: Test Automation (2 hours)
- Test script implementation
- HIL configuration
- Data logging and reporting

### Phase 4: Reporting (0.5-1 hours)
- Test execution summary
- Defect tracking
- Verification sign-off

## Key Technologies
- **Python/pytest** - Test automation framework
- **Vector CANoe/CANalyzer** - HIL simulation
- **CAN/DBC** - Vehicle communication protocol
- **Markdown** - Documentation format

## Test Coverage Areas
- ✅ Functional verification
- ✅ Edge cases and boundary conditions
- ✅ Error handling and fault detection
- ✅ System integration
- ✅ Performance under stress conditions

## Author Notes
This assignment simulates real automotive verification work following ISO 26262 and ASIL requirements for functional safety.
