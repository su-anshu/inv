"""
Inventory Management System - Main Application
Author: Your Name
Date: 2025-06-08
Version: 1.0.0
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import configuration and utilities
import config
from src.utils.helpers import initialize_session_state, load_custom_css, setup_logging
from src.components.sidebar import create_sidebar

# Import pages
from src.pages.dashboard import show_dashboard
from src.pages.data_entry import show_data_entry
from src.pages.reports import show_reports
from src.pages.download_center import show_download_center
from src.pages.settings import show_settings

# Page configuration
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/inventory-management',
        'Report a bug': 'https://github.com/your-repo/inventory-management/issues',
        'About': f"{config.APP_NAME} v{config.APP_VERSION}"
    }
)

def main():
    """Main application function"""
    
    try:
        # Initialize application
        initialize_session_state()
        setup_logging()
        load_custom_css()
        
        # Application header
        st.title(f"📦 {config.APP_NAME}")
        st.markdown(f"*{config.APP_DESCRIPTION}*")
        st.markdown("---")
        
        # Create sidebar navigation and get selected page
        selected_page = create_sidebar()
        
        # Route to selected page
        if selected_page == "📊 Dashboard":
            show_dashboard()
        elif selected_page == "📝 Data Entry":
            show_data_entry()
        elif selected_page == "📈 Reports & Analytics":
            show_reports()
        elif selected_page == "💾 Download Center":
            show_download_center()
        elif selected_page == "⚙️ Settings":
            show_settings()
        else:
            # Default to dashboard
            show_dashboard()
        
        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f"""
                <div style='text-align: center; color: #666; font-size: 0.9rem;'>
                    {config.APP_NAME} v{config.APP_VERSION} | 
                    Last Updated: {st.session_state.get('last_update', 'Never')} |
                    Status: <span style='color: green;'>🟢 Online</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.error("Please check the logs for more details.")
        
        # Show debug info in expander
        with st.expander("🔧 Debug Information"):
            st.write("**Error Details:**")
            st.code(str(e))
            st.write("**Python Path:**")
            st.code(str(sys.path))
            st.write("**Current Directory:**")
            st.code(str(Path.cwd()))

if __name__ == "__main__":
    main()