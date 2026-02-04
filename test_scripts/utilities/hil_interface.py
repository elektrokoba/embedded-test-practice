"""
HIL Interface Module
Provides abstraction for Hardware-in-the-Loop communication with Seat Comfort Module
"""

import time
import logging
from datetime import datetime
from typing import Dict, Optional


logger = logging.getLogger(__name__)


class HILInterface:
    """Interface for communicating with the Seat Comfort Module via CAN HIL"""
    
    # CAN Message IDs
    MSG_CTRL_CMD = 0x100
    MSG_HEAT_STATUS = 0x200
    MSG_MASSAGE_STATUS = 0x300
    MSG_DIAGNOSTIC = 0x7DF
    MSG_DIAGNOSTIC_RESPONSE = 0x7E8
    
    def __init__(self, config):
        """Initialize HIL interface"""
        self.config = config
        self.can_interface = None
        self.last_ctrl_command = None
        self.last_heat_status = None
        self.last_massage_status = None
        self.event_log = []
        self.simulated_time = 0.0
        
        logger.info("HIL Interface initialized")
    
    def send_control_command(self, heat_enable=False, heat_intensity=0, 
                           massage_enable=False, massage_intensity=0, 
                           massage_pattern=0):
        """Send SEAT_CTRL_CMD (0x100) to SCM"""
        byte0 = (heat_enable & 0x01) | ((heat_intensity & 0x03) << 1)
        byte1 = (massage_enable & 0x01) | ((massage_intensity & 0x07) << 1) | \
                ((massage_pattern & 0x07) << 4)
        
        message = {
            'arbitration_id': self.MSG_CTRL_CMD,
            'data': [byte0, byte1, 0, 0, 0, 0, 0, 0],
            'is_extended_id': False,
            'timestamp': time.time()
        }
        
        self.last_ctrl_command = {
            'heat_enable': heat_enable,
            'heat_intensity': heat_intensity,
            'massage_enable': massage_enable,
            'massage_intensity': massage_intensity,
            'massage_pattern': massage_pattern
        }
        
        logger.debug(f"Sent SEAT_CTRL_CMD: {message}")
        return message
    
    def read_heat_status(self) -> Dict:
        """Read SEAT_HEAT_STATUS (0x200) from SCM"""
        # Simulate reading from CAN
        status = {
            'temperature_c': 25.0 + (time.time() % 40),  # Simulated ramp
            'duty_cycle': 50 if self.last_ctrl_command and self.last_ctrl_command['heat_enable'] else 0,
            'heating_active': self.last_ctrl_command and self.last_ctrl_command['heat_enable'],
            'temp_warning': False,
            'heater_fault': False,
            'flags': 0
        }
        
        self.last_heat_status = status
        logger.debug(f"Read SEAT_HEAT_STATUS: {status}")
        return status
    
    def read_heat_status_raw(self) -> Dict:
        """Read raw SEAT_HEAT_STATUS message with timestamp"""
        status = self.read_heat_status()
        return {
            'data': status,
            'timestamp': time.time(),
            'arbitration_id': self.MSG_HEAT_STATUS
        }
    
    def read_massage_status(self) -> Dict:
        """Read SEAT_MASSAGE_STATUS (0x300) from SCM"""
        status = {
            'pressure_kpa': 120.0 if (self.last_ctrl_command and self.last_ctrl_command['massage_enable']) else 0,
            'duty_cycle': (self.last_ctrl_command['massage_intensity'] * 20 if self.last_ctrl_command else 0),
            'pump_active': self.last_ctrl_command and self.last_ctrl_command['massage_enable'],
            'pressure_warning': False,
            'pump_fault': False,
            'flags': 0
        }
        
        self.last_massage_status = status
        logger.debug(f"Read SEAT_MASSAGE_STATUS: {status}")
        return status
    
    def read_massage_status_raw(self) -> Dict:
        """Read raw SEAT_MASSAGE_STATUS message with timestamp"""
        status = self.read_massage_status()
        return {
            'data': status,
            'timestamp': time.time(),
            'arbitration_id': self.MSG_MASSAGE_STATUS
        }
    
    def set_heat_intensity(self, level: int):
        """Set heating intensity level (0-3)"""
        self.send_control_command(heat_enable=True, heat_intensity=level)
    
    def set_massage_intensity(self, level: int):
        """Set massage intensity level (1-5)"""
        self.send_control_command(massage_enable=True, massage_intensity=level)
    
    def read_temperature(self) -> float:
        """Read current seat temperature in Celsius"""
        status = self.read_heat_status()
        return status['temperature_c']
    
    def read_voltage(self) -> float:
        """Read supply voltage"""
        return 13.2  # Nominal 13.2V (typically from vehicle)
    
    def read_current(self) -> float:
        """Read current consumption in Amperes"""
        if self.last_ctrl_command and self.last_ctrl_command['heat_enable']:
            intensity = self.last_ctrl_command['heat_intensity']
            voltage = self.read_voltage()
            # Calculate approximate current based on intensity
            power_map = {0: 0, 1: 30, 2: 50, 3: 70}  # Watts
            return power_map.get(intensity, 0) / voltage if voltage > 0 else 0
        return 0.05  # Quiescent current
    
    def read_event_log(self) -> Optional[Dict]:
        """Read next event from diagnostic log"""
        if self.event_log:
            return self.event_log.pop(0)
        return None
    
    def read_massage_zone_state(self) -> Dict:
        """Read state of massage zones (left, center, right)"""
        return {
            'left_active': False,
            'center_active': True,
            'right_active': False,
            'timestamp': time.time()
        }
    
    def set_reference_temperature(self, temp_c: float):
        """Set reference/simulated seat temperature (for HIL simulation)"""
        logger.debug(f"Setting reference temperature to {temp_c}°C")
    
    def set_supply_voltage(self, voltage: float):
        """Set supply voltage for testing (for HIL simulation)"""
        logger.debug(f"Setting supply voltage to {voltage}V")
    
    def simulate_pump_overpressure(self):
        """Simulate pump overpressure condition"""
        logger.debug("Simulating pump overpressure condition")
        if self.last_massage_status:
            self.last_massage_status['pressure_kpa'] = 160.0
    
    def simulate_pump_fault(self):
        """Simulate pump fault (pressure not rising)"""
        logger.debug("Simulating pump fault")
        if self.last_massage_status:
            self.last_massage_status['pump_fault'] = True
    
    def simulate_time_advance(self, seconds: float):
        """Simulate advancing time (for timeout/duration tests)"""
        self.simulated_time += seconds
        logger.debug(f"Advanced simulated time by {seconds}s (total: {self.simulated_time}s)")
    
    def wait_for_message(self, msg_id: int, timeout: float = 1.0) -> Optional[Dict]:
        """Wait for a specific CAN message"""
        start = time.time()
        while time.time() - start < timeout:
            # Poll for message
            if msg_id == self.MSG_HEAT_STATUS:
                return self.read_heat_status_raw()
            elif msg_id == self.MSG_MASSAGE_STATUS:
                return self.read_massage_status_raw()
            time.sleep(0.01)
        return None
    
    def close(self):
        """Close HIL interface"""
        logger.info("Closing HIL interface")
