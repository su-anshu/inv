"""
Transaction Data Model - Defines transaction structures and operations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, date
from enum import Enum
import uuid

class TransactionType(Enum):
    """Transaction type enumeration"""
    SALE = "sale"
    PURCHASE = "purchase"
    PRODUCTION = "production"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"

class TransactionStatus(Enum):
    """Transaction status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

@dataclass
class Transaction:
    """Base transaction model"""
    
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    transaction_type: TransactionType = TransactionType.SALE
    transaction_date: date = field(default_factory=date.today)
    status: TransactionStatus = TransactionStatus.PENDING
    reference_number: str = ""
    notes: str = ""
    created_by: str = "System"
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate transaction after initialization"""
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())
    
    def mark_completed(self) -> None:
        """Mark transaction as completed"""
        self.status = TransactionStatus.COMPLETED
        self.updated_date = datetime.now()
    
    def mark_cancelled(self) -> None:
        """Mark transaction as cancelled"""
        self.status = TransactionStatus.CANCELLED
        self.updated_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'transaction_type': self.transaction_type.value,
            'transaction_date': self.transaction_date.isoformat(),
            'status': self.status.value,
            'reference_number': self.reference_number,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }

@dataclass
class SaleTransaction(Transaction):
    """Sales transaction model"""
    
    product_id: str = ""
    product_name: str = ""
    quantity: int = 0
    unit_price: float = 0.0
    total_amount: float = 0.0
    sales_channel: str = ""
    order_id: str = ""
    customer_name: str = ""
    customer_address: str = ""
    shipping_cost: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        self.transaction_type = TransactionType.SALE
        
        # Calculate total if not provided
        if self.total_amount == 0 and self.quantity > 0 and self.unit_price > 0:
            self.total_amount = (self.quantity * self.unit_price) + self.shipping_cost + self.tax_amount - self.discount_amount
    
    @property
    def net_amount(self) -> float:
        """Calculate net amount after taxes and discounts"""
        base_amount = self.quantity * self.unit_price
        return base_amount + self.shipping_cost + self.tax_amount - self.discount_amount
    
    def apply_discount(self, discount_percentage: float) -> None:
        """Apply percentage discount"""
        base_amount = self.quantity * self.unit_price
        self.discount_amount = base_amount * (discount_percentage / 100)
        self.total_amount = self.net_amount
        self.updated_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_amount': self.total_amount,
            'net_amount': self.net_amount,
            'sales_channel': self.sales_channel,
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'shipping_cost': self.shipping_cost,
            'tax_amount': self.tax_amount,
            'discount_amount': self.discount_amount
        })
        return base_dict

@dataclass
class PurchaseTransaction(Transaction):
    """Purchase transaction model"""
    
    supplier_name: str = ""
    supplier_contact: str = ""
    material_type: str = ""
    quantity_kg: float = 0.0
    rate_per_kg: float = 0.0
    total_amount: float = 0.0
    invoice_number: str = ""
    delivery_date: Optional[date] = None
    quality_grade: str = ""
    payment_method: str = ""
    payment_status: str = "Pending"
    
    def __post_init__(self):
        super().__post_init__()
        self.transaction_type = TransactionType.PURCHASE
        
        # Calculate total if not provided
        if self.total_amount == 0 and self.quantity_kg > 0 and self.rate_per_kg > 0:
            self.total_amount = self.quantity_kg * self.rate_per_kg
    
    def mark_paid(self) -> None:
        """Mark purchase as paid"""
        self.payment_status = "Paid"
        self.updated_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'supplier_name': self.supplier_name,
            'supplier_contact': self.supplier_contact,
            'material_type': self.material_type,
            'quantity_kg': self.quantity_kg,
            'rate_per_kg': self.rate_per_kg,
            'total_amount': self.total_amount,
            'invoice_number': self.invoice_number,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'quality_grade': self.quality_grade,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status
        })
        return base_dict

@dataclass
class ProductionTransaction(Transaction):
    """Production transaction model"""
    
    batch_number: str = ""
    raw_material_used_kg: float = 0.0
    operator_name: str = ""
    shift: str = ""
    production_line: str = ""
    output_data: Dict[str, int] = field(default_factory=dict)
    efficiency_percentage: float = 0.0
    quality_grade: str = ""
    quality_notes: str = ""
    issues: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.transaction_type = TransactionType.PRODUCTION
        
        # Calculate efficiency if not provided
        if self.efficiency_percentage == 0 and self.raw_material_used_kg > 0:
            self.efficiency_percentage = self.calculate_efficiency()
    
    @property
    def total_output_packets(self) -> int:
        """Calculate total output packets"""
        return sum(self.output_data.values())
    
    @property
    def total_output_kg(self) -> float:
        """Calculate total output in kg"""
        total_kg = 0
        for product, quantity in self.output_data.items():
            # Extract weight from product name (e.g., "1.0kg" -> 1.0)
            try:
                weight = float(product.replace('kg', ''))
                total_kg += weight * quantity
            except:
                continue
        return total_kg
    
    def calculate_efficiency(self) -> float:
        """Calculate production efficiency percentage"""
        if self.raw_material_used_kg > 0:
            return (self.total_output_kg / self.raw_material_used_kg) * 100
        return 0
    
    def add_output(self, product: str, quantity: int) -> None:
        """Add production output"""
        if product in self.output_data:
            self.output_data[product] += quantity
        else:
            self.output_data[product] = quantity
        
        self.efficiency_percentage = self.calculate_efficiency()
        self.updated_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'batch_number': self.batch_number,
            'raw_material_used_kg': self.raw_material_used_kg,
            'operator_name': self.operator_name,
            'shift': self.shift,
            'production_line': self.production_line,
            'output_data': self.output_data,
            'total_output_packets': self.total_output_packets,
            'total_output_kg': self.total_output_kg,
            'efficiency_percentage': self.efficiency_percentage,
            'quality_grade': self.quality_grade,
            'quality_notes': self.quality_notes,
            'issues': self.issues
        })
        return base_dict

@dataclass
class ReturnTransaction(Transaction):
    """Return transaction model"""
    
    original_transaction_id: str = ""
    product_id: str = ""
    product_name: str = ""
    quantity: int = 0
    return_reason: str = ""
    condition: str = ""
    action_taken: str = ""
    refund_amount: float = 0.0
    restocking_fee: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        self.transaction_type = TransactionType.RETURN
    
    @property
    def net_refund(self) -> float:
        """Calculate net refund after restocking fee"""
        return self.refund_amount - self.restocking_fee
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'original_transaction_id': self.original_transaction_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'return_reason': self.return_reason,
            'condition': self.condition,
            'action_taken': self.action_taken,
            'refund_amount': self.refund_amount,
            'restocking_fee': self.restocking_fee,
            'net_refund': self.net_refund
        })
        return base_dict

class TransactionManager:
    """Manages all transaction operations"""
    
    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a new transaction"""
        if transaction.transaction_id in self.transactions:
            return False
        
        self.transactions[transaction.transaction_id] = transaction
        return True
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        return self.transactions.get(transaction_id)
    
    def update_transaction(self, transaction_id: str, updates: Dict[str, Any]) -> bool:
        """Update transaction details"""
        if transaction_id not in self.transactions:
            return False
        
        transaction = self.transactions[transaction_id]
        
        for key, value in updates.items():
            if hasattr(transaction, key):
                setattr(transaction, key, value)
        
        transaction.updated_date = datetime.now()
        return True
    
    def get_transactions_by_type(self, transaction_type: TransactionType) -> List[Transaction]:
        """Get transactions by type"""
        return [t for t in self.transactions.values() if t.transaction_type == transaction_type]
    
    def get_transactions_by_date_range(self, start_date: date, end_date: date) -> List[Transaction]:
        """Get transactions within date range"""
        return [t for t in self.transactions.values() 
                if start_date <= t.transaction_date <= end_date]
    
    def get_transactions_by_status(self, status: TransactionStatus) -> List[Transaction]:
        """Get transactions by status"""
        return [t for t in self.transactions.values() if t.status == status]
    
    def get_sales_summary(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Get sales summary for date range"""
        sales = [t for t in self.transactions.values() 
                if (isinstance(t, SaleTransaction) and 
                    start_date <= t.transaction_date <= end_date and
                    t.status == TransactionStatus.COMPLETED)]
        
        total_revenue = sum(t.total_amount for t in sales)
        total_quantity = sum(t.quantity for t in sales)
        
        return {
            'total_sales': len(sales),
            'total_revenue': total_revenue,
            'total_quantity': total_quantity,
            'average_order_value': total_revenue / len(sales) if sales else 0,
            'period_start': start_date,
            'period_end': end_date
        }
    
    def get_purchase_summary(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Get purchase summary for date range"""
        purchases = [t for t in self.transactions.values() 
                    if (isinstance(t, PurchaseTransaction) and 
                        start_date <= t.transaction_date <= end_date and
                        t.status == TransactionStatus.COMPLETED)]
        
        total_amount = sum(t.total_amount for t in purchases)
        total_quantity = sum(t.quantity_kg for t in purchases)
        
        return {
            'total_purchases': len(purchases),
            'total_amount': total_amount,
            'total_quantity_kg': total_quantity,
            'average_rate_per_kg': total_amount / total_quantity if total_quantity > 0 else 0,
            'period_start': start_date,
            'period_end': end_date
        }
    
    def export_transactions(self, transaction_type: Optional[TransactionType] = None) -> Dict[str, Any]:
        """Export transaction data"""
        transactions_to_export = self.transactions.values()
        
        if transaction_type:
            transactions_to_export = [t for t in transactions_to_export if t.transaction_type == transaction_type]
        
        return {
            'transactions': [t.to_dict() for t in transactions_to_export],
            'total_transactions': len(transactions_to_export),
            'export_date': datetime.now().isoformat(),
            'transaction_type_filter': transaction_type.value if transaction_type else 'all'
        }
    
    def to_dataframe(self, transaction_type: Optional[TransactionType] = None):
        """Convert transactions to pandas DataFrame"""
        import pandas as pd
        
        transactions_to_convert = self.transactions.values()
        
        if transaction_type:
            transactions_to_convert = [t for t in transactions_to_convert if t.transaction_type == transaction_type]
        
        data = [t.to_dict() for t in transactions_to_convert]
        return pd.DataFrame(data)