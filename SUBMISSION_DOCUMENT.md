# SYSTEMS VERIFICATION ENGINEER - HOME ASSIGNMENT
## Seat Comfort Module: Heating and Massage Control System

**Candidate:** _____________________  
**Date:** _____________________  
**Assignment Title:** Embedded System Test Engineering  
**Duration:** 4-6 hours  
**Document Version:** 1.0  

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Requirements Decomposition](#2-requirements-decomposition)
3. [Traceability Matrix](#3-traceability-matrix)
4. [System Wiring Diagram](#4-system-wiring-diagram)
5. [Test Cases](#5-test-cases)
6. [Test Scripts - C/CAPL Pseudo-code](#6-test-scripts---ccapl-pseudo-code)
7. [Test Report Template](#7-test-report-template)
8. [Key Performance Metrics](#8-key-performance-metrics)

---

## 1. EXECUTIVE SUMMARY

This document provides a comprehensive verification test plan for the seat comfort module, a subsystem controlling heating and massage functionality in luxury automotive applications. The module integrates:

- **Heating Control:** PWM-based temperature management with hysteresis
- **Massage System:** Pneumatic valve control with precise cycle timing
- **Safety Mechanisms:** Overcurrent and over-temperature protection
- **Communication:** CAN bus integration for vehicle network

### Scope

- **5 System Requirements** decomposed into functional segments
- **10 Test Cases** (automated and manual) with full traceability
- **VT System Compatible** hardware-in-loop architecture
- **C/CAPL Pseudo-code** examples for Vector CANoe integration
- **Submission-Ready** documentation (≤10 pages)

### Success Criteria

- ✅ Requirements coverage >80%
- ✅ All critical tests passed
- ✅ Fault handling <100ms latency
- ✅ Boot-up <2 seconds
- ✅ Clear, readable documentation

---

## 2. REQUIREMENTS DECOMPOSITION

### Overview

The seat comfort module operates on a 24V automotive power supply, controlled via CAN bus (500 kbps). Two primary functions are implemented:

1. **Heating Subsystem:** Maintains comfortable seat temperature (20-30°C operating band)
2. **Massage Subsystem:** Provides pneumatic massage with controlled cycles

### Detailed Requirements

#### **SysReq-001: Boot-up and Initialization**
- System must boot within 2 seconds
- CAN "System Ready" message transmitted after boot
- All subsystems initialized and operational
- LED indication: Green (ready), Red (fault)

#### **SysReq-002: Heating Control (PWM-based)**
- Input: 0-5V analog (linear 0-100°C temperature mapping)
- Output: PWM signal controlling heating element (20 kHz frequency)
- Activation threshold: 20°C (±1°C)
- Deactivation threshold: 30°C (±1°C)
- Hysteresis: 2°C prevents oscillation
- CAN message: "Heating_OK" when active

#### **SysReq-003: Massage Valve Control**
- Pneumatic system with 2 solenoid valves (inflate/deflate)
- Pressure maintained: 1.5-2.5 bar
- Cycle timing: 5 min ON, 1 min OFF
- Constraint: Maximum 3 cycles per hour
- Pressure feedback via sensor (0-5bar linear)

#### **SysReq-004: Fault Handling**
- CAN error frame (ID: 0x7FF) transmitted within 100ms of fault
- LED fault indication: 1Hz blink pattern
- Triggers: 
  - Current >10A (overcurrent)
  - Temperature >50°C (over-temperature)
  - CAN communication failure
- Safe state: Heating OFF, Massage OFF, LED blink

#### **SysReq-005: Sleep/Low-Power Mode**
- Power consumption <50mW in sleep state (<50mA @ 1V supply)
- Wakeup latency <500ms
- Triggered by: >3°C temperature change or CAN command
- CAN standby mode enabled

---

## 3. TRACEABILITY MATRIX

### Requirement-to-Test Mapping

| Req ID | Requirement | Test Case | Type | Priority |
|--------|-------------|-----------|------|----------|
| SysReq-001 | Boot-up <2s, CAN ready | TC-001 | Automated | CRITICAL |
| SysReq-002 | Heating PWM 0-100% linear | TC-002 | Automated | HIGH |
| SysReq-002 | Hysteresis 2°C | TC-003 | Automated | HIGH |
| SysReq-002 | Activation at 20°C | TC-004 | Manual | HIGH |
| SysReq-002 | Deactivation at 30°C | TC-005 | Manual | HIGH |
| SysReq-003 | Pressure 1.5-2.5 bar | TC-006 | Automated | HIGH |
| SysReq-003 | Cycle 5min ON/1min OFF | TC-007 | Automated | HIGH |
| SysReq-004 | CAN error <100ms | TC-008 | Automated | CRITICAL |
| SysReq-004 | LED 1Hz fault blink | TC-009 | Manual | HIGH |
| SysReq-005 | Sleep <50mW | TC-010 | Automated | MEDIUM |

**Coverage:** 10 tests / 5 requirements = **200% coverage**

---

## 4. SYSTEM WIRING DIAGRAM

### Block Diagram Overview

```
┌─────────────────────────────────────────────────────────┐
│           SEAT COMFORT SYSTEM ARCHITECTURE              │
└─────────────────────────────────────────────────────────┘

    SENSORS (Inputs)          MICROCONTROLLER          ACTUATORS (Outputs)
    
    Thermistor ─────┐         ┌──────────────┐         ┌─→ Heating PWM
    (0-5V Temp) ─┬──┼─→ ADC 0 │              │ PWM ────┤
                 │  │         │  STM32 ARM   │ Output 1 └─→ Solenoid Valve #1
    Pressure ───┼──┼─→ ADC 1  │ Cortex-M4    │
    Sensor      │  │         │              │ GPIO ────┬─→ Solenoid Valve #2
    (0-5V) ─────┼──┼─→ ADC 2  │  + CAN Intf  │ Output   └─→ LED Fault
                │  │         │              │
    Current ────┘  │         │              │ CAN TX/RX
    Sensor (0-5V)  └─→ ADC 3 │              │
                            └──────┬───────┘
                                   │
                         ┌─────────▼─────────┐
                         │  CAN Bus (500kbps)│
                         │  TJA1050 Trans    │
                         └─────────┬─────────┘
                                   │
                        ┌──────────▼──────────┐
                        │ Vector CANoe VT Sys │
                        │ HIL Simulation      │
                        └─────────────────────┘
```

### Signal Connections

**Heating Control Path:**
```
Thermistor (0-5V) → ADC0 → Temperature Logic
                           ↓
                    [T<20°C] YES → PWM Enable
                    [T>30°C] YES → PWM Disable
                           ↓
                    PWM Output (0-100%) → MOSFET → Heating Resistor
```

**Massage Control Path:**
```
Pressure (0-5V) → ADC1 → Pneumatic Logic
                         ↓
                  [Timer: 5min ON/1min OFF] → Solenoid Drivers
                         ↓
                  GPIO5 → Valve 1 (Inflate)
                  GPIO6 → Valve 2 (Deflate)
```

**Safety Path:**
```
Current (0-5V) → ADC2 → Safety Check [>10A?]
Temperature → ADC0 → Safety Check [>50°C?]
                    ↓ [FAULT DETECTED]
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
CAN Error Frame  PWM=0%           LED=1Hz
(0x7FF)         (Heating OFF)     (Blinking)
```

---

## 5. TEST CASES

### Test Case Summary

| TC-ID | Title | Type | Duration | Status |
|-------|-------|------|----------|--------|
| TC-001 | Boot-up Time <2s | Automated | 5 min | Pending |
| TC-002 | PWM Linearity | Automated | 10 min | Pending |
| TC-003 | Hysteresis 2°C | Automated | 15 min | Pending |
| TC-004 | Heating Activation | Manual | 20 min | Pending |
| TC-005 | Heating Deactivation | Manual | 25 min | Pending |
| TC-006 | Pressure Control | Automated | 10 min | Pending |
| TC-007 | Cycle Timing | Automated | 20 min | Pending |
| TC-008 | CAN Error Frame | Automated | 10 min | Pending |
| TC-009 | LED Fault Indication | Manual | 10 min | Pending |
| TC-010 | Sleep Mode | Automated | 15 min | Pending |

**Total Estimated Time:** ~2.5 hours (including setup)

### Sample Test Case Detail

**TC-001: Boot-up Time Verification**

**Requirement:** SysReq-001 - System boot-up must complete within 2 seconds

**Pre-Condition:**
- System powered off
- CAN interface ready
- HIL simulator connected

**Test Steps:**
1. Record system power-on time (T0)
2. Monitor CAN bus for "System Ready" message
3. Record message reception time (T1)
4. Calculate boot duration: T1 - T0
5. Verify boot duration ≤ 2000ms

**Expected Result:**
- Boot-up ≤ 2 seconds
- CAN message sent on startup
- LED turns green
- System ready for operation

**Pass Criteria:** Boot time ≤ 2000ms AND CAN message received

---

## 6. TEST SCRIPTS - C/CAPL Pseudo-code

### Script 1: Boot-up Test (TC-001)

```c
// CAPL Pseudo-code: Boot-up Time Measurement
dword Test_BootupTime() {
  write("LOG: Starting Boot-up Test (TC-001)\n");
  
  // Record power-on time
  gBootStartTime = GetTimeMS();
  
  // Wait for CAN ready message
  dword timeout = GetTimeMS() + 3000;
  while (!gSystemReady && (GetTimeMS() < timeout)) {
    Yield();  // Allow message reception
  }
  
  if (gSystemReady) {
    gBootDuration = GetTimeMS() - gBootStartTime;
    
    if (gBootDuration <= 2000) {
      write("LOG: PASS - Boot time: %d ms\n", gBootDuration);
      return 0;  // PASSED
    } else {
      write("LOG: FAIL - Boot time: %d ms (exceeds 2000ms)\n", gBootDuration);
      return 1;  // FAILED
    }
  } else {
    write("LOG: FAIL - System Ready message not received\n");
    return 1;  // FAILED
  }
}

// Message Handler
on message SystemReady {
  write("LOG: SystemReady CAN message received\n");
  gSystemReady = 1;
}
```

### Script 2: Fault Handling Test (TC-008)

```c
// CAPL Pseudo-code: Error Frame Transmission Test
dword Test_FaultHandling_OverCurrent() {
  write("LOG: Injecting overcurrent condition (>10A)\n");
  
  gFaultInjectionTime = GetTimeMS();
  gErrorFrameReceived = 0;
  
  // Inject >10A via VT System
  // VT_SetAnalogValue(VT_CURRENT_INPUT, 4.0);  // 4.0V = 15.7A
  
  // Monitor error frame
  dword timeout = gFaultInjectionTime + 500;
  while (!gErrorFrameReceived && (GetTimeMS() < timeout)) {
    Yield();
  }
  
  if (gErrorFrameReceived) {
    dword latency = gErrorFrameTime - gFaultInjectionTime;
    
    if (latency <= 100) {
      write("LOG: PASS - Error frame latency: %d ms\n", latency);
      return 0;  // PASSED
    } else {
      write("LOG: FAIL - Error latency exceeds 100ms: %d ms\n", latency);
      return 1;  // FAILED
    }
  } else {
    write("LOG: FAIL - Error frame not received\n");
    return 1;  // FAILED
  }
}

// Error Frame Handler
on message ErrorFrame {
  write("LOG: Error frame received (ID: 0x7FF)\n");
  gErrorFrameReceived = 1;
  gErrorFrameTime = GetTimeMS();
}
```

### Vector CANoe Integration Notes

- Use CAPL language within Vector CANoe measurement setup
- Configure VT System (VT1004/VT2504) for analog signal injection
- Enable CAN Trace for message monitoring
- Use Oscilloscope measurement tool for PWM/timing verification
- Set breakpoints on message handlers for debugging

---

## 7. TEST REPORT TEMPLATE

A comprehensive test report template is provided (see separate attachment) with sections for:

- Executive summary and key metrics
- Detailed results for all 10 test cases
- Requirements coverage analysis
- Traceability verification
- Edge case testing documentation
- Issues and recommendations
- Compliance verification

**Report Format:** PDF/Word (max 10 pages)

**Minimum Content:**
- [ ] Requirements coverage table (>80% required)
- [ ] Test execution results (Pass/Fail per TC)
- [ ] Traceability matrix verification
- [ ] Edge case findings
- [ ] Critical issues summary
- [ ] Improvement recommendations

---

## 8. KEY PERFORMANCE METRICS

### Primary Acceptance Criteria

| Metric | Target | Unit | Status |
|--------|--------|------|--------|
| Boot-up Time | <2 | seconds | ☐ Pass ☐ Fail |
| Heating Response | <5 | minutes | ☐ Pass ☐ Fail |
| Temperature Hysteresis | 2 ±0.5 | °C | ☐ Pass ☐ Fail |
| Pressure Band | 1.5-2.5 | bar | ☐ Pass ☐ Fail |
| Cycle Accuracy | ±5 | % | ☐ Pass ☐ Fail |
| Fault Detection Latency | <100 | ms | ☐ Pass ☐ Fail |
| LED Blink Frequency | 1 ±0.1 | Hz | ☐ Pass ☐ Fail |
| Sleep Mode Power | <50 | mW | ☐ Pass ☐ Fail |

### Coverage Metrics

- **Requirements Coverage:** ___% (Target: >80%)
- **Test Case Coverage:** ___% (10/10 tests planned)
- **Critical Functions:** ___% (100% target)
- **Edge Cases Tested:** ___% (>80% target)

---

## SUBMISSION CHECKLIST

Before submission, verify:

- [ ] All 5 system requirements documented
- [ ] Traceability matrix complete (10 test cases)
- [ ] VT System wiring diagram included
- [ ] C/CAPL pseudo-code examples provided (2+ scripts)
- [ ] Test report template prepared
- [ ] All requirements have clear acceptance criteria
- [ ] Document is max 10 pages (without raw data)
- [ ] All diagrams are clear and labeled
- [ ] PDF/Word format ready for submission
- [ ] Candidate name and date included

---

## DOCUMENT METADATA

**File:** Systems_Verification_Home_Assignment_v1.0  
**Format:** PDF/Word  
**Pages:** 6-10 (main document)  
**Attachments:** 
- Requirements breakdown (ASSIGNMENT_REQUIREMENTS.md)
- Test cases (ASSIGNMENT_TEST_CASES.md)
- Wiring diagram (ASSIGNMENT_WIRING_DIAGRAM.md)
- Pseudo-code (ASSIGNMENT_PSEUDOCODE_CAPL.c)
- Report template (ASSIGNMENT_TEST_REPORT_TEMPLATE.md)

**Compliance:**
- ✅ Gentherm Systems specification aligned
- ✅ Vector CANoe compatible
- ✅ ISO 26262 ASIL B considerations
- ✅ Automotive industry standards

---

## NOTES FOR CANDIDATES

### Key Points

1. **Traceability is Critical:** Every test must map to a requirement
2. **Edge Cases Matter:** Document how you handle temperature oscillations, pressure overshoot
3. **Safety First:** Over-temperature and overcurrent must trigger immediate shutdown
4. **Timing is Everything:** Fault detection <100ms is a hard requirement
5. **Documentation Quality:** Clear diagrams and tables score higher

### Common Pitfalls to Avoid

- ❌ Insufficient hysteresis causing oscillation
- ❌ Fault response >100ms latency
- ❌ Incomplete traceability matrix
- ❌ Missing edge case analysis
- ❌ Unclear test step descriptions

### Time Management

- Setup & verification: 30 minutes
- Manual tests (TC-004, 005, 009): 55 minutes
- Automated tests (TC-001, 002, 003, 006, 007, 008, 010): 85 minutes
- Report preparation: 30 minutes
- **Total: ~3.5 hours (within 4-6 hour window)**

---

## FINAL REMARKS

This assignment evaluates your ability to:
- ✅ **Decompose requirements** into testable criteria
- ✅ **Create traceability** between requirements and tests
- ✅ **Design test cases** with clear acceptance criteria
- ✅ **Understand automotive systems** (CAN, safety, temperature control)
- ✅ **Think like a verification engineer** (edge cases, fault injection, timing)

Success requires systematic thinking, clear communication, and attention to detail. Focus on completeness and clarity over complexity.

---

**Ready to Submit?** Review the checklist above, verify all attachments are included, and ensure the document flow is logical and easy to follow.

**Good luck!** 🚗✨

---

*End of Home Assignment Submission Document*  
*Version 1.0 - February 2026*
