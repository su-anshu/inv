"""
Data Formatters - Functions to format data for display and export
"""

from datetime import datetime, date
from typing import Union, Optional, Any, List, Dict
import locale
from src.utils.constants import CURRENCY_SYMBOL, DATE_FORMATS, DATETIME_FORMATS, NUMBER_FORMATS

class DataFormatter:
    """Class containing various data formatting methods"""
    
    def __init__(self):
        # Try to set Indian locale for number formatting
        try:
            locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except:
                pass  # Use default locale
    
    @staticmethod
    def format_currency(amount: Union[int, float], symbol: str = CURRENCY_SYMBOL, precision: int = 2) -> str:
        """Format amount as currency with proper Indian formatting"""
        if amount is None:
            return f"{symbol}0.00"
        
        try:
            # Handle large numbers with Indian notation (Lakh, Crore)
            if abs(amount) >= 10000000:  # 1 Crore
                formatted = f"{symbol}{amount/10000000:.1f}Cr"
            elif abs(amount) >= 100000:  # 1 Lakh
                formatted = f"{symbol}{amount/100000:.1f}L"
            elif abs(amount) >= 1000:  # 1 Thousand
                formatted = f"{symbol}{amount/1000:.1f}K"
            else:
                formatted = f"{symbol}{amount:,.{precision}f}"
            
            return formatted
            
        except (TypeError, ValueError):
            return f"{symbol}0.00"
    
    @staticmethod
    def format_number(number: Union[int, float], precision: int = 0, use_separator: bool = True) -> str:
        """Format number with thousand separators"""
        if number is None:
            return "0"
        
        try:
            if use_separator:
                if precision == 0:
                    return f"{int(number):,}"
                else:
                    return f"{number:,.{precision}f}"
            else:
                if precision == 0:
                    return str(int(number))
                else:
                    return f"{number:.{precision}f}"
                    
        except (TypeError, ValueError):
            return "0"
    
    @staticmethod
    def format_percentage(value: Union[int, float], precision: int = 1) -> str:
        """Format value as percentage"""
        if value is None:
            return "0.0%"
        
        try:
            return f"{value:.{precision}f}%"
        except (TypeError, ValueError):
            return "0.0%"
    
    @staticmethod
    def format_date(date_obj: Union[date, datetime, str], format_type: str = 'DISPLAY') -> str:
        """Format date object to string"""
        if date_obj is None:
            return ""
        
        format_str = DATE_FORMATS.get(format_type, DATE_FORMATS['DISPLAY'])
        
        try:
            if isinstance(date_obj, str):
                # Try to parse ISO format string
                if 'T' in date_obj:
                    date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00')).date()
                else:
                    date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
            
            if isinstance(date_obj, datetime):
                date_obj = date_obj.date()
            
            if isinstance(date_obj, date):
                return date_obj.strftime(format_str)
                
        except (ValueError, TypeError):
            pass
        
        return str(date_obj)
    
    @staticmethod
    def format_datetime(datetime_obj: Union[datetime, str], format_type: str = 'DISPLAY') -> str:
        """Format datetime object to string"""
        if datetime_obj is None:
            return ""
        
        format_str = DATETIME_FORMATS.get(format_type, DATETIME_FORMATS['DISPLAY'])
        
        try:
            if isinstance(datetime_obj, str):
                # Try to parse ISO format string
                datetime_obj = datetime.fromisoformat(datetime_obj.replace('Z', '+00:00'))
            
            if isinstance(datetime_obj, datetime):
                return datetime_obj.strftime(format_str)
                
        except (ValueError, TypeError):
            pass
        
        return str(datetime_obj)
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes is None or size_bytes < 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                if unit == 'B':
                    return f"{int(size_bytes)} {unit}"
                else:
                    return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} PB"
    
    @staticmethod
    def format_duration(seconds: Union[int, float]) -> str:
        """Format duration in seconds to human readable format"""
        if seconds is None or seconds < 0:
            return "0s"
        
        seconds = int(seconds)
        
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes}m"
            return f"{minutes}m {remaining_seconds}s"
        elif seconds < 86400:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            if remaining_minutes == 0:
                return f"{hours}h"
            return f"{hours}h {remaining_minutes}m"
        else:
            days = seconds // 86400
            remaining_hours = (seconds % 86400) // 3600
            if remaining_hours == 0:
                return f"{days}d"
            return f"{days}d {remaining_hours}h"
    
    @staticmethod
    def format_stock_status(status: str) -> str:
        """Format stock status with appropriate styling"""
        status_mapping = {
            'out_of_stock': '🔴 Out of Stock',
            'critical': '🟠 Critical',
            'low': '🟡 Low Stock',
            'normal': '🟢 Normal',
            'overstocked': '🟣 Overstocked'
        }
        
        return status_mapping.get(status.lower(), f"❓ {status.title()}")
    
    @staticmethod
    def format_transaction_type(transaction_type: str) -> str:
        """Format transaction type with icons"""
        type_mapping = {
            'sale': '🛒 Sale',
            'purchase': '🛍️ Purchase',
            'production': '🏭 Production',
            'return': '↩️ Return',
            'adjustment': '🔧 Adjustment',
            'transfer': '📦 Transfer'
        }
        
        return type_mapping.get(transaction_type.lower(), f"📄 {transaction_type.title()}")
    
    @staticmethod
    def format_channel(channel: str) -> str:
        """Format sales channel with appropriate styling"""
        channel_mapping = {
            'amazon fba': '📦 Amazon FBA',
            'amazon easyship': '📮 Amazon Easyship',
            'flipkart': '🛒 Flipkart',
            'direct sales': '🤝 Direct Sales',
            'wholesale': '🏢 Wholesale',
            'retail': '🏪 Retail',
            'online store': '💻 Online Store',
            'others': '📋 Others'
        }
        
        return channel_mapping.get(channel.lower(), f"🔗 {channel.title()}")
    
    @staticmethod
    def format_priority(priority: str) -> str:
        """Format priority level with colors"""
        priority_mapping = {
            'low': '🟢 Low',
            'medium': '🟡 Medium',
            'high': '🟠 High',
            'critical': '🔴 Critical',
            'emergency': '🚨 Emergency'
        }
        
        return priority_mapping.get(priority.lower(), f"❓ {priority.title()}")
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
        """Truncate text to specified length"""
        if text is None:
            return ""
        
        text = str(text).strip()
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def format_phone_number(phone: str) -> str:
        """Format phone number for display"""
        if not phone:
            return ""
        
        # Remove all non-digits
        digits_only = ''.join(filter(str.isdigit, phone))
        
        # Handle Indian phone numbers
        if len(digits_only) == 10:
            return f"+91 {digits_only[:5]} {digits_only[5:]}"
        elif len(digits_only) == 12 and digits_only.startswith('91'):
            return f"+{digits_only[:2]} {digits_only[2:7]} {digits_only[7:]}"
        else:
            return phone  # Return original if can't format
    
    @staticmethod
    def format_address(address_parts: Dict[str, str]) -> str:
        """Format address from components"""
        parts = []
        
        # Standard address order
        order = ['line1', 'line2', 'city', 'state', 'pincode', 'country']
        
        for key in order:
            value = address_parts.get(key, '').strip()
            if value:
                parts.append(value)
        
        return ', '.join(parts)
    
    @staticmethod
    def format_list_display(items: List[Any], max_items: int = 3, separator: str = ", ") -> str:
        """Format list for display with truncation"""
        if not items:
            return "None"
        
        items_str = [str(item) for item in items]
        
        if len(items_str) <= max_items:
            return separator.join(items_str)
        else:
            displayed = separator.join(items_str[:max_items])
            remaining = len(items_str) - max_items
            return f"{displayed} and {remaining} more"
    
    @staticmethod
    def format_boolean(value: bool, true_text: str = "Yes", false_text: str = "No") -> str:
        """Format boolean value for display"""
        if value is None:
            return "Unknown"
        
        return true_text if value else false_text
    
    @staticmethod
    def format_rating(rating: Union[int, float], max_rating: int = 5) -> str:
        """Format rating with stars"""
        if rating is None:
            return "No rating"
        
        try:
            rating = float(rating)
            full_stars = int(rating)
            half_star = 1 if (rating - full_stars) >= 0.5 else 0
            empty_stars = max_rating - full_stars - half_star
            
            stars = "⭐" * full_stars
            if half_star:
                stars += "✨"
            stars += "☆" * empty_stars
            
            return f"{stars} ({rating:.1f}/{max_rating})"
            
        except (TypeError, ValueError):
            return "Invalid rating"
    
    @staticmethod
    def format_json_display(data: Dict[str, Any], max_length: int = 100) -> str:
        """Format JSON data for display"""
        if not data:
            return "{}"
        
        try:
            import json
            json_str = json.dumps(data, indent=2)
            
            if len(json_str) <= max_length:
                return json_str
            else:
                return DataFormatter.truncate_text(json_str, max_length)
                
        except (TypeError, ValueError):
            return str(data)
    
    @staticmethod
    def format_change_indicator(old_value: Union[int, float], new_value: Union[int, float]) -> str:
        """Format change indicator with arrows and colors"""
        if old_value is None or new_value is None:
            return ""
        
        try:
            change = new_value - old_value
            percentage_change = (change / old_value * 100) if old_value != 0 else 0
            
            if change > 0:
                return f"↗️ +{abs(change):.1f} (+{percentage_change:.1f}%)"
            elif change < 0:
                return f"↘️ -{abs(change):.1f} (-{abs(percentage_change):.1f}%)"
            else:
                return "➡️ No change"
                
        except (TypeError, ValueError, ZeroDivisionError):
            return ""
    
    @staticmethod
    def format_table_cell(value: Any, data_type: str = "text", **kwargs) -> str:
        """Format value for table cell display"""
        if value is None:
            return ""
        
        if data_type == "currency":
            return DataFormatter.format_currency(value, **kwargs)
        elif data_type == "number":
            return DataFormatter.format_number(value, **kwargs)
        elif data_type == "percentage":
            return DataFormatter.format_percentage(value, **kwargs)
        elif data_type == "date":
            return DataFormatter.format_date(value, **kwargs)
        elif data_type == "datetime":
            return DataFormatter.format_datetime(value, **kwargs)
        elif data_type == "boolean":
            return DataFormatter.format_boolean(value, **kwargs)
        elif data_type == "file_size":
            return DataFormatter.format_file_size(value)
        elif data_type == "duration":
            return DataFormatter.format_duration(value)
        elif data_type == "truncate":
            max_length = kwargs.get('max_length', 50)
            return DataFormatter.truncate_text(str(value), max_length)
        else:
            return str(value)
    
    @staticmethod
    def format_search_highlight(text: str, search_term: str) -> str:
        """Highlight search terms in text"""
        if not search_term or not text:
            return text
        
        import re
        
        try:
            # Case-insensitive search and replace
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
            highlighted = pattern.sub(f'**{search_term}**', text)
            return highlighted
        except:
            return text
    
    @staticmethod
    def format_validation_message(field_name: str, error_type: str, **kwargs) -> str:
        """Format validation error messages"""
        messages = {
            'required': f"{field_name} is required",
            'min_length': f"{field_name} must be at least {kwargs.get('min_length', 0)} characters",
            'max_length': f"{field_name} cannot exceed {kwargs.get('max_length', 0)} characters",
            'min_value': f"{field_name} must be at least {kwargs.get('min_value', 0)}",
            'max_value': f"{field_name} cannot exceed {kwargs.get('max_value', 0)}",
            'invalid_format': f"{field_name} has invalid format",
            'invalid_email': f"{field_name} must be a valid email address",
            'invalid_phone': f"{field_name} must be a valid phone number",
            'invalid_date': f"{field_name} must be a valid date",
            'future_date': f"{field_name} cannot be a future date",
            'past_date': f"{field_name} cannot be a past date"
        }
        
        return messages.get(error_type, f"{field_name} is invalid")

