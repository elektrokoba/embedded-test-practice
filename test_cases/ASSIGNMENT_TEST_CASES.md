# Test Cases - Seat Comfort Module (Home Assignment)

**Document ID:** ASSIGN-TESTCASES  
**Version:** 1.0  
**Date:** 2026-02-04  
**Total Cases:** 10

---

## Test Case Summary

| TC-ID | Category | Title | Type | Priority | Status |
|-------|----------|-------|------|----------|--------|
| TC-001 | Initialization | Boot-up Time <2s | Automated | CRITICAL | Not Executed |
| TC-002 | Heating | PWM Linearity (0-5V to 0-100%) | Automated | HIGH | Not Executed |
| TC-003 | Heating | Hysteresis Function 2°C | Automated | HIGH | Not Executed |
| TC-004 | Heating | Temperature Activation 20°C | Manual | HIGH | Not Executed |
| TC-005 | Heating | Temperature Deactivation 30°C | Manual | HIGH | Not Executed |
| TC-006 | Massage | Pressure Control 1.5-2.5 bar | Automated | HIGH | Not Executed |
| TC-007 | Massage | Cycle Timing 5min ON/1min OFF | Automated | HIGH | Not Executed |
| TC-008 | Fault | CAN Error Frame on Fault | Automated | CRITICAL | Not Executed |
| TC-009 | Fault | LED Blink 1Hz on Fault | Manual | HIGH | Not Executed |
| TC-010 | Power | Sleep Mode <50mW | Automated | MEDIUM | Not Executed |

---

## Detailed Test Cases

### TC-001: Boot-up Time Verification

**Requirement Link:** SysReq-001  
**Type:** Automated  
**Priority:** CRITICAL

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
- Boot-up completes within 2 seconds
- CAN ready message sent
- LED turns green
- System enters normal operation mode

**Pass Criteria:** Boot time ≤ 2000ms AND CAN message received

---

### TC-002: Heating PWM Linearity

**Requirement Link:** SysReq-002  
**Type:** Automated  
**Priority:** HIGH

**Pre-Condition:**
- System in run mode
- Heating element disabled
- Voltage source ready (DAC simulator)

**Test Steps:**
1. Set input voltage to 0V
2. Verify PWM output = 0%
3. Set input voltage to 2.5V (50%)
4. Verify PWM output = 50% (±2%)
5. Set input voltage to 5V
6. Verify PWM output = 100%
7. Record all intermediate measurements

**Expected Result:**
- Linear relationship: PWM% = (Input_V / 5V) * 100%
- Linearity error <3%
- Response time <100ms

**Pass Criteria:** All voltage steps produce expected PWM outputs within tolerance

---

### TC-003: Heating Hysteresis Function

**Requirement Link:** SysReq-002  
**Type:** Automated  
**Priority:** HIGH

**Pre-Condition:**
- System in run mode
- Temperature sensor simulator ready
- Heating off state

**Test Steps:**
1. Ramp temperature to 19°C (below threshold)
2. Record heating PWM = 0
3. Ramp to 20°C (activation threshold)
4. Verify heating PWM > 0
5. Ramp to 30°C (deactivation threshold)
6. Verify heating PWM = 0
7. Verify heating OFF remains at 29°C (hysteresis)
8. Repeat cycle 3 times

**Expected Result:**
- Heating activates at 20°C ±1°C
- Heating deactivates at 30°C ±1°C
- No oscillation in 20-30°C band
- 2°C hysteresis maintained

**Pass Criteria:** Temperature bands stable with <100ms oscillations

---

### TC-004: Heating Activation Below 20°C (Manual)

**Requirement Link:** SysReq-002  
**Type:** Manual  
**Priority:** HIGH

**Pre-Condition:**
- Hardware setup: Seat element, thermistor, power supply
- Thermistor positioned in heating element
- Temperature sensor calibrated

**Test Steps:**
1. Set ambient to 15°C (climatic chamber)
2. Power on system
3. Wait for boot-up (≤2s)
4. Verify heating element starts heating
5. Monitor temperature rise
6. Record activation time
7. Verify CAN "Heating_OK" message

**Expected Result:**
- Heating element activates within 5 seconds of boot
- Temperature rises from 15°C toward target
- CAN message sent within 500ms
- LED indicates heating active (blue)

**Pass Criteria:** Heating activates AND temperature rising AND CAN message present

---

### TC-005: Heating Deactivation Above 30°C (Manual)

**Requirement Link:** SysReq-002  
**Type:** Manual  
**Priority:** HIGH

**Pre-Condition:**
- System running with heating active
- Temperature at 25°C and rising
- Climate chamber set to warm

**Test Steps:**
1. Allow heating to warm element to 30°C
2. Monitor PWM signal
3. Record deactivation point
4. Verify PWM goes to 0
5. Confirm element stops heating
6. Monitor for 2-minute cooldown
7. Verify re-activation only at 20°C

**Expected Result:**
- Heating deactivates at exactly 30°C ±1°C
- PWM output drops to 0%
- Element temperature stabilizes
- No re-activation until ≤20°C

**Pass Criteria:** Deactivation at 30°C AND PWM=0 AND hysteresis maintained

---

### TC-006: Massage Pressure Control

**Requirement Link:** SysReq-003  
**Type:** Automated  
**Priority:** HIGH

**Pre-Condition:**
- Massage system pressurized to 2 bar
- Pressure sensor calibrated
- Solenoid valves ready
- CAN interface active

