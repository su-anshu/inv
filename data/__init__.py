"""
Data package for Inventory Management System

This package contains data storage, templates, uploads and exports.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Data directory information
DATA_DESCRIPTION = {
    "templates": "Excel and CSV templates for data import",
    "uploads": "User uploaded files including main Excel inventory file", 
    "exports": "Generated reports, backups, and exported data"
}

def get_data_info():
    """Get information about the data package"""
    return {
        "version": __version__,
        "description": "Data storage package for inventory management",
        "directories": DATA_DESCRIPTION
    }