"""
Tests package for Inventory Management System

Contains unit tests, integration tests, and test utilities.
"""

__version__ = "1.0.0"

# Test configuration
TEST_CONFIG = {
    'test_data_dir': 'test_data',
    'mock_excel_file': 'mock_inventory.xlsx',
    'test_timeout': 30,
    'use_mock_data': True
}

def get_test_config():
    """Get test configuration"""
    return TEST_CONFIG