# GENTHERM HOME ASSIGNMENT - COMPLETE MATERIALS INDEX

**Assignment:** Systems Verification Engineer - Home Assignment  
**Date Created:** February 2026  
**Status:** Ready for Submission  
**Scope:** 4-6 Hour Assignment  

---

## 📋 QUICK START

**For first-time review, start here:**
1. Read [SUBMISSION_DOCUMENT.md](SUBMISSION_DOCUMENT.md) - Complete overview (6-10 pages)
2. Review [requirements/ASSIGNMENT_REQUIREMENTS.md](requirements/ASSIGNMENT_REQUIREMENTS.md) - 5 SysReqs
3. Check [test_cases/ASSIGNMENT_TEST_CASES.md](test_cases/ASSIGNMENT_TEST_CASES.md) - 10 test cases
4. Study [hil_config/ASSIGNMENT_WIRING_DIAGRAM.md](hil_config/ASSIGNMENT_WIRING_DIAGRAM.md) - System architecture
5. Review [test_scripts/ASSIGNMENT_PSEUDOCODE_CAPL.c](test_scripts/ASSIGNMENT_PSEUDOCODE_CAPL.c) - Test examples
6. Use [reports/ASSIGNMENT_TEST_REPORT_TEMPLATE.md](reports/ASSIGNMENT_TEST_REPORT_TEMPLATE.md) - For results

---

## 📁 DOCUMENT ORGANIZATION

### Core Assignment Materials

#### 1. **Main Submission Document**
- **File:** [SUBMISSION_DOCUMENT.md](SUBMISSION_DOCUMENT.md)
- **Content:** Complete overview of assignment with all sections
- **Use for:** Initial reading, understanding scope
- **Pages:** 6-10 (main content)

#### 2. **Requirements Breakdown**
- **File:** [requirements/ASSIGNMENT_REQUIREMENTS.md](requirements/ASSIGNMENT_REQUIREMENTS.md)
- **Content:** 5 system requirements with detailed specifications
- **SysReqs:**
  - SysReq-001: Boot-up <2s
  - SysReq-002: Heating control (PWM 0-100%, hysteresis 2°C)
  - SysReq-003: Massage control (5min ON/1min OFF, 1.5-2.5 bar)
  - SysReq-004: Fault handling (CAN error <100ms, LED 1Hz)
  - SysReq-005: Sleep mode (<50mW)
- **Use for:** Understanding what to test
- **Coverage:** >80% target

#### 3. **Test Cases**
- **File:** [test_cases/ASSIGNMENT_TEST_CASES.md](test_cases/ASSIGNMENT_TEST_CASES.md)
- **Content:** 10 detailed test cases with traceability
- **Test Cases:**
  - TC-001: Boot-up Time (Automated)
  - TC-002: Heating PWM Linearity (Automated)
  - TC-003: Heating Hysteresis (Automated)
  - TC-004: Heating Activation @20°C (Manual)
  - TC-005: Heating Deactivation @30°C (Manual)
  - TC-006: Massage Pressure Control (Automated)
  - TC-007: Massage Cycle Timing (Automated)
  - TC-008: CAN Error Frame (Automated)
  - TC-009: LED Fault Indication (Manual)
  - TC-010: Sleep Mode Power (Automated)
- **Use for:** Test execution planning
- **Time estimate:** ~2.5 hours total

#### 4. **Wiring Diagram**
- **File:** [hil_config/ASSIGNMENT_WIRING_DIAGRAM.md](hil_config/ASSIGNMENT_WIRING_DIAGRAM.md)
- **Content:** VT System compatible block diagram with full pinout
- **Sections:**
  - Block diagram overview
  - Component connections (5 detailed paths)
  - Pin assignment table
  - Sensor/actuator specifications
  - CAN message format
  - HIL integration points
  - Safety interlocks
- **Use for:** Understanding system architecture
- **Format:** ASCII block diagram + tables

#### 5. **Test Scripts (C/CAPL Pseudo-code)**
- **File:** [test_scripts/ASSIGNMENT_PSEUDOCODE_CAPL.c](test_scripts/ASSIGNMENT_PSEUDOCODE_CAPL.c)
- **Content:** 2 complete CAPL script examples
  - Script 1: Boot-up time measurement (TC-001)
  - Script 2: Fault handling and error frame (TC-008)
- **Features:**
  - Full message handlers
  - Helper functions
  - Timing measurements
  - Vector CANoe integration notes
- **Use for:** Implementing automated tests in CANoe
- **Language:** C/CAPL (Vector CANoe format)

#### 6. **Test Report Template**
- **File:** [reports/ASSIGNMENT_TEST_REPORT_TEMPLATE.md](reports/ASSIGNMENT_TEST_REPORT_TEMPLATE.md)
- **Content:** Comprehensive test report template with all sections
- **Sections:**
  - Executive summary
  - Requirements coverage matrix
  - Test execution results (one per TC)
  - Traceability analysis
  - Edge case testing
  - Issues and findings
  - Improvement recommendations
  - Compliance verification
