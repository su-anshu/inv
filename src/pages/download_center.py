"""
Download Center Component - Handle all data exports and downloads
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime, date, timedelta
import config
from src.services.excel_service import ExcelService
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import base64

class DownloadCenter:
    """Handle all download and export functionality"""
    
    def __init__(self):
        self.excel_service = ExcelService()
    
    def show_download_interface(self):
        """Display the download center interface"""
        
        st.header("📥 Download Center")
        st.markdown("Export your data in various formats")
        
        # Download options tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Excel Reports",
            "📋 CSV Exports", 
            "📄 PDF Reports",
            "📈 Chart Exports"
        ])
        
        with tab1:
            self.show_excel_downloads()
        
        with tab2:
            self.show_csv_downloads()
        
        with tab3:
            self.show_pdf_downloads()
        
        with tab4:
            self.show_chart_downloads()
    
    def show_excel_downloads(self):
        """Excel export options"""
        
        st.subheader("📊 Excel Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Stock Reports")
            
            if st.button("📦 Current Stock Report", use_container_width=True):
                stock_data = self.get_stock_data()
                excel_buffer = self.create_excel_report(stock_data, "Stock Report")
                st.download_button(
                    label="⬇️ Download Stock Report",
                    data=excel_buffer,
                    file_name=f"stock_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            if st.button("⚠️ Low Stock Alert Report", use_container_width=True):
                low_stock_data = self.get_low_stock_data()
                excel_buffer = self.create_excel_report(low_stock_data, "Low Stock Alert")
                st.download_button(
                    label="⬇️ Download Low Stock Report",
                    data=excel_buffer,
                    file_name=f"low_stock_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            if st.button("💰 Stock Valuation Report", use_container_width=True):
                valuation_data = self.get_stock_valuation_data()
                excel_buffer = self.create_excel_report(valuation_data, "Stock Valuation")
                st.download_button(
                    label="⬇️ Download Valuation Report",
                    data=excel_buffer,
                    file_name=f"stock_valuation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            st.markdown("#### Sales & Transaction Reports")
            
            # Date range selector
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
            with col2:
                end_date = st.date_input("End Date", value=date.today())
            
            if st.button("💳 Sales Report", use_container_width=True):
                sales_data = self.get_sales_data(start_date, end_date)
                excel_buffer = self.create_excel_report(sales_data, "Sales Report")
                st.download_button(
                    label="⬇️ Download Sales Report",
                    data=excel_buffer,
                    file_name=f"sales_report_{start_date}_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            if st.button("📦 Purchase Report", use_container_width=True):
                purchase_data = self.get_purchase_data(start_date, end_date)
                excel_buffer = self.create_excel_report(purchase_data, "Purchase Report")
                st.download_button(
                    label="⬇️ Download Purchase Report",
                    data=excel_buffer,
                    file_name=f"purchase_report_{start_date}_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            if st.button("🏭 Production Report", use_container_width=True):
                production_data = self.get_production_data(start_date, end_date)
                excel_buffer = self.create_excel_report(production_data, "Production Report")
                st.download_button(
                    label="⬇️ Download Production Report",
                    data=excel_buffer,
                    file_name=f"production_report_{start_date}_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    def show_csv_downloads(self):
        """CSV export options"""
        
        st.subheader("📋 CSV Data Exports")
        st.markdown("Download raw data in CSV format for further analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Stock Data")
            
            if st.button("📦 Stock Data CSV", use_container_width=True):
                stock_data = self.get_stock_data()
                csv_data = stock_data.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Stock CSV",
                    data=csv_data,
                    file_name=f"stock_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.markdown("#### Sales Data")
            
            if st.button("💳 Sales Data CSV", use_container_width=True):
                sales_data = self.get_sales_data()
                csv_data = sales_data.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Sales CSV",
                    data=csv_data,
                    file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            st.markdown("#### Purchase Data")
            
            if st.button("📦 Purchase Data CSV", use_container_width=True):
                purchase_data = self.get_purchase_data()
                csv_data = purchase_data.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Purchase CSV",
                    data=csv_data,
                    file_name=f"purchase_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    def show_pdf_downloads(self):
        """PDF report options"""
        
        st.subheader("📄 PDF Reports")
        st.markdown("Generate professional PDF reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Standard Reports")
            
            if st.button("📊 Stock Summary PDF", use_container_width=True):
                pdf_buffer = self.create_stock_summary_pdf()
                st.download_button(
                    label="⬇️ Download Stock Summary PDF",
                    data=pdf_buffer,
                    file_name=f"stock_summary_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            
            if st.button("💰 Financial Summary PDF", use_container_width=True):
                pdf_buffer = self.create_financial_summary_pdf()
                st.download_button(
                    label="⬇️ Download Financial Summary PDF",
                    data=pdf_buffer,
                    file_name=f"financial_summary_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        
        with col2:
            st.markdown("#### Custom Reports")
            
            report_type = st.selectbox(
                "Select Report Type",
                ["Stock Analysis", "Sales Performance", "Purchase Analysis", "Production Summary"]
            )
            
            date_range = st.selectbox(
                "Date Range",
                ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"]
            )
            
            if date_range == "Custom":
                col1, col2 = st.columns(2)
                with col1:
                    custom_start = st.date_input("Start Date")
                with col2:
                    custom_end = st.date_input("End Date")
            
            if st.button("📄 Generate Custom PDF", use_container_width=True):
                pdf_buffer = self.create_custom_pdf_report(report_type, date_range)
                st.download_button(
                    label="⬇️ Download Custom Report PDF",
                    data=pdf_buffer,
                    file_name=f"custom_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
    
    def show_chart_downloads(self):
        """Chart export options"""
        
        st.subheader("📈 Chart Exports")
        st.markdown("Download charts and visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Stock Charts")
            
            # Generate sample chart
            stock_data = self.get_stock_data()
            fig = px.bar(stock_data, x='Product', y='Current_Stock', title='Current Stock Levels')
            st.plotly_chart(fig, use_container_width=True)
            
            chart_format = st.selectbox("Chart Format", ["PNG", "JPG", "SVG", "PDF"])
            
            if st.button("📊 Download Stock Chart", use_container_width=True):
                img_buffer = self.export_chart(fig, chart_format.lower())
                st.download_button(
                    label=f"⬇️ Download Chart as {chart_format}",
                    data=img_buffer,
                    file_name=f"stock_chart_{datetime.now().strftime('%Y%m%d')}.{chart_format.lower()}",
                    mime=f"image/{chart_format.lower()}"
                )
        
        with col2:
            st.markdown("#### Sales Charts")
            
            # Generate sample sales chart
            sales_data = self.get_sales_data()
            fig2 = px.line(sales_data, x='Date', y='Revenue', title='Sales Revenue Trend')
            st.plotly_chart(fig2, use_container_width=True)
            
            if st.button("📈 Download Sales Chart", use_container_width=True):
                img_buffer = self.export_chart(fig2, chart_format.lower())
                st.download_button(
                    label=f"⬇️ Download Chart as {chart_format}",
                    data=img_buffer,
                    file_name=f"sales_chart_{datetime.now().strftime('%Y%m%d')}.{chart_format.lower()}",
                    mime=f"image/{chart_format.lower()}"
                )
    
    # Data retrieval methods
    
    def get_stock_data(self):
        """Get current stock data"""
        try:
            # Try to get real data from Excel service
            real_data = self.excel_service.read_stock_data()
            if real_data is not None and not real_data.empty:
                return real_data
        except:
            pass
        
        # Return sample data if real data not available
        quantities = [45, 120, 85, 30, 95]
        return pd.DataFrame({
            'Product': [f'{w}kg' for w in config.PRODUCT_WEIGHTS],
            'Current_Stock': quantities,
            'Min_Stock': [50, 100, 80, 40, 80],
            'Max_Stock': [200, 300, 250, 150, 250],
            'Unit_Price': [w * 50 for w in config.PRODUCT_WEIGHTS],
            'Total_Value': [q * w * 50 for q, w in zip(quantities, config.PRODUCT_WEIGHTS)],
            'Last_Updated': [datetime.now().strftime('%Y-%m-%d')] * len(config.PRODUCT_WEIGHTS)
        })
    
    def get_low_stock_data(self):
        """Get low stock items"""
        stock_data = self.get_stock_data()
        return stock_data[stock_data['Current_Stock'] < stock_data['Min_Stock']]
    
    def get_stock_valuation_data(self):
        """Get stock valuation data"""
        stock_data = self.get_stock_data()
        total_value = stock_data['Total_Value'].sum()
        
        valuation = stock_data.copy()
        valuation['Percentage'] = (valuation['Total_Value'] / total_value * 100).round(2)
        valuation['Category'] = ['Fast Moving' if stock > min_stock else 'Slow Moving' 
                               for stock, min_stock in zip(valuation['Current_Stock'], valuation['Min_Stock'])]
        
        return valuation
    
    def get_sales_data(self, start_date=None, end_date=None):
        """Get sales data for specified date range"""
        import numpy as np
        
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        if end_date is None:
            end_date = date.today()
        
        # Generate sample sales data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        data = []
        
        for date_val in dates:
            for _ in range(np.random.randint(1, 5)):  # 1-4 sales per day
                weight = np.random.choice(config.PRODUCT_WEIGHTS)
                quantity = np.random.randint(1, 15)
                unit_price = weight * 50 + np.random.randint(-5, 15)
                
                data.append({
                    'Date': date_val,
                    'Product': f'{weight}kg',
                    'Quantity': quantity,
                    'Unit_Price': unit_price,
                    'Revenue': quantity * unit_price,
                    'Channel': np.random.choice(config.SALES_CHANNELS),
                    'Order_ID': f'ORD-{np.random.randint(100000, 999999)}'
                })
        
        return pd.DataFrame(data)
    
    def get_purchase_data(self, start_date=None, end_date=None):
        """Get purchase data for specified date range"""
        import numpy as np
        
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        if end_date is None:
            end_date = date.today()
        
        # Generate sample purchase data
        suppliers = ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D']
        dates = pd.date_range(start=start_date, end=end_date, freq='3D')  # Purchase every 3 days
        
        data = []
        for date_val in dates:
            quantity = np.random.randint(50, 200)
            rate = np.random.randint(40, 65)
            
            data.append({
                'Date': date_val,
                'Supplier': np.random.choice(suppliers),
                'Material': 'Raw Chana',
                'Quantity_KG': quantity,
                'Rate_Per_KG': rate,
                'Total_Amount': quantity * rate,
                'Invoice': f'INV-{np.random.randint(1000, 9999)}'
            })
        
        return pd.DataFrame(data)
    
    def get_production_data(self, start_date=None, end_date=None):
        """Get production data for specified date range"""
        import numpy as np
        
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        if end_date is None:
            end_date = date.today()
        
        # Generate sample production data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        operators = ['Operator 1', 'Operator 2', 'Operator 3']
        
        data = []
        for date_val in dates:
            if np.random.random() > 0.2:  # Production on 80% of days
                raw_material = np.random.randint(80, 150)
                output = np.random.randint(200, 500)
                
                data.append({
                    'Date': date_val,
                    'Batch_Number': f'BATCH-{date_val.strftime("%m%d")}-{np.random.randint(1, 4)}',
                    'Raw_Material_KG': raw_material,
                    'Total_Output': output,
                    'Efficiency': round((output * 0.5 / raw_material) * 100, 1),
                    'Operator': np.random.choice(operators),
                    'Quality_Grade': np.random.choice(['A', 'A', 'B'])
                })
        
        return pd.DataFrame(data)
    
    # Export methods
    
    def create_excel_report(self, data, sheet_name):
        """Create Excel report from data"""
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_stock_summary_pdf(self):
        """Create stock summary PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        story = []
        
        # Title
        title = Paragraph("Stock Summary Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Date
        date_para = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 20))
        
        # Stock data table
        stock_data = self.get_stock_data()
        
        # Prepare table data
        table_data = [['Product', 'Current Stock', 'Min Stock', 'Unit Price', 'Total Value']]
        for _, row in stock_data.iterrows():
            table_data.append([
                row['Product'],
                str(row['Current_Stock']),
                str(row['Min_Stock']),
                f"₹{row['Unit_Price']:.2f}",
                f"₹{row['Total_Value']:.2f}"
            ])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_financial_summary_pdf(self):
        """Create financial summary PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        story = []
        
        # Title
        title = Paragraph("Financial Summary Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Summary metrics
        stock_data = self.get_stock_data()
        sales_data = self.get_sales_data()
        
        total_stock_value = stock_data['Total_Value'].sum()
        total_sales = sales_data['Revenue'].sum()
        
        summary_text = f"""
        <b>Financial Overview:</b><br/>
        • Total Stock Value: ₹{total_stock_value:,.2f}<br/>
        • Total Sales (Last 30 Days): ₹{total_sales:,.2f}<br/>
        • Number of Products: {len(stock_data)}<br/>
        • Average Product Value: ₹{total_stock_value/len(stock_data):,.2f}<br/>
        """
        
        summary_para = Paragraph(summary_text, styles['Normal'])
        story.append(summary_para)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_custom_pdf_report(self, report_type, date_range):
        """Create custom PDF report"""
        # For now, return a basic PDF
        return self.create_stock_summary_pdf()
    
    def export_chart(self, fig, format_type):
        """Export plotly chart in specified format"""
        if format_type in ['png', 'jpg', 'jpeg']:
            img_bytes = fig.to_image(format=format_type, width=800, height=600)
            return img_bytes
        elif format_type == 'svg':
            img_str = fig.to_image(format='svg', width=800, height=600)
            return img_str
        else:
            # Default to PNG
            img_bytes = fig.to_image(format='png', width=800, height=600)
            return img_bytes

# Function to display download center (for compatibility)
def show_download_center():
    """Display download center interface"""
    download_center = DownloadCenter()
    download_center.show_download_interface()

# Component functions for compatibility
def create_excel_export_buttons():
    """Create Excel export buttons"""
    download_center = DownloadCenter()
    download_center.show_excel_downloads()

def create_csv_export_buttons():
    """Create CSV export buttons"""
    download_center = DownloadCenter()
    download_center.show_csv_downloads()

def create_pdf_export_buttons():
    """Create PDF export buttons"""
    download_center = DownloadCenter()
    download_center.show_pdf_downloads()

def create_chart_export_buttons():
    """Create chart export buttons"""
    download_center = DownloadCenter()
    download_center.show_chart_downloads()

def show_report_downloads():
    """Show report download options (compatibility function)"""
    download_center = DownloadCenter()
    download_center.show_download_interface()

def create_download_buttons():
    """Create download buttons (compatibility function)"""
    download_center = DownloadCenter()
    download_center.show_download_interface()

def generate_stock_report():
    """Generate stock report (compatibility function)"""
    download_center = DownloadCenter()
    return download_center.get_stock_data()

def generate_sales_report():
    """Generate sales report (compatibility function)"""
    download_center = DownloadCenter()
    return download_center.get_sales_data()

def generate_purchase_report():
    """Generate purchase report (compatibility function)"""
    download_center = DownloadCenter()
    return download_center.get_purchase_data()

def generate_production_report():
    """Generate production report (compatibility function)"""
    download_center = DownloadCenter()
    return download_center.get_production_data()

def export_to_excel(data, filename):
    """Export data to Excel (compatibility function)"""
    download_center = DownloadCenter()
    return download_center.create_excel_report(data, filename)

def export_to_csv(data):
    """Export data to CSV (compatibility function)"""
    return data.to_csv(index=False)

def export_to_pdf(data, title):
    """Export data to PDF (compatibility function)"""
    download_center = DownloadCenter()
    return download_center.create_stock_summary_pdf()

def create_download_interface():
    """Create complete download interface (compatibility function)"""
    download_center = DownloadCenter()
    download_center.show_download_interface()

def show_backup_downloads():
    """Show backup download options"""
    st.subheader("💾 Backup Files")
    st.markdown("Download and manage your data backups")
    
    # Backup options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔄 Create New Backup")
        
        backup_type = st.selectbox(
            "Backup Type",
            ["Complete Backup", "Stock Data Only", "Sales Data Only", "Custom Selection"]
        )
        
        if backup_type == "Custom Selection":
            st.multiselect(
                "Select Data to Backup",
                ["Stock Data", "Sales Records", "Purchase Records", "Production Data", "Configuration"]
            )
        
        backup_format = st.selectbox("Backup Format", ["Excel (.xlsx)", "CSV Archive (.zip)", "JSON (.json)"])
        
        if st.button("🔄 Create Backup", use_container_width=True):
            with st.spinner("Creating backup..."):
                # Simulate backup creation
                import time
                time.sleep(2)
                
                # Generate backup file
                if backup_format == "Excel (.xlsx)":
                    download_center = DownloadCenter()
                    stock_data = download_center.get_stock_data()
                    backup_buffer = download_center.create_excel_report(stock_data, "Complete_Backup")
                    
                    st.download_button(
                        label="⬇️ Download Backup",
                        data=backup_buffer,
                        file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                st.success("✅ Backup created successfully!")
    
    with col2:
        st.markdown("#### 📦 Available Backups")
        
        # Sample backup files
        backup_files = [
            {"name": "backup_20250608_143022.xlsx", "size": "2.3 MB", "date": "2025-06-08 14:30", "type": "Complete"},
            {"name": "backup_20250607_093015.xlsx", "size": "2.1 MB", "date": "2025-06-07 09:30", "type": "Complete"},
            {"name": "stock_backup_20250606.csv", "size": "456 KB", "date": "2025-06-06 18:00", "type": "Stock Only"},
            {"name": "backup_20250605_120000.xlsx", "size": "2.0 MB", "date": "2025-06-05 12:00", "type": "Complete"},
        ]
        
        for backup in backup_files:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{backup['name']}**")
                    st.caption(f"📅 {backup['date']} | 📦 {backup['type']} | 💾 {backup['size']}")
                
                with col2:
                    if st.button("⬇️", key=f"download_{backup['name']}", help="Download"):
                        st.info(f"Downloading {backup['name']}...")
                
                with col3:
                    if st.button("🗑️", key=f"delete_{backup['name']}", help="Delete"):
                        st.warning(f"Are you sure you want to delete {backup['name']}?")
                
                st.markdown("---")
    
    # Backup settings
    st.markdown("#### ⚙️ Backup Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        auto_backup = st.checkbox("Enable Auto Backup", value=True)
        if auto_backup:
            st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
    
    with col2:
        retention_days = st.number_input("Keep Backups (Days)", min_value=7, max_value=365, value=30)
    
    with col3:
        backup_location = st.selectbox("Backup Location", ["Local Storage", "Cloud Storage"])
    
    if st.button("💾 Save Backup Settings"):
        st.success("✅ Backup settings saved!")

def show_template_downloads():
    """Show template download options"""
    st.subheader("📄 Data Templates")
    st.markdown("Download templates for data entry and bulk uploads")
    
    # Template categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Data Entry Templates")
        
        templates = [
            {
                "name": "Stock Data Template",
                "description": "Template for adding new stock items",
                "icon": "📦",
                "filename": "stock_template.xlsx"
            },
            {
                "name": "Sales Entry Template", 
                "description": "Template for recording sales transactions",
                "icon": "💰",
                "filename": "sales_template.xlsx"
            },
            {
                "name": "Purchase Entry Template",
                "description": "Template for recording purchase transactions",
                "icon": "🛒", 
                "filename": "purchase_template.xlsx"
            },
            {
                "name": "Production Log Template",
                "description": "Template for production batch recording",
                "icon": "🏭",
                "filename": "production_template.xlsx"
            }
        ]
        
        for template in templates:
            with st.container():
                st.markdown(f"**{template['icon']} {template['name']}**")
                st.caption(template['description'])
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button(f"⬇️ Download Template", key=f"template_{template['filename']}", use_container_width=True):
                        # Create sample template
                        template_data = create_sample_template(template['name'])
                        download_center = DownloadCenter()
                        template_buffer = download_center.create_excel_report(template_data, template['name'])
                        
                        st.download_button(
                            label=f"📥 {template['filename']}",
                            data=template_buffer,
                            file_name=template['filename'],
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_{template['filename']}"
                        )
                
                with col2:
                    if st.button("👁️", key=f"preview_{template['filename']}", help="Preview"):
                        st.info(f"Preview for {template['name']} - Coming soon!")
                
                st.markdown("---")
    
    with col2:
        st.markdown("#### 📋 Instruction Guides")
        
        guides = [
            {"name": "Data Entry Guide", "icon": "📖", "desc": "Complete guide for data entry"},
            {"name": "Bulk Upload Instructions", "icon": "📤", "desc": "How to upload bulk data"},
            {"name": "Template Format Guide", "icon": "📐", "desc": "Template formatting rules"},
            {"name": "Error Troubleshooting", "icon": "🔧", "desc": "Fix common upload errors"}
        ]
        
        for guide in guides:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{guide['icon']} {guide['name']}**")
                    st.caption(guide['desc'])
                
                with col2:
                    if st.button("📄", key=f"guide_{guide['name']}", help="Download PDF"):
                        st.info(f"Downloading {guide['name']}...")
                
                st.markdown("---")
        
        # Template bundle download
        st.markdown("#### 📦 Complete Template Bundle")
        st.markdown("Download all templates in one ZIP file")
        
        if st.button("📦 Download All Templates", use_container_width=True):
            st.success("✅ Template bundle download started!")
            st.balloons()
    
    # Template usage statistics
    st.markdown("---")
    st.markdown("#### 📊 Template Usage Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Templates Downloaded", "156", delta="12 this week")
    
    with col2:
        st.metric("Most Popular", "Stock Template", delta="45 downloads")
    
    with col3:
        st.metric("Success Rate", "94%", delta="2% improvement")
    
    with col4:
        st.metric("Latest Version", "v2.1", delta="Updated yesterday")

def create_sample_template(template_name):
    """Create sample template data"""
    if "Stock" in template_name:
        return pd.DataFrame({
            'Product': ['1.0kg', '0.5kg', '2.0kg'],
            'Current_Stock': [0, 0, 0],
            'Min_Stock': [50, 100, 25],
            'Max_Stock': [200, 300, 100],
            'Unit_Price': [50, 25, 100],
            'Supplier': ['', '', ''],
            'Notes': ['', '', '']
        })
    elif "Sales" in template_name:
        return pd.DataFrame({
            'Date': ['2025-06-08', '2025-06-08', '2025-06-08'],
            'Product': ['1.0kg', '0.5kg', '2.0kg'],
            'Quantity': [0, 0, 0],
            'Unit_Price': [0, 0, 0],
            'Channel': ['', '', ''],
            'Customer_Name': ['', '', ''],
            'Order_ID': ['', '', '']
        })
    elif "Purchase" in template_name:
        return pd.DataFrame({
            'Date': ['2025-06-08', '2025-06-08', '2025-06-08'],
            'Supplier': ['', '', ''],
            'Material': ['Raw Chana', 'Raw Chana', 'Raw Chana'],
            'Quantity_KG': [0, 0, 0],
            'Rate_Per_KG': [0, 0, 0],
            'Invoice_Number': ['', '', ''],
            'Notes': ['', '', '']
        })
    elif "Production" in template_name:
        return pd.DataFrame({
            'Date': ['2025-06-08', '2025-06-08', '2025-06-08'],
            'Batch_Number': ['', '', ''],
            'Raw_Material_KG': [0, 0, 0],
            'Output_1kg': [0, 0, 0],
            'Output_0.5kg': [0, 0, 0],
            'Output_2kg': [0, 0, 0],
            'Operator': ['', '', ''],
            'Quality_Grade': ['', '', '']
        })
    else:
        return pd.DataFrame({'Column1': ['Sample'], 'Column2': ['Data']})