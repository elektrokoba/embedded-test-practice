# Assignment Brief - Gentherm Seat Comfort Module Verification

**Document ID:** ASSIGN-001  
**Version:** 1.0  
**Date:** 2026-02-04  
**Duration:** 4-6 hours  
**Difficulty:** Intermediate-Advanced

---

## 1. Introduction

This take-home assignment simulates a real embedded systems verification project for an automotive Seat Comfort Module (SCM). The assignment tests your ability to:

- Decompose complex systems into testable requirements
- Design comprehensive test cases with traceability
- Implement automated test scripts using industry-standard frameworks
- Configure Hardware-in-the-Loop (HIL) testing environments
- Generate professional verification reports

The assignment is aligned with Gentherm's expertise in thermal and pneumatic comfort systems, using a realistic automotive example compliant with ISO 26262 functional safety standards.

---

## 2. System Overview

### 2.1 The Seat Comfort Module (SCM)

You are tasked with verifying a vehicle seat feature that combines:

**Heating Subsystem**
- Electric heating element (0-70W)
- Temperature control (20-65°C)
- 3 intensity levels
- Safety limits and fault detection

**Pneumatic Massage Subsystem**
- Air pump and valve control
- Pressure regulation (0-150 kPa)
- 5 intensity levels and 3 patterns (Wave, Pulse, Continuous)
- Auto-shutdown after 30 minutes

**Integration**
- CAN-based communication (500 kbps)
- Simultaneous operation capability
- Fault logging and diagnostics

---

## 3. Assignment Tasks

### Task 1: Requirements Analysis (1 hour)

**Objectives:**
- Read and understand system requirements
- Identify functional decomposition
- Trace requirements to test coverage

**Deliverables:**
- ✅ [SYSTEM_REQUIREMENTS.md](../requirements/SYSTEM_REQUIREMENTS.md) - Already provided
- ✅ [FUNCTIONAL_REQUIREMENTS.md](../requirements/FUNCTIONAL_REQUIREMENTS.md) - Already provided
- Your own analysis document (optional)

**Questions to Answer:**
1. Identify the main subsystems and their interfaces
2. List all safety-critical requirements (CRITICAL priority)
3. What are the key performance parameters?
4. How does CAN communication impact testing strategy?

---

### Task 2: Test Case Design (1.5 hours)

**Objectives:**
- Create comprehensive test cases
- Ensure full requirement coverage
- Design traceability matrix

**Deliverables:**
- ✅ [test_cases.csv](../test_cases/test_cases.csv) - 42 test cases provided
- ✅ [test_coverage_analysis.md](../test_cases/test_coverage_analysis.md) - Coverage matrix provided
- Your own test execution plan (optional)

**Key Areas to Test:**
1. **Heating Tests** (TC-HEAT-001 to TC-HEAT-012)
   - Enable/disable control
   - Intensity levels (Low/Medium/High)
   - Temperature accuracy and limits
   - Safety thresholds
   - Telemetry timing

2. **Massage Tests** (TC-MASS-001 to TC-MASS-014)
   - Enable/disable control
   - Intensity levels (1-5)
   - Pattern selection (Wave/Pulse/Continuous)
   - Pressure regulation
   - Fault detection

3. **Integration Tests** (TC-INT-001 to TC-INT-005)
   - Simultaneous operation
   - CAN communication reliability
   - Message loss handling
   - Diagnostic interface

4. **Safety Tests** (TC-SAFE-001 to TC-SAFE-004)
   - Over-temperature shutdown
   - Over-pressure relief
   - Failsafe conditions
   - Event logging

5. **Edge Cases & Stress** (TC-EDGE-001 to TC-STRESS-003)
   - Boundary conditions
   - Extended duration operation
   - Rapid state transitions

---

### Task 3: Test Automation Implementation (2 hours)

**Objectives:**
- Implement pytest-based test automation
- Create HIL interface abstraction layer
- Build data logging and reporting

