"""
Data Logger Module
Handles test data logging and report generation
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)


class DataLogger:
    """Logger for test execution data and results"""
    
    def __init__(self, log_file: str):
        """Initialize data logger"""
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.test_results = []
        self.measurements = []
        
        logger.info(f"Data logger initialized with file: {log_file}")
    
    def log_test(self, test_id: str, status: str, message: str, details: dict = None):
        """Log test execution result"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'test_id': test_id,
            'status': status,
            'message': message,
            'details': details or {}
        }
        
        self.test_results.append(result)
        logger.info(f"{test_id}: {status} - {message}")
        
        # Write to CSV
        self._append_to_csv(test_id, status, message)
    
    def log_measurement(self, test_id: str, measurement_name: str, value: float, unit: str):
        """Log a measurement during test execution"""
        measurement = {
            'timestamp': datetime.now().isoformat(),
            'test_id': test_id,
            'measurement': measurement_name,
            'value': value,
            'unit': unit
        }
        
        self.measurements.append(measurement)
        logger.debug(f"{test_id}: {measurement_name} = {value} {unit}")
    
    def log_error(self, test_id: str, error_message: str, traceback: str = ""):
        """Log test error"""
        self.log_test(test_id, "FAIL", error_message, {'traceback': traceback})
        logger.error(f"{test_id}: {error_message}")
    
    def _append_to_csv(self, test_id: str, status: str, message: str):
        """Append test result to CSV file"""
        try:
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    test_id,
                    status,
                    message
                ])
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")
    
    def generate_summary_report(self) -> Dict:
        """Generate summary report from test results"""
        summary = {
            'total_tests': len(self.test_results),
            'passed': sum(1 for r in self.test_results if r['status'] == 'PASS'),
            'failed': sum(1 for r in self.test_results if r['status'] == 'FAIL'),
            'skipped': sum(1 for r in self.test_results if r['status'] == 'SKIP'),
            'errors': sum(1 for r in self.test_results if r['status'] == 'ERROR'),
            'pass_rate': 0.0
        }
        
        if summary['total_tests'] > 0:
            summary['pass_rate'] = (summary['passed'] / summary['total_tests']) * 100
        
        return summary
    
    def export_json_report(self, output_file: str):
        """Export test results as JSON"""
        report = {
            'generated': datetime.now().isoformat(),
            'summary': self.generate_summary_report(),
            'test_results': self.test_results,
            'measurements': self.measurements
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"JSON report exported to {output_file}")
    
    def export_html_report(self, output_file: str):
        """Export test results as HTML"""
        summary = self.generate_summary_report()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Seat Comfort Module - Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ background-color: #f0f0f0; padding: 10px; margin: 10px 0; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
            </style>
        </head>
        <body>
            <h1>Seat Comfort Module - Test Execution Report</h1>
            <div class="summary">
                <p><strong>Total Tests:</strong> {summary['total_tests']}</p>
                <p><strong class="pass">Passed:</strong> {summary['passed']}</p>
                <p><strong class="fail">Failed:</strong> {summary['failed']}</p>
                <p><strong>Pass Rate:</strong> {summary['pass_rate']:.1f}%</p>
            </div>
            
            <h2>Test Results</h2>
            <table>
                <tr>
                    <th>Test ID</th>
                    <th>Status</th>
                    <th>Message</th>
                    <th>Timestamp</th>
                </tr>
        """
        
        for result in self.test_results:
            status_class = 'pass' if result['status'] == 'PASS' else 'fail'
            html_content += f"""
                <tr>
                    <td>{result['test_id']}</td>
                    <td class="{status_class}">{result['status']}</td>
                    <td>{result['message']}</td>
                    <td>{result['timestamp']}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report exported to {output_file}")
