"""
Pages package for Inventory Management System

Contains all application pages and navigation routes.
"""

__version__ = "1.0.0"

# Available pages
AVAILABLE_PAGES = [
    "dashboard",
    "data_entry", 
    "reports",
    "download_center",
    "settings"
]

def get_available_pages():
    """Get list of available pages"""
    return AVAILABLE_PAGES