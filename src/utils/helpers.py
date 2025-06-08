"""
Helper Functions - Common utility functions for the application
"""

import streamlit as st
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Union
import config
import json

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    
    # App state
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
    
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    # User preferences
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'theme': 'light',
            'auto_refresh': False,
            'default_date_range': 30,
            'items_per_page': 25
        }
    
    # Navigation state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    if 'page_history' not in st.session_state:
        st.session_state.page_history = ["Dashboard"]
    
    # Data cache
    if 'cached_data' not in st.session_state:
        st.session_state.cached_data = {}
    
    if 'cache_timestamp' not in st.session_state:
        st.session_state.cache_timestamp = {}

def load_custom_css():
    """Load custom CSS styles"""
    
    css_file = config.STATIC_DIR / "css" / "custom.css"
    
    if css_file.exists():
        try:
            with open(css_file, 'r') as f:
                css_content = f.read()
            
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            
        except Exception as e:
            logging.error(f"Error loading custom CSS: {str(e)}")
    
    # Default styles if file doesn't exist
    else:
        default_css = """
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ff4b4b;
            margin: 0.5rem 0;
        }
        
        .success-message {
            padding: 0.75rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 0.25rem;
            color: #155724;
        }
        
        .warning-message {
            padding: 0.75rem;
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 0.25rem;
            color: #856404;
        }
        
        .error-message {
            padding: 0.75rem;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 0.25rem;
            color: #721c24;
        }
        """
        
        st.markdown(f"<style>{default_css}</style>", unsafe_allow_html=True)

def setup_logging():
    """Setup application logging"""
    
    log_dir = config.LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "app.log"
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Create logger for the application
    logger = logging.getLogger('inventory_management')
    logger.info("Application logging initialized")

def format_currency(amount: float, currency: str = "₹") -> str:
    """Format amount as currency"""
    if amount >= 100000:  # 1 Lakh
        return f"{currency}{amount/100000:.1f}L"
    elif amount >= 1000:  # 1 Thousand
        return f"{currency}{amount/1000:.1f}K"
    else:
        return f"{currency}{amount:,.2f}"

def format_number(number: Union[int, float], decimal_places: int = 0) -> str:
    """Format number with thousand separators"""
    if decimal_places == 0:
        return f"{int(number):,}"
    else:
        return f"{number:,.{decimal_places}f}"

def format_date(date_obj: Union[date, datetime, str], format_str: str = "%Y-%m-%d") -> str:
    """Format date object to string"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj).date()
        except:
            return date_obj
    
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    if isinstance(date_obj, date):
        return date_obj.strftime(format_str)
    
    return str(date_obj)

def format_datetime(datetime_obj: Union[datetime, str], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object to string"""
    if isinstance(datetime_obj, str):
        try:
            datetime_obj = datetime.fromisoformat(datetime_obj)
        except:
            return datetime_obj
    
    if isinstance(datetime_obj, datetime):
        return datetime_obj.strftime(format_str)
    
    return str(datetime_obj)

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    
    return ((new_value - old_value) / old_value) * 100

def get_date_range_options() -> Dict[str, Dict[str, date]]:
    """Get predefined date range options"""
    today = date.today()
    
    return {
        "Today": {
            "start": today,
            "end": today
        },
        "Yesterday": {
            "start": today - timedelta(days=1),
            "end": today - timedelta(days=1)
        },
        "Last 7 Days": {
            "start": today - timedelta(days=7),
            "end": today
        },
        "Last 30 Days": {
            "start": today - timedelta(days=30),
            "end": today
        },
        "This Month": {
            "start": today.replace(day=1),
            "end": today
        },
        "Last Month": {
            "start": (today.replace(day=1) - timedelta(days=1)).replace(day=1),
            "end": today.replace(day=1) - timedelta(days=1)
        },
        "This Year": {
            "start": today.replace(month=1, day=1),
            "end": today
        }
    }

def create_download_link(data: Union[str, bytes], filename: str, mime_type: str = "text/plain") -> str:
    """Create a download link for data"""
    import base64
    
    if isinstance(data, str):
        data = data.encode()
    
    b64_data = base64.b64encode(data).decode()
    
    return f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}">Download {filename}</a>'

def validate_file_upload(uploaded_file, allowed_extensions: List[str], max_size_mb: float = 10) -> tuple[bool, str]:
    """Validate uploaded file"""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
    
    # Check file size
    file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File too large. Maximum size: {max_size_mb}MB"
    
    return True, "File is valid"

def cache_data(key: str, data: Any, ttl_minutes: int = 5) -> None:
    """Cache data in session state with TTL"""
    st.session_state.cached_data[key] = data
    st.session_state.cache_timestamp[key] = datetime.now()

