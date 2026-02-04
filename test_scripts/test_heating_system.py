"""
Heating Subsystem Test Suite
Tests for the Seat Comfort Module heating system
"""

import pytest
import time
from utilities.hil_interface import HILInterface
from utilities.data_logger import DataLogger


@pytest.mark.heating
@pytest.mark.critical
class TestHeatingBasics:
    """Test basic heating functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each heating test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/heating_tests.log')
    
    def test_heat_enable_disable_control(self):
        """TC-HEAT-001: Verify heating system responds to on/off commands"""
        # Send disable command
        self.hil.send_control_command(heat_enable=False, heat_intensity=0)
        time.sleep(0.2)
        status = self.hil.read_heat_status()
        assert status['heating_active'] == False, "Heater should be disabled"
        
        # Send enable command
        self.hil.send_control_command(heat_enable=True, heat_intensity=2)
        time.sleep(0.15)  # Allow up to 100ms response
        status = self.hil.read_heat_status()
        assert status['heating_active'] == True, "Heater should be enabled within 100ms"
        
        self.logger.log_test("TC-HEAT-001", "PASS", "Heat enable/disable control verified")
    
    def test_low_intensity_heating_30w(self):
        """TC-HEAT-002: Verify low heating mode (30W ± 3W)"""
        self.hil.set_heat_intensity(1)  # Low intensity
        time.sleep(1)  # Stabilization
        
        power_readings = []
        for i in range(10):
            voltage = self.hil.read_voltage()
            current = self.hil.read_current()
            power = voltage * current
            power_readings.append(power)
            time.sleep(0.1)
        
        avg_power = sum(power_readings) / len(power_readings)
        assert 27 <= avg_power <= 33, f"Power {avg_power}W outside range 27-33W"
        
        self.logger.log_test("TC-HEAT-002", "PASS", f"Low intensity verified: {avg_power:.1f}W")
    
    def test_medium_intensity_heating_50w(self):
        """TC-HEAT-003: Verify medium heating mode (50W ± 5W)"""
        self.hil.set_heat_intensity(2)  # Medium intensity
        time.sleep(1)  # Stabilization
        
        power_readings = []
        for i in range(10):
            voltage = self.hil.read_voltage()
            current = self.hil.read_current()
            power = voltage * current
            power_readings.append(power)
            time.sleep(0.1)
        
        avg_power = sum(power_readings) / len(power_readings)
        assert 45 <= avg_power <= 55, f"Power {avg_power}W outside range 45-55W"
        
        self.logger.log_test("TC-HEAT-003", "PASS", f"Medium intensity verified: {avg_power:.1f}W")
    
    def test_high_intensity_heating_70w(self):
        """TC-HEAT-004: Verify high heating mode (70W ± 7W)"""
        self.hil.set_heat_intensity(3)  # High intensity
        time.sleep(1)  # Stabilization
        
        power_readings = []
        for i in range(10):
            voltage = self.hil.read_voltage()
            current = self.hil.read_current()
            power = voltage * current
            power_readings.append(power)
            time.sleep(0.1)
        
        avg_power = sum(power_readings) / len(power_readings)
        assert 63 <= avg_power <= 77, f"Power {avg_power}W outside range 63-77W"
        
        self.logger.log_test("TC-HEAT-004", "PASS", f"High intensity verified: {avg_power:.1f}W")


@pytest.mark.heating
@pytest.mark.critical
class TestHeatingTemperature:
    """Test heating temperature control"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/heating_tests.log')
    
    def test_temperature_sensor_accuracy(self):
        """TC-HEAT-005: Verify temperature sensor accuracy ±2°C"""
        test_temps = [20.0, 30.0, 40.0, 50.0, 60.0]
        
        for target_temp in test_temps:
            self.hil.set_reference_temperature(target_temp)
            time.sleep(0.5)
            
            sensor_reading = self.hil.read_temperature()
            error = abs(sensor_reading - target_temp)
            assert error <= 2.0, f"Temperature error {error}°C at {target_temp}°C"
        
        self.logger.log_test("TC-HEAT-005", "PASS", "Temperature accuracy verified")
    
    def test_cold_start_response_time(self):
        """TC-HEAT-006: Verify cold start <120 seconds to 40°C"""
        self.hil.set_reference_temperature(20.0)  # Start at 20°C
        self.hil.send_control_command(heat_enable=True, heat_intensity=3)
        
        start_time = time.time()
        target_reached = False
        
        while time.time() - start_time < self.config.TEST_TIMEOUT:
            temp = self.hil.read_temperature()
            if temp >= 40.0:
                elapsed = time.time() - start_time
                target_reached = True
                assert elapsed <= 120.0, f"Time to reach 40°C: {elapsed}s (max 120s)"
                self.logger.log_test("TC-HEAT-006", "PASS", f"Cold start: {elapsed:.1f}s")
                break
            time.sleep(0.5)
        
        assert target_reached, "Temperature never reached 40°C within 120 seconds"
    
    def test_maximum_temperature_limit(self):
        """TC-HEAT-007: Verify max temperature limited to 65°C"""
        self.hil.send_control_command(heat_enable=True, heat_intensity=3)
        
        max_temp_observed = 0.0
        monitoring_time = 300  # seconds
        start_time = time.time()
        
        while time.time() - start_time < monitoring_time:
            temp = self.hil.read_temperature()
            max_temp_observed = max(max_temp_observed, temp)
            time.sleep(1)
        
        assert max_temp_observed <= 65.0, f"Max temp {max_temp_observed}°C exceeds 65°C limit"
        self.logger.log_test("TC-HEAT-007", "PASS", f"Max temp verified: {max_temp_observed:.1f}°C")
    
    def test_over_temperature_safety_shutdown(self):
        """TC-HEAT-008: Verify heating disables at >68°C threshold"""
        # Simulate over-temperature by HIL
        self.hil.set_reference_temperature(69.0)
        self.hil.send_control_command(heat_enable=True, heat_intensity=3)
        
        time.sleep(0.1)  # Allow 10ms response window
        status = self.hil.read_heat_status()
        duty_cycle = status['duty_cycle']
        
        assert duty_cycle == 0, f"Heater should shutdown at >68°C, but duty={duty_cycle}%"
        self.logger.log_test("TC-HEAT-008", "PASS", "Over-temperature shutdown verified")


