# VT System Wiring Diagram - Seat Comfort Module (Home Assignment)

**Document ID:** ASSIGN-WIRING  
**Version:** 1.0  
**Date:** 2026-02-04  
**Format:** Block Diagram with Component Connections

---

## System Architecture Block Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SEAT COMFORT SYSTEM - VT SYSTEM WIRING                 │
└─────────────────────────────────────────────────────────────────────────────┘

                           ┌──────────────────────────┐
                           │   MICROCONTROLLER        │
                           │   (STM32 ARM Cortex-M4)  │
                           │                          │
                    ┌──────┼──────────────────────┬───┼──────────────────┐
                    │      │                      │   │                  │
                    │      └──────────────────────┘   │                  │
                    │                                 │                  │
                    │                                 │                  │
        ┌───────────▼──────────┐       ┌─────────────▼──────┐   ┌──────▼──────┐
        │  ADC INPUTS          │       │  PWM OUTPUT        │   │ GPIO OUTPUT │
        │  (0-5V Range)        │       │  (Frequency: 20kHz)│   │ (Digital)   │
        └──┬──────────┬────┬───┘       └────┬────┬─────────┘   └─┬───┬──────┘
           │          │    │               │    │             │   │
           │          │    │               │    │             │   │
    ┌──────▼──┐ ┌────▼───┐│  ┌───────────▼┐  ┌▼────────┐  ┌─▼─┬─▼──┐
    │Thermistor│ │Pressure││  │ Heating    │  │Valve    │  │LED │CAN │
    │(Temp)    │ │Sensor  ││  │ PWM Driver │  │Solenoid1│  │Ctrl│IO  │
    │          │ │(Massage)│  │            │  │         │  │    │    │
    └──────────┘ └────────┘│  └────────────┘  └─────────┘  └────┴────┘
                           │
    ┌──────────────────────┐│  ┌───────────────────────┐
    │ Current Sensor ADC   ││  │ Valve Solenoid Driver │
    │ (0-20A range)        ││  │ (2x Outputs)          │
    └──────────────────────┘│  └──────────┬────────────┘
                           │             │
                           │          ┌──▼──────────┐
                           │          │Solenoid #2  │
                           │          │             │
                           │          └─────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │     CAN INTERFACE                   │
        │     (ISO 11898 - 500 kbps)          │
        │     TJA1050 CAN Transceiver         │
        └──────────────┬───────────────────────┘
                       │
                  ┌────▼────┐
                  │ CAN Bus  │
                  │ (2-wire) │
                  └────┬─────┘
                       │
        ┌──────────────▼──────────────┐
        │  HIL/VECTOR CANoe VT SYSTEM │
        │  - Signal Simulation        │
        │  - CAN Message Analysis     │
        │  - Real-time Monitoring     │
        └─────────────────────────────┘
```

---

## Detailed Component Connections

### 1. TEMPERATURE CONTROL PATH

```
Thermistor (Seat Sensor)
    ↓
    └─→ [10kΩ Pull-up] ─→ ADC Channel 0 (STM32)
        Range: 0-5V (Linear)
        Conversion: ADC_Val × (100°C / 4095) = Temperature
        
        ↓ [Logic: T < 20°C → Heating ON]
        
PWM Output (Timer 2, Channel 1)
    ↓
    └─→ [MOSFET Driver] ─→ [Heating Resistor Element]
        Frequency: 20 kHz
        Duty Cycle: 0-100%
        Load: 6Ω, 24W max at 100%
        
        ↓ [CAN Message: Heating_Status]
        
CAN TX → Vector CANoe VT System
```

### 2. MASSAGE CONTROL PATH

```
Pressure Sensor (Pneumatic System)
    ↓
    └─→ [Voltage Divider] ─→ ADC Channel 1 (STM32)
        Range: 0-5V (0-5 bar linear)
        Conversion: ADC_Val × (5bar / 4095) = Pressure
        
        ↓ [Timer: 5min ON / 1min OFF cycle]
        
GPIO Output #1 (Pin PA5) → Solenoid Valve #1 (Inflate)
GPIO Output #2 (Pin PA6) → Solenoid Valve #2 (Deflate)
        
    ↓ [Pressure Feedback Loop: Target 1.5-2.5 bar]
        
CAN TX → Vector CANoe VT System
    Message: Pressure_Value, Massage_Status, Cycle_Count
