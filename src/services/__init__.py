"""
Services package for Inventory Management System

Contains business logic, data processing, and external integrations.
"""

__version__ = "1.0.0"

# Available services
AVAILABLE_SERVICES = [
    "excel_service",
    "data_validation",
    "stock_calculator", 
    "report_generator",
    "backup_service"
]

def get_available_services():
    """Get list of available services"""
    return AVAILABLE_SERVICES