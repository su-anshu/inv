"""
Data Validators - Functions to validate various types of data
"""

import re
from datetime import datetime, date
from typing import Union, List, Dict, Any, Optional, Tuple
from src.utils.constants import VALIDATION_PATTERNS, VALIDATION_LIMITS
import config

class DataValidator:
    """Class containing various data validation methods"""
    
    @staticmethod
    def validate_required(value: Any, field_name: str = "Field") -> Tuple[bool, str]:
        """Validate that a field is not empty"""
        if value is None:
            return False, f"{field_name} is required"
        
        if isinstance(value, str) and not value.strip():
            return False, f"{field_name} cannot be empty"
        
        if isinstance(value, (list, dict)) and len(value) == 0:
            return False, f"{field_name} cannot be empty"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email address format"""
        if not email:
            return False, "Email is required"
        
        pattern = VALIDATION_PATTERNS['EMAIL']
        if not re.match(pattern, email):
            return False, "Please enter a valid email address"
        
        return True, ""
    
    @staticmethod
    def validate_phone_number(phone: str, country: str = "IN") -> Tuple[bool, str]:
        """Validate phone number format"""
        if not phone:
            return False, "Phone number is required"
        
        if country == "IN":
            pattern = VALIDATION_PATTERNS['PHONE_IN']
            if not re.match(pattern, phone):
                return False, "Please enter a valid Indian phone number"
        
        return True, ""
    
    @staticmethod
    def validate_pan_number(pan: str) -> Tuple[bool, str]:
        """Validate PAN number format"""
        if not pan:
            return False, "PAN number is required"
        
        pattern = VALIDATION_PATTERNS['PAN']
        if not re.match(pattern, pan.upper()):
            return False, "Please enter a valid PAN number (e.g., ABCDE1234F)"
        
        return True, ""
    
    @staticmethod
    def validate_gst_number(gst: str) -> Tuple[bool, str]:
        """Validate GST number format"""
        if not gst:
            return False, "GST number is required"
        
        pattern = VALIDATION_PATTERNS['GST']
        if not re.match(pattern, gst.upper()):
            return False, "Please enter a valid GST number"
        
        return True, ""
    
    @staticmethod
    def validate_pincode(pincode: str) -> Tuple[bool, str]:
        """Validate Indian pincode"""
        if not pincode:
            return False, "Pincode is required"
        
        pattern = VALIDATION_PATTERNS['PINCODE']
        if not re.match(pattern, pincode):
            return False, "Please enter a valid 6-digit pincode"
        
        return True, ""
    
    @staticmethod
    def validate_number_range(value: Union[int, float], min_val: Optional[float] = None, 
                            max_val: Optional[float] = None, field_name: str = "Value") -> Tuple[bool, str]:
        """Validate number within range"""
        try:
            num_value = float(value)
        except (TypeError, ValueError):
            return False, f"{field_name} must be a valid number"
        
        if min_val is not None and num_value < min_val:
            return False, f"{field_name} must be at least {min_val}"
        
        if max_val is not None and num_value > max_val:
            return False, f"{field_name} cannot exceed {max_val}"
        
        return True, ""
    
    @staticmethod
    def validate_string_length(value: str, min_length: Optional[int] = None, 
                             max_length: Optional[int] = None, field_name: str = "Field") -> Tuple[bool, str]:
        """Validate string length"""
        if not isinstance(value, str):
            return False, f"{field_name} must be text"
        
        length = len(value.strip())
        
        if min_length is not None and length < min_length:
            return False, f"{field_name} must be at least {min_length} characters"
        
        if max_length is not None and length > max_length:
            return False, f"{field_name} cannot exceed {max_length} characters"
        
        return True, ""
    
    @staticmethod
    def validate_date(date_value: Union[str, date, datetime], 
                     allow_future: bool = True, allow_past: bool = True,
                     field_name: str = "Date") -> Tuple[bool, str]:
        """Validate date value"""
        try:
            if isinstance(date_value, str):
                # Try to parse different date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                    try:
                        parsed_date = datetime.strptime(date_value, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return False, f"{field_name} has invalid date format. Use YYYY-MM-DD"
            elif isinstance(date_value, datetime):
                parsed_date = date_value.date()
            elif isinstance(date_value, date):
                parsed_date = date_value
            else:
                return False, f"{field_name} must be a valid date"
            
            today = date.today()
            
            if not allow_future and parsed_date > today:
                return False, f"{field_name} cannot be a future date"
            
            if not allow_past and parsed_date < today:
                return False, f"{field_name} cannot be a past date"
            
            return True, ""
            
        except (ValueError, TypeError):
            return False, f"{field_name} has invalid date format"
    
    @staticmethod
    def validate_choice(value: Any, choices: List[Any], field_name: str = "Field") -> Tuple[bool, str]:
        """Validate value is in allowed choices"""
        if value not in choices:
            choices_str = ", ".join(str(choice) for choice in choices)
            return False, f"{field_name} must be one of: {choices_str}"
        
        return True, ""
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> Tuple[bool, str]:
        """Validate file extension"""
        if not filename:
            return False, "Filename is required"
        
        file_ext = filename.lower().split('.')[-1] if '.' in filename else ""
        
        if file_ext not in [ext.lower().lstrip('.') for ext in allowed_extensions]:
            return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        
        return True, ""
    
    @staticmethod
    def validate_file_size(file_size: int, max_size_mb: float = 10) -> Tuple[bool, str]:
        """Validate file size"""
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if file_size > max_size_bytes:
            return False, f"File size cannot exceed {max_size_mb}MB"
        
        return True, ""

class InventoryValidator:
    """Specialized validators for inventory management"""
    
    @staticmethod
    def validate_product_weight(weight: float) -> Tuple[bool, str]:
        """Validate product weight"""
        is_valid, message = DataValidator.validate_number_range(
            weight, 
            VALIDATION_LIMITS['MIN_WEIGHT'], 
            VALIDATION_LIMITS['MAX_WEIGHT'], 
            "Product weight"
        )
        
        if not is_valid:
            return is_valid, message
        
        # Check if weight is in predefined product weights
        if weight not in config.PRODUCT_WEIGHTS:
            valid_weights = ", ".join(str(w) for w in config.PRODUCT_WEIGHTS)
            return False, f"Product weight must be one of: {valid_weights}kg"
        
        return True, ""
    
    @staticmethod
    def validate_stock_quantity(quantity: int) -> Tuple[bool, str]:
        """Validate stock quantity"""
        return DataValidator.validate_number_range(
            quantity, 
            VALIDATION_LIMITS['MIN_STOCK'], 
            VALIDATION_LIMITS['MAX_STOCK'], 
            "Stock quantity"
        )
    
    @staticmethod
    def validate_price(price: float) -> Tuple[bool, str]:
        """Validate price value"""
        return DataValidator.validate_number_range(
            price, 
            VALIDATION_LIMITS['MIN_PRICE'], 
            VALIDATION_LIMITS['MAX_PRICE'], 
            "Price"
        )
    
    @staticmethod
    def validate_sales_channel(channel: str) -> Tuple[bool, str]:
        """Validate sales channel"""
        return DataValidator.validate_choice(
            channel, 
            config.SALES_CHANNELS, 
            "Sales channel"
        )
    
    @staticmethod
    def validate_batch_number(batch_number: str) -> Tuple[bool, str]:
        """Validate batch number format"""
        if not batch_number:
            return False, "Batch number is required"
        
        # Pattern: BATCH-YYYYMMDD-XXX
        pattern = r'^BATCH-\d{8}-\d{1,3}$'
        if not re.match(pattern, batch_number):
            return False, "Batch number must be in format: BATCH-YYYYMMDD-XXX"
        
        return True, ""
    
    @staticmethod
    def validate_product_code(product_code: str) -> Tuple[bool, str]:
        """Validate product code format"""
        if not product_code:
            return False, "Product code is required"
        
        # Pattern: RC_X.XKG
        pattern = r'^[A-Z]{2,3}_\d+(\.\d+)?KG$'
        if not re.match(pattern, product_code):
            return False, "Product code must be in format: RC_X.XKG"
        
        return True, ""
    
    @staticmethod
    def validate_order_id(order_id: str) -> Tuple[bool, str]:
        """Validate order ID format"""
        if not order_id:
            return True, ""  # Order ID is optional
        
        # Basic alphanumeric with hyphens
        pattern = r'^[A-Za-z0-9\-]{5,20}$'
        if not re.match(pattern, order_id):
            return False, "Order ID must be 5-20 characters with letters, numbers, and hyphens only"
        
        return True, ""
    
    @staticmethod
    def validate_supplier_name(supplier_name: str) -> Tuple[bool, str]:
        """Validate supplier name"""
        is_valid, message = DataValidator.validate_required(supplier_name, "Supplier name")
        if not is_valid:
            return is_valid, message
        
        return DataValidator.validate_string_length(supplier_name, 2, 100, "Supplier name")
    
    @staticmethod
    def validate_efficiency_percentage(efficiency: float) -> Tuple[bool, str]:
        """Validate production efficiency percentage"""
        return DataValidator.validate_number_range(
            efficiency, 0, 200, "Efficiency percentage"
        )

class BusinessRuleValidator:
    """Validators for business rules and constraints"""
    
    @staticmethod
    def validate_stock_levels(current: int, minimum: int, maximum: int) -> Tuple[bool, str]:
        """Validate stock level relationships"""
        if minimum < 0:
            return False, "Minimum stock cannot be negative"
        
        if maximum <= 0:
            return False, "Maximum stock must be greater than zero"
        
        if minimum >= maximum:
            return False, "Minimum stock must be less than maximum stock"
        
        if current < 0:
            return False, "Current stock cannot be negative"
        
        return True, ""
    
    @staticmethod
    def validate_transaction_amount(quantity: int, unit_price: float, total_amount: float, 
                                  tolerance: float = 0.01) -> Tuple[bool, str]:
        """Validate transaction amount calculation"""
        expected_total = quantity * unit_price
        
        if abs(total_amount - expected_total) > tolerance:
            return False, f"Total amount mismatch. Expected: ₹{expected_total:.2f}, Got: ₹{total_amount:.2f}"
        
        return True, ""
    
    @staticmethod
    def validate_return_quantity(return_quantity: int, original_quantity: int) -> Tuple[bool, str]:
        """Validate return quantity against original"""
        if return_quantity <= 0:
            return False, "Return quantity must be greater than zero"
        
        if return_quantity > original_quantity:
            return False, f"Return quantity ({return_quantity}) cannot exceed original quantity ({original_quantity})"
        
        return True, ""
    
    @staticmethod
    def validate_production_efficiency(raw_material_kg: float, output_packets: int, 
                                     avg_packet_weight: float = 0.5) -> Tuple[bool, str]:
        """Validate production efficiency"""
        if raw_material_kg <= 0:
            return False, "Raw material quantity must be greater than zero"
        
        if output_packets <= 0:
            return False, "Output packets must be greater than zero"
        
        output_weight = output_packets * avg_packet_weight
        efficiency = (output_weight / raw_material_kg) * 100
        
        if efficiency > 100:
            return False, f"Production efficiency ({efficiency:.1f}%) cannot exceed 100%"
        
        if efficiency < 50:
            return False, f"Production efficiency ({efficiency:.1f}%) is suspiciously low. Please verify data"
        
        return True, ""
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: date, max_range_days: int = 365) -> Tuple[bool, str]:
        """Validate business date ranges"""
        if start_date > end_date:
            return False, "Start date cannot be after end date"
        
        if end_date > date.today():
            return False, "End date cannot be in the future"
        
        date_diff = (end_date - start_date).days
        if date_diff > max_range_days:
            return False, f"Date range cannot exceed {max_range_days} days"
        
        return True, ""

class FormValidator:
    """Validator for form data"""
    
    @staticmethod
    def validate_sale_form(form_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate sale form data"""
        errors = []
        
        # Required fields
        required_fields = ['product', 'quantity', 'unit_price', 'sales_channel']
        for field in required_fields:
            is_valid, message = DataValidator.validate_required(form_data.get(field), field.replace('_', ' ').title())
            if not is_valid:
                errors.append(message)
        
        # Quantity validation
        if 'quantity' in form_data:
            is_valid, message = DataValidator.validate_number_range(
                form_data['quantity'], 1, 10000, "Quantity"
            )
            if not is_valid:
                errors.append(message)
        
        # Price validation
        if 'unit_price' in form_data:
            is_valid, message = InventoryValidator.validate_price(form_data['unit_price'])
            if not is_valid:
                errors.append(message)
        
        # Sales channel validation
        if 'sales_channel' in form_data:
            is_valid, message = InventoryValidator.validate_sales_channel(form_data['sales_channel'])
            if not is_valid:
                errors.append(message)
        
        # Order ID validation (optional)
        if form_data.get('order_id'):
            is_valid, message = InventoryValidator.validate_order_id(form_data['order_id'])
            if not is_valid:
                errors.append(message)
        
        # Amount calculation validation
        if all(key in form_data for key in ['quantity', 'unit_price', 'total_amount']):
            is_valid, message = BusinessRuleValidator.validate_transaction_amount(
                form_data['quantity'], form_data['unit_price'], form_data['total_amount']
            )
            if not is_valid:
                errors.append(message)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_purchase_form(form_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate purchase form data"""
        errors = []
        
        # Required fields
        required_fields = ['supplier_name', 'material_type', 'quantity_kg', 'rate_per_kg']
        for field in required_fields:
            is_valid, message = DataValidator.validate_required(form_data.get(field), field.replace('_', ' ').title())
            if not is_valid:
                errors.append(message)
        
        # Supplier name validation
        if 'supplier_name' in form_data:
            is_valid, message = InventoryValidator.validate_supplier_name(form_data['supplier_name'])
            if not is_valid:
                errors.append(message)
        
        # Quantity validation
        if 'quantity_kg' in form_data:
            is_valid, message = DataValidator.validate_number_range(
                form_data['quantity_kg'], 0.1, 1000, "Quantity"
            )
            if not is_valid:
                errors.append(message)
        
        # Rate validation
        if 'rate_per_kg' in form_data:
            is_valid, message = DataValidator.validate