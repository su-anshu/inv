"""
UI Components package

Contains reusable UI components and widgets for the inventory management system.
"""

__version__ = "1.0.0"

# Available components
AVAILABLE_COMPONENTS = [
    "sidebar",
    "data_entry_forms", 
    "dashboard_widgets",
    "download_center"
]

def get_available_components():
    """Get list of available UI components"""
    return AVAILABLE_COMPONENTS