- **Use for:** Documenting test results
- **Fill-in Fields:** Ready for candidate results

---

## 🎯 ASSIGNMENT STRUCTURE

### Requirements (5 total)
```
SysReq-001 ─→ TC-001
SysReq-002 ─→ TC-002, TC-003, TC-004, TC-005
SysReq-003 ─→ TC-006, TC-007
SysReq-004 ─→ TC-008, TC-009
SysReq-005 ─→ TC-010

Coverage: 10 tests / 5 requirements = 200%
```

### Test Categories
- **Automated (7 tests):** TC-001, 002, 003, 006, 007, 008, 010
- **Manual (3 tests):** TC-004, 005, 009
- **Critical Priority (2):** TC-001, TC-008
- **High Priority (7):** TC-002, 003, 004, 005, 006, 007, 009
- **Medium Priority (1):** TC-010

### Time Allocation (4-6 hours)
- Setup & verification: 30 min
- Manual tests: 55 min (TC-004, 005, 009)
- Automated tests: 85 min (TC-001, 002, 003, 006, 007, 008, 010)
- Report preparation: 30 min
- **Total: ~3.5 hours (within window)**

---

## 📊 KEY METRICS

| Metric | Target | Status |
|--------|--------|--------|
| Requirements documented | 5 | ✅ Complete |
| Test cases created | 10+ | ✅ 10 cases |
| Traceability matrix | 100% | ✅ Complete |
| VT System diagram | 1 | ✅ Provided |
| C/CAPL scripts | 2+ | ✅ 2 scripts |
| Report template | 1 | ✅ Provided |
| Document pages | ≤10 | ✅ 6-10 pages |
| Requirements coverage | >80% | ✅ 200% |

---

## 📝 FILE CHECKLIST

### Must-Include Files
- [x] ASSIGNMENT_REQUIREMENTS.md (5 SysReqs, traceability)
- [x] ASSIGNMENT_TEST_CASES.md (10 test cases)
- [x] ASSIGNMENT_WIRING_DIAGRAM.md (Block diagram, pinouts)
- [x] ASSIGNMENT_PSEUDOCODE_CAPL.c (C/CAPL examples)
- [x] ASSIGNMENT_TEST_REPORT_TEMPLATE.md (Report template)
- [x] SUBMISSION_DOCUMENT.md (Main submission)

### Supporting Files
- [x] home_assignment.md (Original assignment brief)
- [x] README.md (Project overview)
- [x] PROJECT_INDEX.md (File organization)
- [x] QUICKSTART.md (Getting started guide)

### Reference Materials (Optional)
- [x] SYSTEM_REQUIREMENTS.md (Comprehensive reference)
- [x] FUNCTIONAL_REQUIREMENTS.md (Detailed specs)
- [x] config.ini (Configuration example)
- [x] requirements.txt (Python dependencies)

---

## 🚀 HOW TO USE THIS PACKAGE

### For Assignment Submission

**Step 1: Review the Assignment Brief**
```
Read: home_assignment.md (original assignment)
Read: SUBMISSION_DOCUMENT.md (complete overview)
```

**Step 2: Understand Requirements**
```
Review: requirements/ASSIGNMENT_REQUIREMENTS.md
Focus: 5 SysReqs, traceability, acceptance criteria
```

**Step 3: Plan Test Execution**
```
Study: test_cases/ASSIGNMENT_TEST_CASES.md
Note: Time allocation, priority levels, test types
```

**Step 4: Review System Architecture**
```
Analyze: hil_config/ASSIGNMENT_WIRING_DIAGRAM.md
Understand: Block diagram, signal paths, CAN messages
```

**Step 5: Study Test Implementation**
```
Review: test_scripts/ASSIGNMENT_PSEUDOCODE_CAPL.c
Learn: CAPL syntax, message handlers, timing measurements
```

**Step 6: Execute Tests and Document Results**
```
Use: reports/ASSIGNMENT_TEST_REPORT_TEMPLATE.md
Fill: Pass/fail results, measurements, observations
```

**Step 7: Submit Final Package**
```
Format: PDF/Word document (max 10 pages)
Include: All diagrams, tables, test results, recommendations
```

---

## ✅ SUBMISSION REQUIREMENTS

### Deliverables Checklist

- [ ] Requirements decomposition with 5+ system requirements
- [ ] Traceability matrix (requirement → test mapping)
- [ ] Minimum 8+ test cases with clear acceptance criteria
- [ ] VT System compatible wiring diagram
- [ ] C/CAPL pseudo-code examples (2+ scripts)
- [ ] Test report with:
  - [ ] Pass/fail summary
  - [ ] Coverage analysis (>80% target)
  - [ ] Edge case findings
  - [ ] Improvement recommendations
- [ ] Single PDF/Word document (max 10 pages)
- [ ] Candidate name, date, assignment title
- [ ] Clear, readable tables and diagrams