**Deliverables:**
- ✅ [conftest.py](../test_scripts/conftest.py) - Test configuration and fixtures
- ✅ [test_heating_system.py](../test_scripts/test_heating_system.py) - Heating tests
- ✅ [test_massage_system.py](../test_scripts/test_massage_system.py) - Massage tests
- ✅ [test_hil_integration.py](../test_scripts/test_hil_integration.py) - Integration tests
- ✅ [utilities/hil_interface.py](../test_scripts/utilities/hil_interface.py) - HIL abstraction
- ✅ [utilities/data_logger.py](../test_scripts/utilities/data_logger.py) - Test data logging
- ✅ [utilities/signal_generator.py](../test_scripts/utilities/signal_generator.py) - Signal simulation

**To Run Tests:**

```bash
# Install dependencies
pip install pytest pytest-cov cantools python-can

# Run all tests
python -m pytest test_scripts/ -v

# Run specific test category
python -m pytest test_scripts/test_heating_system.py -v --tb=short

# Run only critical tests
python -m pytest test_scripts/ -v -m critical

# Generate coverage report
python -m pytest test_scripts/ --cov=test_scripts --cov-report=html

# Run with timeout
python -m pytest test_scripts/ -v --timeout=30
```

---

### Task 4: HIL Configuration (1 hour)

**Objectives:**
- Set up CAN interface configuration
- Define message structures
- Document wiring and connections

**Deliverables:**
- ✅ [wiring_diagram.md](../hil_config/wiring_diagram.md) - Complete HIL architecture
- ✅ [bus_definitions.dbc](../hil_config/bus_definitions.dbc) - CAN database file
- ✅ [config.ini](../config.ini) - Project configuration
- Vector CANoe configuration (optional, if tools available)

**Configuration Tasks:**
1. Understand CAN message IDs and structures
2. Review wiring diagrams and pinouts
3. Verify message timing (100ms cycles ±10ms)
4. Set up virtual CAN interface for testing

---

### Task 5: Verification Reporting (0.5-1 hour)

**Objectives:**
- Execute test suite
- Generate verification report
- Document findings and recommendations

**Deliverables:**
- Test execution log (CSV format)
- Summary report (HTML/Markdown)
- Defect list (if any failures)
- Sign-off documentation

**Report Should Include:**
1. Executive Summary
2. Test Coverage Analysis
3. Results by Category
4. Identified Defects (if any)
5. Recommendations
6. Sign-off

---

## 4. Technical Requirements

### 4.1 Hardware Prerequisites (Simulated)

The assignment uses a **simulated HIL environment** for desktop testing:

```
┌─ Python Test Framework ──┐
│  pytest + python-can     │
│  Virtual CAN interface   │
│  Simulated sensors       │
└──────────────────────────┘
     ↓
┌─ CAN Bus (virtual) ──────┐
│  500 kbps simulated      │
└──────────────────────────┘
     ↓
┌─ SCM Simulator ──────────┐
│  Mock ECU responses      │
│  Sensor simulation       │
│  State machine logic     │
└──────────────────────────┘
```

### 4.2 Software Requirements

**Required:**
- Python 3.9+
- pytest (test framework)
- pytest-cov (coverage reporting)

**Optional:**
- Vector CANoe/CANalyzer (if real HIL available)
- PEAK PCAN drivers (for hardware CAN)
- Oscilloscope software (for timing analysis)

### 4.3 Installation

```bash
# Clone/setup project
cd embedded-test-practice

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pytest pytest-cov cantools python-can

# Verify installation
pytest --version
python -m can.interfaces.virtual
```

---

## 5. Evaluation Criteria

Your assignment will be evaluated on:

### Technical Excellence (50%)
- ✅ Test coverage completeness (target ≥85%)
- ✅ Test code quality and maintainability
- ✅ Proper use of fixtures and parametrization
- ✅ Realistic HIL simulation
- ✅ Comprehensive assertions and validations