```

### 3. CURRENT MONITORING PATH

```
Current Sensor (0-20A Hall Effect)
    ↓
    └─→ [Signal Conditioning] ─→ ADC Channel 2 (STM32)
        Range: 0-5V (0-20A linear)
        Conversion: ADC_Val × (20A / 4095) = Current
        
        ↓ [Threshold Check: > 10A]
        ↓ [If exceeds → FAULT]
        
GPIO Output → LED (Red) - Fault Indication
CAN Error Frame TX → Vector CANoe VT System
```

### 4. TEMPERATURE PROTECTION PATH

```
Temperature Sensor Reading (ADC Channel 0)
    ↓
    └─→ [Threshold Check: > 50°C]
        ↓ [If exceeds → SAFETY SHUTDOWN]
        
GPIO Output → LED (Red) - Fault Indication
PWM Output → 0% (Heating OFF)
Solenoid Valves → Deflate (Massage OFF)
CAN Error Frame TX → Vector CANoe VT System
    Message: Error_Code = 0x02 (Over-Temperature)
```

### 5. CAN BUS ARCHITECTURE

```
STM32 Microcontroller
    │
    ├─ CAN TX (PD1)
    ├─ CAN RX (PD0)
    │
    └─→ [TJA1050 CAN Transceiver]
            │
            ├─ CAN_H (High)
            └─ CAN_L (Low)
                │
    ┌───────────┼───────────┐
    │           │           │
    │      ┌────▼────┐      │
    │      │ Vector  │      │
    │      │ CANoe   │      │
    │      │ VT Sys  │      │
    │      └─────────┘      │
    │           │           │
    │    [CAN Analysis]     │
    │    [Signal Gen]       │
    │    [Monitoring]       │
    │                       │
    │    [External ECU]     │
    │    [Simulator]        │
    │                       │
    └───────────────────────┘
    
Bus Speed: 500 kbps
Message Format: 11-bit ID (Standard)
```

### 6. POWER DISTRIBUTION

```
24V Vehicle Power
    ↓
    ├─→ [LDO Regulator 3.3V] ─→ STM32 Core Logic (50mA typical)
    │
    ├─→ [LDO Regulator 5V] ─→ ADC Sensors (30mA)
    │
    ├─→ [MOSFET Switch] ─→ Heating Element (0-1A, controlled by PWM)
    │
    ├─→ [Solenoid Driver] ─→ Pneumatic Valves (0.5A per valve)
    │
    ├─→ [LED Driver] ─→ Status LED (20mA)
    │
    └─→ [CAN Termination] ─→ 120Ω (both ends of CAN bus)

Sleep Mode:
    - Microcontroller: STOP mode (5mA typical)
    - ADC: Disabled (0mA)
    - CAN: Standby mode (1mA)
    - Heating: OFF (0mA)
    - Total Sleep: <50mA (@1V = <50mW) ✓
