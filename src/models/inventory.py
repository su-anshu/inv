"""
Inventory Data Model - Defines inventory structure and operations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from enum import Enum
import config

class StockStatus(Enum):
    """Inventory stock status enumeration"""
    OUT_OF_STOCK = "out_of_stock"
    CRITICAL = "critical"
    LOW = "low"
    NORMAL = "normal"
    OVERSTOCKED = "overstocked"

@dataclass
class InventoryItem:
    """Individual inventory item model"""
    
    product_id: str
    product_name: str
    weight_kg: float
    current_stock: int
    opening_stock: int = 0
    min_stock: int = 10
    max_stock: int = 1000
    unit_price: float = 0.0
    location: str = "Main Warehouse"
    batch_number: str = ""
    expiry_date: Optional[date] = None
    last_updated: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate inventory item after initialization"""
        if self.current_stock < 0:
            raise ValueError("Current stock cannot be negative")
        
        if self.min_stock < 0:
            raise ValueError("Minimum stock cannot be negative")
        
        if self.max_stock < self.min_stock:
            raise ValueError("Maximum stock cannot be less than minimum stock")
    
    @property
    def stock_status(self) -> StockStatus:
        """Determine current stock status"""
        if self.current_stock == 0:
            return StockStatus.OUT_OF_STOCK
        elif self.current_stock <= config.CRITICAL_STOCK_THRESHOLD:
            return StockStatus.CRITICAL
        elif self.current_stock <= self.min_stock:
            return StockStatus.LOW
        elif self.current_stock >= self.max_stock:
            return StockStatus.OVERSTOCKED
        else:
            return StockStatus.NORMAL
    
    @property
    def stock_value(self) -> float:
        """Calculate total stock value"""
        return self.current_stock * self.unit_price
    
    @property
    def days_until_expiry(self) -> Optional[int]:
        """Calculate days until expiry"""
        if self.expiry_date:
            delta = self.expiry_date - date.today()
            return delta.days
        return None
    
    @property
    def is_expired(self) -> bool:
        """Check if item is expired"""
        if self.expiry_date:
            return self.expiry_date < date.today()
        return False
    
    @property
    def reorder_quantity(self) -> int:
        """Calculate recommended reorder quantity"""
        return max(self.max_stock - self.current_stock, 0)
    
    def adjust_stock(self, quantity: int, reason: str = "Manual adjustment") -> bool:
        """Adjust stock quantity"""
        new_stock = self.current_stock + quantity
        
        if new_stock < 0:
            return False
        
        self.current_stock = new_stock
        self.last_updated = datetime.now()
        return True
    
    def set_stock_level(self, new_level: int, reason: str = "Stock update") -> bool:
        """Set absolute stock level"""
        if new_level < 0:
            return False
        
        self.current_stock = new_level
        self.last_updated = datetime.now()
        return True
    
    def reduce_stock(self, quantity: int) -> bool:
        """Reduce stock (for sales)"""
        if self.current_stock >= quantity:
            self.current_stock -= quantity
            self.last_updated = datetime.now()
            return True
        return False
    
    def add_stock(self, quantity: int) -> bool:
        """Add stock (for purchases/production)"""
        self.current_stock += quantity
        self.last_updated = datetime.now()
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'weight_kg': self.weight_kg,
            'current_stock': self.current_stock,
            'opening_stock': self.opening_stock,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'unit_price': self.unit_price,
            'stock_value': self.stock_value,
            'stock_status': self.stock_status.value,
            'location': self.location,
            'batch_number': self.batch_number,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'days_until_expiry': self.days_until_expiry,
            'is_expired': self.is_expired,
            'reorder_quantity': self.reorder_quantity,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryItem':
        """Create from dictionary"""
        # Handle date fields
        if data.get('expiry_date'):
            data['expiry_date'] = date.fromisoformat(data['expiry_date'])
        
        if isinstance(data.get('last_updated'), str):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        
        # Remove calculated fields
        calculated_fields = ['stock_value', 'stock_status', 'days_until_expiry', 'is_expired', 'reorder_quantity']
        for field in calculated_fields:
            data.pop(field, None)
        
        return cls(**data)

