# Quick Start Guide - Gentherm Assignment

## Setup Instructions (5 minutes)

### Step 1: Install Dependencies
```bash
cd embedded-test-practice
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
pytest --version
python -c "import can; print('python-can installed')"
```

### Step 3: Run Tests
```bash
# Run all tests
python -m pytest test_scripts/ -v

# Run heating tests only
python -m pytest test_scripts/test_heating_system.py -v

# Run with coverage
python -m pytest test_scripts/ --cov=test_scripts --cov-report=html

# Run only critical tests
python -m pytest test_scripts/ -v -m critical
```

---

## Project Overview

### Directory Structure

```
embedded-test-practice/
├── README.md                          # Project overview
├── config.ini                         # Configuration parameters
├── requirements.txt                   # Python dependencies
├── requirements/                      # System requirements
│   ├── SYSTEM_REQUIREMENTS.md         # High-level specs
│   └── FUNCTIONAL_REQUIREMENTS.md     # Detailed specs
├── test_cases/                        # Test design
│   ├── test_cases.csv                 # 42 test cases
│   └── test_coverage_analysis.md      # Traceability matrix
├── test_scripts/                      # Automated tests
│   ├── conftest.py                    # pytest configuration
│   ├── test_heating_system.py         # Heating tests (12)
│   ├── test_massage_system.py         # Massage tests (14)
│   ├── test_hil_integration.py        # Integration tests (16)
│   └── utilities/                     # Helper modules
│       ├── hil_interface.py           # CAN communication
│       ├── data_logger.py             # Test logging
│       └── signal_generator.py        # Signal simulation
├── hil_config/                        # HIL setup
│   ├── wiring_diagram.md              # Architecture docs
│   └── bus_definitions.dbc            # CAN database
├── docs/                              # Documentation
│   ├── ASSIGNMENT_BRIEF.md            # Assignment details
│   ├── TEST_STRATEGY.md               # Testing approach
│   ├── verification_report.md         # Report template
│   └── HIL_SETUP_GUIDE.md             # Setup instructions
└── reports/                           # Test results
    └── (generated at runtime)
```

---

## Key Files to Review

### For Understanding Requirements
1. **START HERE:** [README.md](README.md) - Project overview
2. **Then:** [docs/ASSIGNMENT_BRIEF.md](docs/ASSIGNMENT_BRIEF.md) - Assignment details
3. **Requirements:** [requirements/SYSTEM_REQUIREMENTS.md](requirements/SYSTEM_REQUIREMENTS.md)
4. **Functional:** [requirements/FUNCTIONAL_REQUIREMENTS.md](requirements/FUNCTIONAL_REQUIREMENTS.md)

### For Test Design
1. **Test Cases:** [test_cases/test_cases.csv](test_cases/test_cases.csv) - 42 test cases
2. **Coverage:** [test_cases/test_coverage_analysis.md](test_cases/test_coverage_analysis.md) - Traceability
3. **Strategy:** [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md) - Testing approach

### For Implementation
1. **Configuration:** [conftest.py](test_scripts/conftest.py) - pytest fixtures
2. **Heating Tests:** [test_heating_system.py](test_scripts/test_heating_system.py) - 12 tests
3. **Massage Tests:** [test_massage_system.py](test_scripts/test_massage_system.py) - 14 tests
4. **Integration:** [test_hil_integration.py](test_scripts/test_hil_integration.py) - 16 tests
5. **HIL Layer:** [utilities/hil_interface.py](test_scripts/utilities/hil_interface.py) - CAN interface

### For HIL Setup
1. **Wiring:** [hil_config/wiring_diagram.md](hil_config/wiring_diagram.md) - System architecture
2. **CAN DB:** [hil_config/bus_definitions.dbc](hil_config/bus_definitions.dbc) - Message definitions
3. **Config:** [config.ini](config.ini) - Project settings

---

## Test Execution Map

### Phase 1: Unit Tests - Heating (12 tests, ~45 min)
```
pytest test_scripts/test_heating_system.py -v

Tests:
✅ Enable/Disable
✅ Power Levels (Low/Med/High)
✅ Temperature Control
✅ Safety Limits
✅ Telemetry
✅ Voltage Tolerance
✅ Event Logging
```

### Phase 2: Unit Tests - Massage (14 tests, ~60 min)
```
pytest test_scripts/test_massage_system.py -v

Tests:
✅ Enable/Disable
✅ Intensity Levels
✅ Massage Patterns
✅ Pressure Regulation
✅ Response Times
✅ Fault Detection
✅ Auto-Shutdown
```

### Phase 3: Integration Tests (5 tests, ~30 min)
```
pytest test_scripts/test_hil_integration.py::TestSystemIntegration -v

Tests:
✅ Simultaneous Operation
✅ CAN Cycle Stability
✅ Message Loss Handling
✅ Diagnostics
```

### Phase 4: Safety Tests (4 tests, ~20 min)
```
pytest test_scripts/test_hil_integration.py::TestSafetyCritical -v -m critical

Tests:
✅ MCU Failsafe
✅ Over-Temperature Shutdown
✅ Over-Pressure Relief
✅ Fault Logging
```