def get_cached_data(key: str, ttl_minutes: int = 5) -> Optional[Any]:
    """Get cached data if still valid"""
    if key not in st.session_state.cached_data:
        return None
    
    cache_time = st.session_state.cache_timestamp.get(key)
    if cache_time is None:
        return None
    
    # Check if cache is expired
    if datetime.now() - cache_time > timedelta(minutes=ttl_minutes):
        # Remove expired cache
        st.session_state.cached_data.pop(key, None)
        st.session_state.cache_timestamp.pop(key, None)
        return None
    
    return st.session_state.cached_data[key]

def clear_cache(key: Optional[str] = None) -> None:
    """Clear cached data"""
    if key is None:
        # Clear all cache
        st.session_state.cached_data.clear()
        st.session_state.cache_timestamp.clear()
    else:
        # Clear specific key
        st.session_state.cached_data.pop(key, None)
        st.session_state.cache_timestamp.pop(key, None)

def create_alert_message(message: str, alert_type: str = "info") -> None:
    """Create styled alert messages"""
    alert_styles = {
        "success": "success-message",
        "warning": "warning-message", 
        "error": "error-message",
        "info": "info-message"
    }
    
    css_class = alert_styles.get(alert_type, "info-message")
    
    st.markdown(
        f'<div class="{css_class}">{message}</div>',
        unsafe_allow_html=True
    )

def paginate_dataframe(df: pd.DataFrame, page_size: int = 25, page_number: int = 1) -> tuple[pd.DataFrame, Dict[str, Any]]:
    """Paginate DataFrame and return pagination info"""
    total_rows = len(df)
    total_pages = (total_rows + page_size - 1) // page_size
    
    start_idx = (page_number - 1) * page_size
    end_idx = min(start_idx + page_size, total_rows)
    
    paginated_df = df.iloc[start_idx:end_idx]
    
    pagination_info = {
        'current_page': page_number,
        'total_pages': total_pages,
        'total_rows': total_rows,
        'start_row': start_idx + 1,
        'end_row': end_idx,
        'page_size': page_size
    }
    
    return paginated_df, pagination_info

def create_pagination_controls(pagination_info: Dict[str, Any]) -> int:
    """Create pagination controls and return selected page"""
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    current_page = pagination_info['current_page']
    total_pages = pagination_info['total_pages']
    
    with col1:
        if st.button("⏮️ First", disabled=(current_page == 1)):
            return 1
    
    with col2:
        if st.button("◀️ Prev", disabled=(current_page == 1)):
            return max(1, current_page - 1)
    
    with col3:
        st.write(f"Page {current_page} of {total_pages} ({pagination_info['start_row']}-{pagination_info['end_row']} of {pagination_info['total_rows']} rows)")
    
    with col4:
        if st.button("Next ▶️", disabled=(current_page == total_pages)):
            return min(total_pages, current_page + 1)
    
    with col5:
        if st.button("Last ⏭️", disabled=(current_page == total_pages)):
            return total_pages
    
    return current_page

