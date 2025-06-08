"""
Models package for Inventory Management System

Contains data models and structures for the application.
"""

from .product import Product, ProductCatalog

__version__ = "1.0.0"

# Export main classes
__all__ = ['Product', 'ProductCatalog']

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