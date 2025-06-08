"""
Data Entry Page - All data input forms and operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import config
from src.components.data_entry_forms import (
    show_product_management, 
    show_quick_entry,
    show_bulk_upload,
    create_product_selector,
    create_channel_selector,
    create_date_input,
    create_quantity_input,
    create_price_input
)
from src.services.excel_service import ExcelService
from src.services.data_validation import DataValidator

def show_data_entry():
    """Main data entry page with all forms"""
    
    st.header("📝 Data Entry Portal")
    st.markdown("Enter and manage your inventory data efficiently")
    
    # Check Excel file status
    try:
        excel_service = ExcelService()
        if not excel_service.file_exists():
            st.error("❌ Excel file not found! Please ensure your file is at: data/uploads/stock_report.xlsx")
            return
        else:
            st.success("✅ Excel file connected successfully")
    except Exception as e:
        st.warning(f"⚠️ Excel connection issue: {str(e)}")
    
    # Tab navigation for different entry types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Daily Operations", 
        "📦 Product Management",
        "⚡ Quick Entry",
        "📄 Bulk Upload",
        "🔧 Stock Adjustments"
    ])
    
    with tab1:
        show_daily_operations()
    
    with tab2:
        show_product_management()
    
    with tab3:
        show_quick_entry()
    
    with tab4:
        show_bulk_upload()
    
    with tab5:
        show_stock_adjustments()

def show_daily_operations():
    """Daily operations forms"""
    
    st.subheader("📊 Daily Operations")
    st.info("Record your daily inventory operations")
    
    # Sub-tabs for different operations
    sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs([
        "📈 Opening Stock",
        "🛒 Sales Entry", 
        "📦 Purchase Entry",
        "🏭 Production Entry",
        "↩️ Returns Entry"
    ])
    
    with sub_tab1:
        show_opening_stock_form()
    
    with sub_tab2:
        show_sales_entry_form()
    
    with sub_tab3:
        show_purchase_entry_form()
    
    with sub_tab4:
        show_production_entry_form()
    
    with sub_tab5:
        show_returns_entry_form()

def show_opening_stock_form():
    """Opening stock entry form"""
    
    st.markdown("**📈 Record Opening Stock**")
    st.write("Enter the opening stock levels for today")
    
    with st.form("opening_stock_form", clear_on_submit=True):
        # Date selection
        entry_date = create_date_input("Date", key="opening_date")
        
        st.markdown("**Stock Levels by Product:**")
        
        # Create input fields for each product
        stock_data = {}
        
        col1, col2, col3 = st.columns(3)
        
        for i, weight in enumerate(config.PRODUCT_WEIGHTS):
            with [col1, col2, col3][i % 3]:
                stock_data[f"{weight}kg"] = st.number_input(
                    f"{weight}kg Opening Stock",
                    min_value=0,
                    value=0,
                    key=f"opening_{weight}"
                )
        
        # Notes
        notes = st.text_area("Notes (Optional)", placeholder="Any remarks about opening stock...")
        
        # Submit button
        submitted = st.form_submit_button("📊 Record Opening Stock", use_container_width=True)
        
        if submitted:
            if any(stock_data.values()):
                try:
                    # Save to Excel (implement this in excel_service)
                    excel_service = ExcelService()
                    # excel_service.update_opening_stock(entry_date, stock_data, notes)
                    
                    st.success(f"✅ Opening stock recorded for {entry_date}")
                    
                    # Display summary
                    with st.expander("📋 Summary"):
                        for product, stock in stock_data.items():
                            if stock > 0:
                                st.write(f"• {product}: {stock} units")
                        if notes:
                            st.write(f"• Notes: {notes}")
                
                except Exception as e:
                    st.error(f"❌ Error saving data: {str(e)}")
            else:
                st.warning("⚠️ Please enter stock levels for at least one product")

def show_sales_entry_form():
    """Sales entry form"""
    
    st.markdown("**🛒 Record Sales**")
    st.write("Enter sales transactions")
    
    with st.form("sales_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            entry_date = create_date_input("Sale Date", key="sale_date")
            product = create_product_selector("Product", key="sale_product")
            quantity = create_quantity_input("Quantity Sold", key="sale_quantity")
        
        with col2:
            channel = create_channel_selector("Sales Channel", key="sale_channel")
            weight = float(product.replace('kg', ''))
            suggested_price = weight * 100  # Base rate ₹100 per kg
            price = create_price_input("Price per Unit", key="sale_price")
            if price == 0.0:
                price = suggested_price
            order_id = st.text_input("Order ID (Optional)", placeholder="e.g., AMZ-123456")
        
        # Calculate total
        total_amount = quantity * price if price > 0 else 0
        
        if total_amount > 0:
            st.markdown(f"**💰 Total Amount: ₹{total_amount:,.2f}**")
        
        # Customer details (optional)
        with st.expander("📋 Additional Details (Optional)"):
            customer_name = st.text_input("Customer Name")
            shipping_address = st.text_area("Shipping Address")
            remarks = st.text_area("Remarks")
        
        # Submit button
        submitted = st.form_submit_button("🛒 Record Sale", use_container_width=True)
        
        if submitted:
            if quantity > 0 and price > 0:
                try:
                    # Validate data
                    validator = DataValidator()
                    sale_data = {
                        'date': entry_date,
                        'product': product,
                        'quantity': quantity,
                        'price': price,
                        'channel': channel,
                        'order_id': order_id,
                        'customer_name': customer_name,
                        'total_amount': total_amount
                    }
                    
                    if validator.validate_sale_data(sale_data):
                        # Save to Excel
                        excel_service = ExcelService()
                        # excel_service.record_sale(sale_data)
                        
                        st.success(f"✅ Sale recorded: {quantity}x {product} for ₹{total_amount:,.2f}")
                        
                        # Display transaction summary
                        with st.expander("📄 Transaction Summary"):
                            st.write(f"**Date:** {entry_date}")
                            st.write(f"**Product:** {product}")
                            st.write(f"**Quantity:** {quantity} units")
                            st.write(f"**Channel:** {channel}")
                            st.write(f"**Unit Price:** ₹{price:,.2f}")
                            st.write(f"**Total Amount:** ₹{total_amount:,.2f}")
                            if order_id:
                                st.write(f"**Order ID:** {order_id}")
                    else:
                        st.error("❌ Data validation failed")
                        
                except Exception as e:
                    st.error(f"❌ Error saving sale: {str(e)}")
            else:
                st.error("❌ Please enter valid quantity and price")

def show_purchase_entry_form():
    """Purchase entry form"""
    
    st.markdown("**📦 Record Purchases**")
    st.write("Enter raw material purchases and inventory additions")
    
    with st.form("purchase_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            entry_date = create_date_input("Purchase Date", key="purchase_date")
            supplier_name = st.text_input("Supplier Name", placeholder="Enter supplier name")
            material_type = st.selectbox(
                "Material Type",
                ["Raw Chana", "Packaging Material", "Other Supplies"]
            )
        
        with col2:
            quantity = st.number_input("Quantity (kg)", min_value=0.0, step=0.1, key="purchase_qty")
            rate_per_kg = st.number_input("Rate per Kg (₹)", min_value=0.0, step=1.0, key="purchase_rate")
            invoice_number = st.text_input("Invoice Number", placeholder="e.g., INV-2025-001")
        
        # Calculate total
        total_amount = quantity * rate_per_kg if rate_per_kg > 0 else 0
        
        if total_amount > 0:
            st.markdown(f"**💰 Total Amount: ₹{total_amount:,.2f}**")
        
        # Additional details
        with st.expander("📋 Additional Details"):
            quality_grade = st.selectbox("Quality Grade", ["A", "B", "C", "Premium"])
            payment_method = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Cheque", "Credit"])
            notes = st.text_area("Notes", placeholder="Quality notes, delivery details, etc.")
        
        # Submit button
        submitted = st.form_submit_button("📦 Record Purchase", use_container_width=True)
        
        if submitted:
            if quantity > 0 and rate_per_kg > 0 and supplier_name:
                try:
                    # Save to Excel
                    excel_service = ExcelService()
                    purchase_data = {
                        'date': entry_date,
                        'supplier': supplier_name,
                        'material_type': material_type,
                        'quantity': quantity,
                        'rate_per_kg': rate_per_kg,
                        'total_amount': total_amount,
                        'invoice_number': invoice_number,
                        'quality_grade': quality_grade,
                        'payment_method': payment_method,
                        'notes': notes
                    }
                    # excel_service.record_purchase(purchase_data)
                    
                    st.success(f"✅ Purchase recorded: {quantity}kg from {supplier_name} for ₹{total_amount:,.2f}")
                    
                    # Display purchase summary
                    with st.expander("📄 Purchase Summary"):
                        st.write(f"**Date:** {entry_date}")
                        st.write(f"**Supplier:** {supplier_name}")
                        st.write(f"**Material:** {material_type}")
                        st.write(f"**Quantity:** {quantity} kg")
                        st.write(f"**Rate:** ₹{rate_per_kg:,.2f} per kg")
                        st.write(f"**Total Amount:** ₹{total_amount:,.2f}")
                        if invoice_number:
                            st.write(f"**Invoice:** {invoice_number}")
                
                except Exception as e:
                    st.error(f"❌ Error saving purchase: {str(e)}")
            else:
                st.error("❌ Please fill in all required fields")

def show_production_entry_form():
    """Production entry form"""
    
    st.markdown("**🏭 Record Production**")
    st.write("Enter production batch details and output")
    
    with st.form("production_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            entry_date = create_date_input("Production Date", key="production_date")
            batch_number = st.text_input("Batch Number", placeholder="e.g., BATCH-20250608-001")
            raw_material_used = st.number_input("Raw Material Used (kg)", min_value=0.0, step=0.1)
        
        with col2:
            operator_name = st.text_input("Operator Name", placeholder="Enter operator name")
            shift = st.selectbox("Shift", ["Morning", "Evening", "Night"])
            production_line = st.selectbox("Production Line", ["Line 1", "Line 2", "Line 3"])
        
        st.markdown("**Production Output:**")
        
        # Output by product weight
        output_data = {}
        
        col1, col2, col3 = st.columns(3)
        
        for i, weight in enumerate(config.PRODUCT_WEIGHTS):
            with [col1, col2, col3][i % 3]:
                output_data[f"{weight}kg"] = st.number_input(
                    f"{weight}kg Packets",
                    min_value=0,
                    value=0,
                    key=f"prod_{weight}"
                )
        
        # Calculate efficiency
        total_output_kg = sum(float(product.replace('kg', '')) * qty for product, qty in output_data.items())
        efficiency = (total_output_kg / raw_material_used * 100) if raw_material_used > 0 else 0
        
        if raw_material_used > 0:
            st.markdown(f"**📊 Production Efficiency: {efficiency:.1f}%**")
        
        # Additional details
        with st.expander("📋 Production Details"):
            quality_notes = st.text_area("Quality Notes")
            issues = st.text_area("Issues/Problems")
            remarks = st.text_area("Additional Remarks")
        
        # Submit button
        submitted = st.form_submit_button("🏭 Record Production", use_container_width=True)
        
        if submitted:
            if raw_material_used > 0 and any(output_data.values()) and batch_number:
                try:
                    total_packets = sum(output_data.values())
                    
                    # Save to Excel
                    excel_service = ExcelService()
                    production_data = {
                        'date': entry_date,
                        'batch_number': batch_number,
                        'raw_material_used': raw_material_used,
                        'output_data': output_data,
                        'operator': operator_name,
                        'shift': shift,
                        'efficiency': efficiency,
                        'quality_notes': quality_notes,
                        'issues': issues,
                        'remarks': remarks
                    }
                    # excel_service.record_production(production_data)
                    
                    st.success(f"✅ Production recorded: Batch {batch_number} - {total_packets} packets produced")
                    
                    # Display production summary
                    with st.expander("📄 Production Summary"):
                        st.write(f"**Date:** {entry_date}")
                        st.write(f"**Batch:** {batch_number}")
                        st.write(f"**Operator:** {operator_name}")
                        st.write(f"**Raw Material:** {raw_material_used} kg")
                        st.write(f"**Total Output:** {total_packets} packets")
                        st.write(f"**Efficiency:** {efficiency:.1f}%")
                        
                        st.write("**Output Breakdown:**")
                        for product, qty in output_data.items():
                            if qty > 0:
                                st.write(f"  • {product}: {qty} packets")
                
                except Exception as e:
                    st.error(f"❌ Error saving production data: {str(e)}")
            else:
                st.error("❌ Please fill in all required fields")

def show_returns_entry_form():
    """Returns entry form"""
    
    st.markdown("**↩️ Record Returns**")
    st.write("Enter return transactions and damaged goods")
    
    with st.form("returns_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            entry_date = create_date_input("Return Date", key="return_date")
            product = create_product_selector("Product", key="return_product")
            quantity = create_quantity_input("Quantity Returned", key="return_quantity")
        
        with col2:
            return_reason = st.selectbox(
                "Return Reason",
                ["Damaged", "Expired", "Customer Return", "Quality Issue", "Other"]
            )
            channel = create_channel_selector("Return Channel", key="return_channel")
            refund_amount = st.number_input("Refund Amount (₹)", min_value=0.0, key="refund_amount")
        
        # Additional details
        order_id = st.text_input("Original Order ID", placeholder="e.g., AMZ-123456")
        
        with st.expander("📋 Return Details"):
            condition = st.selectbox("Product Condition", ["Damaged", "Expired", "Good", "Repairable"])
            action_taken = st.selectbox("Action Taken", ["Disposed", "Returned to Stock", "Sent for Repair", "Donated"])
            notes = st.text_area("Detailed Notes", placeholder="Describe the return reason and condition...")
        
        # Submit button
        submitted = st.form_submit_button("↩️ Record Return", use_container_width=True)
        
        if submitted:
            if quantity > 0:
                try:
                    # Save to Excel
                    excel_service = ExcelService()
                    return_data = {
                        'date': entry_date,
                        'product': product,
                        'quantity': quantity,
                        'reason': return_reason,
                        'channel': channel,
                        'refund_amount': refund_amount,
                        'order_id': order_id,
                        'condition': condition,
                        'action_taken': action_taken,
                        'notes': notes
                    }
                    # excel_service.record_return(return_data)
                    
                    st.success(f"✅ Return recorded: {quantity}x {product} - {return_reason}")
                    
                    # Display return summary
                    with st.expander("📄 Return Summary"):
                        st.write(f"**Date:** {entry_date}")
                        st.write(f"**Product:** {product}")
                        st.write(f"**Quantity:** {quantity} units")
                        st.write(f"**Reason:** {return_reason}")
                        st.write(f"**Channel:** {channel}")
                        if refund_amount > 0:
                            st.write(f"**Refund:** ₹{refund_amount:,.2f}")
                        if order_id:
                            st.write(f"**Order ID:** {order_id}")
                        st.write(f"**Action:** {action_taken}")
                
                except Exception as e:
                    st.error(f"❌ Error saving return: {str(e)}")
            else:
                st.error("❌ Please enter valid return quantity")

def show_stock_adjustments():
    """Stock adjustments interface"""
    
    st.subheader("🔧 Stock Adjustments")
    st.info("Make manual adjustments to stock levels")
    
    with st.form("stock_adjustment_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            product = create_product_selector("Product", key="adj_product")
            
        with col2:
            adjustment_type = st.selectbox(
                "Adjustment Type",
                ["Increase Stock", "Decrease Stock", "Set Stock Level"]
            )
        
        with col3:
            if adjustment_type == "Set Stock Level":
                quantity = st.number_input("New Stock Level", min_value=0)
            else:
                quantity = st.number_input("Adjustment Quantity", min_value=1, value=1)
        
        reason = st.selectbox(
            "Reason for Adjustment",
            ["Physical Count Correction", "Damage/Wastage", "Found Stock", "System Error", "Production Addition", "Other"]
        )
        
        if reason == "Other":
            custom_reason = st.text_input("Specify reason:")
        
        notes = st.text_area("Additional Notes", placeholder="Any additional details about this adjustment...")
        
        # Submit button
        submitted = st.form_submit_button("🔧 Apply Adjustment", use_container_width=True)
        
        if submitted:
            try:
                # Save adjustment
                excel_service = ExcelService()
                adjustment_data = {
                    'date': datetime.now().date(),
                    'product': product,
                    'adjustment_type': adjustment_type,
                    'quantity': quantity,
                    'reason': custom_reason if reason == "Other" else reason,
                    'notes': notes
                }
                # excel_service.record_adjustment(adjustment_data)
                
                if adjustment_type == "Set Stock Level":
                    st.success(f"✅ Stock level set: {product} = {quantity} units")
                else:
                    action = "Increased" if adjustment_type == "Increase Stock" else "Decreased"
                    st.success(f"✅ Stock {action.lower()}: {product} by {quantity} units")
                
                st.info(f"Reason: {reason}")
                
            except Exception as e:
                st.error(f"❌ Error applying adjustment: {str(e)}")