### Phase 5: Edge Cases & Stress (7 tests, ~65 min)
```
pytest test_scripts/test_hil_integration.py::TestEdgeCases -v
pytest test_scripts/test_hil_integration.py::TestStressIntegration -v

Tests:
✅ Temperature Oscillation
✅ Pressure Oscillation
✅ Voltage Sag
✅ CAN Jitter
✅ Cold Start Cycles
✅ Pattern Switching
✅ Extended Operation
```

---

## Common Commands

```bash
# Run all tests
pytest test_scripts/ -v

# Run specific test class
pytest test_scripts/test_heating_system.py::TestHeatingBasics -v

# Run specific test
pytest test_scripts/test_heating_system.py::TestHeatingBasics::test_heat_enable_disable_control -v

# Run with markers
pytest test_scripts/ -v -m heating          # All heating tests
pytest test_scripts/ -v -m critical         # Critical tests only
pytest test_scripts/ -v -m safety           # Safety tests
pytest test_scripts/ -v -m "not stress"     # All except stress

# Coverage reporting
pytest test_scripts/ --cov=test_scripts --cov-report=term-missing
pytest test_scripts/ --cov=test_scripts --cov-report=html

# Verbose output with timing
pytest test_scripts/ -v --durations=10

# Stop on first failure
pytest test_scripts/ -v -x

# Run with custom timeout
pytest test_scripts/ --timeout=60 -v
```

---

## Expected Results

### Overall Pass Rate
- **Target:** ≥95%
- **Expected:** 100% (all 42 tests pass)

### Coverage
- **Requirement Coverage:** 96.4% (26/27 fully covered)
- **Test Coverage:** ≥85%
- **Critical Path:** 100%

### Performance
- **Total Test Duration:** ~4 hours
- **Heating Subsystem:** 45 minutes
- **Massage Subsystem:** 60 minutes
- **Integration & Safety:** 50 minutes
- **Edge Cases & Stress:** 65 minutes
- **Reporting:** 15 minutes

---

## Troubleshooting

### Tests Won't Run
```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip list | grep pytest

# Reinstall
pip install --upgrade -r requirements.txt
```

### CAN Interface Issues
```bash
# Verify virtual CAN (Linux/macOS)
ifconfig vcan0  # Should exist

# Create if missing
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

### Import Errors
```bash
# Check PYTHONPATH
echo $PYTHONPATH

# Run from project root
cd embedded-test-practice
pytest test_scripts/
```

### Timeout Issues
```bash
# Increase timeout
pytest test_scripts/ --timeout=60 -v

# Check for slow tests
pytest test_scripts/ --durations=5
```

---

## Documentation Map

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [README.md](README.md) | Project overview | 5 min |
| [ASSIGNMENT_BRIEF.md](docs/ASSIGNMENT_BRIEF.md) | Assignment details | 15 min |
| [SYSTEM_REQUIREMENTS.md](requirements/SYSTEM_REQUIREMENTS.md) | Requirements spec | 20 min |
| [FUNCTIONAL_REQUIREMENTS.md](requirements/FUNCTIONAL_REQUIREMENTS.md) | Functional spec | 20 min |
| [TEST_STRATEGY.md](docs/TEST_STRATEGY.md) | Testing approach | 15 min |
| [test_coverage_analysis.md](test_cases/test_coverage_analysis.md) | Coverage matrix | 10 min |
| [wiring_diagram.md](hil_config/wiring_diagram.md) | HIL architecture | 15 min |

**Total Reading Time:** ~100 minutes (comprehensive understanding)

---

## Assignment Timeline (4-6 hours)

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Setup** | 15 min | Install deps, verify environment |
| **Requirements** | 30 min | Read specs, understand system |
| **Test Design** | 45 min | Review test cases, traceability |
| **Test Execution** | 180 min | Run all test phases |
| **Analysis** | 30 min | Review results, generate report |
| **Documentation** | 30 min | Summarize findings, sign-off |
| **TOTAL** | **290 min** | 4.8 hours |

---

## Success Criteria

✅ **Functional Requirements:** All tests pass (100%)
✅ **Coverage:** ≥85% of code executed
✅ **Safety:** All CRITICAL tests pass
✅ **Traceability:** All requirements mapped to tests
✅ **Documentation:** Complete and professional
✅ **Report:** Generated and signed off

---

## Next Steps

1. **Install** dependencies: `pip install -r requirements.txt`
2. **Read** requirements: Start with [SYSTEM_REQUIREMENTS.md](requirements/SYSTEM_REQUIREMENTS.md)
3. **Review** tests: Check [test_cases.csv](test_cases/test_cases.csv)
4. **Run** tests: `pytest test_scripts/ -v`
5. **Generate** report: `pytest --cov=test_scripts --cov-report=html`
6. **Document** findings: Create verification report

---

## Key Contacts

For questions about:
- **Requirements:** See [requirements/](requirements/) directory
- **Test Design:** See [test_cases/](test_cases/) directory
- **Implementation:** See [test_scripts/](test_scripts/) directory
- **HIL Setup:** See [hil_config/](hil_config/) directory
- **Overall:** See [docs/ASSIGNMENT_BRIEF.md](docs/ASSIGNMENT_BRIEF.md)

---

**Ready to Start?** → Run: `pytest test_scripts/ -v` 🚀

Good luck with the assignment!
