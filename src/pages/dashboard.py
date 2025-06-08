"""
Dashboard Page - Main overview and analytics
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import config
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
    except Exception as