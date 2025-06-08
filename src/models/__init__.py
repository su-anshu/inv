"""
Models package for Inventory Management System

Contains data models and structures for the application.
"""

__version__ = "1.0.0"

# Available models
AVAILABLE_MODELS = [
    "product",
    "inventory",
    "transaction",
    "report"
]

def get_available_models():
    """Get list of available data models"""
    return AVAILABLE_MODELS