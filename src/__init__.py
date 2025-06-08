"""
Source code package for Inventory Management System

This package contains all the application logic, components, and services.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Package information
PACKAGE_INFO = {
    "components": "UI components and reusable widgets",
    "pages": "Main application pages and routes",
    "services": "Business logic and data processing services",
    "models": "Data models and structures",
    "utils": "Utility functions and helpers"
}

def get_package_info():
    """Get information about the source package"""
    return {
        "version": __version__,
        "description": "Main source code package for inventory management system",
        "modules": PACKAGE_INFO
    }