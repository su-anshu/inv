"""
Reports & Analytics Page - Detailed reports and business analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import config
from src.services.excel_service import ExcelService

def show_reports():
    """Display reports and analytics page"""
    
    st.header("📈 Reports & Analytics")
    st.markdown("Detailed business analytics and performance reports")
    
    # Report navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Stock Reports",
        "💰 Sales Analytics", 
        "📦 Purchase Reports",
        "🏭 Production Reports",
        "📋 Custom Reports"
    ])
    
    with tab1:
        show_stock_reports()
    
    with tab2:
        show_sales_analytics()
    
    with tab3:
        show_purchase_reports()
    
    with tab4:
        show_production_reports()
    
    with tab5:
        show_custom_reports()

def show_stock_reports():
    """Stock analysis and reports"""
    
    st.subheader("📊 Stock Analysis")
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Stock overview metrics
    st.markdown("### 📈 Current Stock Overview")
    
    # Sample stock data (replace with real data)
    stock_data = create_stock_sample_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_items = len(stock_data)
        st.metric("Total Products", total_items)
    
    with col2:
        total_stock = stock_data['Current_Stock'].sum()
        st.metric("Total Stock", f"{total_stock:,}")
    
    with col3:
        low_stock_count = len(stock_data[stock_data['Current_Stock'] < stock_data['Min_Stock']])
        st.metric("Low Stock Items", low_stock_count, delta=f"🔴" if low_stock_count > 0 else "✅")
    
    with col4:
        total_value = stock_data['Stock_Value'].sum()
        st.metric("Total Value", f"₹{total_value:,.0f}")
    
    # Stock level charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Current vs Min stock chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=stock_data['Product'],
            y=stock_data['Current_Stock'],
            name='Current Stock',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Scatter(
            x=stock_data['Product'],
            y=stock_data['Min_Stock'],
            mode='lines+markers',
            name='Min Stock Level',
            line=dict(color='red', dash='dash')
        ))
        fig.update_layout(title="Current Stock vs Minimum Levels", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Stock value distribution
        fig = px.pie(
            stock_data,
            values='Stock_Value',
            names='Product',
            title='Stock Value Distribution'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed stock table
    st.markdown("### 📋 Detailed Stock Report")
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Low Stock", "Normal", "Overstocked"])
    with col2:
        product_filter = st.multiselect("Filter by Product", stock_data['Product'].tolist())
    
    # Apply filters
    filtered_data = stock_data.copy()
    
    if status_filter == "Low Stock":
        filtered_data = filtered_data[filtered_data['Current_Stock'] < filtered_data['Min_Stock']]
    elif status_filter == "Normal":
        filtered_data = filtered_data[
            (filtered_data['Current_Stock'] >= filtered_data['Min_Stock']) & 
            (filtered_data['Current_Stock'] <= filtered_data['Max_Stock'])
        ]
    elif status_filter == "Overstocked":
        filtered_data = filtered_data[filtered_data['Current_Stock'] > filtered_data['Max_Stock']]
    
    if product_filter:
        filtered_data = filtered_data[filtered_data['Product'].isin(product_filter)]
    
    # Display table with color coding
    st.dataframe(
        filtered_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Stock_Value": st.column_config.NumberColumn("Stock Value (₹)", format="₹%.0f"),
            "Current_Stock": st.column_config.NumberColumn("Current Stock"),
            "Min_Stock": st.column_config.NumberColumn("Min Stock"),
            "Max_Stock": st.column_config.NumberColumn("Max Stock"),
            "Unit_Price": st.column_config.NumberColumn("Unit Price (₹)", format="₹%.2f")
        }
    )

def show_sales_analytics():
    """Sales analytics and trends"""
    
    st.subheader("💰 Sales Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.selectbox("Date Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year", "Custom"])
    with col2:
        if date_range == "Custom":
            custom_start = st.date_input("Custom Start Date")
        else:
            custom_start = None
    
    # Generate sample sales data
    sales_data = create_sales_sample_data()
    
    # Sales overview metrics
    st.markdown("### 📊 Sales Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = sales_data['Quantity'].sum()
        st.metric("Total Units Sold", f"{total_sales:,}")
    
    with col2:
        total_revenue = sales_data['Revenue'].sum()
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    
    with col3:
        avg_order_value = sales_data['Revenue'].mean()
        st.metric("Avg Order Value", f"₹{avg_order_value:.0f}")
    
    with col4:
        total_orders = len(sales_data)
        st.metric("Total Orders", total_orders)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily sales trend
        daily_sales = sales_data.groupby('Date')['Revenue'].sum().reset_index()
        fig = px.line(daily_sales, x='Date', y='Revenue', title='Daily Sales Revenue Trend')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Product performance
        product_sales = sales_data.groupby('Product')['Quantity'].sum().reset_index()
        fig = px.bar(product_sales, x='Product', y='Quantity', title='Sales by Product')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Channel performance
        channel_sales = sales_data.groupby('Channel')['Revenue'].sum().reset_index()
        fig = px.pie(channel_sales, values='Revenue', names='Channel', title='Revenue by Sales Channel')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly comparison
        monthly_sales = sales_data.groupby(sales_data['Date'].dt.month)['Revenue'].sum().reset_index()
        monthly_sales['Month'] = monthly_sales['Date'].apply(lambda x: f"Month {x}")
        fig = px.bar(monthly_sales, x='Month', y='Revenue', title='Monthly Sales Comparison')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top products table
    st.markdown("### 🏆 Top Performing Products")
    
    top_products = sales_data.groupby('Product').agg({
        'Quantity': 'sum',
        'Revenue': 'sum',
        'Order_ID': 'count'
    }).rename(columns={'Order_ID': 'Orders'}).reset_index()
    
    top_products = top_products.sort_values('Revenue', ascending=False)
    
    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn("Revenue (₹)", format="₹%.0f"),
            "Quantity": st.column_config.NumberColumn("Units Sold"),
            "Orders": st.column_config.NumberColumn("Total Orders")
        }
    )

def show_purchase_reports():
    """Purchase analysis and reports"""
    
    st.subheader("📦 Purchase Reports")
    
    # Generate sample purchase data
    purchase_data = create_purchase_sample_data()
    
    # Purchase overview
    st.markdown("### 📈 Purchase Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_purchases = len(purchase_data)
        st.metric("Total Purchases", total_purchases)
    
    with col2:
        total_quantity = purchase_data['Quantity_KG'].sum()
        st.metric("Total Quantity", f"{total_quantity:.0f} kg")
    
    with col3:
        total_amount = purchase_data['Total_Amount'].sum()
        st.metric("Total Amount", f"₹{total_amount:,.0f}")
    
    with col4:
        avg_rate = purchase_data['Rate_Per_KG'].mean()
        st.metric("Avg Rate/KG", f"₹{avg_rate:.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Purchase trend
        fig = px.line(purchase_data, x='Date', y='Total_Amount', title='Purchase Amount Trend')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Supplier analysis
        supplier_data = purchase_data.groupby('Supplier')['Total_Amount'].sum().reset_index()
        fig = px.bar(supplier_data, x='Supplier', y='Total_Amount', title='Purchase by Supplier')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Purchase details table
    st.markdown("### 📋 Purchase Details")
    
    st.dataframe(
        purchase_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total_Amount": st.column_config.NumberColumn("Total Amount (₹)", format="₹%.0f"),
            "Rate_Per_KG": st.column_config.NumberColumn("Rate/KG (₹)", format="₹%.2f"),
            "Quantity_KG": st.column_config.NumberColumn("Quantity (KG)", format="%.1f kg")
        }
    )

def show_production_reports():
    """Production analysis and reports"""
    
    st.subheader("🏭 Production Reports")
    
    # Generate sample production data
    production_data = create_production_sample_data()
    
    # Production overview
    st.markdown("### 📊 Production Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_batches = len(production_data)
        st.metric("Total Batches", total_batches)
    
    with col2:
        total_output = production_data['Total_Output'].sum()
        st.metric("Total Output", f"{total_output:,} packets")
    
    with col3:
        avg_efficiency = production_data['Efficiency'].mean()
        st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%")
    
    with col4:
        total_raw_material = production_data['Raw_Material_KG'].sum()
        st.metric("Raw Material Used", f"{total_raw_material:.0f} kg")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Production trend
        fig = px.line(production_data, x='Date', y='Total_Output', title='Daily Production Output')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Efficiency trend
        fig = px.line(production_data, x='Date', y='Efficiency', title='Production Efficiency Trend')
        fig.update_layout(height=400, yaxis_title="Efficiency (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Production details table
    st.markdown("### 📋 Production Details")
    
    st.dataframe(
        production_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Efficiency": st.column_config.NumberColumn("Efficiency (%)", format="%.1f%%"),
            "Raw_Material_KG": st.column_config.NumberColumn("Raw Material (KG)", format="%.1f kg"),
            "Total_Output": st.column_config.NumberColumn("Output (Packets)")
        }
    )

def show_custom_reports():
    """Custom report builder"""
    
    st.subheader("📋 Custom Report Builder")
    st.info("Build custom reports with your specific requirements")
    
    # Report configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Report Configuration")
        
        report_type = st.selectbox(
            "Report Type",
            ["Stock Analysis", "Sales Summary", "Purchase Summary", "Production Summary", "Financial Overview"]
        )
        
        date_range = st.selectbox(
            "Date Range",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year", "Custom Range"]
        )
        
        if date_range == "Custom Range":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
            with col2:
                end_date = st.date_input("End Date")
        
        group_by = st.selectbox(
            "Group By",
            ["None", "Product", "Channel", "Supplier", "Date", "Month"]
        )
        
        include_charts = st.checkbox("Include Charts", value=True)
        include_summary = st.checkbox("Include Summary", value=True)
    
    with col2:
        st.markdown("#### Filters")
        
        if report_type in ["Stock Analysis", "Sales Summary"]:
            product_filter = st.multiselect(
                "Select Products",
                [f"{w}kg" for w in config.PRODUCT_WEIGHTS]
            )
        
        if report_type == "Sales Summary":
            channel_filter = st.multiselect(
                "Select Channels",
                config.SALES_CHANNELS
            )
        
        if report_type == "Purchase Summary":
            supplier_filter = st.text_input("Supplier Filter (optional)")
        
        min_amount = st.number_input("Minimum Amount Filter", min_value=0.0, value=0.0)
    
    # Generate report button
    if st.button("📊 Generate Custom Report", use_container_width=True):
        with st.spinner("Generating custom report..."):
            # Simulate report generation
            st.success("✅ Custom report generated successfully!")
            
            # Sample report output
            st.markdown("### 📋 Report Output")
            
            if include_summary:
                st.markdown("#### Executive Summary")
                st.write("• Total transactions: 150")
                st.write("• Total value: ₹125,000")
                st.write("• Average transaction: ₹833")
                st.write("• Period: Last 30 days")
            
            if include_charts:
                # Sample chart
                sample_data = pd.DataFrame({
                    'Category': ['Product A', 'Product B', 'Product C'],
                    'Value': [30000, 45000, 50000]
                })
                
                fig = px.bar(sample_data, x='Category', y='Value', title='Custom Report Chart')
                st.plotly_chart(fig, use_container_width=True)
            
            # Sample table
            sample_table = pd.DataFrame({
                'Date': ['2025-06-01', '2025-06-02', '2025-06-03'],
                'Product': ['1.0kg', '0.5kg', '2.0kg'],
                'Quantity': [25, 30, 15],
                'Amount': [2500, 1500, 3000]
            })
            
            st.dataframe(sample_table, use_container_width=True, hide_index=True)

# Helper functions to create sample data

def create_stock_sample_data():
    """Create sample stock data for testing"""
    return pd.DataFrame({
        'Product': [f'{w}kg' for w in config.PRODUCT_WEIGHTS],
        'Current_Stock': [45, 120, 85, 30, 95],
        'Min_Stock': [50, 100, 80, 40, 80],
        'Max_Stock': [200, 300, 250, 150, 250],
        'Unit_Price': [w * 50 for w in config.PRODUCT_WEIGHTS],
        'Stock_Value': [45*w*50, 120*w*50, 85*w*50, 30*w*50, 95*w*50 for w in config.PRODUCT_WEIGHTS],
        'Status': ['Low' if stock < min_stock else 'Normal' for stock, min_stock in zip([45, 120, 85, 30, 95], [50, 100, 80, 40, 80])]
    })

def create_sales_sample_data():
    """Create sample sales data for testing"""
    import numpy as np
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    data = []
    
    for date in dates:
        for _ in range(np.random.randint(1, 8)):  # 1-7 sales per day
            weight = np.random.choice(config.PRODUCT_WEIGHTS)
            quantity = np.random.randint(1, 20)
            unit_price = weight * 50 + np.random.randint(-10, 20)
            
            data.append({
                'Date': date,
                'Product': f'{weight}kg',
                'Quantity': quantity,
                'Unit_Price': unit_price,
                'Revenue': quantity * unit_price,
                'Channel': np.random.choice(config.SALES_CHANNELS),
                'Order_ID': f'ORD-{np.random.randint(100000, 999999)}'
            })
    
    return pd.DataFrame(data)

def create_purchase_sample_data():
    """Create sample purchase data for testing"""
    import numpy as np
    
    dates = pd.date_range(end=datetime.now(), periods=15, freq='D')
    suppliers = ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D']
    
    data = []
    for date in dates[::3]:  # Purchase every 3 days
        data.append({
            'Date': date,
            'Supplier': np.random.choice(suppliers),
            'Material': 'Raw Chana',
            'Quantity_KG': np.random.randint(50, 200),
            'Rate_Per_KG': np.random.randint(40, 65),
            'Total_Amount': 0,  # Will calculate below
            'Invoice': f'INV-{np.random.randint(1000, 9999)}'
        })
    
    df = pd.DataFrame(data)
    df['Total_Amount'] = df['Quantity_KG'] * df['Rate_Per_KG']
    
    return df

def create_production_sample_data():
    """Create sample production data for testing"""
    import numpy as np
    
    dates = pd.date_range(end=datetime.now(), periods=20, freq='D')
    operators = ['Operator 1', 'Operator 2', 'Operator 3']
    
    data = []
    for date in dates:
        if np.random.random() > 0.2:  # Production on 80% of days
            raw_material = np.random.randint(80, 150)
            output = np.random.randint(200, 500)
            
            data.append({
                'Date': date,
                'Batch_Number': f'BATCH-{date.strftime("%m%d")}-{np.random.randint(1, 4)}',
                'Raw_Material_KG': raw_material,
                'Total_Output': output,
                'Efficiency': (output * 0.5 / raw_material) * 100,  # Assuming 0.5kg average per packet
                'Operator': np.random.choice(operators),
                'Quality_Grade': np.random.choice(['A', 'A', 'B'])  # 67% Grade A
            })
    
    return pd.DataFrame(data)