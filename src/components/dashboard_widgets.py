"""
Dashboard Widgets - Reusable dashboard components and charts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import config

def create_kpi_cards(data):
    """Create KPI metric cards"""
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_stock_value = data.get('total_stock_value', 0)
        st.metric(
            label="💰 Total Stock Value",
            value=f"₹{total_stock_value:,.0f}",
            delta=f"₹{np.random.randint(1000, 5000):,}"
        )
    
    with col2:
        total_products = len(config.PRODUCT_WEIGHTS)
        st.metric(
            label="📦 Total Products",
            value=total_products,
            delta="0"
        )
    
    with col3:
        low_stock_count = data.get('low_stock_count', 0)
        st.metric(
            label="⚠️ Low Stock Items",
            value=low_stock_count,
            delta=f"{np.random.randint(-2, 1)}"
        )
    
    with col4:
        today_sales = data.get('today_sales', 0)
        st.metric(
            label="📊 Today's Sales",
            value=today_sales,
            delta=f"{np.random.randint(-10, 20)}"
        )
    
    with col5:
        avg_stock = data.get('avg_stock', 0)
        st.metric(
            label="📈 Avg Stock Level",
            value=f"{avg_stock:.0f}",
            delta=f"{np.random.randint(-5, 10)}"
        )

def create_stock_levels_chart(stock_data):
    """Create stock levels bar chart"""
    
    if stock_data is None or stock_data.empty:
        stock_data = create_sample_stock_data()
    
    fig = go.Figure()
    
    # Add current stock bars
    fig.add_trace(go.Bar(
        x=stock_data['Product'],
        y=stock_data['Current_Stock'],
        name='Current Stock',
        marker_color='lightblue',
        text=stock_data['Current_Stock'],
        textposition='auto'
    ))
    
    # Add minimum stock line
    fig.add_trace(go.Scatter(
        x=stock_data['Product'],
        y=stock_data['Min_Stock'],
        mode='lines+markers',
        name='Min Stock Level',
        line=dict(color='red', dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Current Stock Levels vs Minimum Requirements",
        xaxis_title="Products",
        yaxis_title="Quantity",
        height=400,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def create_sales_trend_chart(sales_data):
    """Create sales trend line chart"""
    
    if sales_data is None or sales_data.empty:
        sales_data = create_sample_sales_data()
    
    fig = px.line(
        sales_data,
        x='Date',
        y='Sales',
        title='Daily Sales Trend (Last 30 Days)',
        markers=True,
        line_shape='spline'
    )
    
    # Add trend line
    if len(sales_data) > 1:
        z = np.polyfit(range(len(sales_data)), sales_data['Sales'], 1)
        p = np.poly1d(z)
        
        fig.add_trace(go.Scatter(
            x=sales_data['Date'],
            y=p(range(len(sales_data))),
            mode='lines',
            name='Trend',
            line=dict(dash='dash', color='orange')
        ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Units Sold",
        hovermode='x unified'
    )
    
    return fig

def create_channel_performance_chart(channel_data):
    """Create channel performance pie chart"""
    
    if channel_data is None or channel_data.empty:
        channel_data = create_sample_channel_data()
    
    fig = px.pie(
        channel_data,
        values='Sales',
        names='Channel',
        title='Sales Distribution by Channel',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Sales: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(height=400)
    
    return fig

def create_revenue_chart(sales_data):
    """Create revenue trend chart"""
    
    if sales_data is None or sales_data.empty:
        sales_data = create_sample_sales_data()
    
    fig = go.Figure()
    
    # Revenue bars
    fig.add_trace(go.Bar(
        x=sales_data['Date'],
        y=sales_data['Revenue'],
        name='Daily Revenue',
        marker_color='lightgreen',
        opacity=0.7
    ))
    
    # Moving average line
    window = 7
    if len(sales_data) >= window:
        moving_avg = sales_data['Revenue'].rolling(window=window).mean()
        fig.add_trace(go.Scatter(
            x=sales_data['Date'],
            y=moving_avg,
            mode='lines',
            name=f'{window}-Day Moving Average',
            line=dict(color='darkgreen', width=3)
        ))
    
    fig.update_layout(
        title="Daily Revenue with Moving Average",
        xaxis_title="Date",
        yaxis_title="Revenue (₹)",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_inventory_value_chart(stock_data):
    """Create inventory value breakdown chart"""
    
    if stock_data is None or stock_data.empty:
        stock_data = create_sample_stock_data()
    
    fig = px.bar(
        stock_data,
        x='Product',
        y='Value',
        title='Inventory Value by Product',
        color='Value',
        color_continuous_scale='Blues',
        text='Value'
    )
    
    fig.update_traces(
        texttemplate='₹%{text:,.0f}',
        textposition='auto'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Products",
        yaxis_title="Value (₹)",
        showlegend=False
    )
    
    return fig

def create_low_stock_alerts(stock_data):
    """Create low stock alerts widget"""
    
    if stock_data is None or stock_data.empty:
        stock_data = create_sample_stock_data()
    
    # Find low stock items
    low_stock = stock_data[stock_data['Current_Stock'] < stock_data['Min_Stock']]
    
    # Check for critical stock threshold
    critical_stock_threshold = getattr(config, 'CRITICAL_STOCK_THRESHOLD', 5)
    critical_stock = stock_data[stock_data['Current_Stock'] < critical_stock_threshold]
    
    if not critical_stock.empty:
        st.error(f"🚨 CRITICAL: {len(critical_stock)} items are critically low!")
        for _, item in critical_stock.iterrows():
            st.error(f"🔴 {item['Product']}: {item['Current_Stock']} units (Critical level)")
    
    if not low_stock.empty:
        st.warning(f"⚠️ {len(low_stock)} items are below minimum stock level!")
        for _, item in low_stock.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{item['Product']}**")
            with col2:
                st.write(f"Current: {item['Current_Stock']}")
            with col3:
                st.write(f"Min: {item['Min_Stock']}")
    else:
        st.success("✅ All items are above minimum stock levels!")
    
    return len(low_stock), len(critical_stock)

def create_recent_activity_table():
    """Create recent activity table"""
    
    # Sample recent activities (replace with actual data)
    activities = [
        {"Time": "10:30 AM", "Activity": "Sale recorded", "Details": "5x 1.0kg via Amazon FBA", "Status": "✅"},
        {"Time": "09:15 AM", "Activity": "Stock updated", "Details": "2.0kg stock adjusted +10", "Status": "🔄"},
        {"Time": "08:45 AM", "Activity": "Purchase recorded", "Details": "Raw material 100kg received", "Status": "📦"},
        {"Time": "08:00 AM", "Activity": "Backup created", "Details": "Automatic backup completed", "Status": "💾"},
        {"Time": "Yesterday", "Activity": "Low stock alert", "Details": "0.2kg below minimum level", "Status": "⚠️"}
    ]
    
    activity_df = pd.DataFrame(activities)
    
    # Custom styling for the table
    st.dataframe(
        activity_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn("Status", width=60),
            "Time": st.column_config.TextColumn("Time", width=100),
            "Activity": st.column_config.TextColumn("Activity", width=150),
            "Details": st.column_config.TextColumn("Details", width=300)
        }
    )

def create_stock_value_breakdown(stock_data):
    """Create stock value breakdown widget"""
    
    if stock_data is None or stock_data.empty:
        stock_data = create_sample_stock_data()
    
    st.markdown("### 💰 Stock Value Breakdown")
    
    total_value = stock_data['Value'].sum()
    
    for _, item in stock_data.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{item['Product']}**")
        with col2:
            st.write(f"₹{item['Value']:,}")
        with col3:
            percentage = (item['Value'] / total_value) * 100 if total_value > 0 else 0
            st.write(f"{percentage:.1f}%")
    
    st.markdown(f"**Total Value: ₹{total_value:,}**")

def create_performance_summary():
    """Create performance summary widget"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 This Week")
        st.metric("Sales", "245", "↗️ 15%")
        st.metric("Revenue", "₹24,500", "↗️ 12%")
        st.metric("Orders", "89", "↗️ 8%")
    
    with col2:
        st.markdown("### 📊 This Month")
        st.metric("Sales", "1,045", "↗️ 22%")
        st.metric("Revenue", "₹1,04,500", "↗️ 18%")
        st.metric("Orders", "378", "↗️ 15%")