### Requirements Traceability (20%)
- ✅ All requirements covered by tests
- ✅ Traceability matrix accuracy
- ✅ Requirement ID references in tests
- ✅ Gap analysis (if any requirements uncovered)

### Documentation Quality (15%)
- ✅ Test case clarity and completeness
- ✅ HIL setup instructions
- ✅ Verification report professionalism
- ✅ Code comments and docstrings

### Problem-Solving Approach (15%)
- ✅ Logical decomposition of complex system
- ✅ Edge case identification
- ✅ Error handling strategy
- ✅ Scalability of test framework

---

## 6. Grading Scale

| Score | Assessment |
|-------|------------|
| 90-100% | Excellent - Production-ready verification suite |
| 80-89% | Very Good - Comprehensive coverage with minor gaps |
| 70-79% | Good - Solid approach with some areas for improvement |
| 60-69% | Satisfactory - Basic requirements met |
| <60% | Needs Improvement - Significant gaps or issues |

---

## 7. Tips for Success

### 7.1 Time Management
- **Hour 0-1:** Read requirements thoroughly; create mental model
- **Hour 1-2.5:** Design test cases; verify coverage
- **Hour 2.5-4.5:** Implement and debug tests
- **Hour 4.5-6:** Execute tests; generate reports

### 7.2 Best Practices
1. **Start Simple:** Implement basic tests first (enable/disable)
2. **Build Incrementally:** Add complexity gradually
3. **Use Fixtures:** Leverage pytest fixtures for setup/teardown
4. **Test Edge Cases:** Don't just happy-path testing
5. **Document Assumptions:** Explain any simplifications made

### 7.3 Common Pitfalls to Avoid
- ❌ Ignoring safety-critical requirements
- ❌ Insufficient timeout handling
- ❌ Poor test naming (non-descriptive names)
- ❌ Hard-coded values instead of configuration
- ❌ No error recovery testing
- ❌ Incomplete traceability matrix

---

## 8. References and Resources

### 8.1 Automotive Standards
- **ISO 26262:** Functional Safety for Electrical/Electronic Systems
- **AUTOSAR:** AUTomotive Open System Architecture
- **CAN 11898-1:** CAN Bus Protocol Specification

### 8.2 Testing Frameworks
- [pytest Documentation](https://docs.pytest.org/)
- [python-can Library](https://python-can.readthedocs.io/)
- [Vector CANoe](https://www.vector.com/int/en/products/products-a-z/software/canooe/)

### 8.3 Python Testing Resources
- Real Python: [Getting Started with pytest](https://realpython.com/pytest-python-testing/)
- Real Python: [CAN Bus Communication](https://realpython.com/python-can/)

---

## 9. Submission Checklist

Before submitting your assignment, verify:

- [ ] All test scripts execute without errors
- [ ] Test coverage ≥85% of requirements
- [ ] Traceability matrix complete and accurate
- [ ] HIL configuration documented
- [ ] Verification report generated
- [ ] Code is clean and well-commented
- [ ] README updated with instructions
- [ ] No hardcoded paths or credentials
- [ ] Tests pass on clean machine (try in fresh venv)
- [ ] Documentation is professional and clear

---

## 10. Next Steps After Completion

Once you've completed this assignment:

1. **Share Your Work:** Present test results and architecture
2. **Code Review:** Be prepared to discuss design decisions
3. **Extensions:** Discuss how you'd extend testing to other subsystems
4. **Production Readiness:** Discuss integration with CI/CD pipeline
5. **Standards Compliance:** Discuss alignment with automotive standards

---

**Good Luck!** This assignment demonstrates real-world verification engineering skills that are directly applicable to automotive embedded systems development.

For questions or clarifications, refer to the detailed specifications in the `requirements/` and `docs/` directories.
