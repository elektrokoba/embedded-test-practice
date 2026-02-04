

# AI generated home assignment

Systems Verification Engineer Home Assignment

This take-home assignment is tailored to the Gentherm job description, testing key skills like requirements decomposition, test case design, Vector HIL wiring diagrams, automated scripting, and reporting. It's designed for 4-6 hours of work, using an automotive electromechanical system example (seat comfort module: heating + pneumatic massage, aligned with thermal/pneumatic expertise).

## Assignment Overview

**Objective:** Analyze system requirements for a seat comfort module, design test cases, create a VT System wiring diagram, draft automated test scripts, and prepare a sample report.

**Scenario:**
The seat comfort system must meet these high-level requirements:

1. Heating activation below 20°C, deactivation above 30°C (thermistors input).
2. Massage cycle: 5 min ON, 1 min OFF, max 3 cycles/hour (pressure sensor feedback).
3. CAN bus messaging to ECU: "Heating OK", "Massage Fault" states.
4. Safety shutdown: current >10A or temp >50°C.

**Detailed System Requirements (SysReq-001 to SysReq-005):**

- SysReq-001: Boot-up <2s, CAN ready message sent.
- SysReq-002: Heating PWM 0-100% (based on 0-5V input), 2°C hysteresis.
- SysReq-003: Massage valve control (2 valves: inflate/deflate), pressure 1.5-2.5 bar.
- SysReq-004: Fault: CAN error frame + 1Hz LED blink.
- SysReq-005: Sleep mode: <50mW power in inactive state.


## Tasks (Step-by-Step)

1. **Requirements Decomposition:** Break down the 5 SysReqs into logical segments (e.g., input/processing/output). Create a traceability matrix (table/Excel): Req ID | Segment | Test Type.
2. **Test Case Design (Min. 8 cases):**
    - Include manual and automated cases (Gentherm tool-style, pseudo-code sketches).
    - Example format:


| TC-ID | Description | Pre-condition | Steps | Expected Result | Priority |
| :-- | :-- | :-- | :-- | :-- | :-- |
| TC-001 | Heating activation | Temp=15°C | Apply PWM=50% | Heating ON, CAN "OK" | High |

3. **VT System Wiring Diagram:**
    - Draw a simple block diagram (Draw.io/PowerPoint): sensors (thermistors, pressure), actuators (valves, heating resistor), CAN transceiver, microcontroller. Mark HIL interfaces (Vector VT System compatible).
4. **Automated Test Script Outline:**
    - Pseudo-code in C/C++ (Vector CANoe/CAPL style):

```c  
test_heating_activation() {  
    set_temp(15.0);  // Simulate input  
    start_timer(2s);  
    check_pwm(50);   // Expected  
    if (can_msg == "Heating_OK") pass();  
    else fail();  
}  
```

    - Provide at least 2 full scripts: boot-up and fault handling.
5. **Test Report Template:**
    - Draft a report outline: Pass/Fail summary, coverage (e.g., 90% req coverage), improvement suggestions.

## Submission Guidelines

- PDF/Word document (max 10 pages): diagrams, tables, code.
- Include name, date, "Systems Verification Engineer Home Assignment".
- Optional: Python script for test case execution (bonus).


## Evaluation Criteria

- Completeness (traceability, >80% coverage).
- Accuracy (edge cases, fault handling).
- Clarity (readable tables/diagrams).
- Automotive mindset (safety, CAN, HIL realism).