def create_sample_stock_data():
    """Create sample stock data for testing - FIXED ARRAY LENGTHS"""
    try:
        # Ensure all arrays have the same length as PRODUCT_WEIGHTS
        num_products = len(config.PRODUCT_WEIGHTS)
        
        # Base data - extend or trim to match num_products
        current_stock_base = [45, 120, 85, 30, 95]
        min_stock_base = [50, 100, 80, 40, 80]
        value_base = [2250, 12000, 8500, 4500, 19000]
        
        # Ensure arrays match length
        current_stock = (current_stock_base * ((num_products // len(current_stock_base)) + 1))[:num_products]
        min_stock = (min_stock_base * ((num_products // len(min_stock_base)) + 1))[:num_products]
        value = (value_base * ((num_products // len(value_base)) + 1))[:num_products]
        
        return pd.DataFrame({
            'Product': [f'{w}kg' for w in config.PRODUCT_WEIGHTS],
            'Current_Stock': current_stock,
            'Min_Stock': min_stock,
            'Value': value
        })
    except Exception as e:
        # Fallback minimal data
        return pd.DataFrame({
            'Product': ['1.0kg'],
            'Current_Stock': [100],
            'Min_Stock': [50],
            'Value': [5000]
        })

def create_sample_sales_data():
    """Create sample sales data for testing - FIXED ARRAY LENGTHS"""
    try:
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        num_days = len(dates)
        
        return pd.DataFrame({
            'Date': dates,
            'Sales': np.random.randint(20, 100, num_days),
            'Revenue': np.random.randint(2000, 10000, num_days)
        })
    except Exception as e:
        # Fallback minimal data
        return pd.DataFrame({
            'Date': [datetime.now()],
            'Sales': [50],
            'Revenue': [5000]
        })

def create_sample_channel_data():
    """Create sample channel data for testing - FIXED ARRAY LENGTHS"""
    try:
        # Use only the first few channels to ensure data matches
        channels = config.SALES_CHANNELS[:4]  # Take first 4 channels
        num_channels = len(channels)
        
        # Generate matching data
        sales_base = [450, 280, 320, 150]
        revenue_base = [45000, 28000, 32000, 15000]
        
        # Ensure arrays match channel length
        sales = (sales_base * ((num_channels // len(sales_base)) + 1))[:num_channels]
        revenue = (revenue_base * ((num_channels // len(revenue_base)) + 1))[:num_channels]
        
        return pd.DataFrame({
            'Channel': channels,
            'Sales': sales,
            'Revenue': revenue
        })
    except Exception as e:
        # Fallback minimal data
        return pd.DataFrame({
            'Channel': ['Others'],
            'Sales': [300],
            'Revenue': [30000]
        })

# Additional helper functions for compatibility

def create_stock_sample_data():
    """Compatibility function"""
    return create_sample_stock_data()

def create_sales_sample_data():
    """Compatibility function"""
    return create_sample_sales_data()

def create_channel_sample_data():
    """Compatibility function"""
    return create_sample_channel_data()