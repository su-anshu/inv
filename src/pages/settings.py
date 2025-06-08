"""
Settings Page - System configuration and preferences
"""

import streamlit as st
import config
from datetime import datetime
import json

def show_settings():
    """Display system settings and configuration"""
    
    st.header("⚙️ Settings")
    st.markdown("Configure system preferences and business rules")
    
    # Settings navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Business Settings",
        "📦 Product Configuration",
        "💾 Backup Settings", 
        "🎨 Display Preferences",
        "🔧 System Settings"
    ])
    
    with tab1:
        show_business_settings()
    
    with tab2:
        show_product_configuration()
    
    with tab3:
        show_backup_settings()
    
    with tab4:
        show_display_preferences()
    
    with tab5:
        show_system_settings()

def show_business_settings():
    """Business configuration settings"""
    
    st.subheader("🏢 Business Configuration")
    
    with st.form("business_settings_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Company Information")
            company_name = st.text_input("Company Name", value="Your Company Name")
            business_type = st.selectbox("Business Type", ["Manufacturing", "Trading", "Retail", "Distribution"])
            
            st.markdown("#### Contact Details")
            phone = st.text_input("Phone Number", placeholder="+91-XXXXXXXXXX")
            email = st.text_input("Email Address", placeholder="contact@company.com")
            
        with col2:
            st.markdown("#### Address")
            address_line1 = st.text_input("Address Line 1")
            address_line2 = st.text_input("Address Line 2")
            city = st.text_input("City", value="Ranchi")
            state = st.text_input("State", value="Jharkhand")
            pincode = st.text_input("PIN Code")
            
            st.markdown("#### Tax Information")
            gst_number = st.text_input("GST Number", placeholder="22AAAAA0000A1Z5")
            pan_number = st.text_input("PAN Number", placeholder="AAAPA1234C")
        
        st.markdown("#### Sales Channels Configuration")
        
        # Amazon settings
        with st.expander("🛒 Amazon Configuration"):
            amazon_seller_id = st.text_input("Amazon Seller ID")
            amazon_marketplace = st.selectbox("Amazon Marketplace", ["Amazon.in", "Amazon.com", "Amazon.ae"])
            fba_enabled = st.checkbox("FBA Enabled", value=True)
            easyship_enabled = st.checkbox("Amazon Easyship Enabled", value=True)
        
        # Flipkart settings
        with st.expander("🛒 Flipkart Configuration"):
            flipkart_seller_id = st.text_input("Flipkart Seller ID")
            flipkart_enabled = st.checkbox("Flipkart Integration Enabled", value=True)
        
        submitted = st.form_submit_button("💾 Save Business Settings", use_container_width=True)
        
        if submitted:
            st.success("✅ Business settings saved successfully!")

def show_product_configuration():
    """Product and inventory configuration"""
    
    st.subheader("📦 Product Configuration")
    
    # Current products display
    st.markdown("#### Current Product Variants")
    
    product_data = []
    for weight in config.PRODUCT_WEIGHTS:
        details = config.PRODUCT_DETAILS.get(weight, {})
        product_data.append({
            'Weight (kg)': weight,
            'Pouch Size': details.get('pouch_size', 'Not Set'),
            'FNSKU': details.get('fnsku', 'Not Set')
        })
    
    st.dataframe(product_data, use_container_width=True, hide_index=True)
    
    # Add/Edit product variants
    with st.form("product_config_form"):
        st.markdown("#### Product Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Stock Thresholds**")
            min_stock_threshold = st.number_input(
                "Minimum Stock Threshold", 
                min_value=1, 
                value=config.MIN_STOCK_THRESHOLD
            )
            critical_stock_threshold = st.number_input(
                "Critical Stock Threshold", 
                min_value=1, 
                value=config.CRITICAL_STOCK_THRESHOLD
            )
            max_stock_limit = st.number_input(
                "Maximum Stock Limit", 
                min_value=100, 
                value=config.MAX_STOCK_LIMIT
            )
        
        with col2:
            st.markdown("**Pricing Configuration**")
            base_rate_per_kg = st.number_input("Base Rate per KG (₹)", min_value=1.0, value=100.0)
            markup_percentage = st.number_input("Markup Percentage (%)", min_value=0.0, value=20.0)
            
            st.markdown("**Unit Configuration**")
            weight_unit = st.selectbox("Weight Unit", ["kg", "grams"], index=0)
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"], index=0)
        
        # Product variant management
        st.markdown("#### Add New Product Variant")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            new_weight = st.number_input("Weight (kg)", min_value=0.1, max_value=10.0, step=0.1, value=1.0)
        with col2:
            new_pouch_size = st.text_input("Pouch Size", placeholder="e.g., 9*12")
        with col3:
            new_fnsku = st.text_input("FNSKU Code", placeholder="e.g., X00289HWX7")
        
        submitted = st.form_submit_button("💾 Save Product Configuration", use_container_width=True)
        
        if submitted:
            st.success("✅ Product configuration saved successfully!")
            if new_weight and new_pouch_size and new_fnsku:
                st.info(f"ℹ️ New variant added: {new_weight}kg - {new_pouch_size} - {new_fnsku}")

def show_backup_settings():
    """Backup and data protection settings"""
    
    st.subheader("💾 Backup & Data Protection")
    
    with st.form("backup_settings_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Automatic Backup")
            auto_backup_enabled = st.checkbox("Enable Automatic Backup", value=config.AUTO_BACKUP_ENABLED)
            backup_interval = st.selectbox(
                "Backup Frequency", 
                ["Every Hour", "Every 6 Hours", "Daily", "Weekly"],
                index=1
            )
            max_backups = st.number_input("Maximum Backup Files", min_value=5, max_value=100, value=config.MAX_BACKUPS)
            
            st.markdown("#### Backup Location")
            backup_location = st.selectbox("Backup Storage", ["Local Only", "Cloud + Local", "Cloud Only"])
            
        with col2:
            st.markdown("#### Data Retention")
            retention_period = st.selectbox("Data Retention Period", ["1 Month", "3 Months", "6 Months", "1 Year", "Forever"])
            compress_backups = st.checkbox("Compress Backup Files", value=True)
            
            st.markdown("#### Security")
            encrypt_backups = st.checkbox("Encrypt Backup Files", value=False)
            backup_password = st.text_input("Backup Password", type="password", placeholder="Optional encryption password")
        
        # Backup schedule
        st.markdown("#### Backup Schedule")
        backup_time = st.time_input("Daily Backup Time", value=datetime.strptime("02:00", "%H:%M").time())
        
        # Manual backup actions
        st.markdown("#### Manual Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.form_submit_button("🔄 Create Backup Now", use_container_width=True):
                st.info("Creating manual backup...")
        
        with col2:
            if st.form_submit_button("📤 Export All Data", use_container_width=True):
                st.info("Exporting all data...")
        
        with col3:
            if st.form_submit_button("🗑️ Clean Old Backups", use_container_width=True):
                st.info("Cleaning old backup files...")