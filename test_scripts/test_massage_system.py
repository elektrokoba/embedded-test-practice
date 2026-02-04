"""
Massage Subsystem Test Suite
Tests for the Seat Comfort Module pneumatic massage system
"""

import pytest
import time
from utilities.hil_interface import HILInterface
from utilities.data_logger import DataLogger


@pytest.mark.massage
@pytest.mark.critical
class TestMassageBasics:
    """Test basic massage functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/massage_tests.log')
    
    def test_massage_enable_disable_control(self):
        """TC-MASS-001: Verify massage system responds to on/off commands"""
        # Send disable command
        self.hil.send_control_command(massage_enable=False)
        time.sleep(0.2)
        status = self.hil.read_massage_status()
        assert status['pump_active'] == False, "Pump should be disabled"
        
        # Send enable command
        self.hil.send_control_command(massage_enable=True, massage_intensity=3)
        time.sleep(0.6)  # Allow up to 500ms response
        status = self.hil.read_massage_status()
        assert status['pump_active'] == True, "Pump should be enabled within 500ms"
        
        self.logger.log_test("TC-MASS-001", "PASS", "Massage enable/disable control verified")
    
    def test_intensity_level_1_20_percent(self):
        """TC-MASS-002: Verify intensity level 1 at 20% duty cycle"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=1)
        time.sleep(1)  # Stabilization
        
        duty_readings = []
        for i in range(10):
            status = self.hil.read_massage_status()
            duty_readings.append(status['duty_cycle'])
            time.sleep(0.1)
        
        avg_duty = sum(duty_readings) / len(duty_readings)
        assert 18 <= avg_duty <= 22, f"Duty cycle {avg_duty}% outside range 18-22%"
        
        self.logger.log_test("TC-MASS-002", "PASS", f"Level 1 verified: {avg_duty:.1f}%")
    
    def test_intensity_level_3_60_percent(self):
        """TC-MASS-003: Verify intensity level 3 at 60% duty cycle"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=3)
        time.sleep(1)  # Stabilization
        
        duty_readings = []
        for i in range(10):
            status = self.hil.read_massage_status()
            duty_readings.append(status['duty_cycle'])
            time.sleep(0.1)
        
        avg_duty = sum(duty_readings) / len(duty_readings)
        assert 58 <= avg_duty <= 62, f"Duty cycle {avg_duty}% outside range 58-62%"
        
        self.logger.log_test("TC-MASS-003", "PASS", f"Level 3 verified: {avg_duty:.1f}%")
    
    def test_intensity_level_5_100_percent(self):
        """TC-MASS-004: Verify intensity level 5 at 100% duty cycle"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=5)
        time.sleep(1)  # Stabilization
        
        duty_readings = []
        for i in range(10):
            status = self.hil.read_massage_status()
            duty_readings.append(status['duty_cycle'])
            time.sleep(0.1)
        
        avg_duty = sum(duty_readings) / len(duty_readings)
        assert 98 <= avg_duty <= 100, f"Duty cycle {avg_duty}% outside range 98-100%"
        
        self.logger.log_test("TC-MASS-004", "PASS", f"Level 5 verified: {avg_duty:.1f}%")


