# HIL Wiring Diagram and Architecture

**Document ID:** HIL-001  
**Version:** 1.0  
**Date:** 2026-02-04

---

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Host Test Computer                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Python Test Framework (pytest)                          │   │
│  │  - test_heating_system.py                                │   │
│  │  - test_massage_system.py                                │   │
│  │  - test_hil_integration.py                               │   │
│  │  - conftest.py (fixtures & config)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│               ↓                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  HIL Interface Layer (hil_interface.py)                   │   │
│  │  - CAN Message Formatting                                │   │
│  │  - Simulated Sensor Readings                             │   │
│  │  - Control Command Injection                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│               ↓                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  CAN Interface (Virtual or Hardware)                      │   │
│  │  - python-can library                                     │   │
│  │  - 500 kbps baud rate                                     │   │
│  │  - Virtual CAN interface (for desktop testing)            │   │
│  │  - Hardware CAN interface (for real HIL)                  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         ↓ CAN Bus (500 kbps)
┌─────────────────────────────────────────────────────────────────┐
│              Seat Comfort Module ECU (Target)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  CAN Interface Module                                    │   │
│  │  - Message ID 0x100: SEAT_CTRL_CMD (from host)          │   │
│  │  - Message ID 0x200: SEAT_HEAT_STATUS (to host)         │   │
│  │  - Message ID 0x300: SEAT_MASSAGE_STATUS (to host)      │   │
│  └──────────────────────────────────────────────────────────┘   │
│               ↓                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Heating Control Module      │  Massage Control Module   │   │
│  │  - Temperature Sensor        │  - Pressure Sensor       │   │
│  │  - PWM Heater Driver         │  - Pump Motor Driver     │   │
│  │  - Thermostat Logic          │  - Solenoid Valve Ctrl   │   │
│  │  - Over-temp Protection      │  - Relief Valve Ctrl     │   │
│  └──────────────────────────────────────────────────────────┘   │
│               ↓                                   ↓               │
│  ┌────────────────────────┐        ┌──────────────────────────┐  │
│  │  Heating System        │        │  Pneumatic System        │  │
│  │  - Heater Element      │        │  - Pump Motor            │  │
│  │  - Temp Sensor (NTC)   │        │  - Pressure Regulator    │  │
│  │  - Fuse/Protection     │        │  - Relief Valve          │  │
│  │  - Vehicle Power 12V   │        │  - Solenoid Valves       │  │
│  └────────────────────────┘        │  - Manifold              │  │
│                                    │  - Vehicle Power 12V     │  │
│                                    └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. CAN Bus Specification

### 2.1 Physical Layer
- **Standard:** ISO 11898-1
- **Baud Rate:** 500 kbps
- **Bus Type:** Two-wire (CAN_H, CAN_L)
- **Cable Impedance:** 120Ω termination at each end

### 2.2 Message IDs and Allocation

```
0x100 - SEAT_CTRL_CMD (Host → SCM, Periodic, 100ms)
  Priority: HIGH
  Data Length: 8 bytes
  Format: [Heat_Ctrl | Massage_Ctrl | Reserved x6]

0x200 - SEAT_HEAT_STATUS (SCM → Host, Periodic, 100ms)
  Priority: HIGH
  Data Length: 8 bytes
  Format: [Temp | Duty | Flags | Reserved x5]

0x300 - SEAT_MASSAGE_STATUS (SCM → Host, Periodic, 100ms)
  Priority: HIGH
  Data Length: 8 bytes
  Format: [Pressure | Duty | Flags | Reserved x5]

0x7DF - SEAT_DIAGNOSTIC_CMD (Host → SCM, On-demand)
  Priority: LOW
  Data Length: 8 bytes
  Format: UDS Diagnostic Service

0x7E8 - SEAT_DIAGNOSTIC_RESPONSE (SCM → Host, On-demand)
  Priority: LOW
  Data Length: 8 bytes
  Format: UDS Diagnostic Response
```

---

## 3. Hardware Interface Wiring (Physical ECU)

### 3.1 Heating Circuit

```
┌─ Vehicle 12V Battery (8-14.4V)
│
├─ FUSE (15A)
│
├─ N-Channel MOSFET Driver (High-side PWM)
│
├─ Heating Element (70W max)
│
├─ Current Sense Resistor (0.1Ω)
│
└─ GND (Negative)

Temperature Sensor (NTC):
├─ ADC_IN1 (0-3.3V) ← Thermistor divider
├─ Reference Voltage
└─ GND
```

