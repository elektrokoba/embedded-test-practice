# Functional Requirements - Seat Comfort Module

**Document ID:** FUNCREQ-001  
**Version:** 1.0  
**Date:** 2026-02-04

---

## 1. Heating Subsystem - Detailed Functional Specifications

### 1.1 Operating Modes

#### Mode 1: Off
- Heating element de-energized
- Temperature monitoring continues
- Response to activation within 100ms

#### Mode 2: Low Intensity (30W)
- Heating element power: 30W ± 3W
- Target temperature: 40°C
- Ramp time: 120-180 seconds from 20°C
- Thermostat control: ±2°C accuracy

#### Mode 3: Medium Intensity (50W)
- Heating element power: 50W ± 5W
- Target temperature: 50°C
- Ramp time: 90-120 seconds from 20°C
- Thermostat control: ±2°C accuracy

#### Mode 4: High Intensity (70W)
- Heating element power: 70W ± 7W
- Target temperature: 60°C
- Ramp time: 60-90 seconds from 20°C
- Thermostat control: ±2°C accuracy

### 1.2 Functional Behavior

**Temperature Ramp Profile:**
- Phase 1 (0-30s): Maximum power application
- Phase 2 (30-60s): Proportional control begins
- Phase 3 (60+s): PID thermostat maintains setpoint

**Overshoot Protection:**
- Maximum allowed overshoot: 5°C above setpoint
- Overshoot recovery time: <30 seconds

**Hysteresis:**
- Turn-on threshold: Setpoint - 1°C
- Turn-off threshold: Setpoint + 2°C
- Prevents relay chatter

### 1.3 Fault Detection and Response

| Fault Condition | Detection Method | Response |
|-----------------|------------------|----------|
| Temperature sensor open circuit | No change after 60s at max power | Disable heater, log event |
| Temperature sensor short circuit | Reading > 95°C after 10s | Disable heater, log event |
| Heating element open | Current = 0 after enable | Log event, retry enabled |
| Over-temperature (>68°C) | Sensor reading | Immediate shutdown |
| CAN message loss | No message for 500ms | Maintain current state, log timeout |

### 1.4 State Machine

```
┌─────────┐
│   OFF   │
└────┬────┘
     │ Enable command
     ▼
┌─────────────┐
│  RAMPING    │ (Heating at max power)
└────┬────────┘
     │ Temperature approaches setpoint
     ▼
┌─────────────┐
│  STEADY     │ (Thermostat control active)
└────┬────────┘
     │ Disable command
     ▼
┌─────────┐
│   OFF   │
└─────────┘
     ▲
     │ Safety threshold exceeded
     │
┌─────────────┐
│  FAULT_SAFE │ (Heating disabled)
└─────────────┘
```

---

## 2. Pneumatic Massage Subsystem - Detailed Functional Specifications

### 2.1 Operating Modes

#### Mode 0: Off
- Pump de-energized
- Solenoid valves de-energized
- Pressure bleeds down over 5-10 seconds

#### Mode 1: Continuous Pattern
- Pump runs continuously
- Air pressure maintained at setpoint
- Valve pattern: All massage zones active

#### Mode 2: Wave Pattern
- Pump operates in duty-cycle mode
- Sequential activation of massage zones
- Cycle time: 4 seconds
- Sequence: Left → Center → Right → Center → repeat

#### Mode 3: Pulse Pattern
- Pump operates with 1-second ON/OFF cycles
- All zones active simultaneously
- Provides rhythmic massage effect

### 2.2 Intensity Levels

| Level | Pump Duty Cycle | Pressure Target |
|-------|-----------------|-----------------|
| 1 (Min) | 20% | 80 kPa |
| 2 | 40% | 100 kPa |
| 3 (Mid) | 60% | 120 kPa |
| 4 | 80% | 140 kPa |
| 5 (Max) | 100% | 150 kPa |

### 2.3 Functional Behavior

**Pressure Control:**
- Regulator maintains ±10 kPa of setpoint
- Proportional valve modulation
- Pressure feedback from transducer every 50ms

**Response Timing:**
- Pump start-up: <500ms to reach target pressure
- Pump shutdown: <2s for pressure relief
- Pattern switching: <100ms synchronization

