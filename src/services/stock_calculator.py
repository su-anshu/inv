"""
Stock Calculator Service - Handles stock calculations and business logic
"""

import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Tuple
import config
import logging

class StockCalculator:
    """Service class for stock calculations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.product_weights = config.PRODUCT_WEIGHTS
        self.min_stock_threshold = config.MIN_STOCK_THRESHOLD
        self.critical_stock_threshold = config.CRITICAL_STOCK_THRESHOLD
    
    def calculate_stock_summary(self, stock_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive stock summary"""
        try:
            if stock_data is None or stock_data.empty:
                return self._get_empty_summary()
            
            summary = {
                'total_products': len(stock_data),
                'total_stock_units': 0,
                'total_stock_value': 0,
                'low_stock_items': 0,
                'critical_stock_items': 0,
                'overstocked_items': 0,
                'out_of_stock_items': 0,
                'average_stock_level': 0,
                'stock_turnover_ratio': 0,
                'reorder_recommendations': [],
                'product_breakdown': []
            }
            
            # Calculate basic metrics
            if 'current_stock' in stock_data.columns:
                summary['total_stock_units'] = stock_data['current_stock'].sum()
                summary['average_stock_level'] = stock_data['current_stock'].mean()
                summary['out_of_stock_items'] = len(stock_data[stock_data['current_stock'] == 0])
            
            # Calculate stock value
            if 'stock_value' in stock_data.columns:
                summary['total_stock_value'] = stock_data['stock_value'].sum()
            elif 'current_stock' in stock_data.columns and 'unit_price' in stock_data.columns:
                stock_data['calculated_value'] = stock_data['current_stock'] * stock_data['unit_price']
                summary['total_stock_value'] = stock_data['calculated_value'].sum()
            
            # Calculate stock status items
            if 'current_stock' in stock_data.columns and 'min_stock' in stock_data.columns:
                summary['low_stock_items'] = len(
                    stock_data[stock_data['current_stock'] < stock_data['min_stock']]
                )
                summary['critical_stock_items'] = len(
                    stock_data[stock_data['current_stock'] < self.critical_stock_threshold]
                )
            
            if 'current_stock' in stock_data.columns and 'max_stock' in stock_data.columns:
                summary['overstocked_items'] = len(
                    stock_data[stock_data['current_stock'] > stock_data['max_stock']]
                )
            
            # Generate reorder recommendations
            summary['reorder_recommendations'] = self._generate_reorder_recommendations(stock_data)
            
            # Product breakdown
            summary['product_breakdown'] = self._calculate_product_breakdown(stock_data)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error calculating stock summary: {str(e)}")
            return self._get_empty_summary()
    
    def calculate_stock_valuation(self, stock_data: pd.DataFrame, method: str = 'current') -> Dict[str, float]:
        """Calculate stock valuation using different methods"""
        try:
            if stock_data is None or stock_data.empty:
                return {'total_value': 0, 'average_value_per_unit': 0}
            
            valuation = {'total_value': 0, 'average_value_per_unit': 0, 'method': method}
            
            if method == 'current':
                # Use current stock and unit prices
                if 'current_stock' in stock_data.columns and 'unit_price' in stock_data.columns:
                    stock_data['value'] = stock_data['current_stock'] * stock_data['unit_price']
                    valuation['total_value'] = stock_data['value'].sum()
                    total_units = stock_data['current_stock'].sum()
                    if total_units > 0:
                        valuation['average_value_per_unit'] = valuation['total_value'] / total_units
            
            elif method == 'fifo':
                # First In, First Out valuation (simplified)
                valuation = self._calculate_fifo_valuation(stock_data)
            
            elif method == 'weighted_average':
                # Weighted average cost
                valuation = self._calculate_weighted_average_valuation(stock_data)
            
            return valuation
            
        except Exception as e:
            self.logger.error(f"Error calculating stock valuation: {str(e)}")
            return {'total_value': 0, 'average_value_per_unit': 0, 'error': str(e)}
    
    def calculate_reorder_points(self, stock_data: pd.DataFrame, sales_data: Optional[pd.DataFrame] = None) -> Dict[str, Dict[str, float]]:
        """Calculate optimal reorder points for each product"""
        try:
            reorder_points = {}
            
            for _, row in stock_data.iterrows():
                product = row.get('product_name', row.get('product', 'Unknown'))
                current_stock = row.get('current_stock', 0)
                min_stock = row.get('min_stock', self.min_stock_threshold)
                
                # Basic reorder point calculation
                reorder_point = {
                    'current_stock': current_stock,
                    'min_stock': min_stock,
                    'recommended_reorder_point': min_stock * 1.5,  # Safety buffer
                    'recommended_order_quantity': 0,
                    'days_of_stock_remaining': 0,
                    'reorder_urgency': 'low'
                }
                
                # Calculate based on sales velocity if sales data available
                if sales_data is not None:
                    velocity = self._calculate_sales_velocity(product, sales_data)
                    if velocity > 0:
                        reorder_point['days_of_stock_remaining'] = current_stock / velocity
                        reorder_point['recommended_order_quantity'] = velocity * 30  # 30 days supply
                        
                        # Determine urgency
                        if current_stock <= self.critical_stock_threshold:
                            reorder_point['reorder_urgency'] = 'critical'
                        elif current_stock <= min_stock:
                            reorder_point['reorder_urgency'] = 'high'
                        elif reorder_point['days_of_stock_remaining'] <= 7:
                            reorder_point['reorder_urgency'] = 'medium'
                
                reorder_points[product] = reorder_point
            
            return reorder_points
            
        except Exception as e:
            self.logger.error(f"Error calculating reorder points: {str(e)}")
            return {}
    
    def calculate_stock_turnover(self, stock_data: pd.DataFrame, sales_data: Optional[pd.DataFrame] = None, period_days: int = 30) -> Dict[str, float]:
        """Calculate stock turnover ratios"""
        try:
            if sales_data is None or sales_data.empty:
                return {}
            
            turnover_data = {}
            
            for _, row in stock_data.iterrows():
                product = row.get('product_name', row.get('product', 'Unknown'))
                avg_stock = row.get('current_stock', 0)
                
                # Calculate sales for the period
                product_sales = sales_data[sales_data['product'] == product]['quantity'].sum() if 'product' in sales_data.columns else 0
                
                # Calculate turnover ratio
                if avg_stock > 0:
                    turnover_ratio = product_sales / avg_stock
                    days_to_sell = period_days / turnover_ratio if turnover_ratio > 0 else float('inf')
                else:
                    turnover_ratio = 0
                    days_to_sell = float('inf')
                
                turnover_data[product] = {
                    'turnover_ratio': turnover_ratio,
                    'days_to_sell_current_stock': days_to_sell,
                    'sales_in_period': product_sales,
                    'average_stock': avg_stock
                }
            
            return turnover_data
            
        except Exception as e:
            self.logger.error(f"Error calculating stock turnover: {str(e)}")
            return {}
    
    def calculate_abc_analysis(self, stock_data: pd.DataFrame, sales_data: Optional[pd.DataFrame] = None) -> Dict[str, Dict[str, Any]]:
        """Perform ABC analysis on inventory"""
        try:
            if sales_data is None or stock_data.empty:
                return {}
            
            # Calculate revenue for each product
            product_revenue = {}
            
            for _, row in stock_data.iterrows():
                product = row.get('product_name', row.get('product', 'Unknown'))
                
                # Calculate revenue from sales data
                if 'product' in sales_data.columns and 'total_amount' in sales_data.columns:
                    revenue = sales_data[sales_data['product'] == product]['total_amount'].sum()
                else:
                    # Fallback to stock value
                    revenue = row.get('stock_value', 0)
                
                product_revenue[product] = revenue
            
            # Sort by revenue
            sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
            total_revenue = sum(product_revenue.values())
            
            # Classify into A, B, C categories
            abc_analysis = {}
            cumulative_revenue = 0
            
            for i, (product, revenue) in enumerate(sorted_products):
                cumulative_revenue += revenue
                cumulative_percentage = (cumulative_revenue / total_revenue) * 100 if total_revenue > 0 else 0
                
                # ABC classification
                if cumulative_percentage <= 80:
                    category = 'A'
                elif cumulative_percentage <= 95:
                    category = 'B'
                else:
                    category = 'C'
                
                abc_analysis[product] = {
                    'category': category,
                    'revenue': revenue,
                    'revenue_percentage': (revenue / total_revenue) * 100 if total_revenue > 0 else 0,
                    'cumulative_percentage': cumulative_percentage,
                    'rank': i + 1
                }
            
            return abc_analysis
            
        except Exception as e:
            self.logger.error(f"Error performing ABC analysis: {str(e)}")
            return {}
    
    def calculate_safety_stock(self, product: str, sales_data: Optional[pd.DataFrame] = None, service_level: float = 0.95) -> float:
        """Calculate safety stock for a product"""
        try:
            if sales_data is None or sales_data.empty:
                return self.min_stock_threshold
            
            # Get sales data for the product
            product_sales = sales_data[sales_data['product'] == product] if 'product' in sales_data.columns else pd.DataFrame()
            
            if product_sales.empty:
                return self.min_stock_threshold
            
            # Calculate demand variability
            daily_demand = product_sales.groupby('date')['quantity'].sum() if 'date' in product_sales.columns else product_sales['quantity']
            
            if len(daily_demand) < 2:
                return self.min_stock_threshold
            
            # Calculate standard deviation of demand
            demand_std = daily_demand.std()
            avg_demand = daily_demand.mean()
            
            # Assume lead time of 7 days (configurable)
            lead_time = 7
            
            # Z-score for service level (95% = 1.65, 99% = 2.33)
            z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
            z_score = z_scores.get(service_level, 1.65)
            
            # Safety stock formula: Z * sqrt(lead_time) * demand_std
            safety_stock = z_score * (lead_time ** 0.5) * demand_std
            
            return max(safety_stock, self.min_stock_threshold)
            
        except Exception as e:
            self.logger.error(f"Error calculating safety stock: {str(e)}")
            return self.min_stock_threshold
    
    def _get_empty_summary(self) -> Dict[str, Any]:
        """Return empty summary structure"""
        return {
            'total_products': 0,
            'total_stock_units': 0,
            'total_stock_value': 0,
            'low_stock_items': 0,
            'critical_stock_items': 0,
            'overstocked_items': 0,
            'out_of_stock_items': 0,
            'average_stock_level': 0,
            'stock_turnover_ratio': 0,
            'reorder_recommendations': [],
            'product_breakdown': []
        }
    
    def _generate_reorder_recommendations(self, stock_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate reorder recommendations"""
        recommendations = []
        
        try:
            for _, row in stock_data.iterrows():
                current_stock = row.get('current_stock', 0)
                min_stock = row.get('min_stock', self.min_stock_threshold)
                product = row.get('product_name', row.get('product', 'Unknown'))
                
                if current_stock <= self.critical_stock_threshold:
                    urgency = 'Critical'
                    action = 'Immediate reorder required'
                elif current_stock <= min_stock:
                    urgency = 'High'
                    action = 'Reorder soon'
                elif current_stock <= min_stock * 1.5:
                    urgency = 'Medium'
                    action = 'Plan reorder'
                else:
                    continue
                
                recommendations.append({
                    'product': product,
                    'current_stock': current_stock,
                    'min_stock': min_stock,
                    'urgency': urgency,
                    'action': action,
                    'recommended_quantity': max(min_stock * 2 - current_stock, min_stock)
                })
        
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
        
        return recommendations
    
    def _calculate_product_breakdown(self, stock_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Calculate breakdown by product"""
        breakdown = []
        
        try:
            for _, row in stock_data.iterrows():
                product = row.get('product_name', row.get('product', 'Unknown'))
                current_stock = row.get('current_stock', 0)
                stock_value = row.get('stock_value', 0)
                
                if 'unit_price' in row and stock_value == 0:
                    stock_value = current_stock * row['unit_price']
                
                breakdown.append({
                    'product': product,
                    'current_stock': current_stock,
                    'stock_value': stock_value,
                    'percentage_of_total': 0  # Will be calculated after all products
                })
        
        except Exception as e:
            self.logger.error(f"Error calculating breakdown: {str(e)}")
        
        return breakdown
    
    def _calculate_sales_velocity(self, product: str, sales_data: pd.DataFrame) -> float:
        """Calculate average daily sales velocity for a product"""
        try:
            product_sales = sales_data[sales_data['product'] == product] if 'product' in sales_data.columns else pd.DataFrame()
            
            if product_sales.empty:
                return 0
            
            # Calculate total quantity sold
            total_quantity = product_sales['quantity'].sum() if 'quantity' in product_sales.columns else 0
            
            # Calculate number of days in the data
            if 'date' in product_sales.columns:
                date_range = (product_sales['date'].max() - product_sales['date'].min()).days
                days = max(date_range, 1)
            else:
                days = 30  # Default assumption
            
            return total_quantity / days
            
        except Exception as e:
            self.logger.error(f"Error calculating sales velocity: {str(e)}")
            return 0
    
    def _calculate_fifo_valuation(self, stock_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate FIFO valuation (simplified)"""
        # This is a simplified FIFO - in reality you'd need purchase history
        return {'total_value': 0, 'average_value_per_unit': 0, 'method': 'fifo'}
    
    def _calculate_weighted_average_valuation(self, stock_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate weighted average valuation"""
        try:
            if 'current_stock' in stock_data.columns and 'unit_price' in stock_data.columns:
                total_value = (stock_data['current_stock'] * stock_data['unit_price']).sum()
                total_units = stock_data['current_stock'].sum()
                
                avg_value_per_unit = total_value / total_units if total_units > 0 else 0
                
                return {
                    'total_value': total_value,
                    'average_value_per_unit': avg_value_per_unit,
                    'method': 'weighted_average'
                }
            
            return {'total_value': 0, 'average_value_per_unit': 0, 'method': 'weighted_average'}
            
        except Exception as e:
            self.logger.error(f"Error calculating weighted average valuation: {str(e)}")
            return {'total_value': 0, 'average_value_per_unit': 0, 'method': 'weighted_average'}