### 3.2 Pneumatic Circuit

```
┌─ Vehicle 12V Battery
│
├─ FUSE (15A)
│
├─ Relay Driver (Pump Motor)
│ │
│ ├─ Pump Motor (12V DC, <8A)
│ └─ Freewheel Diode
│
├─ Pressure Relief Valve (150 kPa set point)
│
├─ Proportional Solenoid Valve (PWM Control)
│ │
│ ├─ Manifold with Zone Valves
│ └─ Seat Massage Zones (Left, Center, Right)
│
├─ Pressure Sensor (0-200 kPa)
│ │
│ ├─ ADC_IN2 (0-3.3V) ← Pressure transducer
│ └─ 4-20mA loop option
│
└─ GND (Negative)
```

### 3.3 CAN Bus Interface

```
CAN High (CAN_H)  ─── Termination Resistor 120Ω ───
    │
    ├─ SCM CAN Transceiver
    ├─ Test Computer CAN Interface
    └─ Other Vehicle Nodes

CAN Low (CAN_L)   ─── Termination Resistor 120Ω ───
    │
    └─ GND (Common Ground)
```

---

## 4. Vector CANoe Configuration

### 4.1 Database Definition (DBC)

```
BO_ 256 SEAT_CTRL_CMD: 8 Vector__XXX
 SG_ HeatEnable : 0|1@1+ (1,0) [0|1] "" Vector__XXX
 SG_ HeatIntensity : 1|2@1+ (1,0) [0|3] "" Vector__XXX
 SG_ MassageEnable : 8|1@1+ (1,0) [0|1] "" Vector__XXX
 SG_ MassageIntensity : 9|3@1+ (1,0) [0|5] "" Vector__XXX
 SG_ MassagePattern : 12|3@1+ (1,0) [0|7] "" Vector__XXX

BO_ 512 SEAT_HEAT_STATUS: 8 Vector__XXX
 SG_ Temperature : 0|8@1+ (0.39,0) [0|100] "C" Vector__XXX
 SG_ HeaterDutyCycle : 8|8@1+ (0.39,0) [0|100] "%" Vector__XXX
 SG_ HeatingActive : 16|1@1+ (1,0) [0|1] "" Vector__XXX
 SG_ TempWarning : 17|1@1+ (1,0) [0|1] "" Vector__XXX
 SG_ HeaterFault : 18|1@1+ (1,0) [0|1] "" Vector__XXX

BO_ 768 SEAT_MASSAGE_STATUS: 8 Vector__XXX
 SG_ Pressure : 0|8@1+ (0.78,0) [0|200] "kPa" Vector__XXX
 SG_ PumpDutyCycle : 8|8@1+ (0.39,0) [0|100] "%" Vector__XXX
 SG_ PumpActive : 16|1@1+ (1,0) [0|1] "" Vector__XXX
 SG_ PressureWarning : 17|1@1+ (1,0) [0|1] "" Vector__XXX
 SG_ PumpFault : 18|1@1+ (1,0) [0|1] "" Vector__XXX
```

### 4.2 Simulation Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CANoe>
  <Configuration>
    <Application Name="Seat_Comfort_Module_HIL">
      <Database File="bus_definitions.dbc"/>
      
      <Bus Name="HighSpeedCAN">
        <BaudRate>500000</BaudRate>
        <SimulatedNodes>
          <Node Name="SeatComfortModule">
            <SendMessage ID="0x200" Cycle="100ms"/>
            <SendMessage ID="0x300" Cycle="100ms"/>
            <ReceiveMessage ID="0x100"/>
          </Node>
        </SimulatedNodes>
      </Bus>
      
      <VirtualChannels>
        <Channel Name="Heating_Temp_Input"/>
        <Channel Name="Heating_Enable_Output"/>
        <Channel Name="Massage_Pressure_Input"/>
        <Channel Name="Pump_Enable_Output"/>
      </VirtualChannels>
    </Application>
  </Configuration>
</CANoe>
```

---

## 5. Python-CAN Interface Setup

### 5.1 Virtual CAN Interface (Linux/macOS)

```bash
# Create virtual CAN interface
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Verify
ip link show vcan0

# Python code
import can