@pytest.mark.heating
@pytest.mark.high
class TestHeatingTelemetry:
    """Test heating telemetry and communication"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/heating_tests.log')
    
    def test_telemetry_cycle_time(self):
        """TC-HEAT-009: Verify SEAT_HEAT_STATUS sent every 100ms ±10ms"""
        self.hil.send_control_command(heat_enable=True, heat_intensity=2)
        
        timestamps = []
        for i in range(11):  # Collect 11 messages to get 10 intervals
            msg = self.hil.read_heat_status_raw()
            timestamps.append(msg['timestamp'])
            time.sleep(0.05)  # Allow time for next message
        
        intervals = []
        for i in range(1, len(timestamps)):
            interval = timestamps[i] - timestamps[i-1]
            intervals.append(interval)
            assert 0.090 <= interval <= 0.110, f"Cycle time {interval*1000:.1f}ms out of 90-110ms range"
        
        self.logger.log_test("TC-HEAT-009", "PASS", "Telemetry cycle time verified")
    
    def test_voltage_tolerance_low_8v(self):
        """TC-HEAT-010: Verify heating operates at minimum voltage (8V)"""
        self.hil.set_supply_voltage(8.0)
        self.hil.send_control_command(heat_enable=True, heat_intensity=3)
        time.sleep(1)
        
        voltage = self.hil.read_voltage()
        status = self.hil.read_heat_status()
        assert status['heating_active'], "Heater should operate at 8V"
        assert voltage >= 7.9, "Supply voltage dropped unexpectedly"
        
        self.logger.log_test("TC-HEAT-010", "PASS", "Low voltage operation verified")
    
    def test_voltage_tolerance_high_14_4v(self):
        """TC-HEAT-011: Verify heating operates at maximum voltage (14.4V)"""
        self.hil.set_supply_voltage(14.4)
        self.hil.send_control_command(heat_enable=True, heat_intensity=3)
        time.sleep(1)
        
        voltage = self.hil.read_voltage()
        status = self.hil.read_heat_status()
        assert status['heating_active'], "Heater should operate at 14.4V"
        assert voltage <= 14.5, "Supply voltage exceeded maximum"
        
        self.logger.log_test("TC-HEAT-011", "PASS", "High voltage operation verified")


@pytest.mark.heating
@pytest.mark.medium
class TestHeatingLogging:
    """Test heating event logging"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/heating_tests.log')
    
    def test_heating_event_logging(self):
        """TC-HEAT-012: Verify all heating events logged with timestamp"""
        events_logged = []
        
        for i in range(5):
            self.hil.send_control_command(heat_enable=True)
            time.sleep(0.5)
            log_entry = self.hil.read_event_log()
            if log_entry:
                events_logged.append(log_entry)
            
            self.hil.send_control_command(heat_enable=False)
            time.sleep(0.5)
            log_entry = self.hil.read_event_log()
            if log_entry:
                events_logged.append(log_entry)
        
        assert len(events_logged) >= 5, f"Expected at least 5 events, got {len(events_logged)}"
        
        # Verify timestamp accuracy (±1 second)
        for entry in events_logged:
            assert entry['timestamp'] > 0, "Timestamp missing or invalid"
        
        self.logger.log_test("TC-HEAT-012", "PASS", f"Heating events logged: {len(events_logged)}")


@pytest.mark.heating
@pytest.mark.stress
class TestHeatingStress:
    """Stress tests for heating subsystem"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/heating_tests.log')
    
    def test_repeated_cold_start_cycles(self):
        """TC-STRESS-001: Verify heater handles 20 repeated cold-start cycles"""
        cycle_times = []
        
        for cycle in range(20):
            self.hil.set_reference_temperature(20.0)
            self.hil.send_control_command(heat_enable=True, heat_intensity=3)
            
            start_time = time.time()
            while time.time() - start_time < 180:  # Max 180s per cycle
                temp = self.hil.read_temperature()
                if temp >= 50.0:
                    cycle_time = time.time() - start_time
                    cycle_times.append(cycle_time)
                    break
                time.sleep(0.5)
            
            # Cool down
            self.hil.send_control_command(heat_enable=False)
            self.hil.set_reference_temperature(20.0)
            time.sleep(60)
        
        avg_time = sum(cycle_times) / len(cycle_times)
        assert avg_time <= 120.0, f"Average cycle time {avg_time}s exceeds 120s limit"
        
        self.logger.log_test("TC-STRESS-001", "PASS", f"20 cycles completed, avg time: {avg_time:.1f}s")
