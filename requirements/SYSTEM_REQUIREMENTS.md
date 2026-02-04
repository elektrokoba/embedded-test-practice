# System Requirements - Seat Comfort Module

**Document ID:** SYSREQ-001  
**Version:** 1.0  
**Date:** 2026-02-04  
**Status:** Draft

---

## 1. System Overview

### 1.1 Purpose
The Seat Comfort Module (SCM) provides integrated heating and pneumatic massage functionality for automotive front-row seats. The system enhances passenger comfort and is controlled via CAN-based vehicle network.

### 1.2 System Scope
- Electric heating element control (0-65°C)
- Pneumatic massage pump and valve control
- Multiple intensity levels and massage patterns
- Safety interlocks and fault detection
- Thermal and pressure monitoring

### 1.3 Design Life
- Vehicle operational life: 10 years
- Expected seat usage: 5,000+ operating hours
- Environmental: -40°C to +85°C ambient
- ASIL Classification: ASIL B (Functional Safety)

---

## 2. Functional Requirements

### 2.1 Heating Subsystem

| Req ID | Description | Acceptance Criteria | Priority |
|--------|-------------|-------------------|----------|
| HEAT-001 | System shall support heating on/off control | Control via CAN message | HIGH |
| HEAT-002 | System shall support 3 heating intensity levels (Low: 30W, Medium: 50W, High: 70W) | Selectable via CAN command | HIGH |
| HEAT-003 | System shall maintain setpoint temperature within ±2°C tolerance | Temperature sensor feedback | HIGH |
| HEAT-004 | Heating element shall reach 40°C from cold start within 120 seconds | Maximum 120s ramp-up time | HIGH |
| HEAT-005 | System shall limit maximum temperature to 65°C (hardware limit) | Enforced by firmware | HIGH |
| HEAT-006 | System shall disable heating if seat temperature > 68°C | Safety shutdown | CRITICAL |
| HEAT-007 | System shall provide temperature telemetry every 100ms | CAN message SEAT_HEAT_STATUS | HIGH |
| HEAT-008 | System shall handle power supply voltage variations (8V to 14.4V) | Maintain stability across range | HIGH |
| HEAT-009 | System shall log heating events for diagnostics | Event timestamps and duration | MEDIUM |

### 2.2 Pneumatic Massage Subsystem

| Req ID | Description | Acceptance Criteria | Priority |
|--------|-------------|-------------------|----------|
| MASS-001 | System shall support massage on/off control | Control via CAN message | HIGH |
| MASS-002 | System shall support 5 massage intensity levels (1-5) | Duty cycle 20% to 100% | HIGH |
| MASS-003 | System shall support 3 massage patterns (Wave, Pulse, Continuous) | Pattern selection via CAN | HIGH |
| MASS-004 | Pneumatic pressure shall be maintained at 120 ± 10 kPa during operation | Pressure regulator control | HIGH |
| MASS-005 | Pump shall start within 500ms of command | Quick response requirement | HIGH |
| MASS-006 | System shall limit maximum pressure to 150 kPa (safety relief) | Hardware pressure valve | CRITICAL |
| MASS-007 | System shall provide pressure and pump status telemetry every 100ms | CAN message SEAT_MASSAGE_STATUS | HIGH |
| MASS-008 | System shall automatically stop after 30 minutes of continuous operation | Energy/comfort management | HIGH |
| MASS-009 | System shall detect and log pump failures (pressure not reached within 10s) | Fault detection and logging | MEDIUM |

### 2.3 Integration Requirements

| Req ID | Description | Acceptance Criteria | Priority |
|--------|-------------|-------------------|----------|
| INT-001 | System shall support simultaneous heating and massage operation | Both subsystems active together | HIGH |
| INT-002 | CAN message cycle time shall be 100ms (±10ms) | Real-time performance | HIGH |
| INT-003 | System shall handle CAN message loss gracefully (timeout after 500ms) | Safe state on communication loss | CRITICAL |
| INT-004 | System shall support seat position sensors for context-aware operation | Integrated passenger detection | MEDIUM |
| INT-005 | System shall provide diagnostic CAN interface for troubleshooting | Extended diagnostics support | MEDIUM |

### 2.4 Safety Requirements

| Req ID | Description | Acceptance Criteria | Priority |
|--------|-------------|-------------------|----------|
| SAFE-001 | System shall fail safe on microcontroller failure | Known safe state | CRITICAL |
| SAFE-002 | Over-temperature shall trigger immediate heating shutoff | >68°C threshold | CRITICAL |
| SAFE-003 | Over-pressure shall trigger pump shutoff | >150 kPa pressure relief | CRITICAL |
| SAFE-004 | System shall support diagnostic CAN read of all sensor values | Health monitoring | HIGH |
| SAFE-005 | System shall log all fault events with timestamp | Fault tracking for analysis | HIGH |

---

## 3. Performance Requirements

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Heating Response Time | <120 | seconds (0°C to 40°C) |
| Massage Response Time | <500 | milliseconds |
| CAN Cycle Time | 100 | milliseconds |
| Temperature Accuracy | ±2 | °C |
| Pressure Accuracy | ±3 | kPa |
| Operating Voltage Range | 8.0 - 14.4 | Volts |
| Maximum Current Draw | 15 | Amperes (heating max) |

---

## 4. CAN Message Specifications

### 4.1 Command Messages

**SEAT_CTRL_CMD (0x100) - Sent by Head Unit to SCM**
```
Byte 0-1: Heat Control
  - Bit 0: Heat Enable (0=Off, 1=On)
  - Bits 1-2: Heat Intensity (0=Low, 1=Med, 2=High)
  - Bits 3-7: Reserved

Byte 2-3: Massage Control
  - Bit 0: Massage Enable (0=Off, 1=On)
  - Bits 1-3: Massage Intensity (1-5)
  - Bits 4-6: Massage Pattern (0=Wave, 1=Pulse, 2=Continuous)
  - Bit 7: Reserved

Byte 4-7: Reserved for future use
```

### 4.2 Status Messages

**SEAT_HEAT_STATUS (0x200) - Sent by SCM every 100ms**
```
Byte 0: Temperature (0-255 maps to 0-100°C)
Byte 1: Heater Duty Cycle (0-255 maps to 0-100%)
Byte 2: Heat Status Flags
  - Bit 0: Heating Active
  - Bit 1: Temperature Warning (>65°C)
  - Bit 2: Heater Fault
  - Bits 3-7: Reserved

Bytes 3-7: Reserved
```

**SEAT_MASSAGE_STATUS (0x300) - Sent by SCM every 100ms**
```
Byte 0: Pressure (0-255 maps to 0-200 kPa)
Byte 1: Pump Duty Cycle (0-255 maps to 0-100%)
Byte 2: Massage Status Flags
  - Bit 0: Pump Active
  - Bit 1: Pressure Warning (>150 kPa)
  - Bit 2: Pump Fault
  - Bits 3-7: Reserved

Bytes 3-7: Reserved
```

---

## 5. Acceptance Criteria

The system is considered acceptable when:
1. ✅ All CRITICAL safety requirements are met
2. ✅ All HIGH priority functional requirements are verified
3. ✅ No unresolved safety-related defects
4. ✅ Test coverage ≥ 85% of requirements
5. ✅ All integration tests pass
6. ✅ Performance specifications met under nominal and edge conditions

---

## 6. References

- ISO 26262: Functional Safety for Electrical/Electronic Systems
- AUTOSAR: AUTomotive Open System Architecture
- CAN ISO 11898-1: Standard for CAN Bus Protocol