# Connect to virtual interface
bus = can.interface.Bus(channel='vcan0', bustype='virtual', bitrate=500000)

# Send message
msg = can.Message(arbitration_id=0x100, data=[0x01, 0x03], is_extended_id=False)
bus.send(msg)

# Receive message
msg = bus.recv(timeout=1.0)
```

### 5.2 Hardware CAN Interface (with PEAK PCAN-USB)

```bash
# Install drivers
# For PEAK PCAN-USB on macOS:
# https://www.peak-system.com/produktdatenblaetter/

# Python code
import can

# Connect to PCAN interface
bus = can.interface.Bus(
    channel='PCAN_USB1',
    bustype='pcan',
    bitrate=500000
)
```

---

## 6. Test Environment Setup Checklist

### 6.1 Hardware Setup
- [ ] Vehicle ECU with CAN transceiver
- [ ] CAN bus with 120Ω termination resistors
- [ ] 12V power supply (8-14.4V adjustable for testing)
- [ ] Temperature sensor simulator or thermocouple
- [ ] Pressure transducer simulator
- [ ] CAN interface adapter (USB or PCIe)
- [ ] Multimeter for voltage/current measurements

### 6.2 Software Setup
- [ ] Python 3.9+ installed
- [ ] pytest and dependencies (`pip install -r requirements.txt`)
- [ ] Vector CANoe or CANalyzer (if using Vector tools)
- [ ] DBC file loaded in HIL simulator
- [ ] Virtual CAN interface created (for desktop testing)

### 6.3 Calibration Steps
1. Verify 12V supply voltage is stable 13.2V ±0.2V
2. Check CAN bus termination: measure 60Ω between CAN_H and CAN_L
3. Verify temperature sensor linearity across 0-100°C
4. Verify pressure sensor linearity across 0-200 kPa
5. Confirm CAN communication: capture messages at 100ms intervals

---

## 7. Message Sequence Diagram

```
Host PC                      CAN Bus                  SCM ECU
  │                            │                         │
  ├──── SEAT_CTRL_CMD(0x100) ─>│ Heat_Enable=1 ────────>│
  │     [Heat:1, Massage:0]    │                         │
  │                            │ <──── SEAT_HEAT_STATUS ─┤
  │                            │       Temp=25°C,Duty=50%│
  │                            │                         │
  ├──────────────── 100ms ─────┼─────────────────────────┤
  │                            │                         │
  ├──── SEAT_CTRL_CMD(0x100) ─>│ Massage_Enable=1 ─────>│
  │     [Heat:1, Massage:3]    │                         │
  │                            │ <──── SEAT_MASSAGE_STATUS
  │                            │       Pressure=120kPa   │
  │                            │                         │
  ├──────────────── 100ms ─────┼─────────────────────────┤
  │                            │                         │
  │                            │ <──── Status Updates ───┤
  │                            │       every 100ms       │
  │                            │                         │
  └─── (Repeats indefinitely) ─┴─────────────────────────┘
```

---

## 8. Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|---|---|---|
| CAN messages not received | Bus not terminated | Check 120Ω resistors at both ends |
| Intermittent communication | Loose CAN connectors | Reseat connectors; verify shield grounding |
| Messages received but corrupted | Baud rate mismatch | Verify all nodes set to 500 kbps |
| Temperature not changing | Sensor simulator not connected | Verify ADC channel, check simulator output |
| Pressure reading stuck | Pressure sensor fault | Test sensor with multimeter; check 4-20mA loop |
| ECU not responding | ECU firmware issue | Reprogram ECU; verify watchdog timer |
| Tests timeout | HIL communication lag | Increase timeout; check CAN load |

---

## 9. Performance Monitoring

### Key Metrics to Monitor

- **CAN Bus Load:** Should be <30% at nominal message rate
- **Message Latency:** <5ms round-trip (host → ECU → host)
- **Jitter:** <±15ms on 100ms cycle
- **Temperature Ramp:** <120s from 20°C to 40°C
- **Pressure Buildup:** <500ms to reach 100 kPa
- **Current Draw:** Heating <10A, Pump <8A

### Tools for Monitoring

- **Vector CANoe:** Real-time CAN traffic analysis
- **python-can:** Message rate, timing statistics
- **Oscilloscope:** PWM signal verification
- **Multimeter:** Voltage/current measurements
