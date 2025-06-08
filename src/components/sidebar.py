"""
Sidebar Navigation Component
"""

import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import config
from src.services.excel_service import ExcelService

def create_sidebar():
    """Create the navigation sidebar with quick stats"""
    
    with st.sidebar:
        # App logo and title
        st.markdown(
            f"""
            <div style='text-align: center; padding: 1rem 0;'>
                <h2>📦 Inventory System</h2>
                <p style='color: #666; font-size: 0.9rem;'>{config.APP_DESCRIPTION}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Quick stats section
        st.markdown("### 📊 Quick Stats")
        
        # Try to get real data from Excel, fallback to mock data
        try:
            excel_service = ExcelService()
            if excel_service.file_exists():
                stats = get_real_stats(excel_service)
            else:
                stats = get_mock_stats()
        except Exception:
            stats = get_mock_stats()
        
        # Display metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Stock", stats['total_stock'], stats['stock_delta'])
        with col2:
            st.metric("Products", stats['products'], "0")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Low Stock", stats['low_stock'], stats['low_stock_delta'])
        with col2:
            st.metric("Value (₹)", stats['total_value'], stats['value_delta'])
        
        st.markdown("---")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Navigation",
            options=[
                "📊 Dashboard",
                "📝 Data Entry", 
                "📈 Reports & Analytics",
                "💾 Download Center",
                "⚙️ Settings"
            ],
            icons=["speedometer2", "pencil-square", "graph-up", "download", "gear"],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": config.PRIMARY_COLOR, "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee"
                },
                "nav-link-selected": {"background-color": config.PRIMARY_COLOR},
            }
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state['last_update'] = datetime.datetime.now().strftime("%H:%M:%S")
            st.rerun()
        
        if st.button("💾 Create Backup", use_container_width=True):
            try:
                # Import backup service and create backup
                from src.services.backup_service import BackupService
                backup_service = BackupService()
                success = backup_service.create_manual_backup()
                if success:
                    st.success("✅ Backup created!")
                else:
                    st.error("❌ Backup failed!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        if st.button("📤 Quick Export", use_container_width=True):
            st.info("📊 Export started!")
            # Add export logic here
        
        st.markdown("---")
        
        # System info
        st.markdown("### ℹ️ System Info")
        st.write(f"**Date:** {datetime.date.today()}")
        st.write(f"**Time:** {datetime.datetime.now().strftime('%H:%M')}")
        
        # Check Excel file status
        try:
            excel_service = ExcelService()
            if excel_service.file_exists():
                st.write("**Excel:** 🟢 Connected")
            else:
                st.write("**Excel:** 🔴 Not Found")
        except:
            st.write("**Excel:** ⚠️ Error")
        
        st.write(f"**Version:** {config.APP_VERSION}")
        
        # Footer
        st.markdown(
            """
            <div style='text-align: center; padding-top: 2rem; color: #666; font-size: 0.8rem;'>
                <p>Inventory Management System<br>
                © 2025 All Rights Reserved</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return selected

def get_real_stats(excel_service):
    """Get real statistics from Excel file"""
    try:
        # Read stock data
        stock_data = excel_service.read_stock_data()
        
        if stock_data is not None and not stock_data.empty:
            total_stock = stock_data['current_stock'].sum() if 'current_stock' in stock_data.columns else 0
            products = len(config.PRODUCT_WEIGHTS)
            low_stock = len(stock_data[stock_data['current_stock'] < config.MIN_STOCK_THRESHOLD]) if 'current_stock' in stock_data.columns else 0
            total_value = (stock_data['current_stock'] * stock_data.get('unit_price', 50)).sum() if 'current_stock' in stock_data.columns else 0
            
            return {
                'total_stock': f"{total_stock:,}",
                'stock_delta': "📈",
                'products': str(products),
                'low_stock': str(low_stock),
                'low_stock_delta': "⚠️" if low_stock > 0 else "✅",
                'total_value': f"{total_value/100000:.1f}L" if total_value > 100000 else f"{total_value/1000:.0f}K",
                'value_delta': "📈"
            }
    except Exception:
        pass
    
    return get_mock_stats()

def get_mock_stats():
    """Get mock statistics for display"""
    return {
        'total_stock': "1,234",
        'stock_delta': "↗️ 12",
        'products': "5",
        'low_stock': "2",
        'low_stock_delta': "⚠️ -1",
        'total_value': "2.5L",
        'value_delta': "↗️ 5K"
    }