# Convenience functions that use the DataFormatter class
def currency(amount: Union[int, float], **kwargs) -> str:
    """Quick currency formatting"""
    return DataFormatter.format_currency(amount, **kwargs)

def number(value: Union[int, float], **kwargs) -> str:
    """Quick number formatting"""
    return DataFormatter.format_number(value, **kwargs)

def percentage(value: Union[int, float], **kwargs) -> str:
    """Quick percentage formatting"""
    return DataFormatter.format_percentage(value, **kwargs)

def date_format(date_obj: Union[date, datetime, str], **kwargs) -> str:
    """Quick date formatting"""
    return DataFormatter.format_date(date_obj, **kwargs)

def datetime_format(datetime_obj: Union[datetime, str], **kwargs) -> str:
    """Quick datetime formatting"""
    return DataFormatter.format_datetime(datetime_obj, **kwargs)

def file_size(size_bytes: int) -> str:
    """Quick file size formatting"""
    return DataFormatter.format_file_size(size_bytes)

def duration(seconds: Union[int, float]) -> str:
    """Quick duration formatting"""
    return DataFormatter.format_duration(seconds)

def truncate(text: str, max_length: int = 50) -> str:
    """Quick text truncation"""
    return DataFormatter.truncate_text(text, max_length)

# Specialized formatters for business domain
class InventoryFormatter:
    """Specialized formatters for inventory-specific data"""
    
    @staticmethod
    def format_stock_level(current: int, minimum: int, maximum: int) -> str:
        """Format stock level with status"""
        if current <= 0:
            status = "🔴 Out of Stock"
        elif current <= minimum:
            status = "🟠 Low Stock"
        elif current >= maximum:
            status = "🟣 Overstocked"
        else:
            status = "🟢 Normal"
        
        return f"{current:,} units ({status})"
    
    @staticmethod
    def format_product_code(weight: float, category: str = "RC") -> str:
        """Format product code"""
        return f"{category}_{weight}KG"
    
    @staticmethod
    def format_batch_number(date_obj: date, sequence: int) -> str:
        """Format batch number"""
        date_str = date_obj.strftime("%Y%m%d")
        return f"BATCH-{date_str}-{sequence:03d}"
    
    @staticmethod
    def format_order_id(channel: str, timestamp: datetime, sequence: int) -> str:
        """Format order ID"""
        channel_code = {
            'Amazon FBA': 'AMZ',
            'Amazon Easyship': 'AME',
            'Flipkart': 'FKT',
            'Direct Sales': 'DIR',
            'Others': 'OTH'
        }.get(channel, 'UNK')
        
        date_code = timestamp.strftime("%m%d")
        time_code = timestamp.strftime("%H%M")
        
        return f"{channel_code}-{date_code}{time_code}-{sequence:04d}"
    
    @staticmethod
    def format_efficiency(actual_output: float, expected_output: float) -> str:
        """Format production efficiency"""
        if expected_output <= 0:
            return "N/A"
        
        efficiency = (actual_output / expected_output) * 100
        
        if efficiency >= 95:
            icon = "🟢"
        elif efficiency >= 85:
            icon = "🟡"
        else:
            icon = "🔴"
        
        return f"{icon} {efficiency:.1f}%"