**Test Steps:**
1. Start massage cycle (inflate)
2. Record pressure over 30 seconds
3. Verify pressure stays 1.5-2.5 bar
4. Check for oscillations
5. Stop massage cycle (deflate)
6. Record pressure during deflation
7. Verify controlled descent to 0 bar

**Expected Result:**
- Pressure maintained in 1.5-2.5 bar band
- Oscillation <0.1 bar
- Inflation time <10s
- Deflation time <10s
- CAN message every 100ms

**Pass Criteria:** All pressure measurements within 1.5-2.5 bar range

---

### TC-007: Massage Cycle Timing

**Requirement Link:** SysReq-003  
**Type:** Automated  
**Priority:** HIGH

**Pre-Condition:**
- Massage system pressurized
- Timing reference (system clock)
- CAN monitoring active

**Test Steps:**
1. Start massage cycle counter
2. Measure ON duration (inflated state)
3. Measure OFF duration (deflated state)
4. Record cycle period
5. Repeat for 10 complete cycles
6. Calculate average timing
7. Verify max 3 cycles/hour

**Expected Result:**
- ON time: 5 min ±5% (300 ±15 sec)
- OFF time: 1 min ±5% (60 ±3 sec)
- Total cycle: 6 min ±5% (360 ±18 sec)
- 3 cycles = 18 minutes max per hour
- Timing jitter <1%

**Pass Criteria:** All cycles meet timing within ±5% tolerance

---

### TC-008: CAN Error Frame on Fault

**Requirement Link:** SysReq-004  
**Type:** Automated  
**Priority:** CRITICAL

**Pre-Condition:**
- System running normally
- CAN analyzer ready
- Fault simulation ready

**Test Steps:**
1. Simulate overcurrent condition (>10A)
2. Record time T0
3. Monitor CAN bus for error frame
4. Record error frame reception time (T1)
5. Calculate latency: T1 - T0
6. Verify error code = 0x7FF
7. Repeat for over-temperature (>50°C)

**Expected Result:**
- CAN error frame transmitted within 100ms
- Error frame ID = 0x7FF
- Error byte indicates fault type
- CAN message "Massage_Fault" sent
- System enters safe state

**Pass Criteria:** Error frame received within 100ms with correct ID and data

---

### TC-009: LED Fault Indication (Manual)

**Requirement Link:** SysReq-004  
**Type:** Manual  
**Priority:** HIGH

**Pre-Condition:**
- System running normally
- LED visible and operational
- Oscilloscope for timing measurement

**Test Steps:**
1. Simulate fault condition (current or temp)
2. Observe LED behavior
3. Measure blink frequency with oscilloscope
4. Record on-time and off-time
5. Calculate frequency: F = 1 / (Ton + Toff)
6. Verify frequency = 1Hz ±10%
7. Observe for 10 complete cycles

**Expected Result:**
- LED blinks at 1Hz ±0.1Hz
- On time ≈ 500ms ±50ms
- Off time ≈ 500ms ±50ms
- Blink pattern continuous during fault
- Returns to solid color after fault clear

**Pass Criteria:** LED frequency = 1.0Hz ±0.1Hz for entire fault duration

---

### TC-010: Sleep Mode Power Consumption

**Requirement Link:** SysReq-005  
**Type:** Automated  
**Priority:** MEDIUM

**Pre-Condition:**
- System running in normal mode
- Power meter connected
- Current measurement calibrated

**Test Steps:**
1. Record normal mode current: I_normal
2. Send system to sleep command via CAN
3. Wait 10 seconds for sleep mode entry
4. Measure sleep mode current: I_sleep
5. Record measurement for 60 seconds
6. Calculate average sleep current
7. Wake system with CAN command
8. Verify resume time <500ms

**Expected Result:**
- Sleep mode current <50mA (assuming 1V supply = <50mW)
- Normal mode current ~200-300mA
- Power reduction >80%
- Wake-up latency <500ms
- CAN communication restored
- All functions operational

**Pass Criteria:** Sleep current <50mA AND wake-up <500ms AND system operational

---

## Test Execution Matrix

| TC-ID | Manual | Automated | Tools Required | Estimated Time |
|-------|--------|-----------|-----------------|-----------------|
| TC-001 | ❌ | ✅ | CAN Analyzer, Timer | 5 min |
| TC-002 | ❌ | ✅ | DAC, Oscilloscope | 10 min |
| TC-003 | ❌ | ✅ | Temp Simulator, CAN | 15 min |
| TC-004 | ✅ | ❌ | Climate Chamber, CAN | 20 min |
| TC-005 | ✅ | ❌ | Climate Chamber, Oscilloscope | 25 min |
| TC-006 | ❌ | ✅ | Pressure Gauge, CAN | 10 min |
| TC-007 | ❌ | ✅ | CAN Analyzer, Timer | 20 min |
| TC-008 | ❌ | ✅ | CAN Analyzer, Fault Injector | 10 min |
| TC-009 | ✅ | ❌ | Oscilloscope, Visual | 10 min |
| TC-010 | ❌ | ✅ | Power Meter, CAN | 15 min |

**Total Manual Test Time:** ~55 minutes  
**Total Automated Test Time:** ~85 minutes  
**Total Duration:** ~2.5 hours (including setup)

---

## Coverage Analysis

**Requirements Coverage:**
- SysReq-001: 1 test (100%)
- SysReq-002: 4 tests (200%)
- SysReq-003: 2 tests (100%)
- SysReq-004: 2 tests (100%)
- SysReq-005: 1 test (100%)

**Total Coverage:** 10 tests / 5 requirements = **200%**

**Functional Coverage:** >80% (All critical and high-priority requirements covered)
