"""
Signal Generator Module
Generates test signals for CAN bus simulation
"""

import math
import time
from typing import Dict, List


class SignalGenerator:
    """Generates various test signals for HIL testing"""
    
    @staticmethod
    def generate_ramp(start_value: float, end_value: float, duration: float, step_time: float = 0.01) -> List[float]:
        """Generate linear ramp signal"""
        num_steps = int(duration / step_time)
        values = []
        for i in range(num_steps):
            t = i / num_steps if num_steps > 0 else 0
            value = start_value + (end_value - start_value) * t
            values.append(value)
        return values
    
    @staticmethod
    def generate_sine_wave(amplitude: float, frequency: float, duration: float, step_time: float = 0.01) -> List[float]:
        """Generate sine wave signal"""
        values = []
        num_steps = int(duration / step_time)
        for i in range(num_steps):
            t = i * step_time
            value = amplitude * math.sin(2 * math.pi * frequency * t)
            values.append(value)
        return values
    
    @staticmethod
    def generate_square_wave(low_value: float, high_value: float, frequency: float, duration: float, step_time: float = 0.01) -> List[float]:
        """Generate square wave signal"""
        values = []
        num_steps = int(duration / step_time)
        period = 1.0 / frequency if frequency > 0 else 1.0
        
        for i in range(num_steps):
            t = i * step_time
            phase = (t % period) / period
            value = high_value if phase < 0.5 else low_value
            values.append(value)
        return values
    
    @staticmethod
    def generate_step_response(initial_value: float, step_value: float, step_time: float, duration: float, step_interval: float = 0.01) -> List[float]:
        """Generate step response signal"""
        values = []
        num_steps = int(duration / step_interval)
        step_index = int(step_time / step_interval)
        
        for i in range(num_steps):
            value = step_value if i >= step_index else initial_value
            values.append(value)
        return values
    
    @staticmethod
    def generate_noise(mean: float, std_dev: float, duration: float, step_time: float = 0.01) -> List[float]:
        """Generate Gaussian noise signal"""
        import random
        values = []
        num_steps = int(duration / step_time)
        
        for i in range(num_steps):
            value = random.gauss(mean, std_dev)
            values.append(value)
        return values
    
    @staticmethod
    def generate_temperature_ramp(start_temp: float, end_temp: float, duration: float, overshoot_percent: float = 5.0) -> List[float]:
        """Generate realistic temperature ramp with overshoot"""
        values = []
        num_steps = int(duration * 100)  # 10ms steps
        
        # Calculate overshoot point (typically at 70% of ramp time)
        overshoot_point = int(num_steps * 0.7)
        max_temp = end_temp + (end_temp - start_temp) * (overshoot_percent / 100.0)
        
        for i in range(num_steps):
            if i < overshoot_point:
                # Fast ramp to overshoot
                t = i / overshoot_point
                # Exponential approach
                value = start_temp + (max_temp - start_temp) * (1 - math.exp(-3 * t))
            else:
                # Decay to setpoint
                t = (i - overshoot_point) / (num_steps - overshoot_point)
                value = max_temp - (max_temp - end_temp) * (1 - math.exp(-2 * t))
            
            values.append(value)
        
        return values
    
    @staticmethod
    def generate_pressure_buildup(start_pressure: float, target_pressure: float, ramp_time: float, 
                                 overshoot_percent: float = 10.0, step_time: float = 0.01) -> List[float]:
        """Generate realistic pressure buildup curve"""
        values = []
        num_steps = int(ramp_time / step_time)
        
        # Calculate overshoot point
        overshoot_point = int(num_steps * 0.8)
        max_pressure = target_pressure + (target_pressure - start_pressure) * (overshoot_percent / 100.0)
        
        for i in range(num_steps):
            if i < overshoot_point:
                # Fast buildup
                t = i / overshoot_point
                value = start_pressure + (max_pressure - start_pressure) * (1 - math.exp(-4 * t))
            else:
                # Settle to target
                t = (i - overshoot_point) / (num_steps - overshoot_point)
                value = max_pressure - (max_pressure - target_pressure) * (1 - math.exp(-3 * t))
            
            values.append(max(start_pressure, value))
        
        return values
    
    @staticmethod
    def generate_jitter(base_signal: List[float], jitter_std_dev: float) -> List[float]:
        """Add jitter to a signal"""
        import random
        jittered = []
        for value in base_signal:
            noisy_value = value + random.gauss(0, jitter_std_dev)
            jittered.append(noisy_value)
        return jittered
    
    @staticmethod
    def generate_realistic_can_timing(nominal_interval: float, jitter_percent: float, num_messages: int) -> List[float]:
        """Generate realistic CAN message timing with jitter"""
        import random
        intervals = []
        max_jitter = nominal_interval * (jitter_percent / 100.0)
        
        for i in range(num_messages):
            jitter = random.uniform(-max_jitter, max_jitter)
            interval = nominal_interval + jitter
            intervals.append(interval)
        
        return intervals


class WaveformAnalyzer:
    """Analyzes waveforms and signals"""
    
    @staticmethod
    def calculate_statistics(values: List[float]) -> Dict:
        """Calculate statistics from signal values"""
        if not values:
            return {}
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)
        
        return {
            'mean': mean,
            'min': min(values),
            'max': max(values),
            'std_dev': std_dev,
            'range': max(values) - min(values),
            'count': len(values)
        }
    
    @staticmethod
    def detect_settling_time(values: List[float], final_value: float, tolerance: float = 0.05) -> float:
        """Detect settling time (time to reach final value ±tolerance)"""
        target_min = final_value * (1 - tolerance)
        target_max = final_value * (1 + tolerance)
        
        for i, value in enumerate(values):
            if target_min <= value <= target_max:
                # Check if it stays settled
                remaining = values[i:]
                settled = all(target_min <= v <= target_max for v in remaining[::len(remaining)//5])
                if settled:
                    return i * 0.01  # Assuming 10ms steps
        
        return None
    
    @staticmethod
    def detect_overshoot(values: List[float], steady_state: float) -> float:
        """Detect overshoot percentage"""
        max_value = max(values)
        if steady_state == 0:
            return 0
        
        overshoot_percent = ((max_value - steady_state) / abs(steady_state)) * 100
        return max(0, overshoot_percent)
