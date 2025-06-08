"""
Utils package for Inventory Management System

Contains utility functions, helpers, and common tools.
"""

__version__ = "1.0.0"

# Available utilities
AVAILABLE_UTILS = [
    "helpers",
    "constants",
    "formatters",
    "validators"
]

def get_available_utils():
    """Get list of available utility modules"""
    return AVAILABLE_UTILS