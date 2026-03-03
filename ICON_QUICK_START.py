"""
Quick Start Guide - Using the IconSystem

This guide shows how to use the new Font Awesome icon system in your app.
"""

# ============================================================================
# BASIC USAGE
# ============================================================================

import streamlit as st

# Example 1: Display a single icon
st.markdown(IconSystem.icon('rocket', 'large'), unsafe_allow_html=True)

# Example 2: Display icon with text (automatic combination)
st.markdown(IconSystem.text('chart', 'View Analytics'))

# Example 3: Use icon in a button
if st.button(IconSystem.text('download', 'Download Report')):
    print("Download clicked!")

# Example 4: Use icon in a header
st.markdown("<h2>" + IconSystem.icon('robot', 'large') + " My Dashboard</h2>", 
            unsafe_allow_html=True)

# Example 5: Use icon in markdown
st.markdown(f"{IconSystem.icon('check', 'small')} Task completed successfully!")

# ============================================================================
# ICON SIZES
# ============================================================================

# Three standard sizes for visual hierarchy:

# Large (1.5rem) - Main titles and emphasis
st.markdown(IconSystem.icon('robot', 'large') + " This is a large icon")

# Medium (1.2rem) - Section headers, important elements
st.markdown(IconSystem.icon('rocket', 'medium') + " This is a medium icon")

# Small (0.9rem) - Buttons, inline elements
st.markdown(IconSystem.icon('check', 'small') + " This is a small icon")

# ============================================================================
# AVAILABLE ICONS - QUICK REFERENCE
# ============================================================================

# Navigation & Branding
# - 'robot'       : Robot/AI agent
# - 'home'        : Home, main dashboard
# - 'settings'    : Settings, configuration
# - 'gear'        : Settings gear variant

# Charts & Visualization
# - 'chart'       : Bar chart
# - 'chart-line'  : Line chart, trends
# - 'area-chart'  : Area chart
# - 'pie-chart'   : Pie chart
# - 'trend'       : Upward trend arrow

# Data Operations
# - 'upload'      : File upload
# - 'download'    : File download
# - 'table'       : Data table, spreadsheet
# - 'database'    : Database, storage
# - 'file'        : Document file
# - 'folder'      : Directory, folder

# Actions & Controls
# - 'rocket'      : Launch, run analysis
# - 'magic'       : Auto-generate, create
# - 'refresh'     : Reload, refresh data
# - 'trash'       : Delete, clear
# - 'plus'        : Add, create new
# - 'edit'        : Edit, modify
# - 'copy'        : Copy, duplicate

# Search & Filter
# - 'search'      : Search, find
# - 'filter'      : Filter data
# - 'exchange'    : Compare, switch
# - 'target'      : Target, focus

# Status & Feedback
# - 'check'       : Success, active (green)
# - 'warning'     : Alert, caution (orange)
# - 'error'       : Error, failed (red)
# - 'info'        : Information, tip (blue)

# Intelligence
# - 'brain'       : AI, thinking, agents
# - 'code'        : Code, developer
# - 'microchip'   : Processor, computing
# - 'bolt'        : Power, speed, energy

# UI Elements
# - 'eye'         : View, visibility
# - 'heart'       : Favorite, important
# - 'star'        : Featured, rated
# - 'bookmark'    : Save, mark
# - 'lock'        : Security, locked
# - 'unlock'      : Unlocked, accessible
# - 'user'        : User, profile
# - 'bars'        : Menu, list
# - 'times'       : Close, cancel
# - 'spinner'     : Loading indicator

# ============================================================================
# REAL-WORLD EXAMPLES
# ============================================================================

