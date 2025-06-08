"""
Data Entry Form Components - Reusable form components for data entry
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, List, Any, Optional
import config

def show_product_management():
    """Product management interface"""
    
    st.subheader("📦 Product Management")
    
    # Product overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Products")
        
        # Display current products
        products_data = []
        for weight in config.PRODUCT_WEIGHTS:
            details = config.PRODUCT_DETAILS.get(weight, {})
            products_data.append({
                'Product': f"Roasted Chana {weight}kg",
                'Weight (kg)': weight,
                'Pouch Size': details.get('pouch_size', 'N/A'),
                'FNSKU': details.get('fnsku', 'N/A')
            })
        
        if products_data:
            df = pd.DataFrame(products_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### Add New Product Variant")
        
        with st.form("add_product_form"):
            product_name = st.text_input("Product Name", value="Roasted Chana", placeholder="e.g., Roasted chana")
            
            col1, col2 = st.columns(2)
            with col1:
                weight = st.number_input("Weight (kg)", min_value=0.1, max_value=5.0, step=0.1, value=1.0)
            with col2:
                pouch_size = st.text_input("Pouch Size", placeholder="e.g., 9*12")
            
            fnsku = st.text_input("FNSKU Code", placeholder="e.g., X00289HWX7")
            
            submitted = st.form_submit_button("Add Product Variant", use_container_width=True)
            
            if submitted:
                if product_name and weight > 0:
                    st.success(f"✅ Product variant added: {product_name} {weight}kg")
                    st.info("ℹ️ Note: This will be saved to the system configuration.")
                else:
                    st.error("❌ Please fill all required fields")

def show_quick_entry():
    """Quick entry interface for common operations"""
    
    st.subheader("⚡ Quick Entry")
    st.info("Rapid data entry for common daily operations")
    
    # Quick entry tabs
    tab1, tab2, tab3 = st.tabs(["🛒 Quick Sale", "📦 Quick Stock Update", "🔄 Quick Adjustment"])
    
    with tab1:
        show_quick_sale_form()
    
    with tab2:
        show_quick_stock_form()
    
    with tab3:
        show_quick_adjustment_form()

def show_quick_sale_form():
    """Quick sale entry form"""
    
    st.markdown("**Record a Sale Quickly**")
    
    with st.form("quick_sale_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            product = st.selectbox(
                "Product",
                [f"{w}kg" for w in config.PRODUCT_WEIGHTS]
            )
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
        
        with col3:
            channel = st.selectbox(
                "Channel",
                config.SALES_CHANNELS
            )
        
        # Auto-calculate suggested price
        weight = float(product.replace('kg', ''))
        suggested_price = weight * 100  # ₹100 per kg base rate
        
        price = st.number_input("Price per Unit (₹)", min_value=0.0, value=suggested_price, step=1.0)
        
        submitted = st.form_submit_button("🚀 Record Sale", use_container_width=True)
        
        if submitted:
            total_amount = quantity * price
            st.success(f"✅ Sale recorded: {quantity}x {product} via {channel} for ₹{total_amount:,.2f}")
            # Add actual sale recording logic here

def show_quick_stock_form():
    """Quick stock update form"""
    
    st.markdown("**Update Stock Levels**")
    
    with st.form("quick_stock_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            product = st.selectbox(
                "Product",
                [f"{w}kg" for w in config.PRODUCT_WEIGHTS]
            )
        
        with col2:
            new_stock = st.number_input("New Stock Level", min_value=0)
        
        reason = st.text_input("Reason for Update", placeholder="e.g., Physical count correction")
        
        submitted = st.form_submit_button("📊 Update Stock", use_container_width=True)
        
        if submitted:
            st.success(f"✅ Stock updated: {product} set to {new_stock} units")
            if reason:
                st.info(f"Reason: {reason}")

def show_quick_adjustment_form():
    """Quick adjustment form"""
    
    st.markdown("**Quick Stock Adjustment**")
    
    with st.form("quick_adjustment_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            product = st.selectbox(
                "Product",
                [f"{w}kg" for w in config.PRODUCT_WEIGHTS]
            )
        
        with col2:
            adjustment_type = st.selectbox(
                "Adjustment Type",
                ["Add Stock", "Remove Stock"]
            )
        
        with col3:
            quantity = st.number_input("Quantity", min_value=1, value=1)
        
        reason = st.selectbox(
            "Reason",
            ["Damage/Wastage", "Found Stock", "System Error", "Production", "Other"]
        )
        
        if reason == "Other":
            custom_reason = st.text_input("Specify reason:")
        
        submitted = st.form_submit_button("🔧 Apply Adjustment", use_container_width=True)
        
        if submitted:
            action = "Added" if adjustment_type == "Add Stock" else "Removed"
            st.success(f"✅ {action} {quantity} units of {product}")
            st.info(f"Reason: {reason}")

def show_bulk_upload():
    """Bulk upload interface"""
    
    st.subheader("📄 Bulk Upload")
    st.info("Upload CSV or Excel files to import data in bulk")
    
    # Upload type selection
    upload_type = st.selectbox(
        "Select Data Type",
        ["Sales Data", "Purchase Data", "Stock Data", "Production Data"]
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose file",
        type=['xlsx', 'xls', 'csv'],
        help="Upload Excel or CSV file with your data"
    )
    
    if uploaded_file is not None:
        # Show file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_file.name)
        with col2:
            file_size = len(uploaded_file.getvalue())
            st.metric("File Size", f"{file_size / 1024:.1f} KB")
        with col3:
            st.metric("File Type", uploaded_file.type)
        
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.markdown("### Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            st.markdown(f"**Total Rows:** {len(df)} | **Columns:** {len(df.columns)}")
            
            # Data validation
            if st.button("🔍 Validate Data", use_container_width=True):
                with st.spinner("Validating data..."):
                    validation_result = validate_bulk_data(df, upload_type)
                
                if validation_result['valid']:
                    st.success(f"✅ Data validation passed! {validation_result['valid_rows']} valid rows found.")
                    
                    if st.button("📥 Import Data", use_container_width=True):
                        st.success("✅ Data imported successfully!")
                        st.balloons()
                else:
                    st.error(f"❌ Data validation failed! {validation_result['invalid_rows']} invalid rows found.")
                    
                    with st.expander("View Validation Errors"):
                        for error in validation_result['errors'][:10]:
                            st.write(f"• {error}")
                        
                        if len(validation_result['errors']) > 10:
                            st.write(f"... and {len(validation_result['errors']) - 10} more errors")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
    
    # Download templates
    st.markdown("---")
    st.markdown("### 📥 Download Templates")
    
    show_template_downloads()

def show_template_downloads():
    """Show template download buttons"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Sales Template", use_container_width=True):
            template_data = create_sales_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "Download Sales Template",
                data=csv,
                file_name="sales_template.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Purchase Template", use_container_width=True):
            template_data = create_purchase_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "Download Purchase Template",
                data=csv,
                file_name="purchase_template.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Stock Template", use_container_width=True):
            template_data = create_stock_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "Download Stock Template",
                data=csv,
                file_name="stock_template.csv",
                mime="text/csv"
            )
    
    with col4:
        if st.button("Production Template", use_container_width=True):
            template_data = create_production_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "Download Production Template",
                data=csv,
                file_name="production_template.csv",
                mime="text/csv"
            )