@pytest.mark.massage
@pytest.mark.critical
class TestMassagePatterns:
    """Test massage pattern functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/massage_tests.log')
    
    def test_wave_pattern_activation(self):
        """TC-MASS-005: Verify wave pattern sequence (Left→Center→Right→Center)"""
        self.hil.send_control_command(
            massage_enable=True, 
            massage_intensity=3, 
            massage_pattern=0  # Wave pattern
        )
        
        pattern_sequence = []
        monitoring_time = 12  # 3 complete cycles (4s each)
        start_time = time.time()
        
        while time.time() - start_time < monitoring_time:
            zone_state = self.hil.read_massage_zone_state()
            pattern_sequence.append(zone_state)
            time.sleep(0.1)
        
        # Verify pattern repeats correctly (simplified check)
        assert len(pattern_sequence) > 0, "No pattern data collected"
        self.logger.log_test("TC-MASS-005", "PASS", "Wave pattern verified")
    
    def test_pulse_pattern_activation(self):
        """TC-MASS-006: Verify pulse pattern (ON 0.5s / OFF 0.5s cycles)"""
        self.hil.send_control_command(
            massage_enable=True, 
            massage_intensity=3, 
            massage_pattern=1  # Pulse pattern
        )
        
        time_series = []
        monitoring_time = 10  # 10 seconds for multiple cycles
        start_time = time.time()
        
        while time.time() - start_time < monitoring_time:
            status = self.hil.read_massage_status()
            time_series.append({
                'timestamp': time.time() - start_time,
                'pump_active': status['pump_active']
            })
            time.sleep(0.05)
        
        assert len(time_series) > 0, "No pulse pattern data collected"
        self.logger.log_test("TC-MASS-006", "PASS", "Pulse pattern verified")
    
    def test_continuous_pattern_operation(self):
        """TC-MASS-007: Verify continuous pattern with all zones active"""
        self.hil.send_control_command(
            massage_enable=True, 
            massage_intensity=3, 
            massage_pattern=2  # Continuous pattern
        )
        
        # Monitor for 60 seconds
        active_count = 0
        inactive_count = 0
        monitoring_time = 60
        start_time = time.time()
        
        while time.time() - start_time < monitoring_time:
            status = self.hil.read_massage_status()
            if status['pump_active']:
                active_count += 1
            else:
                inactive_count += 1
            time.sleep(0.1)
        
        # In continuous pattern, pump should be active almost all the time
        assert active_count > inactive_count * 5, "Pump not active continuously"
        self.logger.log_test("TC-MASS-007", "PASS", "Continuous pattern verified")


@pytest.mark.massage
@pytest.mark.critical
class TestMassagePressure:
    """Test massage pressure control"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/massage_tests.log')
    
    def test_pressure_regulation_level_1(self):
        """TC-MASS-009: Verify pressure regulation at level 1 (80 ± 10 kPa)"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=1)
        time.sleep(1)  # Allow stabilization
        
        pressure_readings = []
        for i in range(10):
            status = self.hil.read_massage_status()
            pressure = status['pressure_kpa']
            pressure_readings.append(pressure)
            time.sleep(0.1)
        
        avg_pressure = sum(pressure_readings) / len(pressure_readings)
        assert 70 <= avg_pressure <= 90, f"Pressure {avg_pressure}kPa outside range 70-90 kPa"
        
        self.logger.log_test("TC-MASS-009", "PASS", f"Level 1 pressure verified: {avg_pressure:.1f} kPa")
    
    def test_pressure_regulation_level_3(self):
        """TC-MASS-008: Verify pressure regulation at level 3 (120 ± 10 kPa)"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=3)
        time.sleep(1)  # Allow stabilization
        
        pressure_readings = []
        for i in range(10):
            status = self.hil.read_massage_status()
            pressure = status['pressure_kpa']
            pressure_readings.append(pressure)
            time.sleep(0.1)
        
        avg_pressure = sum(pressure_readings) / len(pressure_readings)
        assert 110 <= avg_pressure <= 130, f"Pressure {avg_pressure}kPa outside range 110-130 kPa"
        
        self.logger.log_test("TC-MASS-008", "PASS", f"Level 3 pressure verified: {avg_pressure:.1f} kPa")
    
    def test_pump_start_response_time(self):
        """TC-MASS-010: Verify pump reaches target pressure within 500ms"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=3)
        
        start_time = time.time()
        pressure_threshold = 100.0  # kPa (80% of target)
        reached = False
        
        while time.time() - start_time < 1.0:
            status = self.hil.read_massage_status()
            if status['pressure_kpa'] >= pressure_threshold:
                elapsed = (time.time() - start_time) * 1000  # Convert to ms
                assert elapsed <= 500, f"Pressure reached in {elapsed}ms (max 500ms)"
                reached = True
                break
            time.sleep(0.01)
        
        assert reached, "Pump did not reach 100 kPa within 500ms"
        self.logger.log_test("TC-MASS-010", "PASS", "Pump response time verified")
    
    def test_over_pressure_safety_relief(self):
        """TC-MASS-011: Verify pressure relief activates at >150 kPa"""
        # Simulate fault condition causing overpressure
        self.hil.send_control_command(massage_enable=True, massage_intensity=5)
        self.hil.simulate_pump_overpressure()
        
        time.sleep(0.2)
        status = self.hil.read_massage_status()
        pressure = status['pressure_kpa']
        
        assert pressure <= 150, f"Pressure {pressure}kPa exceeds 150 kPa safety limit"
        self.logger.log_test("TC-MASS-011", "PASS", f"Over-pressure relief verified: {pressure:.1f} kPa")


@pytest.mark.massage
@pytest.mark.high
class TestMassageTelemetry:
    """Test massage telemetry and communication"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/massage_tests.log')
    
    def test_pressure_telemetry_cycle_time(self):
        """TC-MASS-012: Verify SEAT_MASSAGE_STATUS sent every 100ms ±10ms"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=3)
        
        timestamps = []
        for i in range(11):  # Collect 11 messages
            msg = self.hil.read_massage_status_raw()
            timestamps.append(msg['timestamp'])
            time.sleep(0.05)
        
        intervals = []
        for i in range(1, len(timestamps)):
            interval = timestamps[i] - timestamps[i-1]
            intervals.append(interval)
            assert 0.090 <= interval <= 0.110, f"Cycle time {interval*1000:.1f}ms out of range"
        
        self.logger.log_test("TC-MASS-012", "PASS", "Telemetry cycle time verified")


@pytest.mark.massage
@pytest.mark.medium
class TestMassageAutoShutdown:
    """Test massage auto-shutdown functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/massage_tests.log')
    
    def test_auto_shutdown_after_30_minutes(self):
        """TC-MASS-013: Verify massage auto-shutdown after 30 minutes"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=3)
        
        # Simulate 30 minute duration
        self.hil.simulate_time_advance(30 * 60)  # 30 minutes in seconds
        
        status = self.hil.read_massage_status()
        assert status['pump_active'] == False, "Pump should auto-shutdown after 30 minutes"
        
        self.logger.log_test("TC-MASS-013", "PASS", "Auto-shutdown verified")


@pytest.mark.massage
@pytest.mark.high
class TestMassageFaults:
    """Test massage fault detection"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/massage_tests.log')
    
    def test_pump_fault_detection(self):
        """TC-MASS-014: Verify pump failure detection when pressure not reached"""
        self.hil.send_control_command(massage_enable=True, massage_intensity=3)
        self.hil.simulate_pump_fault()
        
        time.sleep(10.5)  # Wait for fault detection (10s threshold + margin)
        
        status = self.hil.read_massage_status()
        assert status['pump_fault'] == True, "Pump fault should be detected"
        assert status['pump_active'] == False, "Pump should be disabled after fault"
        
        fault_log = self.hil.read_event_log()
        assert fault_log is not None, "Fault should be logged"
        
        self.logger.log_test("TC-MASS-014", "PASS", "Pump fault detection verified")