class Inventory:
    """Manages collection of inventory items"""
    
    def __init__(self):
        self.items: Dict[str, InventoryItem] = {}
        self._load_default_inventory()
    
    def _load_default_inventory(self):
        """Load default inventory items"""
        for weight in config.PRODUCT_WEIGHTS:
            product_id = f"RC_{weight}KG"
            
            item = InventoryItem(
                product_id=product_id,
                product_name=f"Roasted Chana {weight}kg",
                weight_kg=weight,
                current_stock=100,  # Default stock
                opening_stock=100,
                min_stock=config.MIN_STOCK_THRESHOLD,
                max_stock=config.MAX_STOCK_LIMIT // 10,  # Reasonable max
                unit_price=weight * 100,  # ₹100 per kg
                location="Main Warehouse"
            )
            
            self.items[product_id] = item
    
    def add_item(self, item: InventoryItem) -> bool:
        """Add inventory item"""
        if item.product_id in self.items:
            return False
        
        self.items[item.product_id] = item
        return True
    
    def get_item(self, product_id: str) -> Optional[InventoryItem]:
        """Get inventory item by product ID"""
        return self.items.get(product_id)
    
    def get_item_by_weight(self, weight: float) -> Optional[InventoryItem]:
        """Get inventory item by weight"""
        for item in self.items.values():
            if item.weight_kg == weight:
                return item
        return None
    
    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Update stock level for product"""
        if product_id in self.items:
            return self.items[product_id].set_stock_level(new_stock)
        return False
    
    def adjust_stock(self, product_id: str, quantity: int, reason: str = "Manual adjustment") -> bool:
        """Adjust stock for product"""
        if product_id in self.items:
            return self.items[product_id].adjust_stock(quantity, reason)
        return False
    
    def record_sale(self, product_id: str, quantity: int) -> bool:
        """Record a sale transaction"""
        if product_id in self.items:
            return self.items[product_id].reduce_stock(quantity)
        return False
    
    def record_purchase(self, product_id: str, quantity: int) -> bool:
        """Record a purchase transaction"""
        if product_id in self.items:
            return self.items[product_id].add_stock(quantity)
        return False
    
    def get_low_stock_items(self) -> List[InventoryItem]:
        """Get items with low stock"""
        return [item for item in self.items.values() 
                if item.stock_status in [StockStatus.LOW, StockStatus.CRITICAL, StockStatus.OUT_OF_STOCK]]
    
    def get_overstocked_items(self) -> List[InventoryItem]:
        """Get overstocked items"""
        return [item for item in self.items.values() 
                if item.stock_status == StockStatus.OVERSTOCKED]
    
    def get_expired_items(self) -> List[InventoryItem]:
        """Get expired items"""
        return [item for item in self.items.values() if item.is_expired]
    
    def get_expiring_soon_items(self, days: int = 30) -> List[InventoryItem]:
        """Get items expiring within specified days"""
        return [item for item in self.items.values() 
                if item.days_until_expiry is not None and 0 <= item.days_until_expiry <= days]
    
    def get_reorder_recommendations(self) -> List[Dict[str, Any]]:
        """Get reorder recommendations"""
        recommendations = []
        
        for item in self.items.values():
            if item.stock_status in [StockStatus.LOW, StockStatus.CRITICAL, StockStatus.OUT_OF_STOCK]:
                urgency = "Critical" if item.stock_status == StockStatus.CRITICAL else "High"
                if item.stock_status == StockStatus.OUT_OF_STOCK:
                    urgency = "Emergency"
                
                recommendations.append({
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'current_stock': item.current_stock,
                    'min_stock': item.min_stock,
                    'recommended_quantity': item.reorder_quantity,
                    'urgency': urgency,
                    'stock_status': item.stock_status.value
                })
        
        # Sort by urgency (Emergency > Critical > High)
        urgency_order = {'Emergency': 0, 'Critical': 1, 'High': 2}
        recommendations.sort(key=lambda x: urgency_order.get(x['urgency'], 3))
        
        return recommendations
    
    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get overall inventory summary"""
        total_items = len(self.items)
        total_value = sum(item.stock_value for item in self.items.values())
        total_stock = sum(item.current_stock for item in self.items.values())
        
        status_counts = {}
        for status in StockStatus:
            status_counts[status.value] = len([item for item in self.items.values() 
                                             if item.stock_status == status])
        
        return {
            'total_items': total_items,
            'total_stock_units': total_stock,
            'total_stock_value': total_value,
            'average_stock_value': total_value / total_items if total_items > 0 else 0,
            'status_breakdown': status_counts,
            'low_stock_count': status_counts.get('low', 0) + status_counts.get('critical', 0) + status_counts.get('out_of_stock', 0),
            'reorder_needed': len(self.get_reorder_recommendations()),
            'expired_items': len(self.get_expired_items())
        }
    
    def get_stock_movements(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get stock movement history (placeholder - would need transaction history)"""
        # This is a placeholder - in a real system, you'd track all stock movements
        movements = []
        
        for item in self.items.values():
            # Sample movement data
            movements.append({
                'product_id': item.product_id,
                'product_name': item.product_name,
                'movement_type': 'Sale',
                'quantity': -5,
                'date': datetime.now().date(),
                'reason': 'Customer sale'
            })
        
        return movements
    
    def perform_stock_take(self, actual_counts: Dict[str, int]) -> Dict[str, Any]:
        """Perform stock take and identify variances"""
        variances = []
        adjustments_made = 0
        
        for product_id, actual_count in actual_counts.items():
            if product_id in self.items:
                item = self.items[product_id]
                system_count = item.current_stock
                variance = actual_count - system_count
                
                if variance != 0:
                    variances.append({
                        'product_id': product_id,
                        'product_name': item.product_name,
                        'system_count': system_count,
                        'actual_count': actual_count,
                        'variance': variance,
                        'variance_percentage': (variance / system_count * 100) if system_count > 0 else 0
                    })
                    
                    # Update system with actual count
                    item.set_stock_level(actual_count, "Stock take adjustment")
                    adjustments_made += 1
        
        return {
            'total_items_counted': len(actual_counts),
            'variances_found': len(variances),
            'adjustments_made': adjustments_made,
            'variance_details': variances,
            'stock_take_date': datetime.now().isoformat()
        }
    
    def to_dataframe(self):
        """Convert inventory to pandas DataFrame"""
        import pandas as pd
        
        data = [item.to_dict() for item in self.items.values()]
        return pd.DataFrame(data)
    
    def export_inventory(self) -> Dict[str, Any]:
        """Export inventory data"""
        return {
            'items': [item.to_dict() for item in self.items.values()],
            'summary': self.get_inventory_summary(),
            'export_date': datetime.now().isoformat(),
            'total_items': len(self.items)
        }
    
    def import_inventory(self, inventory_data: Dict[str, Any]) -> bool:
        """Import inventory data"""
        try:
            items_data = inventory_data.get('items', [])
            
            for item_data in items_data:
                item = InventoryItem.from_dict(item_data)
                self.items[item.product_id] = item
            
            return True
            
        except Exception:
            return False
    
    def calculate_inventory_turnover(self, sales_data: List[Dict[str, Any]], period_days: int = 30) -> Dict[str, float]:
        """Calculate inventory turnover ratios"""
        turnover_ratios = {}
        
        for item in self.items.values():
            # Calculate sales for this product in the period
            product_sales = sum(
                sale.get('quantity', 0) 
                for sale in sales_data 
                if sale.get('product_id') == item.product_id
            )
            
            # Calculate turnover ratio
            avg_inventory = (item.opening_stock + item.current_stock) / 2
            
            if avg_inventory > 0:
                turnover_ratio = product_sales / avg_inventory
            else:
                turnover_ratio = 0
            
            turnover_ratios[item.product_id] = {
                'turnover_ratio': turnover_ratio,
                'sales_quantity': product_sales,
                'average_inventory': avg_inventory,
                'days_to_sell': period_days / turnover_ratio if turnover_ratio > 0 else float('inf')
            }
        
        return turnover_ratios