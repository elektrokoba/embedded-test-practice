# System Requirements - Seat Comfort Module (Home Assignment)

**Document ID:** ASSIGN-SYSREQ  
**Version:** 1.0  
**Date:** 2026-02-04  
**Status:** Submission Ready

---

## 1. High-Level Requirements

The seat comfort system must meet these requirements:

1. **Heating Control:** Activation below 20°C, deactivation above 30°C (thermistors input)
2. **Massage Cycle:** 5 min ON, 1 min OFF, max 3 cycles/hour (pressure sensor feedback)
3. **CAN Bus Messaging:** ECU receives "Heating OK", "Massage Fault" states
4. **Safety Shutdown:** Current >10A or temperature >50°C
5. **Power Management:** Sleep mode <50mW in inactive state

---

## 2. Detailed System Requirements

### SysReq-001: Boot-up and Initialization
- **Requirement:** System boot-up must complete within 2 seconds
- **Details:** CAN ready message must be sent after boot
- **Acceptance Criteria:** 
  - Boot time ≤ 2s
  - CAN message sent on startup
  - System ready for operation

### SysReq-002: Heating Control (PWM-based)
- **Requirement:** Heating element PWM control 0-100% based on 0-5V input
- **Details:** 
  - Temperature hysteresis: 2°C
  - Activation threshold: 20°C
  - Deactivation threshold: 30°C
- **Acceptance Criteria:**
  - PWM linear with input voltage (0V → 0%, 5V → 100%)
  - Hysteresis prevents oscillation
  - CAN message "Heating_OK" sent when active

### SysReq-003: Massage Valve Control
- **Requirement:** Control 2 pneumatic solenoid valves (inflate/deflate)
- **Details:**
  - Pressure range: 1.5-2.5 bar
  - Cycle: 5 min ON, 1 min OFF
  - Max 3 cycles per hour
  - Pressure sensor feedback
- **Acceptance Criteria:**
  - Pressure maintained within 1.5-2.5 bar
  - Cycle timing: 5min ±5% ON, 1min ±5% OFF
  - Respects cycle limit (3/hour max)

### SysReq-004: Fault Handling
- **Requirement:** System must signal faults via CAN and LED
- **Details:**
  - CAN error frame transmission on fault
  - LED blink pattern: 1Hz frequency on fault
  - Triggers: Current >10A, Temperature >50°C, CAN error
- **Acceptance Criteria:**
  - CAN error frame sent within 100ms of fault
  - LED blinks at 1Hz (±10%)
  - CAN message "Massage_Fault" transmitted

### SysReq-005: Sleep/Low-Power Mode
- **Requirement:** System enters sleep mode when inactive
- **Details:**
  - Power consumption <50mW in sleep
  - Wakeup on temperature change >3°C or user command
  - CAN standby mode enabled
- **Acceptance Criteria:**
  - Sleep mode current <50mA
  - Wakeup time <500ms
  - CAN communication restored after wakeup

---

## 3. Traceability Matrix

| Req ID | Requirement | Segment | Test Type | Test Case |
|--------|-------------|---------|-----------|-----------|
| SysReq-001 | Boot-up <2s, CAN ready | Initialization | Automated | TC-001 |
| SysReq-002 | Heating PWM 0-100% | Heating Control | Automated | TC-002 |
| SysReq-002 | Temperature hysteresis 2°C | Heating Control | Automated | TC-003 |
| SysReq-002 | Heating activation 20°C | Heating Control | Manual | TC-004 |
| SysReq-002 | Heating deactivation 30°C | Heating Control | Manual | TC-005 |
| SysReq-003 | Pressure 1.5-2.5 bar | Massage Control | Automated | TC-006 |
| SysReq-003 | Cycle 5min ON/1min OFF | Massage Control | Automated | TC-007 |
| SysReq-004 | CAN error frame on fault | Fault Handling | Automated | TC-008 |
| SysReq-004 | LED 1Hz blink on fault | Fault Handling | Manual | TC-009 |
| SysReq-005 | Sleep mode <50mW | Power Management | Automated | TC-010 |

**Coverage:** 10/5 = 2 tests per requirement (200% coverage)

---

## 4. Input/Output Definition

### Inputs
- **Temperature Sensor (Thermistor):** 0-5V ADC (linear 0-100°C)
- **Pressure Sensor:** 0-5V ADC (linear 0-5 bar)
- **Current Sensor:** 0-5V ADC (linear 0-20A)
- **CAN Input:** Message from external controller

### Processing
- **Microcontroller:** ARM Cortex-M4 (STM32)
- **CAN Interface:** ISO 11898 (500 kbps)
- **Threshold Detection:** Hysteresis logic

### Outputs
- **Heating PWM:** Digital PWM signal (0-100% duty)
- **Valve Control:** 2 solenoid valve signals (GPIO digital)
- **CAN Output:** Status messages, error frames
- **LED Control:** GPIO for fault indication

---

## 5. Safety Requirements

| Condition | Action | Priority |
|-----------|--------|----------|
| Current > 10A | Immediate shutdown, CAN error, LED fault | CRITICAL |
| Temperature > 50°C | Immediate heating shutdown, CAN error, LED fault | CRITICAL |
| CAN Communication Loss | Maintain safe state, LED fault | HIGH |
| Pressure Out of Range | Stop massage cycle, CAN message | HIGH |
| Boot Timeout > 2s | System lockout, LED fault | HIGH |

---

## 6. Message Definitions

### CAN Message 1: System Status (ID: 0x100)
```
Byte 0: Heating Status (0=OFF, 1=ON)
Byte 1: Massage Status (0=OFF, 1=ON)
Byte 2: Current (0-255 maps to 0-20A)
Byte 3: Temperature (0-255 maps to 0-100°C)
Byte 4: Pressure (0-255 maps to 0-5bar)
Byte 5: Error Flags (bit 0=overtemp, bit 1=overcurrent, bit 2=comms_fail)
Byte 6-7: Reserved
```

### CAN Message 2: Error Frame (ID: 0x7FF)
```
Trigger: Any CRITICAL condition
Data: Error code + timestamp
Standard CAN error frame format
```

---

## 7. Requirements Coverage Summary

- ✅ Boot-up and initialization (SysReq-001)
- ✅ Heating PWM control (SysReq-002)
- ✅ Massage valve control (SysReq-003)
- ✅ Fault handling (SysReq-004)
- ✅ Sleep mode (SysReq-005)

**Total Requirements:** 5  
**Total Test Cases:** 10  
**Coverage:** 200%