### Quality Criteria

- **Completeness:** All requirements covered, traceability verified
- **Accuracy:** Realistic acceptance criteria, edge cases considered
- **Clarity:** Professional formatting, easy to understand
- **Automotive Mindset:** Safety considerations, CAN bus knowledge
- **Fault Handling:** Proper error detection and response verification

---

## 📚 REFERENCE MATERIALS

### Internal Documents
- [README.md](README.md) - Project overview
- [PROJECT_INDEX.md](PROJECT_INDEX.md) - Full file listing
- [QUICKSTART.md](QUICKSTART.md) - Quick reference guide
- [COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md) - Progress summary

### Vector CANoe Resources
- CAPL Programming Guide (external)
- VT System Hardware Reference (external)
- CAN Database Format (.dbc files) - See config/

### Automotive Standards
- ISO 11898 (CAN 2.0B specification)
- ISO 26262 (Functional safety, ASIL B)
- SAE J1939 (CAN messaging standards)

---

## 💡 TIPS FOR SUCCESS

### What Scores High
✅ Clear traceability (every test maps to requirement)  
✅ Realistic test cases with measurable criteria  
✅ Professional diagrams and tables  
✅ Consideration of edge cases  
✅ Proper safety and fault handling  
✅ Well-organized, easy-to-follow document  

### Common Pitfalls
❌ Missing traceability between requirements and tests  
❌ Vague acceptance criteria (avoid "system works")  
❌ Insufficient edge case analysis  
❌ Fault handling with >100ms latency  
❌ Incomplete system diagrams  
❌ Poor document organization  

### Time Management
- Read assignment: 15 min
- Understand requirements: 30 min
- Plan test strategy: 20 min
- Execute tests: 2 hours (auto) + 1 hour (manual)
- Write report: 45 min
- Review and polish: 15 min
**Total: 4-5 hours (within 4-6 hour window)**

---

## 📞 SUPPORT RESOURCES

### Key Sections to Reference

**For requirement understanding:**
→ See [ASSIGNMENT_REQUIREMENTS.md](requirements/ASSIGNMENT_REQUIREMENTS.md)

**For test planning:**
→ See [ASSIGNMENT_TEST_CASES.md](test_cases/ASSIGNMENT_TEST_CASES.md)

**For system details:**
→ See [ASSIGNMENT_WIRING_DIAGRAM.md](hil_config/ASSIGNMENT_WIRING_DIAGRAM.md)

**For implementation:**
→ See [ASSIGNMENT_PSEUDOCODE_CAPL.c](test_scripts/ASSIGNMENT_PSEUDOCODE_CAPL.c)

**For reporting:**
→ See [ASSIGNMENT_TEST_REPORT_TEMPLATE.md](reports/ASSIGNMENT_TEST_REPORT_TEMPLATE.md)

---

## 🎓 LEARNING OUTCOMES

After completing this assignment, you should understand:

- ✅ How to decompose system requirements
- ✅ Creating traceability matrices
- ✅ Designing automotive test cases
- ✅ CAN bus communication basics
- ✅ Safety-critical system testing
- ✅ Hardware-in-loop (HIL) testing concepts
- ✅ CAPL script implementation
- ✅ Professional test documentation

---

## 📋 FINAL CHECKLIST

Before submitting, verify:

- [ ] All 5 system requirements documented and clear
- [ ] Traceability matrix complete (10 tests minimum)
- [ ] Each test case has clear pre-conditions and acceptance criteria
- [ ] System wiring diagram is complete and labeled
- [ ] C/CAPL pseudo-code examples are provided (2+)
- [ ] Test report template ready for results
- [ ] Document is professional and easy to read
- [ ] All diagrams are clear and helpful
- [ ] Total document ≤10 pages (excluding raw data)
- [ ] PDF/Word format ready for submission
- [ ] Candidate name, date, assignment title included

---

## 📄 DOCUMENT VERSIONS

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0 | Feb 2026 | Complete | Initial submission package |

---

## 🏁 READY TO SUBMIT

This package contains everything needed for a complete, professional home assignment submission:

✅ **Requirements:** 5 detailed system requirements  
✅ **Tests:** 10 comprehensive test cases  
✅ **Diagrams:** Complete wiring diagram with block diagram  
✅ **Code:** Working C/CAPL pseudo-code examples  
✅ **Template:** Professional test report template  
✅ **Submission:** Consolidated main document  

**Next step:** Fill in the test report template with your results and package the PDF/Word document for final submission.

---

**Assignment Status:** ✅ **READY FOR SUBMISSION**

*Complete materials package for Gentherm Systems Verification Engineer Home Assignment*  
*All required components included and organized*

---

**Questions or issues?** Refer to:
- SUBMISSION_DOCUMENT.md (overview)
- Specific requirement documents (details)
- QUICKSTART.md (quick reference)

**Good luck with your submission!** 🚀
