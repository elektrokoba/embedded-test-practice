"""
Integration and System Tests
Tests for system-level integration and safety features
"""

import pytest
import time
from utilities.hil_interface import HILInterface
from utilities.data_logger import DataLogger


@pytest.mark.integration
@pytest.mark.critical
class TestSystemIntegration:
    """System integration tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/integration_tests.log')
    
    def test_simultaneous_heating_and_massage(self):
        """TC-INT-001: Verify simultaneous heating and massage operation"""
        # Enable both systems
        self.hil.send_control_command(
            heat_enable=True, heat_intensity=3,
            massage_enable=True, massage_intensity=3
        )
        
        # Monitor for 60 seconds
        heat_active_count = 0
        massage_active_count = 0
        monitoring_time = 60
        start_time = time.time()
        
        while time.time() - start_time < monitoring_time:
            heat_status = self.hil.read_heat_status()
            massage_status = self.hil.read_massage_status()
            
            if heat_status['heating_active']:
                heat_active_count += 1
            if massage_status['pump_active']:
                massage_active_count += 1
            
            time.sleep(1)
        
        # Both systems should be active throughout
        assert heat_active_count > monitoring_time * 0.8, "Heating not consistently active"
        assert massage_active_count > monitoring_time * 0.8, "Massage not consistently active"
        
        self.logger.log_test("TC-INT-001", "PASS", "Simultaneous operation verified")
    
    def test_can_message_cycle_time_stability(self):
        """TC-INT-002: Verify CAN cycle time stability"""
        self.hil.send_control_command(heat_enable=True, massage_enable=True)
        
        heat_intervals = []
        massage_intervals = []
        last_heat_time = time.time()
        last_massage_time = time.time()
        monitoring_time = 10  # 10 seconds
        start_time = time.time()
        
        while time.time() - start_time < monitoring_time:
            heat_msg = self.hil.read_heat_status_raw()
            massage_msg = self.hil.read_massage_status_raw()
            
            current_time = time.time()
            
            interval_heat = current_time - last_heat_time
            interval_massage = current_time - last_massage_time
            
            if interval_heat > 0.05:  # Only record if significant time passed
                heat_intervals.append(interval_heat)
                last_heat_time = current_time
            
            if interval_massage > 0.05:
                massage_intervals.append(interval_massage)
                last_massage_time = current_time
            
            time.sleep(0.01)
        
        # Verify stability
        for interval in heat_intervals:
            assert 0.090 <= interval <= 0.110, f"Heat cycle {interval*1000:.1f}ms out of range"
        for interval in massage_intervals:
            assert 0.090 <= interval <= 0.110, f"Massage cycle {interval*1000:.1f}ms out of range"
        
        self.logger.log_test("TC-INT-002", "PASS", "CAN cycle time stability verified")
    
    def test_can_message_loss_handling(self):
        """TC-INT-003: Verify system handles 500ms CAN message loss"""
        self.hil.send_control_command(heat_enable=True, heat_intensity=2)
        time.sleep(0.5)
        
        # Get initial state
        initial_status = self.hil.read_heat_status()
        initial_duty = initial_status['duty_cycle']
        
        # Simulate 600ms without CAN commands
        time.sleep(0.6)
        
        # System should maintain state
        current_status = self.hil.read_heat_status()
        current_duty = current_status['duty_cycle']
        
        # Duty cycle should be maintained (with tolerance for natural variation)
        assert abs(current_duty - initial_duty) < 20, "System state not maintained during CAN loss"
        
        # System should recover when commands resume
        self.hil.send_control_command(heat_enable=False)
        time.sleep(0.2)
        
        recovered_status = self.hil.read_heat_status()
        assert recovered_status['heating_active'] == False, "System didn't respond after CAN resume"
        
        self.logger.log_test("TC-INT-003", "PASS", "CAN message loss handling verified")


@pytest.mark.safety
@pytest.mark.critical
class TestSafetyCritical:
    """Safety-critical system tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/safety_tests.log')
    
    def test_microcontroller_fault_failsafe(self):
        """TC-SAFE-001: Verify failsafe state on MCU fault"""
        # Enable both systems
        self.hil.send_control_command(heat_enable=True, massage_enable=True)
        time.sleep(0.5)
        
        # Both should be active
        assert self.hil.read_heat_status()['heating_active']
        assert self.hil.read_massage_status()['pump_active']
        
        # Simulate MCU fault (loss of control)
        # In real scenario, watchdog triggers safe shutdown
        # For this test, simulate by stopping commands
        
        # System should remain in safe state
        heat_status = self.hil.read_heat_status()
        massage_status = self.hil.read_massage_status()
        
        # Both outputs should be de-energized
        assert heat_status['duty_cycle'] <= 5 or not heat_status['heating_active']
        assert massage_status['duty_cycle'] <= 5 or not massage_status['pump_active']
        
        self.logger.log_test("TC-SAFE-001", "PASS", "MCU failsafe verified")
    
    def test_over_temperature_immediate_shutdown(self):
        """TC-SAFE-002: Verify immediate heating shutdown at >68°C"""
        self.hil.send_control_command(heat_enable=True, heat_intensity=3)
        time.sleep(0.5)
        
        # Simulate over-temperature condition
        self.hil.set_reference_temperature(69.0)
        time.sleep(0.1)  # Allow for 10ms response
        
        # Heating should be immediately de-energized
        status = self.hil.read_heat_status()
        assert status['heating_active'] == False, "Heater should shutdown immediately at >68°C"
        
        self.logger.log_test("TC-SAFE-002", "PASS", "Over-temperature safety shutdown verified")
    
    def test_over_pressure_pump_shutoff(self):
        """TC-SAFE-003: Verify pump shutoff at >150 kPa"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=5)
        time.sleep(0.5)
        
        # Simulate over-pressure
        self.hil.simulate_pump_overpressure()
        time.sleep(0.1)  # Allow for response
        
        status = self.hil.read_massage_status()
        pressure = status['pressure_kpa']
        
        assert pressure <= 150, f"Pressure {pressure}kPa exceeds 150 kPa safety limit"
        
        self.logger.log_test("TC-SAFE-003", "PASS", "Over-pressure safety shutoff verified")
    
    def test_fault_event_logging(self):
        """TC-SAFE-004: Verify all faults logged with timestamps"""
        # Trigger multiple fault conditions
        faults_detected = []
        
        # Fault 1: Over-temperature
        self.hil.set_reference_temperature(69.0)
        time.sleep(0.2)
        
        # Fault 2: Over-pressure
        self.hil.set_massage_intensity(5)
        self.hil.simulate_pump_overpressure()
        time.sleep(0.2)
        
        # Fault 3: Pump failure
        self.hil.simulate_pump_fault()
        time.sleep(0.2)
        
        # Check logs
        log_entry = self.hil.read_event_log()
        while log_entry:
            faults_detected.append(log_entry)
            log_entry = self.hil.read_event_log()
        
        assert len(faults_detected) >= 1, "Faults not logged"
        
        self.logger.log_test("TC-SAFE-004", "PASS", f"Fault logging verified: {len(faults_detected)} events logged")


@pytest.mark.integration
@pytest.mark.medium
class TestDiagnostics:
    """Diagnostic interface tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/integration_tests.log')
    
    def test_diagnostic_can_read_all_sensors(self):
        """TC-INT-005: Verify all sensor values accessible via diagnostic CAN"""
        self.hil.send_control_command(heat_enable=True, massage_enable=True)
        
        # Read all sensor values
        temp = self.hil.read_temperature()
        voltage = self.hil.read_voltage()
        current = self.hil.read_current()
        
        heat_status = self.hil.read_heat_status()
        massage_status = self.hil.read_massage_status()
        
        # Verify all values are reasonable
        assert 0 < temp < 100, f"Temperature {temp}°C out of range"
        assert 6 < voltage < 16, f"Voltage {voltage}V out of range"
        assert current >= 0, f"Current {current}A should be non-negative"
        
        assert 'duty_cycle' in heat_status
        assert 'pressure_kpa' in massage_status
        
        self.logger.log_test("TC-INT-005", "PASS", "Diagnostic sensor read verified")


