"""
Application Constants - Centralized constants for the inventory management system
"""

from datetime import timedelta

# Application Information
APP_NAME = "Inventory Management System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Comprehensive inventory management with Excel integration"

# File and Data Constants
SUPPORTED_FILE_FORMATS = ['.xlsx', '.xls', '.csv']
MAX_FILE_SIZE_MB = 50
DEFAULT_ENCODING = 'utf-8'

# Excel Sheet Names
EXCEL_SHEETS = {
    'STOCK': 'stock sheet',
    'SALES': 'Sales_Log',
    'PURCHASES': 'Purchase_Log',
    'PRODUCTION': 'Production_Log',
    'RETURNS': 'Return_Log',
    'ADJUSTMENTS': 'Adjustment_Log'
}

# Product Constants
PRODUCT_CATEGORIES = [
    'Roasted Chana',
    'Raw Materials',
    'Packaging Materials',
    'Finished Goods'
]

QUALITY_GRADES = ['A', 'B', 'C', 'Premium', 'Standard']

POUCH_SIZES = [
    '6*9',    # For 0.2kg
    '7*10',   # For 0.5kg
    '9*12',   # For 1.0kg
    '11*16',  # For 1.5kg and 2.0kg
]

# Stock Status Constants
STOCK_STATUSES = {
    'OUT_OF_STOCK': 'Out of Stock',
    'CRITICAL': 'Critical (≤5 units)',
    'LOW': 'Low Stock',
    'NORMAL': 'Normal',
    'OVERSTOCKED': 'Overstocked'
}

STOCK_STATUS_COLORS = {
    'OUT_OF_STOCK': '#dc3545',    # Red
    'CRITICAL': '#fd7e14',        # Orange
    'LOW': '#ffc107',             # Yellow
    'NORMAL': '#28a745',          # Green
    'OVERSTOCKED': '#6f42c1'      # Purple
}

# Transaction Types
TRANSACTION_TYPES = {
    'SALE': 'Sale',
    'PURCHASE': 'Purchase',
    'PRODUCTION': 'Production',
    'RETURN': 'Return',
    'ADJUSTMENT': 'Stock Adjustment',
    'TRANSFER': 'Transfer'
}

TRANSACTION_STATUSES = {
    'PENDING': 'Pending',
    'COMPLETED': 'Completed',
    'CANCELLED': 'Cancelled',
    'REFUNDED': 'Refunded'
}

# Sales Channels
SALES_CHANNELS = [
    'Amazon FBA',
    'Amazon Easyship',
    'Flipkart',
    'Direct Sales',
    'Wholesale',
    'Retail',
    'Online Store',
    'Others'
]

CHANNEL_COLORS = {
    'Amazon FBA': '#ff9900',
    'Amazon Easyship': '#ff9900',
    'Flipkart': '#047bd6',
    'Direct Sales': '#28a745',
    'Wholesale': '#6c757d',
    'Retail': '#17a2b8',
    'Online Store': '#6f42c1',
    'Others': '#343a40'
}

# Payment Methods
PAYMENT_METHODS = [
    'Cash',
    'Bank Transfer',
    'Cheque',
    'Credit Card',
    'Debit Card',
    'UPI',
    'Digital Wallet',
    'Credit Terms'
]

# Return Reasons
RETURN_REASONS = [
    'Damaged Product',
    'Expired Product',
    'Customer Return',
    'Quality Issue',
    'Wrong Product',
    'Packaging Issue',
    'Transportation Damage',
    'Other'
]

# Production Shifts
PRODUCTION_SHIFTS = [
    'Morning (6 AM - 2 PM)',
    'Evening (2 PM - 10 PM)',
    'Night (10 PM - 6 AM)'
]

PRODUCTION_LINES = [
    'Line 1 - Main Production',
    'Line 2 - Secondary',
    'Line 3 - Quality Control',
    'Manual Packaging'
]