def export_dataframe(df: pd.DataFrame, format: str = "csv", filename: str = "data") -> bytes:
    """Export DataFrame to various formats"""
    if format.lower() == "csv":
        return df.to_csv(index=False).encode()
    
    elif format.lower() == "excel":
        import io
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
        
        output.seek(0)
        return output.getvalue()
    
    elif format.lower() == "json":
        return df.to_json(orient='records', indent=2).encode()
    
    else:
        raise ValueError(f"Unsupported format: {format}")

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def convert_bytes_to_human_readable(bytes_size: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"

def get_file_info(file_path: Path) -> Dict[str, Any]:
    """Get file information"""
    if not file_path.exists():
        return {'exists': False}
    
    stat = file_path.stat()
    
    return {
        'exists': True,
        'size_bytes': stat.st_size,
        'size_human': convert_bytes_to_human_readable(stat.st_size),
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'created': datetime.fromtimestamp(stat.st_ctime),
        'extension': file_path.suffix,
        'name': file_path.name
    }

def create_backup_filename(base_name: str, extension: str = "xlsx") -> str:
    """Create timestamped backup filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_backup_{timestamp}.{extension}"

def save_user_preferences(preferences: Dict[str, Any]) -> bool:
    """Save user preferences to file"""
    try:
        preferences_file = config.DATA_DIR / "user_preferences.json"
        
        with open(preferences_file, 'w') as f:
            json.dump(preferences, f, indent=2)
        
        # Update session state
        st.session_state.user_preferences = preferences
        
        return True
        
    except Exception as e:
        logging.error(f"Error saving user preferences: {str(e)}")
        return False

def load_user_preferences() -> Dict[str, Any]:
    """Load user preferences from file"""
    try:
        preferences_file = config.DATA_DIR / "user_preferences.json"
        
        if preferences_file.exists():
            with open(preferences_file, 'r') as f:
                preferences = json.load(f)
            
            # Update session state
            st.session_state.user_preferences = preferences
            
            return preferences
    
    except Exception as e:
        logging.error(f"Error loading user preferences: {str(e)}")
    
    # Return default preferences
    return {
        'theme': 'light',
        'auto_refresh': False,
        'default_date_range': 30,
        'items_per_page': 25
    }

def generate_report_filename(report_type: str, format: str = "xlsx") -> str:
    """Generate standardized report filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_type = report_type.lower().replace(" ", "_").replace("&", "and")
    return f"{clean_type}_report_{timestamp}.{format}"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    return convert_bytes_to_human_readable(size_bytes)

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing/replacing invalid characters"""
    import re
    
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove multiple consecutive underscores
    sanitized = re.sub(r'_{2,}', '_', sanitized)
    
    # Strip leading/trailing underscores and spaces
    sanitized = sanitized.strip('_ ')
    
    return sanitized

def create_progress_bar(current: int, total: int, prefix: str = "Progress") -> None:
    """Create a progress bar in Streamlit"""
    if total > 0:
        progress = current / total
        st.progress(progress)
        st.write(f"{prefix}: {current}/{total} ({progress:.1%})")
    else:
        st.write(f"{prefix}: {current}/0")

def validate_date_range(start_date: date, end_date: date, max_days: int = 365) -> tuple[bool, str]:
    """Validate date range"""
    if start_date > end_date:
        return False, "Start date cannot be after end date"
    
    if end_date > date.today():
        return False, "End date cannot be in the future"
    
    if (end_date - start_date).days > max_days:
        return False, f"Date range cannot exceed {max_days} days"
    
    return True, "Valid date range"

def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    import platform
    import psutil
    
    try:
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
            'disk_usage_gb': round(psutil.disk_usage('/').used / (1024**3), 2),
            'app_version': config.APP_VERSION
        }
    except Exception as e:
        logging.error(f"Error getting system info: {str(e)}")
        return {
            'platform': 'Unknown',
            'app_version': config.APP_VERSION,
            'error': str(e)
        }

def create_summary_cards(data: List[Dict[str, Any]], columns: int = 4) -> None:
    """Create summary metric cards"""
    if not data:
        return
    
    # Split data into rows based on columns
    rows = [data[i:i + columns] for i in range(0, len(data), columns)]
    
    for row in rows:
        cols = st.columns(len(row))
        
        for i, item in enumerate(row):
            with cols[i]:
                st.metric(
                    label=item.get('label', ''),
                    value=item.get('value', 0),
                    delta=item.get('delta', None)
                )

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def create_status_indicator(status: str, show_text: bool = True) -> str:
    """Create colored status indicator"""
    status_colors = {
        'active': '🟢',
        'inactive': '🔴',
        'pending': '🟡',
        'warning': '🟠',
        'error': '🔴',
        'success': '🟢',
        'info': '🔵'
    }
    
    indicator = status_colors.get(status.lower(), '⚪')
    
    if show_text:
        return f"{indicator} {status.title()}"
    else:
        return indicator

def batch_process_data(data: List[Any], batch_size: int = 100, process_func=None) -> List[Any]:
    """Process data in batches to avoid memory issues"""
    if not process_func:
        return data
    
    results = []
    total_batches = (len(data) + batch_size - 1) // batch_size
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        
        try:
            batch_results = process_func(batch)
            results.extend(batch_results)
        except Exception as e:
            logging.error(f"Error processing batch {i//batch_size + 1}/{total_batches}: {str(e)}")
            continue
    
    return results

def calculate_statistics(values: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for a list of values"""
    if not values:
        return {}
    
    import statistics
    
    try:
        return {
            'count': len(values),
            'sum': sum(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'mode': statistics.mode(values) if len(set(values)) < len(values) else None,
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values),
            'range': max(values) - min(values)
        }
    except Exception as e:
        logging.error(f"Error calculating statistics: {str(e)}")
        return {'error': str(e)}

def retry_operation(func, max_retries: int = 3, delay: float = 1.0):
    """Retry an operation with exponential backoff"""
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = delay * (2 ** attempt)
            logging.warning(f"Operation failed (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s: {str(e)}")
            time.sleep(wait_time)

def deep_merge_dicts(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result