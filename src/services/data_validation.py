"""
Data Validation Service - Validates all data inputs and business rules
"""

import re
from datetime import datetime, date
from typing import Dict, List, Any, Tuple, Optional
import pandas as pd
import config
import logging

class DataValidator:
    """Service class for data validation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_rules = config.VALIDATION_RULES
    
    def validate_sale_data(self, sale_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate sale transaction data"""
        errors = []
        
        try:
            # Required fields validation
            required_fields = ['date', 'product', 'quantity', 'price', 'channel']
            for field in required_fields:
                if field not in sale_data or not sale_data[field]:
                    errors.append(f"Missing required field: {field}")
            
            # Date validation
            if 'date' in sale_data:
                if not self._validate_date(sale_data['date']):
                    errors.append("Invalid date format or future date")
            
            # Product validation
            if 'product' in sale_data:
                if not self._validate_product(sale_data['product']):
                    errors.append(f"Invalid product: {sale_data['product']}")
            
            # Quantity validation
            if 'quantity' in sale_data:
                if not self._validate_quantity(sale_data['quantity']):
                    errors.append("Quantity must be a positive number")
            
            # Price validation
            if 'price' in sale_data:
                if not self._validate_price(sale_data['price']):
                    errors.append("Price must be a positive number")
            
            # Channel validation
            if 'channel' in sale_data:
                if not self._validate_sales_channel(sale_data['channel']):
                    errors.append(f"Invalid sales channel: {sale_data['channel']}")
            
            # Order ID validation (if provided)
            if sale_data.get('order_id'):
                if not self._validate_order_id(sale_data['order_id']):
                    errors.append("Invalid order ID format")
            
            # Total amount consistency check
            if all(key in sale_data for key in ['quantity', 'price', 'total_amount']):
                expected_total = sale_data['quantity'] * sale_data['price']
                if abs(sale_data['total_amount'] - expected_total) > 0.01:
                    errors.append(f"Total amount mismatch. Expected: {expected_total}, Got: {sale_data['total_amount']}")
            
        except Exception as e:
            self.logger.error(f"Error validating sale data: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_purchase_data(self, purchase_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate purchase transaction data"""
        errors = []
        
        try:
            # Required fields validation
            required_fields = ['date', 'supplier', 'material_type', 'quantity', 'rate_per_kg']
            for field in required_fields:
                if field not in purchase_data or not purchase_data[field]:
                    errors.append(f"Missing required field: {field}")
            
            # Date validation
            if 'date' in purchase_data:
                if not self._validate_date(purchase_data['date']):
                    errors.append("Invalid date format or future date")
            
            # Supplier validation
            if 'supplier' in purchase_data:
                if not self._validate_supplier_name(purchase_data['supplier']):
                    errors.append("Supplier name must be at least 2 characters")
            
            # Quantity validation
            if 'quantity' in purchase_data:
                if not self._validate_weight(purchase_data['quantity']):
                    errors.append("Quantity must be a positive number")
            
            # Rate validation
            if 'rate_per_kg' in purchase_data:
                if not self._validate_price(purchase_data['rate_per_kg']):
                    errors.append("Rate per kg must be a positive number")
            
            # Invoice number validation (if provided)
            if purchase_data.get('invoice_number'):
                if not self._validate_invoice_number(purchase_data['invoice_number']):
                    errors.append("Invalid invoice number format")
            
            # Total amount consistency check
            if all(key in purchase_data for key in ['quantity', 'rate_per_kg', 'total_amount']):
                expected_total = purchase_data['quantity'] * purchase_data['rate_per_kg']
                if abs(purchase_data['total_amount'] - expected_total) > 0.01:
                    errors.append(f"Total amount mismatch. Expected: {expected_total}, Got: {purchase_data['total_amount']}")
            
        except Exception as e:
            self.logger.error(f"Error validating purchase data: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_production_data(self, production_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate production data"""
        errors = []
        
        try:
            # Required fields validation
            required_fields = ['date', 'batch_number', 'raw_material_used', 'output_data']
            for field in required_fields:
                if field not in production_data or not production_data[field]:
                    errors.append(f"Missing required field: {field}")
            
            # Date validation
            if 'date' in production_data:
                if not self._validate_date(production_data['date']):
                    errors.append("Invalid date format or future date")
            
            # Batch number validation
            if 'batch_number' in production_data:
                if not self._validate_batch_number(production_data['batch_number']):
                    errors.append("Invalid batch number format")
            
            # Raw material validation
            if 'raw_material_used' in production_data:
                if not self._validate_weight(production_data['raw_material_used']):
                    errors.append("Raw material used must be a positive number")
            
            # Output data validation
            if 'output_data' in production_data:
                output_data = production_data['output_data']
                if not isinstance(output_data, dict):
                    errors.append("Output data must be a dictionary")
                else:
                    total_output = 0
                    for product, quantity in output_data.items():
                        if not self._validate_product(product):
                            errors.append(f"Invalid product in output: {product}")
                        if not self._validate_quantity(quantity):
                            errors.append(f"Invalid quantity for {product}: {quantity}")
                        total_output += quantity
                    
                    if total_output == 0:
                        errors.append("At least one product output must be greater than 0")
            
            # Efficiency validation (if calculated)
            if 'efficiency' in production_data:
                efficiency = production_data['efficiency']
                if not (0 <= efficiency <= 200):  # Allow up to 200% efficiency
                    errors.append("Efficiency must be between 0% and 200%")
            
        except Exception as e:
            self.logger.error(f"Error validating production data: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_stock_data(self, stock_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate stock data"""
        errors = []
        
        try:
            # Required fields validation
            required_fields = ['product', 'current_stock']
            for field in required_fields:
                if field not in stock_data or stock_data[field] is None:
                    errors.append(f"Missing required field: {field}")
            
            # Product validation
            if 'product' in stock_data:
                if not self._validate_product(stock_data['product']):
                    errors.append(f"Invalid product: {stock_data['product']}")
            
            # Stock quantity validation
            stock_fields = ['current_stock', 'opening_stock', 'closing_stock', 'min_stock', 'max_stock']
            for field in stock_fields:
                if field in stock_data and stock_data[field] is not None:
                    if not self._validate_stock_quantity(stock_data[field]):
                        errors.append(f"{field} must be a non-negative number")
            
            # Business rule validations
            if all(field in stock_data for field in ['current_stock', 'min_stock']):
                if stock_data['current_stock'] < 0:
                    errors.append("Current stock cannot be negative")
                
                if stock_data['min_stock'] < 0:
                    errors.append("Minimum stock cannot be negative")
            
            if all(field in stock_data for field in ['min_stock', 'max_stock']):
                if stock_data['min_stock'] > stock_data['max_stock']:
                    errors.append("Minimum stock cannot be greater than maximum stock")
            
            # Price validation
            if 'unit_price' in stock_data and stock_data['unit_price'] is not None:
                if not self._validate_price(stock_data['unit_price']):
                    errors.append("Unit price must be a positive number")
            
        except Exception as e:
            self.logger.error(f"Error validating stock data: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_bulk_data(self, df: pd.DataFrame, data_type: str) -> Tuple[bool, List[str], pd.DataFrame]:
        """Validate bulk data from DataFrame"""
        errors = []
        valid_rows = []
        
        try:
            if df.empty:
                errors.append("No data provided")
                return False, errors, pd.DataFrame()
            
            # Validate each row based on data type
            for index, row in df.iterrows():
                row_data = row.to_dict()
                row_errors = []
                
                if data_type == "sales":
                    is_valid, row_errors = self.validate_sale_data(row_data)
                elif data_type == "purchases":
                    is_valid, row_errors = self.validate_purchase_data(row_data)
                elif data_type == "production":
                    is_valid, row_errors = self.validate_production_data(row_data)
                elif data_type == "stock":
                    is_valid, row_errors = self.validate_stock_data(row_data)
                else:
                    row_errors = [f"Unknown data type: {data_type}"]
                    is_valid = False
                
                if is_valid:
                    valid_rows.append(row_data)
                else:
                    for error in row_errors:
                        errors.append(f"Row {index + 1}: {error}")
            
            valid_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame()
            overall_valid = len(errors) == 0
            
            return overall_valid, errors, valid_df
            
        except Exception as e:
            self.logger.error(f"Error validating bulk data: {str(e)}")
            errors.append(f"Bulk validation error: {str(e)}")
            return False, errors, pd.DataFrame()
    
    # Private validation methods
    
    def _validate_date(self, date_value: Any) -> bool:
        """Validate date value"""
        try:
            if isinstance(date_value, (date, datetime)):
                return date_value <= date.today()
            
            if isinstance(date_value, str):
                # Try to parse string date
                parsed_date = datetime.strptime(date_value, "%Y-%m-%d").date()
                return parsed_date <= date.today()
            
            return False
        except:
            return False
    
    def _validate_product(self, product: str) -> bool:
        """Validate product name"""
        if not isinstance(product, str):
            return False
        
        # Check if product matches our weight format (e.g., "1.0kg", "0.5kg")
        try:
            valid_products = [f"{w}kg" for w in config.PRODUCT_WEIGHTS]
            return product.strip() in valid_products
        except:
            # Fallback validation if config not available
            pattern = r'^\d+(\.\d+)?kg$'
            return bool(re.match(pattern, product.strip()))
    
    def _validate_quantity(self, quantity: Any) -> bool:
        """Validate quantity value"""
        try:
            qty = float(quantity)
            return qty > 0 and qty <= 10000  # Reasonable upper limit
        except:
            return False
    
    def _validate_stock_quantity(self, quantity: Any) -> bool:
        """Validate stock quantity (can be 0)"""
        try:
            qty = float(quantity)
            max_limit = getattr(config, 'MAX_STOCK_LIMIT', 100000)  # Default if config not available
            return qty >= 0 and qty <= max_limit
        except:
            return False
    
    def _validate_price(self, price: Any) -> bool:
        """Validate price value"""
        try:
            price_val = float(price)
            return price_val > 0 and price_val <= 10000  # Reasonable upper limit
        except:
            return False
    
    def _validate_weight(self, weight: Any) -> bool:
        """Validate weight value"""
        try:
            weight_val = float(weight)
            return weight_val > 0 and weight_val <= 1000  # Reasonable upper limit for raw materials
        except:
            return False
    
    def _validate_sales_channel(self, channel: str) -> bool:
        """Validate sales channel"""
        try:
            return channel in config.SALES_CHANNELS
        except:
            # Fallback validation if config not available
            default_channels = ['Online', 'Retail', 'Wholesale', 'Amazon', 'Flipkart']
            return channel in default_channels
    
    def _validate_order_id(self, order_id: str) -> bool:
        """Validate order ID format"""
        if not isinstance(order_id, str):
            return False
        
        # Basic format validation - alphanumeric with hyphens, 5-20 characters
        pattern = r'^[A-Za-z0-9\-]{5,20}$'
        return bool(re.match(pattern, order_id))
    
    def _validate_supplier_name(self, supplier: str) -> bool:
        """Validate supplier name"""
        if not isinstance(supplier, str):
            return False
        return len(supplier.strip()) >= 2
    
    def _validate_invoice_number(self, invoice: str) -> bool:
        """Validate invoice number format"""
        if not isinstance(invoice, str):
            return False
        
        # Basic format validation - alphanumeric with hyphens/slashes, 3-20 characters
        pattern = r'^[A-Za-z0-9\-/]{3,20}$'
        return bool(re.match(pattern, invoice))
    
    def _validate_batch_number(self, batch: str) -> bool:
        """Validate batch number format"""
        if not isinstance(batch, str):
            return False
        
        # Basic format validation - typically BATCH-YYYYMMDD-XXX format
        pattern = r'^BATCH-\d{8}-\d{1,3}$'
        return bool(re.match(pattern, batch))
    
    def validate_file_upload(self, file_content: bytes, file_type: str) -> Tuple[bool, List[str]]:
        """Validate uploaded file"""
        errors = []
        
        try:
            # File size validation (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB
            if len(file_content) > max_size:
                errors.append(f"File size too large. Maximum allowed: {max_size / (1024*1024)}MB")
            
            # File type validation
            allowed_types = ['.xlsx', '.xls', '.csv']
            if not any(file_type.lower().endswith(ext) for ext in allowed_types):
                errors.append(f"Invalid file type. Allowed types: {', '.join(allowed_types)}")
            
        except Exception as e:
            self.logger.error(f"Error validating file upload: {str(e)}")
            errors.append(f"File validation error: {str(e)}")
        
        return len(errors) == 0, errors
    
    def get_validation_summary(self, validation_results: List[Tuple[bool, List[str]]]) -> Dict[str, Any]:
        """Get summary of validation results"""
        total_validations = len(validation_results)
        successful_validations = sum(1 for result in validation_results if result[0])
        failed_validations = total_validations - successful_validations
        
        all_errors = []
        for result in validation_results:
            all_errors.extend(result[1])
        
        return {
            'total_validations': total_validations,
            'successful': successful_validations,
            'failed': failed_validations,
            'success_rate': (successful_validations / total_validations * 100) if total_validations > 0 else 0,
            'total_errors': len(all_errors),
            'error_list': all_errors[:10]  # Return first 10 errors
        }