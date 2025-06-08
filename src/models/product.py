"""
Product Data Model - Defines product structure and operations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import config

@dataclass
class Product:
    """Product data model"""
    
    product_id: str
    name: str
    weight_kg: float
    pouch_size: str
    fnsku: str
    unit_price: float
    description: str = ""
    category: str = "Roasted Chana"
    is_active: bool = True
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate product data after initialization"""
        if self.weight_kg <= 0:
            raise ValueError("Weight must be positive")
        
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
        
        if not self.name.strip():
            raise ValueError("Product name cannot be empty")
    
    @property
    def display_name(self) -> str:
        """Get display name for the product"""
        return f"{self.name} {self.weight_kg}kg"
    
    @property
    def is_valid_weight(self) -> bool:
        """Check if weight is in valid product weights"""
        return self.weight_kg in config.PRODUCT_WEIGHTS
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'weight_kg': self.weight_kg,
            'pouch_size': self.pouch_size,
            'fnsku': self.fnsku,
            'unit_price': self.unit_price,
            'description': self.description,
            'category': self.category,
            'is_active': self.is_active,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create product from dictionary"""
        # Handle datetime fields
        if isinstance(data.get('created_date'), str):
            data['created_date'] = datetime.fromisoformat(data['created_date'])
        
        if isinstance(data.get('updated_date'), str):
            data['updated_date'] = datetime.fromisoformat(data['updated_date'])
        
        return cls(**data)
    
    def update_price(self, new_price: float) -> None:
        """Update product price"""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        
        self.unit_price = new_price
        self.updated_date = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the product"""
        self.is_active = False
        self.updated_date = datetime.now()
    
    def activate(self) -> None:
        """Activate the product"""
        self.is_active = True
        self.updated_date = datetime.now()

class ProductCatalog:
    """Manages a collection of products"""
    
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self._load_default_products()
    
    def _load_default_products(self):
        """Load default products from configuration"""
        for weight in config.PRODUCT_WEIGHTS:
            details = config.PRODUCT_DETAILS.get(weight, {})
            
            product = Product(
                product_id=f"RC_{weight}KG",
                name="Roasted Chana",
                weight_kg=weight,
                pouch_size=details.get('pouch_size', ''),
                fnsku=details.get('fnsku', ''),
                unit_price=weight * 100,  # Base price of ₹100 per kg
                description=f"Premium roasted chana {weight}kg pack"
            )
            
            self.products[product.product_id] = product
    
    def add_product(self, product: Product) -> bool:
        """Add a new product to catalog"""
        if product.product_id in self.products:
            return False
        
        self.products[product.product_id] = product
        return True
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self.products.get(product_id)
    
    def get_product_by_weight(self, weight: float) -> Optional[Product]:
        """Get product by weight"""
        for product in self.products.values():
            if product.weight_kg == weight:
                return product
        return None
    
    def update_product(self, product_id: str, updates: Dict[str, Any]) -> bool:
        """Update product details"""
        if product_id not in self.products:
            return False
        
        product = self.products[product_id]
        
        for key, value in updates.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        product.updated_date = datetime.now()
        return True
    
    def remove_product(self, product_id: str) -> bool:
        """Remove product from catalog"""
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
    
    def get_active_products(self) -> List[Product]:
        """Get all active products"""
        return [p for p in self.products.values() if p.is_active]
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return [p for p in self.products.values() if p.category == category]
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description"""
        query = query.lower()
        results = []
        
        for product in self.products.values():
            if (query in product.name.lower() or 
                query in product.description.lower() or
                query in str(product.weight_kg)):
                results.append(product)
        
        return results
    
    def get_product_weights(self) -> List[float]:
        """Get all available product weights"""
        return sorted(list(set(p.weight_kg for p in self.products.values())))
    
    def to_dataframe(self):
        """Convert catalog to pandas DataFrame"""
        import pandas as pd
        
        data = [product.to_dict() for product in self.products.values()]
        return pd.DataFrame(data)
    
    def export_catalog(self) -> Dict[str, Any]:
        """Export entire catalog"""
        return {
            'products': [product.to_dict() for product in self.products.values()],
            'total_products': len(self.products),
            'export_date': datetime.now().isoformat()
        }
    
    def import_catalog(self, catalog_data: Dict[str, Any]) -> bool:
        """Import catalog data"""
        try:
            products_data = catalog_data.get('products', [])
            
            for product_data in products_data:
                product = Product.from_dict(product_data)
                self.products[product.product_id] = product
            
            return True
            
        except Exception:
            return False