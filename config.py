"""
Configuration settings for Inventory Management System
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "Inventory Management System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Comprehensive inventory management system with Excel integration"

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = DATA_DIR / "templates"
UPLOADS_DIR = DATA_DIR / "uploads"
EXPORTS_DIR = DATA_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"
STATIC_DIR = BASE_DIR / "static"

# Excel Configuration
EXCEL_TEMPLATE_NAME = "stock_template.xlsx"
EXCEL_BACKUP_PREFIX = "backup_"
MAX_BACKUP_FILES = 10

# Sheet Names (matching your current Excel structure)
SHEET_NAMES = {
    "STOCK": "stock sheet",
    "RETURN": "Return",
    "PACKAGING": "Packaging",
    "CARTOONS": "Cartoons report",
    "PACKGING": "Packging"  # Note: keeping original spelling for compatibility
}

# Product Configuration
DEFAULT_PRODUCTS = {
    "Roasted chana (kg)": {
        "weights": [0.2, 0.5, 1.0, 1.5, 2.0],
        "pouch_sizes": {
            0.2: "6*9",
            0.5: "7*10", 
            1.0: "9*12",
            1.5: "11*16",
            2.0: "11*16"
        },
        "fnskus": {
            0.2: "X00289LA0X",
            0.5: "X00289J14Z",
            1.0: "X00289HWX7",
            1.5: "X00289LA0N",
            2.0: "X00289L9ZT"
        }
    }
}

# Sales Channels
SALES_CHANNELS = {
    "AMAZON": {
        "FBA": "Amazon FBA",
        "EASYSHIP": "Amazon Easyship"
    },
    "FLIPKART": "Flipkart",
    "OTHERS": "Others"
}

# Data Validation Rules
VALIDATION_RULES = {
    "MIN_STOCK": 0,
    "MAX_STOCK": 10000,
    "MIN_WEIGHT": 0.1,
    "MAX_WEIGHT": 5.0,
    "REQUIRED_FIELDS": ["product_name", "weight", "quantity"]
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    "REFRESH_INTERVAL": 30,  # seconds
    "LOW_STOCK_THRESHOLD": 10,
    "CRITICAL_STOCK_THRESHOLD": 5,
    "DEFAULT_DATE_RANGE": 30  # days
}

# Backup Configuration
BACKUP_CONFIG = {
    "AUTO_BACKUP": True,
    "BACKUP_INTERVAL": 3600,  # seconds (1 hour)
    "MAX_BACKUPS": 50,
    "BACKUP_CLOUD": False  # Set to True for cloud backup
}

# Logging Configuration
LOGGING_CONFIG = {
    "LEVEL": "INFO",
    "FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "MAX_FILE_SIZE": 10 * 1024 * 1024,  # 10MB
    "BACKUP_COUNT": 5
}

# UI Configuration
UI_CONFIG = {
    "THEME": "light",
    "PRIMARY_COLOR": "#FF4B4B",
    "BACKGROUND_COLOR": "#FFFFFF",
    "SECONDARY_BACKGROUND_COLOR": "#F0F2F6",
    "TEXT_COLOR": "#262730"
}

# API Configuration (for future integrations)
API_CONFIG = {
    "AMAZON_API_ENABLED": False,
    "FLIPKART_API_ENABLED": False,
    "RATE_LIMIT": 100,  # requests per minute
    "TIMEOUT": 30  # seconds
}

# Security Configuration
SECURITY_CONFIG = {
    "ENABLE_AUTH": False,  # Set to True for authentication
    "SESSION_TIMEOUT": 3600,  # seconds
    "MAX_LOGIN_ATTEMPTS": 3
}

# Export Configuration
EXPORT_CONFIG = {
    "SUPPORTED_FORMATS": ["xlsx", "csv", "pdf"],
    "DEFAULT_FORMAT": "xlsx",
    "INCLUDE_CHARTS": True,
    "COMPRESS_EXPORTS": False
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "CACHE_TTL": 300,  # seconds
    "MAX_ROWS_DISPLAY": 1000,
    "PAGINATION_SIZE": 50
}

# Environment-specific settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    LOGGING_CONFIG["LEVEL"] = "WARNING"
    BACKUP_CONFIG["BACKUP_CLOUD"] = True
    SECURITY_CONFIG["ENABLE_AUTH"] = True

# Create directories if they don't exist
for directory in [DATA_DIR, TEMPLATES_DIR, UPLOADS_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)