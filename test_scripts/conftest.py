"""
Seat Comfort Module Test Framework - Configuration
pytest configuration and fixtures for HIL testing
"""

import pytest
import logging
import json
from datetime import datetime
from pathlib import Path


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TestConfig:
    """Global test configuration"""
    
    # CAN Configuration
    CAN_INTERFACE = 'virtual'
    CAN_CHANNEL = 0
    CAN_BITRATE = 500000
    CAN_TIMEOUT = 1.0  # seconds
    
    # Message IDs
    MSG_SEAT_CTRL_CMD = 0x100
    MSG_SEAT_HEAT_STATUS = 0x200
    MSG_SEAT_MASSAGE_STATUS = 0x300
    
    # Heating Parameters
    HEAT_MIN_VOLTAGE = 8.0
    HEAT_MAX_VOLTAGE = 14.4
    HEAT_MAX_TEMP = 65.0
    HEAT_SAFE_TEMP = 68.0
    HEAT_TEMP_TOLERANCE = 2.0
    
    # Massage Parameters
    MASSAGE_MIN_PRESSURE = 0.5
    MASSAGE_MAX_PRESSURE = 150.0
    MASSAGE_PRESSURE_TOLERANCE = 10.0
    
    # Timing Parameters
    CAN_CYCLE_TIME = 0.1  # 100ms
    CAN_CYCLE_TOLERANCE = 0.01  # ±10ms
    CAN_TIMEOUT_LOSS = 0.5  # 500ms
    PUMP_START_TIME = 0.5  # 500ms
    
    # Test Timeouts
    TEST_TIMEOUT = 30  # seconds per test
    STRESS_TEST_TIMEOUT = 300  # seconds for stress tests
    
    # Thresholds
    VOLTAGE_TOLERANCE = 0.1
    TEMP_TOLERANCE = 1.0
    PRESSURE_TOLERANCE = 2.0
    
    # Log capacity
    MAX_FAULT_EVENTS = 100


@pytest.fixture(scope='session')
def config():
    """Provide test configuration to all tests"""
    return TestConfig()


@pytest.fixture(scope='session')
def test_session_id():
    """Generate unique session ID for test run"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


@pytest.fixture(scope='function')
def test_logger(test_session_id):
    """Provide test-specific logger"""
    logger = logging.getLogger(__name__)
    return logger


@pytest.fixture
def test_report(test_session_id):
    """Create test report data structure"""
    return {
        'session_id': test_session_id,
        'timestamp': datetime.now().isoformat(),
        'test_results': [],
        'statistics': {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0
        }
    }


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "heating: mark test as heating subsystem test")
    config.addinivalue_line("markers", "massage: mark test as massage subsystem test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "safety: mark test as safety-critical test")
    config.addinivalue_line("markers", "edge_case: mark test as edge case")
    config.addinivalue_line("markers", "stress: mark test as stress test")
    config.addinivalue_line("markers", "critical: mark test as CRITICAL priority")
    config.addinivalue_line("markers", "hil: mark test requiring HIL interface")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers"""
    for item in items:
        # Add markers based on test name
        if 'heat' in item.nodeid.lower():
            item.add_marker(pytest.mark.heating)
        if 'massage' in item.nodeid.lower():
            item.add_marker(pytest.mark.massage)
        if 'int_' in item.nodeid.lower() or 'integration' in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)
        if 'safe' in item.nodeid.lower():
            item.add_marker(pytest.mark.safety)
        if 'edge' in item.nodeid.lower():
            item.add_marker(pytest.mark.edge_case)
        if 'stress' in item.nodeid.lower():
            item.add_marker(pytest.mark.stress)


@pytest.fixture(autouse=True)
def test_execution_tracker(test_logger, request):
    """Track test execution timing and results"""
    test_logger.info(f"Starting test: {request.node.name}")
    start_time = datetime.now()
    
    yield
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    test_logger.info(f"Completed test: {request.node.name} in {duration:.2f}s")


class HILMockData:
    """Mock data for HIL interface testing"""
    
    @staticmethod
    def get_can_message(msg_id, data_dict):
        """Create CAN message from ID and data dictionary"""
        return {
            'arbitration_id': msg_id,
            'data': data_dict,
            'is_extended_id': False,
            'timestamp': datetime.now().timestamp()
        }
    
    @staticmethod
    def heat_status_message(temp_c, duty_cycle, flags=0):
        """Generate SEAT_HEAT_STATUS message"""
        temp_byte = int((temp_c / 100.0) * 255)
        duty_byte = int((duty_cycle / 100.0) * 255)
        return HILMockData.get_can_message(
            TestConfig.MSG_SEAT_HEAT_STATUS,
            {'temp': temp_byte, 'duty': duty_byte, 'flags': flags}
        )
    
    @staticmethod
    def massage_status_message(pressure_kpa, duty_cycle, flags=0):
        """Generate SEAT_MASSAGE_STATUS message"""
        pressure_byte = int((pressure_kpa / 200.0) * 255)
        duty_byte = int((duty_cycle / 100.0) * 255)
        return HILMockData.get_can_message(
            TestConfig.MSG_SEAT_MASSAGE_STATUS,
            {'pressure': pressure_byte, 'duty': duty_byte, 'flags': flags}
        )
    
    @staticmethod
    def control_command(heat_enable, heat_intensity, massage_enable, 
                       massage_intensity, massage_pattern):
        """Generate SEAT_CTRL_CMD message"""
        byte0 = (heat_enable & 0x01) | ((heat_intensity & 0x03) << 1)
        byte1 = (massage_enable & 0x01) | ((massage_intensity & 0x07) << 1) | \
                ((massage_pattern & 0x07) << 4)
        return HILMockData.get_can_message(
            TestConfig.MSG_SEAT_CTRL_CMD,
            {'heat_ctrl': byte0, 'massage_ctrl': byte1}
        )


# Markers for test execution
pytestmark = [
    pytest.mark.filterwarnings("ignore::DeprecationWarning"),
]
