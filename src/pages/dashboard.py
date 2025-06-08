"""
Dashboard Page - Main overview and analytics
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import config
# At the top of src/pages/dashboard.py, add:
from src.models import Product, ProductCatalog
from src.services.excel_service import ExcelService
from src.components.dashboard_widgets import (
    create_kpi_cards,
    create_stock_levels_chart,
    create_sales_trend_chart,
    create_channel_performance_chart,
    create_revenue_chart,
    create_inventory_value_chart,
    create_low_stock_alerts,
    create_recent_activity_table,
    create_stock_value_breakdown,
    create_performance_summary,
    create_sample_stock_data,
    create_sample_sales_data,
    create_sample_channel_data
)

def show_dashboard():
    """Display the main dashboard with KPIs and charts"""
    
    st.header("📊 Live Dashboard")
    st.markdown("Real-time overview of your inventory operations")
    
    # Auto-refresh option
    col1, col2, col3 = st.columns([6, 1, 1])
    with col2:
        auto_refresh = st.checkbox("Auto Refresh", value=False)
    with col3:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    if auto_refresh:
        # Auto refresh every 30 seconds
        st.rerun()
    
    # Load data
    try:
        excel_service = ExcelService()
        dashboard_data = load_dashboard_data(excel_service)
    except Exception as e:
        st.warning(f"⚠️ Using sample data. Error: {str(e)}")
        dashboard_data = load_sample_data()
    
    # Top KPI metrics
    st.subheader("📈 Key Performance Indicators")
    create_kpi_cards(dashboard_data['kpis'])
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Stock Analysis")
        
        # Stock levels chart
        fig_stock = create_stock_levels_chart(dashboard_data['stock'])
        st.plotly_chart(fig_stock, use_container_width=True)
        
        # Inventory value chart
        fig_value = create_inventory_value_chart(dashboard_data['stock'])
        st.plotly_chart(fig_value, use_container_width=True)
    
    with col2:
        st.subheader("📈 Sales Analysis")
        
        # Sales trend chart
        fig_sales = create_sales_trend_chart(dashboard_data['sales'])
        st.plotly_chart(fig_sales, use_container_width=True)
        
        # Channel performance chart
        fig_channel = create_channel_performance_chart(dashboard_data['channels'])
        st.plotly_chart(fig_channel, use_container_width=True)
    
    st.markdown("---")
    
    # Additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Revenue Analysis")
        fig_revenue = create_revenue_chart(dashboard_data['sales'])
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        st.subheader("📊 Performance Summary")
        create_performance_summary()
    
    st.markdown("---")
    
    # Alerts and recent activity
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚠️ Stock Alerts")
        create_low_stock_alerts(dashboard_data['stock'])
        
        st.markdown("---")
        create_stock_value_breakdown(dashboard_data['stock'])
    
    with col2:
        st.subheader("🕒 Recent Activity")
        create_recent_activity_table()
    
    # Footer with last update time
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        last_update = st.session_state.get('last_update', 'Never')
        st.markdown(
            f"<div style='text-align: center; color: #666;'>"
            f"Last Updated: {last_update} | "
            f"Data as of: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            f"</div>",
            unsafe_allow_html=True
        )

def load_dashboard_data(excel_service):
    """Load real data from Excel service"""
    
    try:
        # Try to load real data
        stock_data = excel_service.read_stock_data()
        
        if stock_data is not None and not stock_data.empty:
            # Process real stock data
            processed_stock = process_stock_data(stock_data)
            
            # Calculate KPIs from real data
            kpis = calculate_kpis(processed_stock)
            
            # For now, use sample sales and channel data
            # In a real implementation, you'd load this from Excel too
            sales_data = create_sample_sales_data()
            channel_data = create_sample_channel_data()
            
            return {
                'stock': processed_stock,
                'sales': sales_data,
                'channels': channel_data,
                'kpis': kpis
            }
        else:
            # If no real data available, return sample data
            return load_sample_data()
            
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
        # Return sample data as fallback
        return load_sample_data()

def load_sample_data():
    """Load sample data when real data is not available"""
    try:
        return {
            'stock': create_sample_stock_data(),
            'sales': create_sample_sales_data(),
            'channels': create_sample_channel_data(),
            'kpis': {
                'total_products': 150,
                'total_value': 250000,
                'low_stock_items': 8,
                'monthly_sales': 45000
            }
        }
    except Exception as e:
        st.error(f"Error creating sample data: {str(e)}")
        # Return minimal fallback data
        return {
            'stock': pd.DataFrame(),
            'sales': pd.DataFrame(),
            'channels': pd.DataFrame(),
            'kpis': {
                'total_products': 0,
                'total_value': 0,
                'low_stock_items': 0,
                'monthly_sales': 0
            }
        }

def process_stock_data(stock_data):
    """Process raw stock data for dashboard display"""
    try:
        # Ensure required columns exist
        required_columns = ['product_name', 'quantity', 'price', 'category']
        
        # Add missing columns with default values if they don't exist
        for col in required_columns:
            if col not in stock_data.columns:
                if col == 'quantity':
                    stock_data[col] = 0
                elif col == 'price':
                    stock_data[col] = 0.0
                elif col == 'category':
                    stock_data[col] = 'Uncategorized'
                elif col == 'product_name':
                    stock_data[col] = f"Product_{stock_data.index}"
        
        # Calculate total value for each product
        stock_data['total_value'] = stock_data['quantity'] * stock_data['price']
        
        # Add reorder level if not present
        if 'reorder_level' not in stock_data.columns:
            stock_data['reorder_level'] = 10  # Default reorder level
        
        # Add low stock indicator
        stock_data['low_stock'] = stock_data['quantity'] < stock_data['reorder_level']
        
        return stock_data
        
    except Exception as e:
        st.error(f"Error processing stock data: {str(e)}")
        return stock_data

def calculate_kpis(stock_data):
    """Calculate KPIs from stock data"""
    try:
        # Total products
        total_products = len(stock_data) if not stock_data.empty else 0
        
        # Total inventory value
        if 'total_value' in stock_data.columns:
            total_value = stock_data['total_value'].sum()
        elif 'quantity' in stock_data.columns and 'price' in stock_data.columns:
            total_value = (stock_data['quantity'] * stock_data['price']).sum()
        else:
            total_value = 0
        
        # Low stock items
        if 'quantity' in stock_data.columns and 'reorder_level' in stock_data.columns:
            low_stock_items = len(stock_data[stock_data['quantity'] < stock_data['reorder_level']])
        elif 'low_stock' in stock_data.columns:
            low_stock_items = stock_data['low_stock'].sum()
        else:
            low_stock_items = 0
        
        # Monthly sales (placeholder - would come from sales data in real implementation)
        monthly_sales = 45000
        
        return {
            'total_products': int(total_products),
            'total_value': float(total_value),
            'low_stock_items': int(low_stock_items),
            'monthly_sales': float(monthly_sales)
        }
        
    except Exception as e:
        st.error(f"Error calculating KPIs: {str(e)}")
        return {
            'total_products': 0,
            'total_value': 0.0,
            'low_stock_items': 0,
            'monthly_sales': 0.0
        }

def update_session_state():
    """Update session state with current timestamp"""
    st.session_state['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Call update function when module is loaded
if __name__ == "__main__":
    update_session_state()