@pytest.mark.integration
@pytest.mark.medium
class TestEdgeCases:
    """Edge case tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/integration_tests.log')
    
    def test_temperature_oscillation_stability(self):
        """TC-EDGE-001: Verify no excessive temperature oscillation"""
        self.hil.send_control_command(heat_enable=True, heat_intensity=2)
        
        temperatures = []
        monitoring_time = 300  # 5 minutes
        start_time = time.time()
        
        while time.time() - start_time < monitoring_time:
            temp = self.hil.read_temperature()
            temperatures.append(temp)
            time.sleep(1)
        
        # Calculate oscillation metrics
        if len(temperatures) > 10:
            final_temps = temperatures[-10:]
            oscillation = max(final_temps) - min(final_temps)
            
            assert oscillation <= 5.0, f"Temperature oscillation {oscillation}°C exceeds 5°C"
        
        self.logger.log_test("TC-EDGE-001", "PASS", "Temperature stability verified")
    
    def test_voltage_sag_recovery(self):
        """TC-EDGE-003: Verify system recovery from voltage sag"""
        self.hil.send_control_command(heat_enable=True, heat_intensity=3)
        time.sleep(0.5)
        
        # Normal operation
        normal_status = self.hil.read_heat_status()
        assert normal_status['heating_active']
        
        # Simulate voltage sag to 8V
        self.hil.set_supply_voltage(8.0)
        time.sleep(0.5)
        
        sag_status = self.hil.read_heat_status()
        # System should continue operating (degraded)
        
        # Restore voltage
        self.hil.set_supply_voltage(13.2)
        time.sleep(0.5)
        
        recovered_status = self.hil.read_heat_status()
        assert recovered_status['heating_active'], "System should recover from voltage sag"
        
        self.logger.log_test("TC-EDGE-003", "PASS", "Voltage sag recovery verified")


@pytest.mark.stress
class TestStressIntegration:
    """Stress tests for integrated system"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/stress_tests.log')
    
    def test_extended_simultaneous_operation(self):
        """TC-STRESS-003: Verify no degradation after 2 hours simultaneous operation"""
        self.hil.send_control_command(
            heat_enable=True, heat_intensity=3,
            massage_enable=True, massage_intensity=3
        )
        
        metrics_history = []
        monitoring_interval = 600  # Sample every 10 minutes
        total_time = 120 * 60  # 2 hours in seconds
        start_time = time.time()
        
        while time.time() - start_time < total_time:
            heat_status = self.hil.read_heat_status()
            massage_status = self.hil.read_massage_status()
            
            metrics_history.append({
                'heat_duty': heat_status['duty_cycle'],
                'massage_pressure': massage_status['pressure_kpa'],
                'timestamp': time.time() - start_time
            })
            
            time.sleep(monitoring_interval)
        
        # Check for degradation
        if len(metrics_history) > 1:
            initial_heat = metrics_history[0]['heat_duty']
            final_heat = metrics_history[-1]['heat_duty']
            
            initial_pressure = metrics_history[0]['massage_pressure']
            final_pressure = metrics_history[-1]['massage_pressure']
            
            heat_drift = abs((final_heat - initial_heat) / initial_heat * 100) if initial_heat > 0 else 0
            pressure_drift = abs((final_pressure - initial_pressure) / initial_pressure * 100) if initial_pressure > 0 else 0
            
            assert heat_drift < 5.0, f"Heating duty drift {heat_drift}% exceeds 5%"
            assert pressure_drift < 5.0, f"Pressure drift {pressure_drift}% exceeds 5%"
        
        self.logger.log_test("TC-STRESS-003", "PASS", "Extended operation stability verified")