```

---

## Pin Assignment Table (STM32)

| Pin | Function | Type | Connected To | Signal |
|-----|----------|------|--------------|--------|
| PA0 | ADC0 | Input | Thermistor (0-5V) | Temperature |
| PA1 | ADC1 | Input | Pressure Sensor (0-5V) | Pressure |
| PA2 | ADC2 | Input | Current Sensor (0-5V) | Current |
| PA5 | GPIO_OUT | Output | Solenoid Valve #1 | Inflate |
| PA6 | GPIO_OUT | Output | Solenoid Valve #2 | Deflate |
| PA7 | PWM (TIM17) | Output | MOSFET Driver → Heating | PWM_Heating |
| PD0 | CAN_RX | Input | CAN Transceiver | CAN_In |
| PD1 | CAN_TX | Output | CAN Transceiver | CAN_Out |
| PB0 | GPIO_OUT | Output | LED Driver (Red) | Fault_LED |
| VSS | Ground | - | System Ground | 0V Ref |
| VCC | 3.3V | - | Logic Supply | +3.3V |

---

## Sensor Specifications

### Temperature Sensor (Thermistor)
- **Type:** NTC Thermistor, 10kΩ @ 25°C
- **Range:** -40°C to +125°C
- **Accuracy:** ±1°C
- **Time Constant:** <10 seconds
- **Mounting:** Embedded in seat heating element

### Pressure Sensor
- **Type:** Piezoresistive, 0-5 bar
- **Range:** 0-5 bar
- **Accuracy:** ±3%
- **Output:** 0.5-4.5V (linear)
- **Response Time:** <100ms
- **Mounting:** Pneumatic circuit main line

### Current Sensor
- **Type:** Hall Effect, 0-20A DC
- **Range:** 0-20A
- **Accuracy:** ±2%
- **Output:** 0-5V (linear, 2.5V @ 10A)
- **Response Time:** <1ms
- **Mounting:** Main power line (series)

---

## Actuator Specifications

### Heating Element
- **Type:** Resistive heating
- **Power:** 6Ω, 24V → 96W max
- **Control:** MOSFET PWM switch
- **Frequency:** 20 kHz
- **Rise Time:** ~5 minutes (0 → 30°C)

### Solenoid Valves (×2)
- **Type:** 2/2 proportional solenoid valve
- **Voltage:** 24V DC
- **Current:** 0.5A per valve
- **Response Time:** <200ms
- **Pressure Range:** 1.5-2.5 bar
- **Flow Rate:** 30 L/min max

### Status LED
- **Type:** Red indicator
- **Voltage:** 5V
- **Current:** 20mA (PWM 1Hz on fault)
- **Brightness:** 500 mcd

---

## CAN Message Format

### Message 1: Status (ID: 0x100, DLC: 8)
```
Byte 0: Heating Status (0x00=OFF, 0x01=ON)
Byte 1: Massage Status (0x00=OFF, 0x01=ON)
Byte 2: Current [0-255] → [0-20A] (Current_A = Val × 20/255)
Byte 3: Temperature [0-255] → [0-100°C] (Temp_C = Val × 100/255)
Byte 4: Pressure [0-255] → [0-5 bar] (Press_bar = Val × 5/255)
Byte 5: Error Flags (bit0=OTemp, bit1=OCurr, bit2=CAN_Fail)
Byte 6-7: Reserved
```

### Message 2: Error (ID: 0x7FF, DLC: 8, RTR)
```
Triggered on:
- Current > 10A (Error Code: 0x01)
- Temperature > 50°C (Error Code: 0x02)
- CAN Communication Failure (Error Code: 0x03)

Data: [Error_Code, Timestamp_MS, Reserved×6]
Action: Immediate system shutdown, LED fault blink
```

---

## HIL Integration Points

| Component | HIL Interface | Signal Type | Purpose |
|-----------|---------------|-------------|---------|
| Temperature | VT1004/VT Analog | 0-5V Input | Simulate thermistor |
| Pressure | VT1004/VT Analog | 0-5V Input | Simulate pressure |
| Current | VT1004/VT Analog | 0-5V Input | Simulate current |
| PWM Output | VT Oscilloscope | Digital | Verify PWM duty cycle |
| GPIO Outputs | VT GPIO Interface | Digital | Monitor valve signals |
| CAN Bus | VT1004 CAN | CAN Protocol | Bidirectional messaging |
| LED Signal | VT GPIO Interface | Digital 1Hz | Verify blink pattern |

---

## Fault Injection Scenarios

| Scenario | Injection Method | Expected Behavior | Test Case |
|----------|-----------------|-------------------|-----------|
| Overcurrent (>10A) | VT Analog increase | CAN error frame, LED fault | TC-008 |
| Over-Temperature (>50°C) | VT Analog increase | CAN error frame, heating OFF | TC-008 |
| Pressure Out of Range | VT Analog set to 1.0 or 3.0 bar | Solenoid OFF, CAN message | TC-006 |
| CAN Bus Fault | VT CAN disable/flood | Error frame, safe state | TC-008 |
| Boot Timeout | VT clock manipulation | System lockout, LED fault | TC-001 |

---

## Safety Interlocks

```
Temperature > 50°C  ─┐
                     ├─→ [OR Gate] → SHUTDOWN RELAY
Current > 10A       ─┤
                     └─→ [AND Gate] → CAN Error Frame → LED Fault
                     
Fault Duration: 100ms recovery window (manual reset required)
```

---

## Compliance Notes

✅ ISO 11898 CAN 2.0B compliant (500 kbps standard)  
✅ ISO 26262 ASIL B functional safety (basic architecture)  
✅ RoHS compliant components  
✅ Automotive temperature range (-40°C to +85°C)  
✅ Vector CANoe VT System compatible (PCAN, VT interfaces)  
✅ Standard PWM frequency (20 kHz) for automotive heating