# Report Types
REPORT_TYPES = {
    'STOCK_SUMMARY': 'Stock Summary Report',
    'SALES_ANALYSIS': 'Sales Analysis Report',
    'PURCHASE_REPORT': 'Purchase Report',
    'PRODUCTION_REPORT': 'Production Report',
    'FINANCIAL_SUMMARY': 'Financial Summary',
    'INVENTORY_VALUATION': 'Inventory Valuation',
    'ABC_ANALYSIS': 'ABC Analysis',
    'CUSTOM_REPORT': 'Custom Report'
}

REPORT_FORMATS = {
    'PDF': 'Portable Document Format',
    'EXCEL': 'Microsoft Excel',
    'CSV': 'Comma Separated Values',
    'JSON': 'JavaScript Object Notation',
    'HTML': 'HyperText Markup Language'
}

# Date and Time Constants
DATE_FORMATS = {
    'ISO': '%Y-%m-%d',
    'US': '%m/%d/%Y',
    'EU': '%d/%m/%Y',
    'DISPLAY': '%d %b %Y',
    'FULL': '%A, %B %d, %Y'
}

DATETIME_FORMATS = {
    'ISO': '%Y-%m-%d %H:%M:%S',
    'DISPLAY': '%d %b %Y %I:%M %p',
    'FULL': '%A, %B %d, %Y at %I:%M %p'
}

# Cache and Performance
CACHE_TIMEOUTS = {
    'SHORT': timedelta(minutes=5),
    'MEDIUM': timedelta(minutes=30),
    'LONG': timedelta(hours=1),
    'DAILY': timedelta(days=1)
}

PAGINATION_SIZES = [10, 25, 50, 100, 200]
DEFAULT_PAGE_SIZE = 25

# Validation Constants
VALIDATION_PATTERNS = {
    'EMAIL': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'PHONE_IN': r'^(\+91|91|0)?[6-9]\d{9}$',
    'PAN': r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
    'GST': r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
    'PINCODE': r'^[1-9][0-9]{5}$'
}

VALIDATION_LIMITS = {
    'MIN_STOCK': 0,
    'MAX_STOCK': 100000,
    'MIN_PRICE': 0.01,
    'MAX_PRICE': 100000,
    'MIN_WEIGHT': 0.1,
    'MAX_WEIGHT': 50.0,
    'MIN_QUANTITY': 1,
    'MAX_QUANTITY': 10000
}

# UI Constants
COLORS = {
    'PRIMARY': '#ff4b4b',
    'SECONDARY': '#6c757d',
    'SUCCESS': '#28a745',
    'DANGER': '#dc3545',
    'WARNING': '#ffc107',
    'INFO': '#17a2b8',
    'LIGHT': '#f8f9fa',
    'DARK': '#343a40'
}

ICONS = {
    'DASHBOARD': '📊',
    'DATA_ENTRY': '📝',
    'REPORTS': '📈',
    'DOWNLOAD': '💾',
    'SETTINGS': '⚙️',
    'STOCK': '📦',
    'SALES': '🛒',
    'PURCHASE': '🛍️',
    'PRODUCTION': '🏭',
    'RETURN': '↩️',
    'ALERT': '⚠️',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'INFO': 'ℹ️'
}

# Status Messages
SUCCESS_MESSAGES = {
    'DATA_SAVED': 'Data saved successfully!',
    'FILE_UPLOADED': 'File uploaded successfully!',
    'BACKUP_CREATED': 'Backup created successfully!',
    'REPORT_GENERATED': 'Report generated successfully!',
    'SETTINGS_UPDATED': 'Settings updated successfully!'
}

ERROR_MESSAGES = {
    'FILE_NOT_FOUND': 'File not found. Please check the file path.',
    'INVALID_DATA': 'Invalid data provided. Please check your input.',
    'PERMISSION_DENIED': 'Permission denied. Please check file permissions.',
    'CONNECTION_ERROR': 'Connection error. Please try again.',
    'VALIDATION_FAILED': 'Data validation failed. Please correct the errors.'
}

WARNING_MESSAGES = {
    'LOW_STOCK': 'Some items are running low on stock.',
    'LARGE_FILE': 'File size is large. Upload may take time.',
    'UNSAVED_CHANGES': 'You have unsaved changes. Please save before leaving.',
    'DATA_OUTDATED': 'Data may be outdated. Consider refreshing.'
}

