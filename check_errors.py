"""
Test to isolate if streamlit-option-menu is causing the JSON error
"""

import streamlit as st

def test_without_option_menu():
    """Test app without option menu"""
    st.set_page_config(page_title="Test", layout="wide")
    
    st.header("🧪 Test Without Option Menu")
    
    # Use regular selectbox instead
    selected = st.selectbox(
        "Navigation",
        ["Dashboard", "Stock Analysis", "Reports"]
    )
    
    if selected == "Stock Analysis":
        st.subheader("📊 Stock Analysis")
        
        # Simple test data
        import pandas as pd
        test_data = pd.DataFrame({
            'Product': ['0.5kg', '1.0kg', '2.0kg'],
            'Stock': [100, 200, 150]
        })
        
        st.dataframe(test_data)
        st.success("✅ This works without option menu!")

def test_with_option_menu():
    """Test app WITH option menu"""
    st.set_page_config(page_title="Test", layout="wide")
    
    try:
        from streamlit_option_menu import option_menu
        
        st.header("🧪 Test WITH Option Menu")
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Stock Analysis", "Reports"],
            icons=["house", "graph-up", "file-text"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
        
        if selected == "Stock Analysis":
            st.subheader("📊 Stock Analysis")
            
            # Simple test data
            import pandas as pd
            test_data = pd.DataFrame({
                'Product': ['0.5kg', '1.0kg', '2.0kg'],
                'Stock': [100, 200, 150]
            })
            
            st.dataframe(test_data)
            st.success("✅ Option menu works!")
            
    except Exception as e:
        st.error(f"❌ Option menu error: {e}")

# Test both versions
st.sidebar.title("Choose Test")
test_type = st.sidebar.radio("Test Type", ["Without Option Menu", "With Option Menu"])

if test_type == "Without Option Menu":
    test_without_option_menu()
else:
    test_with_option_menu()