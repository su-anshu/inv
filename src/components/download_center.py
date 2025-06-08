"""
Download Center Components - File generation and download functionality
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import config
from src.services.excel_service import ExcelService
import io

def show_report_downloads():
    """Show report download options"""
    
    st.subheader("📊 Generate Reports")
    
    # Report type selection
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            [
                "Stock Summary Report",
                "Sales Report", 
                "Purchase Report",
                "Production Report",
                "Financial Summary",
                "Low Stock Alert Report"
            ]
        )
    
    with col2:
        date_range = st.selectbox(
            "Date Range",
            ["Today", "Last 7 Days", "Last 30 Days", "This Month", "Custom Range"]
        )
    
    # Custom date range
    if date_range == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=date.today())
    else:
        start_date, end_date = get_date_range(date_range)
    
    # Format selection
    export_format = st.selectbox(
        "Export Format",
        ["Excel (.xlsx)", "CSV (.csv)", "PDF (.pdf)"]
    )
    
    # Generate report button
    if st.button("📊 Generate Report", use_container_width=True):
        with st.spinner("Generating report..."):
            report_data = generate_report_data(report_type, start_date, end_date)
            
            if report_data is not None:
                # Create download based on format
                if export_format == "Excel (.xlsx)":
                    excel_file = create_excel_report(report_data, report_type)
                    st.download_button(
                        label="📥 Download Excel Report",
                        data=excel_file,
                        file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                elif export_format == "CSV (.csv)":
                    csv_file = create_csv_report(report_data)
                    st.download_button(
                        label="📥 Download CSV Report", 
                        data=csv_file,
                        file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                elif export_format == "PDF (.pdf)":
                    st.info("📄 PDF generation coming soon!")
                
                # Show preview
                st.markdown("### 👀 Report Preview")
                st.dataframe(report_data.head(20), use_container_width=True)
                
                st.success(f"✅ {report_type} generated successfully!")
            else:
                st.error("❌ No data available for the selected criteria")

def show_backup_downloads():
    """Show backup file downloads"""
    
    st.subheader("💾 Backup Files")
    
    try:
        from src.services.backup_service import BackupService
        backup_service = BackupService()
        
        # List available backups
        backups = backup_service.list_backups()
        
        if backups:
            st.write(f"Found {len(backups)} backup files:")
            
            for backup in backups[:10]:  # Show latest 10 backups
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{backup['filename']}**")
                
                with col2:
                    st.write(f"{backup['size_mb']:.1f} MB")
                
                with col3:
                    st.write(backup['created'].strftime("%Y-%m-%d %H:%M"))
                
                with col4:
                    # Download button for each backup
                    backup_path = config.EXPORTS_DIR / backup['filename']
                    if backup_path.exists():
                        with open(backup_path, 'rb') as f:
                            st.download_button(
                                "📥",
                                data=f.read(),
                                file_name=backup['filename'],
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"backup_{backup['filename']}"
                            )
        else:
            st.info("No backup files found")
            
            if st.button("🔄 Create Backup Now"):
                success = backup_service.create_manual_backup()
                if success:
                    st.success("✅ Backup created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Backup creation failed")
    
    except Exception as e:
        st.error(f"❌ Error accessing backups: {str(e)}")

def show_template_downloads():
    """Show template file downloads"""
    
    st.subheader("📄 Download Templates")
    st.info("Download templates for bulk data import")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Data Entry Templates")
        
        # Sales template
        if st.button("🛒 Sales Template", use_container_width=True):
            template_data = create_sales_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "📥 Download Sales Template",
                data=csv,
                file_name="sales_template.csv",
                mime="text/csv"
            )
        
        # Purchase template
        if st.button("📦 Purchase Template", use_container_width=True):
            template_data = create_purchase_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "📥 Download Purchase Template",
                data=csv,
                file_name="purchase_template.csv",
                mime="text/csv"
            )
    
    with col2:
        st.markdown("#### Inventory Templates")
        
        # Stock template
        if st.button("📊 Stock Template", use_container_width=True):
            template_data = create_stock_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "📥 Download Stock Template",
                data=csv,
                file_name="stock_template.csv",
                mime="text/csv"
            )
        
        # Production template
        if st.button("🏭 Production Template", use_container_width=True):
            template_data = create_production_template()
            csv = template_data.to_csv(index=False)
            st.download_button(
                "📥 Download Production Template", 
                data=csv,
                file_name="production_template.csv",
                mime="text/csv"
            )

def get_date_range(range_type):
    """Get start and end dates based on range type"""
    
    today = date.today()
    
    if range_type == "Today":
        return today, today
    elif range_type == "Last 7 Days":
        return today - timedelta(days=7), today
    elif range_type == "Last 30 Days":
        return today - timedelta(days=30), today
    elif range_type == "This Month":
        return today.replace(day=1), today
    else:
        return today - timedelta(days=30), today

def generate_report_data(report_type, start_date, end_date):
    """Generate report data based on type and date range"""
    
    try:
        excel_service = ExcelService()
        
        if report_type == "Stock Summary Report":
            return generate_stock_summary_report(excel_service)
        elif report_type == "Sales Report":
            return generate_sales_report(excel_service, start_date, end_date)
        elif report_type == "Purchase Report":
            return generate_purchase_report(excel_service, start_date, end_date)
        elif report_type == "Production Report":
            return generate_production_report(excel_service, start_date, end_date)
        elif report_type == "Financial Summary":
            return generate_financial_summary(excel_service, start_date, end_date)
        elif report_type == "Low Stock Alert Report":
            return generate_low_stock_report(excel_service)
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")
        return None

def generate_stock_summary_report(excel_service):
    """Generate stock summary report"""
    
    # Sample data - replace with actual Excel data
    stock_data = pd.DataFrame({
        'Product': [f'{w}kg Roasted Chana' for w in config.PRODUCT_WEIGHTS],
        'Current_Stock': [45, 120, 85, 30, 95],
        'Min_Stock': [50, 100, 80, 40, 80],
        'Max_Stock': [200, 300, 250, 150, 250],
        'Unit_Price': [w * 50 for w in config.PRODUCT_WEIGHTS],
        'Total_Value': [45*w*50, 120*w*50, 85*w*50, 30*w*50, 95*w*50 for w in config.PRODUCT_WEIGHTS],
        'Status': ['Low' if stock < min_stock else 'OK' for stock, min_stock in zip([45, 120, 85, 30, 95], [50, 100, 80, 40, 80])],
        'Last_Updated': [datetime.now().strftime('%Y-%m-%d %H:%M')] * len(config.PRODUCT_WEIGHTS)
    })
    
    return stock_data

def generate_sales_report(excel_service, start_date, end_date):
    """Generate sales report for date range"""
    
    # Sample data - replace with actual Excel data
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    sales_data = []
    
    for date in dates:
        for weight in config.PRODUCT_WEIGHTS:
            if pd.np.random.random() > 0.3:  # Random sales occurrence
                sales_data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Product': f'{weight}kg Roasted Chana',
                    'Quantity': pd.np.random.randint(1, 20),
                    'Unit_Price': weight * 50,
                    'Channel': pd.np.random.choice(config.SALES_CHANNELS),
                    'Order_ID': f'ORD-{pd.np.random.randint(100000, 999999)}',
                    'Total_Amount': pd.np.random.randint(1, 20) * weight * 50
                })
    
    return pd.DataFrame(sales_data)

def generate_purchase_report(excel_service, start_date, end_date):
    """Generate purchase report for date range"""
    
    # Sample data - replace with actual Excel data
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    purchase_data = []
    
    suppliers = ['Supplier A', 'Supplier B', 'Supplier C']
    
    for i, date in enumerate(dates):
        if i % 5 == 0:  # Purchase every 5 days
            purchase_data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Supplier': pd.np.random.choice(suppliers),
                'Material': 'Raw Chana',
                'Quantity_KG': pd.np.random.randint(50, 200),
                'Rate_Per_KG': pd.np.random.randint(40, 60),
                'Total_Amount': pd.np.random.randint(50, 200) * pd.np.random.randint(40, 60),
                'Invoice_Number': f'INV-{pd.np.random.randint(1000, 9999)}'
            })
    
    return pd.DataFrame(purchase_data)

def generate_production_report(excel_service, start_date, end_date):
    """Generate production report for date range"""
    
    # Sample data - replace with actual Excel data
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    production_data = []
    
    operators = ['Operator 1', 'Operator 2', 'Operator 3']
    
    for date in dates:
        if pd.np.random.random() > 0.2:  # Production most days
            production_data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Batch_Number': f'BATCH-{date.strftime("%Y%m%d")}-001',
                'Raw_Material_Used_KG': pd.np.random.randint(80, 120),
                'Total_Packets_Produced': pd.np.random.randint(200, 400),
                'Operator': pd.np.random.choice(operators),
                'Efficiency_Percent': pd.np.random.randint(85, 98),
                'Quality_Grade': pd.np.random.choice(['A', 'B'])
            })
    
    return pd.DataFrame(production_data)

def generate_financial_summary(excel_service, start_date, end_date):
    """Generate financial summary report"""
    
    # Sample data - replace with actual calculations
    financial_data = []
    
    total_sales = pd.np.random.randint(50000, 100000)
    total_purchases = pd.np.random.randint(20000, 40000)
    
    financial_data.append({
        'Metric': 'Total Sales Revenue',
        'Amount': total_sales,
        'Period': f'{start_date} to {end_date}'
    })
    
    financial_data.append({
        'Metric': 'Total Purchase Cost',
        'Amount': total_purchases,
        'Period': f'{start_date} to {end_date}'
    })
    
    financial_data.append({
        'Metric': 'Gross Profit',
        'Amount': total_sales - total_purchases,
        'Period': f'{start_date} to {end_date}'
    })
    
    return pd.DataFrame(financial_data)

def generate_low_stock_report(excel_service):
    """Generate low stock alert report"""
    
    # Sample data - replace with actual Excel data
    stock_data = generate_stock_summary_report(excel_service)
    low_stock = stock_data[stock_data['Status'] == 'Low']
    
    return low_stock

def create_excel_report(data, report_title):
    """Create Excel file from DataFrame"""
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name=report_title[:31], index=False)  # Excel sheet name limit
    
    output.seek(0)
    return output.getvalue()

def create_csv_report(data):
    """Create CSV file from DataFrame"""
    
    return data.to_csv(index=False)

def create_sales_template():
    """Create sales template DataFrame"""
    
    return pd.DataFrame({
        'date': ['2025-06-08'],
        'product_weight': ['1.0'],
        'quantity': [10],
        'unit_price': [100],
        'channel': ['Amazon FBA'],
        'order_id': ['ORD-001'],
        'customer_name': ['Customer Name (Optional)']
    })

def create_purchase_template():
    """Create purchase template DataFrame"""
    
    return pd.DataFrame({
        'date': ['2025-06-08'],
        'supplier_name': ['Supplier Name'],
        'material_type': ['Raw Chana'],
        'quantity_kg': [100],
        'rate_per_kg': [50],
        'total_amount': [5000],
        'invoice_number': ['INV-001'],
        'quality_grade': ['A']
    })

def create_stock_template():
    """Create stock template DataFrame"""
    
    return pd.DataFrame({
        'product_weight': [str(w) for w in config.PRODUCT_WEIGHTS],
        'opening_stock': [50, 100, 200, 75, 150],
        'date': ['2025-06-08'] * len(config.PRODUCT_WEIGHTS),
        'remarks': [''] * len(config.PRODUCT_WEIGHTS)
    })

def create_production_template():
    """Create production template DataFrame"""
    
    return pd.DataFrame({
        'date': ['2025-06-08'],
        'batch_number': ['BATCH-001'],
        'raw_material_used_kg': [100],
        'product_weight': ['1.0'],
        'packets_produced': [95],
        'operator_name': ['Operator Name'],
        'quality_grade': ['A'],
        'remarks': ['']
    })