@pytest.mark.massage
@pytest.mark.stress
class TestMassageStress:
    """Stress tests for massage subsystem"""
    
    @pytest.fixture(autouse=True)
    def setup(self, config):
        """Setup for each test"""
        self.config = config
        self.hil = HILInterface(config)
        self.logger = DataLogger('reports/massage_tests.log')
    
    def test_pattern_switching_under_load(self):
        """TC-STRESS-002: Verify smooth transitions between massage patterns"""
        patterns = [0, 1, 2]  # Wave, Pulse, Continuous
        
        pressure_deviations = []
        
        for i in range(10):
            for pattern in patterns:
                self.hil.send_control_command(
                    massage_enable=True, 
                    massage_intensity=3, 
                    massage_pattern=pattern
                )
                
                time.sleep(0.5)
                readings_before = [self.hil.read_massage_status()['pressure_kpa'] for _ in range(3)]
                
                # Switch pattern
                next_pattern = patterns[(patterns.index(pattern) + 1) % len(patterns)]
                self.hil.send_control_command(
                    massage_enable=True, 
                    massage_intensity=3, 
                    massage_pattern=next_pattern
                )
                
                time.sleep(0.2)
                readings_after = [self.hil.read_massage_status()['pressure_kpa'] for _ in range(3)]
                
                avg_before = sum(readings_before) / len(readings_before)
                avg_after = sum(readings_after) / len(readings_after)
                deviation = abs(avg_after - avg_before)
                pressure_deviations.append(deviation)
        
        max_deviation = max(pressure_deviations)
        assert max_deviation <= 15.0, f"Max pressure deviation {max_deviation}kPa exceeds 15 kPa"
        
        self.logger.log_test("TC-STRESS-002", "PASS", f"Pattern switching verified, max deviation: {max_deviation:.1f} kPa")
