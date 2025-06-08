"""
Download Center Page - File downloads and exports
"""

import streamlit as st
from src.components.download_center import (
    show_report_downloads,
    show_backup_downloads,
    show_template_downloads
)

def show_download_center():
    """Display the download center with all download options"""
    
    st.header("💾 Download Center")
    st.markdown("Download reports, backups, and templates")
    
    # Navigation tabs for different download types
    tab1, tab2, tab3 = st.tabs([
        "📊 Reports & Exports",
        "💾 Backup Files", 
        "📄 Templates"
    ])
    
    with tab1:
        show_report_downloads()
    
    with tab2:
        show_backup_downloads()
    
    with tab3:
        show_template_downloads()
    
    # Quick actions section
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Stock Summary", use_container_width=True):
            st.info("📥 Generating stock summary report...")
    
    with col2:
        if st.button("💰 Sales Report", use_container_width=True):
            st.info("📥 Generating sales report...")
    
    with col3:
        if st.button("💾 Create Backup", use_container_width=True):
            st.info("💾 Creating backup file...")
    
    with col4:
        if st.button("📄 All Templates", use_container_width=True):
            st.info("📦 Preparing template bundle...")
    
    # Help section
    st.markdown("---")
    st.markdown("### ❓ Help & Instructions")
    
    with st.expander("📋 How to use the Download Center"):
        st.markdown("""
        **Reports & Exports:**
        - Select report type and date range
        - Choose export format (Excel, CSV, PDF)
        - Click Generate to create the report
        - Download will start automatically
        
        **Backup Files:**
        - View all available backup files
        - Download specific backup versions
        - Create new manual backups
        
        **Templates:**
        - Download data entry templates
        - Use templates for bulk uploads
        - Templates include sample data and instructions
        """)
    
    with st.expander("🔧 Troubleshooting"):
        st.markdown("""
        **Common Issues:**
        
        1. **Download not starting:**
           - Check your browser's download settings
           - Disable popup blockers for this site
           - Try a different browser
        
        2. **Empty or corrupt files:**
           - Ensure data exists for selected date range
           - Check Excel file connectivity
           - Try generating a smaller date range
        
        3. **Template format issues:**
           - Download fresh templates if having issues
           - Ensure you're using the latest template version
           - Check column names match exactly
        """)
    
    # Download history (if implemented)
    st.markdown("---")
    st.markdown("### 📜 Recent Downloads")
    st.info("Download history feature coming soon!")
    
    # Footer with storage info
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 0.9rem;'>
                💾 Storage: 45MB used | 📁 15 files available | 🔄 Last backup: 2 hours ago
            </div>
            """,
            unsafe_allow_html=True
        )