**Auto-Shutdown:**
- After 30 minutes continuous operation: Pump stops
- User must re-enable massage function
- Prevents seat overheating and energy drain

**Pressure Relief:**
- Safety relief valve: Opens at 150 kPa
- Manual relief: Solenoid valve energization stops pump
- Failsafe: Spring-loaded to open position on loss of control signal

### 2.4 Pattern Definitions

**Wave Pattern Sequence (4-second cycle):**
```
Time 0.0s: Zone L pump → valve opens (1s)
Time 1.0s: Zone L pump → valve closes, Zone C pump → valve opens (1s)
Time 2.0s: Zone C pump → valve closes, Zone R pump → valve opens (1s)
Time 3.0s: Zone R pump → valve closes, Zone C pump → valve opens (1s)
Time 4.0s: Repeat from beginning
```

**Pulse Pattern (1-second cycle):**
```
Time 0.0s: All zones → pump ON (0.5s)
Time 0.5s: All zones → pump OFF (0.5s)
Time 1.0s: Repeat from beginning
```

### 2.5 Fault Detection and Response

| Fault Condition | Detection Method | Response |
|-----------------|------------------|----------|
| Pressure not reached in 10s | Pressure <80% setpoint | Log fault, disable pump |
| Pressure loss | Pressure drop >30 kPa/s | Log fault, attempt restart |
| Over-pressure condition | Pressure >150 kPa | Activate relief valve |
| Pump stalled | No pressure change for 5s | Log fault, disable pump |
| CAN message loss | No message for 500ms | Maintain current pattern, log timeout |

---

## 3. System Integration

### 3.1 Simultaneous Operation

Both heating and massage can operate independently:
- Heating power draw: <10A
- Massage pump draw: <8A
- Total system draw: <15A (battery managed)

No functional interference between subsystems.

### 3.2 Diagnostics and Monitoring

**Available Sensor Values (CAN Read):**
- Heating: Temperature, Heater Duty Cycle, Status Flags
- Massage: Pressure, Pump Duty Cycle, Status Flags, Remaining Runtime
- System: Voltage, Current, Temperature Warnings

**Event Logging:**
- All faults logged with timestamp
- Last 100 events stored in non-volatile memory
- Accessible via CAN diagnostic interface

### 3.3 Communication Protocol

**Message Sequence (100ms cycle):**
```
T=0ms:   Host sends SEAT_CTRL_CMD
T=1ms:   SCM processes command
T=2-10ms: SCM updates internal state, sensor readings
T=50ms:  SCM transmits status telemetry
T=100ms: Cycle repeats
```

**Message Loss Handling:**
- Detection timeout: 500ms of no SEAT_CTRL_CMD
- Action: SCM maintains last known command state
- User notification: Status flag set in telemetry
- Recovery: Automatic when messages resume

---

## 4. Performance Metrics

### 4.1 Response Characteristics

| Parameter | Specification | Test Condition |
|-----------|---------------|-----------------|
| Heating Enable to 50% power | <50ms | CAN command to PWM output |
| Massage Enable to 50% pressure | <300ms | CAN command to solenoid valve |
| CAN Jitter | <±15ms | Measured cycle-to-cycle variation |
| Sensor Latency | <100ms | Sensor reading to CAN transmission |

### 4.2 Reliability

- MTBF (Mean Time Between Failures): > 10,000 hours
- Availability target: 99.5%
- Fault detection coverage: > 90% of detectable faults

### 4.3 Power Efficiency

- Heating idle current: <50mA
- Massage idle current: <50mA
- Heating Max power: 70W
- Massage Max power: 12W

---

## 5. Design Constraints

- CAN baud rate: 500 kbps
- Message ID allocation: 0x100-0x3FF reserved for SCM
- Update frequency: 100ms (±10ms tolerance)
- Temperature sensor: NTC thermistor, 0-100°C range
- Pressure sensor: 0-200 kPa output

---

## Traceability

All functional requirements map to system requirements:
- HEAT-001 ↔ Mode selection functionality
- MASS-001 ↔ Mode selection functionality
- INT-001 ↔ Simultaneous operation capability
- SAFE-001 ↔ Fault detection and failsafe response