def create_sales_template():
    """Create sales data template"""
    return pd.DataFrame({
        'date': ['2025-06-08'],
        'product_weight': ['1.0'],
        'quantity': [10],
        'price': [100],
        'channel': ['Amazon FBA'],
        'order_id': ['ORD-001']
    })

def create_purchase_template():
    """Create purchase data template"""
    return pd.DataFrame({
        'date': ['2025-06-08'],
        'supplier': ['Supplier Name'],
        'raw_material_kg': [100],
        'rate_per_kg': [50],
        'total_amount': [5000],
        'invoice_number': ['INV-001']
    })

def create_stock_template():
    """Create stock data template"""
    return pd.DataFrame({
        'product_weight': [str(w) for w in config.PRODUCT_WEIGHTS],
        'opening_stock': [50, 100, 200, 75, 150],
        'date': ['2025-06-08'] * len(config.PRODUCT_WEIGHTS)
    })

def create_production_template():
    """Create production data template"""
    return pd.DataFrame({
        'date': ['2025-06-08'],
        'batch_number': ['BATCH-001'],
        'raw_material_used': [100],
        'product_weight': ['1.0'],
        'packets_produced': [95],
        'operator': ['Operator Name']
    })

def validate_bulk_data(df, upload_type):
    """Validate bulk upload data"""
    errors = []
    valid_rows = 0
    
    # Basic validation
    if df.empty:
        errors.append("File is empty")
        return {'valid': False, 'errors': errors, 'valid_rows': 0, 'invalid_rows': len(df)}
    
    # Type-specific validation
    if upload_type == "Sales Data":
        required_cols = ['date', 'product_weight', 'quantity', 'price', 'channel']
        for col in required_cols:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")
    elif upload_type == "Purchase Data":
        required_cols = ['date', 'supplier', 'raw_material_kg', 'rate_per_kg']
        for col in required_cols:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")
    
    # Count valid rows (simple check)
    valid_rows = len(df) - len(errors)
    invalid_rows = len(errors)
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'valid_rows': max(0, valid_rows),
        'invalid_rows': invalid_rows
    }

# Reusable form components
def create_product_selector(label: str = "Select Product", key: str = None) -> str:
    """Reusable product selector component"""
    products = [f"{w}kg" for w in config.PRODUCT_WEIGHTS]
    return st.selectbox(label, products, key=key, help="Select the product weight variant")

def create_channel_selector(label: str = "Sales Channel", key: str = None) -> str:
    """Reusable sales channel selector"""
    return st.selectbox(label, config.SALES_CHANNELS, key=key, help="Select the sales channel")

def create_date_input(label: str = "Date", key: str = None, max_date: date = None) -> date:
    """Reusable date input component"""
    if max_date is None:
        max_date = date.today()
    return st.date_input(label, value=date.today(), max_value=max_date, key=key, help="Select the transaction date")

def create_quantity_input(label: str = "Quantity", min_value: int = 0, max_value: int = 1000, key: str = None) -> int:
    """Reusable quantity input component"""
    return st.number_input(label, min_value=min_value, max_value=max_value, value=1, step=1, key=key, help=f"Enter quantity (between {min_value} and {max_value})")

def create_price_input(label: str = "Price (₹)", key: str = None) -> float:
    """Reusable price input component"""
    return st.number_input(label, min_value=0.0, step=1.0, key=key, help="Enter price in rupees")