# Business Rules
BUSINESS_RULES = {
    'MIN_REORDER_QUANTITY': 10,
    'MAX_DISCOUNT_PERCENTAGE': 50,
    'STOCK_ALERT_THRESHOLD': 10,
    'CRITICAL_STOCK_THRESHOLD': 5,
    'AUTO_BACKUP_INTERVAL_HOURS': 6,
    'MAX_BACKUP_FILES': 50,
    'SESSION_TIMEOUT_MINUTES': 60
}

# Currency and Formatting
CURRENCY_SYMBOL = '₹'
CURRENCY_NAME = 'Indian Rupee'
CURRENCY_CODE = 'INR'

NUMBER_FORMATS = {
    'THOUSAND_SEPARATOR': ',',
    'DECIMAL_SEPARATOR': '.',
    'CURRENCY_PRECISION': 2,
    'PERCENTAGE_PRECISION': 1
}

# Location and Regional
DEFAULT_COUNTRY = 'India'
DEFAULT_TIMEZONE = 'Asia/Kolkata'
DEFAULT_LOCALE = 'en_IN'

# System Limits
SYSTEM_LIMITS = {
    'MAX_CONCURRENT_USERS': 10,
    'MAX_PRODUCTS': 1000,
    'MAX_TRANSACTIONS_PER_DAY': 10000,
    'MAX_BACKUP_SIZE_MB': 100,
    'MAX_REPORT_SIZE_MB': 25,
    'MAX_SEARCH_RESULTS': 500
}

# Integration Constants
API_LIMITS = {
    'AMAZON_REQUESTS_PER_HOUR': 100,
    'FLIPKART_REQUESTS_PER_HOUR': 200,
    'MAX_RETRY_ATTEMPTS': 3,
    'REQUEST_TIMEOUT_SECONDS': 30
}

# Logging Constants
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG_FORMATS = {
    'SIMPLE': '%(levelname)s - %(message)s',
    'DETAILED': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'JSON': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
}

# Feature Flags
FEATURES = {
    'ENABLE_AUTO_BACKUP': True,
    'ENABLE_EMAIL_NOTIFICATIONS': False,
    'ENABLE_API_INTEGRATION': False,
    'ENABLE_ADVANCED_ANALYTICS': True,
    'ENABLE_BARCODE_SCANNING': False,
    'ENABLE_MULTI_WAREHOUSE': False,
    'ENABLE_APPROVAL_WORKFLOW': False
}

# Security Constants
SECURITY = {
    'PASSWORD_MIN_LENGTH': 8,
    'SESSION_TIMEOUT_MINUTES': 60,
    'MAX_LOGIN_ATTEMPTS': 3,
    'LOCKOUT_DURATION_MINUTES': 15,
    'REQUIRE_PASSWORD_CHANGE_DAYS': 90
}

# Default Values
DEFAULTS = {
    'STOCK_LEVELS': {
        '0.2': {'opening': 100, 'min': 50, 'max': 500},
        '0.5': {'opening': 200, 'min': 100, 'max': 1000},
        '1.0': {'opening': 300, 'min': 150, 'max': 1500},
        '1.5': {'opening': 150, 'min': 75, 'max': 750},
        '2.0': {'opening': 100, 'min': 50, 'max': 500}
    },
    'PRICES': {
        '0.2': 20.0,
        '0.5': 50.0,
        '1.0': 100.0,
        '1.5': 150.0,
        '2.0': 200.0
    }
}

# Help and Documentation
HELP_URLS = {
    'USER_GUIDE': 'https://docs.company.com/inventory/user-guide',
    'API_DOCS': 'https://docs.company.com/inventory/api',
    'TROUBLESHOOTING': 'https://docs.company.com/inventory/troubleshooting',
    'VIDEO_TUTORIALS': 'https://tutorials.company.com/inventory',
    'SUPPORT': 'https://support.company.com'
}