# Example: Data Dashboard
def create_dashboard():
    """Create a dashboard with icons"""
    
    # Header with icon
    st.markdown("<h1>" + IconSystem.icon('robot', 'large') + " Analytics Dashboard</h1>", 
                unsafe_allow_html=True)
    
    # Tabs with icons
    tab1, tab2, tab3 = st.tabs([
        "📊 Analytics",
        "📈 Trends",
        "🧠 Insights"
    ])
    
    with tab1:
        st.markdown("<h3>" + IconSystem.icon('chart', 'medium') + " Data Overview</h3>", 
                    unsafe_allow_html=True)
        # Your content here
    
    with tab2:
        st.markdown("<h3>" + IconSystem.icon('chart-line', 'medium') + " Trend Analysis</h3>", 
                    unsafe_allow_html=True)
        # Your content here
    
    with tab3:
        st.markdown("<h3>" + IconSystem.icon('brain', 'medium') + " AI Insights</h3>", 
                    unsafe_allow_html=True)
        # Your content here

# Example: Status Messages
def show_status_messages():
    """Show different types of status messages"""
    
    st.success(IconSystem.text('check', 'Processing completed successfully'))
    st.warning(IconSystem.text('warning', 'Please review the data quality report'))
    st.error(IconSystem.text('error', 'An error occurred during analysis'))
    st.info(IconSystem.text('info', 'Click "Run" to start the analysis'))

# Example: Action Buttons
def create_action_buttons():
    """Create buttons with icons"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(IconSystem.text('upload', 'Upload Data')):
            print("Upload action triggered")
    
    with col2:
        if st.button(IconSystem.text('rocket', 'Run Analysis')):
            print("Analysis started")
    
    with col3:
        if st.button(IconSystem.text('download', 'Download')):
            print("Download initiated")

# Example: Data Table with Icons
def create_data_table():
    """Create a data table with icon headers"""
    
    st.markdown("<h3>" + IconSystem.icon('table', 'medium') + " Data Summary</h3>", 
                unsafe_allow_html=True)
    
    # Display your dataframe here
    # df = load_data()
    # st.dataframe(df)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

# You can customize icons further with custom CSS
st.markdown("""
    <style>
    .custom-icon {
        font-size: 2.5rem;
        color: #3b82f6;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Use custom styling
st.markdown('<span class="custom-icon"><i class="fas fa-star"></i></span> Custom Styled Icon', 
            unsafe_allow_html=True)

# ============================================================================
# ANIMATION
# ============================================================================

# Spinning icon (for loading)
st.markdown(IconSystem.icon('spinner', 'large') + " Processing...", 
            unsafe_allow_html=True)

# ============================================================================
# TIPS & TRICKS
# ============================================================================

# Tip 1: Combine multiple icons
combined = (IconSystem.icon('rocket', 'small') + " " + 
            IconSystem.icon('chart', 'small') + " " + 
            IconSystem.icon('check', 'small'))
st.markdown(combined, unsafe_allow_html=True)

# Tip 2: Use icons in expanders
with st.expander(IconSystem.text('filter', 'Advanced Options')):
    # Your options here
    pass

# Tip 3: Use icons in selectbox labels
option = st.selectbox(
    IconSystem.text('chart', 'Choose Visualization Type'),
    ['Bar Chart', 'Line Chart', 'Scatter Plot']
)

# Tip 4: Use icons in metric labels
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(IconSystem.text('rocket', 'Performance'), "95%")
with col2:
    st.metric(IconSystem.text('target', 'Accuracy'), "98.5%")
with col3:
    st.metric(IconSystem.text('rocket', 'Speed'), "2.3s")

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
If icons don't appear:

1. Make sure unsafe_allow_html=True is set in st.markdown()
   st.markdown(icon_html, unsafe_allow_html=True)

2. Check that the icon name exists in IconSystem.ICONS
   You can view available icons in ICON_UPGRADE.md

3. Verify Font Awesome CDN is loading (check browser console)
   The CDN is added automatically in the main app

4. Clear browser cache if icons still don't show

If you need to add a new icon:

1. Find the icon name at fontawesome.com
2. Add to IconSystem.ICONS dictionary:
   'my-new-icon': '<i class="fas fa-my-icon"></i>'
3. Use it: IconSystem.icon('my-new-icon', 'medium')
"""

# ============================================================================
# FURTHER READING
# ============================================================================

# See documentation files for more information:
# - ICON_UPGRADE.md          : Complete technical reference
# - icon_reference.html      : Visual icon gallery (open in browser)
# - ICON_UPGRADE_SUMMARY.md  : Overview of changes made
