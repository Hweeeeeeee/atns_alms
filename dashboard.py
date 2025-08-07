import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from datetime import datetime, timedelta
import math # Import math for floor division

# Matplotlib font setting for Korean characters
plt.rcParams['font.family'] = 'Malgun Gothic' # For Windows
plt.rcParams['axes.unicode_minus'] = False # To prevent minus sign from breaking
# For macOS, you might use 'AppleGothic' or 'NanumGothic' if installed:
# plt.rcParams['font.family'] = 'AppleGothic'
# For Linux, you might need to install a font like 'NanumGothic' and configure it.

# Helper functions for date parsing and status determination
def parse_full_datetime(date_part, time_part):
    """Parses date and time strings (including 오전/오후) into a datetime object."""
    if pd.isna(date_part) or pd.isna(time_part):
        return None
    
    full_str = f"{date_part} {time_part}"
    try:
        if '오전' in full_str:
            return datetime.strptime(full_str.replace('오전 ', ''), '%Y-%m-%d %I:%M:%S')
        elif '오후' in full_str:
            return datetime.strptime(full_str.replace('오후 ', ''), '%Y-%m-%d %I:%M:%S')
        else: # Assume 24-hour if no 오전/오후 marker
            return datetime.strptime(full_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def parse_ymd_or_ym_date(date_str):
    """Parses YYYYMMDD or YYYYMM date strings into a datetime object."""
    if pd.isna(date_str) or date_str == '':
        return None
    s_date_str = str(date_str)
    try:
        if len(s_date_str) == 8: # YYYYMMDD
            return datetime.strptime(s_date_str, '%Y%m%d')
        elif len(s_date_str) == 6: # YYYYMM, default to first day of month
            return datetime.strptime(s_date_str + '01', '%Y%m%d')
    except ValueError:
        pass
    return None

def get_user_status_for_recent_activity(row):
    """Determines user status (Active, Expiring, Inactive) and expiry string."""
    today = datetime.now()
    
    last_logon_dt = parse_full_datetime(row['LASTLOGONDATE'], row['LASTLOGONTIME'])
    expiry_end_dt = parse_ymd_or_ym_date(row['EXPIRATIONENDDATE'])
    
    status_text = "Active"
    expiry_display = "Expires 9999.12.30" # Default for no specific expiry in CSV or very long expiry

    # Determine expiry display string
    if pd.notna(row['EXPIRATIONENDDATE']):
        if str(row['EXPIRATIONENDDATE']) == '99991230': # Special handling for "never expires"
            expiry_display = "Expires 9999.12.30"
        elif expiry_end_dt:
            expiry_display = f"Expires {expiry_end_dt.strftime('%Y.%m.%d')}"
    
    # Determine status based on the provided logic
    if expiry_end_dt and expiry_end_dt < today:
        status_text = "Inactive" # Expired
    elif last_logon_dt and last_logon_dt < today - timedelta(days=30):
        status_text = "Inactive" # No recent login for 30+ days
    elif expiry_end_dt and expiry_end_dt >= today and expiry_end_dt < today + timedelta(days=90):
        status_text = "Expiring" # Expiring within 90 days

    return status_text, expiry_display

# 페이지 설정 (한 번만 선언)
st.set_page_config(layout="wide")

# 헤더 및 메뉴바 스타일 정의
st.markdown("""
    <style>
        /* Overall page font setting */
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Content area background color change */
        .stApp {
            padding-top: 0px;
            background-color: #FFFFFF; /* Set content area background to white */
        }
        .header {
            background-color: white;
            border-bottom: 1px solid #d9d9d9;
            box-shadow: 0 3px 3px -3px rgba(0, 0, 0, 0.1);
            padding: 0.8rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 1rem;
            font-weight: bold;
            font-size: 18px;
        }
        .header-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .menu-bar {
            display: flex;
            gap: 2rem;
            padding: 0.5rem 2rem;
            background-color: white;
            border-bottom: 1px solid #d9d9d9;
            box-shadow: 0px 3px 3px -3px rgba(0,0,0,0.1);
            font-size: 16px;
            font-weight: 500;
        }
        .menu-item {
            padding-bottom: 0.25rem;
            cursor: pointer;
            color: #666;
        }
        .menu-item.active {
            color: #007BFF; /* SAP Blue */
            border-bottom: 2px solid #007BFF;
        }
        .search-box {
            padding: 4px 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        /* Widget common style - shadow and scroll prevention */
        div[data-testid="stVerticalBlock"] > div.st-emotion-cache-ocqkzj {
            box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important; /* Apply stronger shadow */
            overflow: hidden !important; /* Prevent internal scroll */
        }
        .section-title {
            font-size: 24px;
            font-weight: bold;
            margin: 2rem 0; /* Double top margin for section titles */
        }
        .widget-title {
            font-weight: bold;
            font-size: 18px;
            color: black;
            margin-bottom: 0.5rem; /* Reduced bottom margin for titles */
        }
        /* Style for div wrapping widget content */
        .widget-content {
            flex-grow: 1; /* Occupy remaining space */
            display: flex;
            flex-direction: column;
            justify-content: center; /* Vertically center */
            align-items: flex-start; /* Left align */
            padding-bottom: 0.5rem; /* Reduced bottom padding */
        }
        .stat-block {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            text-align: left;
            margin-bottom: 1rem;
            width: 100%; /* Ensure stat-block uses full width */
        }
        .stat-block > div {
            text-align: left;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
        }
        .stat-value {
            font-size: 18px;
            font-weight: bold;
        }
        .my-table {
            font-size: 14px;
            width: 100%;
        }
        .my-table td {
            padding: 4px 8px;
        }
        .big-number {
            font-size: 32px;
            font-weight: bold;
            text-align: left;
            margin-top: 0; /* Reset margin as Flexbox handles alignment */
        }
        .icon {
            font-size: 36px;
            text-align: left;
            margin-top: 0; /* Reset margin as Flexbox handles alignment */
        }
        .user-box {
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            background-color: white;
            padding: 0.5rem 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .user-icon {
            border: 1px solid;
            background-color: rgba(0,0,0,0.05); /* Transparent background */
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 12px;
            text-align: center;
        }
        .user-icon.Active {
            color: #007BFF; /* SAP Blue */
            border-color: #007BFF;
        }
        .user-icon.Expiring {
            color: #FFA500; /* Orange */
            border-color: #FFA500;
        }
        .user-icon.Inactive {
            color: #808080; /* Grey */
            border-color: #808080;
        }
        /* Matplotlib chart container style */
        .chart-container {
            flex-grow: 1; /* Set to fill remaining space */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        /* Add style for text above bar graph */
        .bar-container {
            position: relative;
            width: 100%;
            height: 20px; /* Set similar to bar graph height */
            margin-top: 10px; /* Adjust spacing from bar graph */
        }
        .bar-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-weight: bold;
            font-size: 16px; /* Adjust text size */
            z-index: 1; /* Ensure it's above the bar graph */
        }
        /* CSS modification for text and chart alignment in Composition widget */
        .composition-content {
            display: flex;
            align-items: center;
            justify-content: space-between; /* Distribute space between text and chart */
            flex-grow: 1; /* Set to fill remaining space */
            padding-top: 10px; /* Add top padding */
        }
        .composition-text {
            text-align: left;
            flex-shrink: 0; /* Prevent text from shrinking */
            margin-right: 10px; /* Spacing between text and chart */
        }
        .composition-text .percentage {
            font-size: 40px; /* 76% font size */
            font-weight: bold;
            color: #007BFF; /* SAP Blue */
        }
        .composition-text .description {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }
        /* CSS for User License Type items and value alignment */
        .license-type-row {
            display: flex;
            justify-content: space-between; /* Distribute label and value to ends */
            align-items: center;
            width: 100%;
            margin-bottom: 0.2rem; /* Reduced spacing between items */
        }
        .license-type-label {
            font-size: 16px;
            font-weight: bold;
            text-align: left; /* Left align label */
            flex-grow: 1; /* Label occupies space */
        }
        .license-type-value {
            font-size: 16px;
            font-weight: bold;
            text-align: right; /* Right align value */
            flex-shrink: 0; /* Prevent value from shrinking */
            color: #007BFF; /* Value color */
        }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="header">
    <div class="header-left">
        <img src="https://www.sap.com/dam/application/shared/logos/sap-logo-svg.svg" alt="SAP" width="60">
        FUE License Management
    </div>
    <div class="header-right">
        <input class="search-box" type="text" placeholder="Search...">
        🔔
        ⋯
        <img src="https://www.w3schools.com/howto/img_avatar.png" width="32" height="32" style="border-radius:50%;">
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- MENU BAR ----------
menu_items = ["Home", "FUE License", "User", "My Account"]
active = "Home"  # Currently selected menu

menu_html = '<div class="menu-bar">'
for item in menu_items:
    class_name = "menu-item active" if item == active else "menu-item"
    menu_html += f'<div class="{class_name}">{item}</div>'
menu_html += '</div>'
st.markdown(menu_html, unsafe_allow_html=True)

# Section title
st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

# Overview Section Widget Placement and Sizing
cols_overview_row1 = st.columns([2, 2, 2]) 

# Widget 1: FUE License Status (2x2 size)
with cols_overview_row1[0]:
    with st.container(height=360, border=True): # 2x2 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">FUE License Status</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown("""
            <div class="stat-block">
                <div><div class="stat-label">Active Licenses</div><div class="stat-value">292</div></div>
                <div><div class="stat-label">Total License</div><div class="stat-value">500</div></div>
                <div><div class="stat-value">Transaction Based</div><div class="stat-value">271</div></div>
            </div>
            <hr style="margin: 1rem 0;">
        """, unsafe_allow_html=True)

        active_pct = 292 / 500 * 100
        fig1, ax1 = plt.subplots(figsize=(3, 3)) # Maintain 1:1 ratio
        colors = ['#007BFF', '#FFA500']
        ax1.pie([active_pct, 100 - active_pct], labels=[f'Active ({active_pct:.1f}%)', 'Remaining'], autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.set_aspect('equal')
        st.pyplot(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Widget 2: FUE Active License Variance (2x2 size)
with cols_overview_row1[1]:
    with st.container(height=360, border=True): # 2x2 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">FUE Active License Variance</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)

        base = 292
        months = ['Apr', 'May', 'Jun', 'Jul'] # Months in English
        values = [base]
        for _ in range(3):
            base *= np.random.uniform(0.85, 0.95)
            values.insert(0, int(base))

        fig3, ax3 = plt.subplots(figsize=(4, 3)) # Adjust to near 1:1 ratio
        bar_colors = ['#D3D3D3'] * (len(months) - 1) + ['#007BFF']
        ax3.bar(months, values, color=bar_colors)
        ax3.set_ylabel("Licenses")
        ax3.set_title("Active Licenses in Last 4 Months") # Title in English
        st.pyplot(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Widget 3: My Account (2x1 size) - Placed in the first row
with cols_overview_row1[2]:
    with st.container(height=180, border=True): # 2x1 ratio (width:height = 2:1)
        st.markdown('<div class="widget-title">My Account</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown("""
            <table class="my-table">
                <tr><td><strong>License Type</strong></td><td>ATNS ALMS License</td></tr>
                <tr><td><strong>FUE</strong></td><td>500</td></tr>
                <tr><td><strong>Expiration</strong></td><td>2027.12.31</td></tr>
            </table>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# FUE License Section (Order change and size/position adjustment)
st.markdown('<div class="section-title">FUE License</div>', unsafe_allow_html=True)

# CSV file data loading and preprocessing for user_count
df_users = pd.DataFrame() # Initialize as empty DataFrame
user_count = 0
inactive_users_count = 0
recent_users_data = []

# Initialize two separate dictionaries for license counts
calculated_fue_license_counts = {} # For FUE License section calculations
raw_user_license_counts = {}     # For User section's User License Type widget

try:
    df_users = pd.read_csv('zalmt0020.csv', encoding='euc-kr') # Use euc-kr encoding
    
    # Clean USERID for accurate unique count
    if 'USERID' in df_users.columns:
        df_users['USERID'] = df_users['USERID'].astype(str).str.strip()
        user_count = df_users['USERID'].nunique()
    else:
        st.warning("No 'USERID' column in zalmt0020.csv. Using default value 902 for Total User Count.")
        user_count = 902 

    # Get raw counts from the CSV's ROLETYPID column for User section
    df_users['CLEANED_ROLETYPID'] = df_users['ROLETYPID'].astype(str).str.strip()
    
    raw_advanced_count_user_section = df_users[df_users['CLEANED_ROLETYPID'] == 'GB Advanced Use']['USERID'].nunique()
    raw_core_count_user_section = df_users[df_users['CLEANED_ROLETYPID'] == 'GC Core Use']['USERID'].nunique()
    raw_self_service_count_user_section = df_users[df_users['CLEANED_ROLETYPID'] == 'GD Self-Service Use']['USERID'].nunique()
    raw_not_classified_count_user_section = df_users[df_users['CLEANED_ROLETYPID'] == 'Not classified']['USERID'].nunique()

    raw_user_license_counts = {
        'Advanced': raw_advanced_count_user_section,
        'Core': raw_core_count_user_section,
        'Self Service': raw_self_service_count_user_section,
        'Not Classified': raw_not_classified_count_user_section
    }

    # Calculate license_type_counts based on new formulas for FUE License section
    # Use the raw counts from the CSV for the base of these calculations
    calculated_advanced_fue = raw_advanced_count_user_section * 1
    calculated_core_fue = raw_core_count_user_section // 5
    calculated_self_service_fue = raw_self_service_count_user_section // 30
    calculated_not_classified_fue = 0 # As per user's explicit request

    calculated_fue_license_counts = {
        'Advanced': calculated_advanced_fue,
        'Core': calculated_core_fue,
        'Self Service': calculated_self_service_fue,
        'Not Classified': calculated_not_classified_fue
    }

    # (1) Active License - Sum of calculated values for FUE section
    active_license_count = sum(calculated_fue_license_counts.values())
    
    # (2) Remaining License - Total License (500) - Active License
    total_license_capacity = 500 # Assuming total capacity is 500
    remaining_license_count = total_license_capacity - active_license_count

    # (3) License Utilization Rate - Active License / Total License
    license_utilization_rate = (active_license_count / total_license_capacity) * 100 if total_license_capacity > 0 else 0


    # (2) Inactive Users - Count users whose LASTLOGONDATE is older than 30 days from today
    if 'LASTLOGONDATE' in df_users.columns and 'LASTLOGONTIME' in df_users.columns:
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        # Parse LASTLOGONDATE and LASTLOGONTIME
        df_users['LAST_LOGON_DATETIME'] = df_users.apply(
            lambda row: parse_full_datetime(row['LASTLOGONDATE'], row['LASTLOGONTIME']), axis=1
        )
        
        # Count inactive users (last logon older than 30 days)
        inactive_users_df = df_users[
            (df_users['LAST_LOGON_DATETIME'].notna()) & 
            (df_users['LAST_LOGON_DATETIME'] < thirty_days_ago)
        ]
        inactive_users_count = inactive_users_df['USERID'].nunique()
    else:
        st.warning("Missing 'LASTLOGONDATE' or 'LASTLOGONTIME' columns for Inactive Users calculation. Using default value 19.")
        inactive_users_count = 19 # Default if columns are missing

    # (3) Recent User Activity - Top 5 users whose EXPIRATIONENDDATE has passed, or are Inactive, or have EXPIRATIONSTARTDATE
    if 'EXPIRATIONENDDATE' in df_users.columns and 'EXPIRATIONSTARTDATE' in df_users.columns and 'LASTLOGONDATE' in df_users.columns and 'LASTLOGONTIME' in df_users.columns and 'LASTNAME' in df_users.columns and 'FIRSTNAME' in df_users.columns and 'ROLETYPID' in df_users.columns:
        
        # Filter users based on conditions
        df_users['EXPIRY_END_DATETIME'] = df_users['EXPIRATIONENDDATE'].apply(parse_ymd_or_ym_date)
        df_users['EXPIRY_START_DATETIME'] = df_users['EXPIRATIONSTARTDATE'].apply(parse_ymd_or_ym_date)

        # Condition 1: EXPIRATIONENDDATE is in the past
        cond_expired = (df_users['EXPIRY_END_DATETIME'].notna()) & (df_users['EXPIRY_END_DATETIME'] < today)

        # Condition 2: User is "Inactive" (last logon older than 30 days)
        cond_inactive_by_logon = (df_users['LAST_LOGON_DATETIME'].notna()) & (df_users['LAST_LOGON_DATETIME'] < today - timedelta(days=30))

        # Condition 3: EXPIRATIONSTARTDATE exists
        cond_has_start_date = df_users['EXPIRY_START_DATETIME'].notna()
        
        # Combine unique USERIDs from all conditions
        # Ensure we only consider unique users for the recent activity list
        relevant_users_df = df_users[cond_expired | cond_inactive_by_logon | cond_has_start_date].copy()
        
        # Sort by LAST_LOGON_DATETIME (descending) and take top 5 unique users
        # Fill NA datetimes with a very old date so they sort last if no logon date
        relevant_users_df['LAST_LOGON_DATETIME_SORT'] = relevant_users_df['LAST_LOGON_DATETIME'].fillna(datetime(1900, 1, 1))
        relevant_users_df.sort_values(by='LAST_LOGON_DATETIME_SORT', ascending=False, inplace=True)
        
        # Get top 5 unique users based on USERID
        recent_unique_users = relevant_users_df.drop_duplicates(subset=['USERID']).head(5)

        # Prepare data for display
        recent_users_data = [] # Clear previous data
        for index, row in recent_unique_users.iterrows():
            name_part = str(row['LASTNAME']).strip()
            first_name_part = str(row['FIRSTNAME']).strip()
            full_name = f"{name_part}{first_name_part}" if name_part and first_name_part else name_part or first_name_part or row['USERID']
            
            status_text, expiry_display = get_user_status_for_recent_activity(row)
            
            recent_users_data.append((full_name, row['ROLETYPID'], expiry_display, status_text)) # Use ROLETYPID for grade
    else:
        st.warning("Missing columns for Recent User Activity calculation. Using hardcoded data.")
        recent_users_data = [
            ("Kim Hwi-young", "GB Advanced User", "Expires 9999.12.30", "Active"),
            ("Lee Min", "GB Advanced User", "Expires 9999.12.30", "Active"),
            ("Jung Ha-na", "GB Core User", "Expires 2026.11.03", "Expiring"),
            ("Park Soo-bin", "GB Self Service", "Expires 2024.08.10", "Inactive"),
            ("Yoon Tae", "GB Advanced User", "Expires 9999.12.30", "Active")
        ]

except FileNotFoundError:
    st.error("zalmt0020.csv file not found. Using default values for some widgets.")
    user_count = 902
    inactive_users_count = 19
    recent_users_data = [
        ("Kim Hwi-young", "GB Advanced User", "Expires 9999.12.30", "Active"),
        ("Lee Min", "GB Advanced User", "Expires 9999.12.30", "Active"),
        ("Jung Ha-na", "GB Core User", "Expires 2026.11.03", "Expiring"),
        ("Park Soo-bin", "GB Self Service", "Expires 2024.08.10", "Inactive"),
        ("Yoon Tae", "GB Advanced User", "Expires 9999.12.30", "Active")
    ]
    # Default calculated license type counts if file not found
    raw_advanced_count_user_section = 117 # Assuming 117 users are Advanced if file not found
    raw_core_count_user_section = 2 # Assuming 2 core users if file not found
    raw_self_service_count_user_section = 27 # Assuming 27 self-service users if file not found
    raw_not_classified_count_user_section = 42 # Assuming 42 not classified users if file not found
    
    raw_user_license_counts = {
        'Advanced': raw_advanced_count_user_section,
        'Core': raw_core_count_user_section,
        'Self Service': raw_self_service_count_user_section,
        'Not Classified': raw_not_classified_count_user_section
    }

    calculated_advanced_fue = raw_advanced_count_user_section * 1
    calculated_core_fue = raw_core_count_user_section // 5
    calculated_self_service_fue = raw_self_service_count_user_section // 30
    calculated_not_classified_fue = 0
    calculated_fue_license_counts = {
        'Advanced': calculated_advanced_fue,
        'Core': calculated_core_fue,
        'Self Service': calculated_self_service_fue,
        'Not Classified': calculated_not_classified_fue
    }

    active_license_count = sum(calculated_fue_license_counts.values())
    total_license_capacity = 500
    remaining_license_count = total_license_capacity - active_license_count
    license_utilization_rate = (active_license_count / total_license_capacity) * 100 if total_license_capacity > 0 else 0

except Exception as e:
    st.error(f"An error occurred while reading or processing the CSV file: {e}. Using default values for some widgets.")
    user_count = 902
    inactive_users_count = 19
    recent_users_data = [
        ("Kim Hwi-young", "GB Advanced User", "Expires 9999.12.30", "Active"),
        ("Lee Min", "GB Advanced User", "Expires 9999.12.30", "Active"),
        ("Jung Ha-na", "GB Core User", "Expires 2026.11.03", "Expiring"),
        ("Park Soo-bin", "GB Self Service", "Expires 2024.08.10", "Inactive"),
        ("Yoon Tae", "GB Advanced User", "Expires 9999.12.30", "Active")
    ]
    # Default calculated license type counts if error
    raw_advanced_count_user_section = 117
    raw_core_count_user_section = 2
    raw_self_service_count_user_section = 27
    raw_not_classified_count_user_section = 42
    
    raw_user_license_counts = {
        'Advanced': raw_advanced_count_user_section,
        'Core': raw_core_count_user_section,
        'Self Service': raw_self_service_count_user_section,
        'Not Classified': raw_not_classified_count_user_section
    }

    calculated_advanced_fue = raw_advanced_count_user_section * 1
    calculated_core_fue = raw_core_count_user_section // 5
    calculated_self_service_fue = raw_self_service_count_user_section // 30
    calculated_not_classified_fue = 0
    calculated_fue_license_counts = {
        'Advanced': calculated_advanced_fue,
        'Core': calculated_core_fue,
        'Self Service': calculated_self_service_fue,
        'Not Classified': calculated_not_classified_fue
    }
    active_license_count = sum(calculated_fue_license_counts.values())
    total_license_capacity = 500
    remaining_license_count = total_license_capacity - active_license_count
    license_utilization_rate = (active_license_count / total_license_capacity) * 100 if total_license_capacity > 0 else 0


# First row: 5 1x1 widgets (total 5 units) + 1 unit spacing
cols_fue_row1 = st.columns([1, 1, 1, 1, 1, 1]) # 1+1+1+1+1+1 = 6 units. Last is spacing

with cols_fue_row1[0]: # 1 unit
    with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown(f'<div class="big-number">{total_license_capacity}</div>', unsafe_allow_html=True) # Use total_license_capacity
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[1]: # 1 unit
    with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">Active License</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown(f'<div class="big-number">{active_license_count}</div>', unsafe_allow_html=True) # Use calculated active_license_count
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[2]: # 1 unit
    with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">Remaining Licenses</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown(f'<div class="big-number">{remaining_license_count}</div>', unsafe_allow_html=True) # Use calculated remaining_license_count
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[3]: # 1 unit
    with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">License Utilization Rate</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 0.5)) # Adjust to widget height
        ax.barh(0, license_utilization_rate, color='#007BFF', height=0.4) # Use calculated license_utilization_rate
        ax.text(license_utilization_rate/2, 0, f'{license_utilization_rate:.1f}%', va='center', ha='center', color='white', fontsize=16, fontweight='bold') # Display calculated rate
        ax.set_xlim(0, 100)
        ax.axis('off')
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[4]: # 1 unit
    with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">License Variance</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="big-number">12 ▲</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Second row: Composition Ratio (2x1), Department Status (1x1), Job Status (1x1)
cols_fue_row2 = st.columns([2, 1, 1, 2]) # 2(widget) + 1(widget) + 1(widget) + 2(spacing) = 6 units

# Widget 6: Composition (2x1 size)
with cols_fue_row2[0]:
    with st.container(height=180, border=True): # 2x1 ratio (width:height = 2:1)
        st.markdown('<div class="widget-title">Composition ratio</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        
        # Use calculated_fue_license_counts for Composition Ratio
        composition_data = [(label, calculated_fue_license_counts.get(label, 0)) for label in ['Advanced', 'Core', 'Self Service', 'Not Classified']]
        composition_data.sort(key=lambda x: x[1], reverse=True) # Sort by value descending

        largest_label = composition_data[0][0] if composition_data else "N/A"
        largest_value = composition_data[0][1] if composition_data else 0
        total_calculated_licenses_for_composition = sum(val for _, val in composition_data)
        largest_percentage = (largest_value / total_calculated_licenses_for_composition * 100) if total_calculated_licenses_for_composition > 0 else 0

        text_col, chart_col = st.columns([2, 1])

        with text_col:
            st.markdown(f"""
                <div class="composition-text">
                    <div class="percentage">{largest_percentage:.0f}%</div>
                    <div class="description">{largest_label}</div>
                </div>
            """, unsafe_allow_html=True)

        with chart_col:
            sizes_for_pie = [val for _, val in composition_data]
            labels_for_pie = [label for label, _ in composition_data]
            
            # Filter out zero values for pie chart to prevent errors
            non_zero_sizes = [s for s in sizes_for_pie if s > 0]
            non_zero_labels = [labels_for_pie[i] for i, s in enumerate(sizes_for_pie) if s > 0]

            if non_zero_sizes:
                fig2, ax2 = plt.subplots(figsize=(1.5, 1.5)) # Adjust to widget height
                colors_composition = ['#007BFF', '#ADD8E6', '#87CEEB', '#B0E0E6'][:len(non_zero_sizes)]
                ax2.pie(non_zero_sizes, labels=non_zero_labels, autopct='%1.0f%%', startangle=90, colors=colors_composition,
                        wedgeprops={'linewidth': 0, 'edgecolor': 'white'})
                ax2.axis('equal')
                st.pyplot(fig2, use_container_width=True)
            else:
                st.markdown("No data for composition ratio.")
        st.markdown('</div>', unsafe_allow_html=True)

# Widget 7: Department Status (1x1 size)
with cols_fue_row2[1]: # Second column
    with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">Department Status</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="icon">🏢</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Widget 8: Job Status (1x1 size)
with cols_fue_row2[2]: # Third column
    with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">Job Status</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="icon">🛠️</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# User Section (Order change and size/position adjustment)
st.markdown('<div class="section-title">User</div>', unsafe_allow_html=True) 

# Main columns for User section: col_left_widgets (for 1x1s and 2x1), col_right_recent_activity (for 2x2)
col_left_widgets, col_right_recent_activity, _ = st.columns([3, 2, 1])

with col_left_widgets:
    # Row for Total, User Variance, Inactive Users (1x1 each)
    cols_1x1_user = st.columns(3) 
    
    with cols_1x1_user[0]:
        with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
            st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content">', unsafe_allow_html=True)
            st.markdown(f'<div class="big-number">{user_count}</div>', unsafe_allow_html=True) 
            st.markdown('</div>', unsafe_allow_html=True)

    with cols_1x1_user[1]:
        with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
            st.markdown('<div class="widget-title">User Variance</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content">', unsafe_allow_html=True)
            st.markdown('<div class="big-number">0</div>', unsafe_allow_html=True) # Set to 0
            st.markdown('</div>', unsafe_allow_html=True)

    with cols_1x1_user[2]:
        with st.container(height=180, border=True): # 1x1 ratio (width:height = 1:1)
            st.markdown('<div class="widget-title">Inactive Users</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content">', unsafe_allow_html=True)
            st.markdown(f'<div class="big-number">{inactive_users_count}</div>', unsafe_allow_html=True) # Display calculated value
            st.markdown('</div>', unsafe_allow_html=True)

    # User License Type (2x1) below the 1x1s.
    cols_user_license_type = st.columns([2, 1]) 
    with cols_user_license_type[0]:
        with st.container(height=180, border=True): # 2x1 ratio (width:height = 2:1)
            st.markdown('<div class="widget-title">User License Type</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content" style="padding-top: 0;">', unsafe_allow_html=True) 
            
            labels_order = ['Advanced', 'Core', 'Self Service', 'Not Classified'] # Define order for consistency
            
            # HIGHLIGHT START: Use raw_user_license_counts for User section
            for label in labels_order:
                value = raw_user_license_counts.get(label, 0) # Get raw count for the label
                st.markdown(f"""
                    <div class="license-type-row">
                        <span class="license-type-label">{label}</span>
                        <span class="license-type-value">{value}</span>
                    </div>
                """, unsafe_allow_html=True)
            # HIGHLIGHT END
            st.markdown('</div>', unsafe_allow_html=True)

with col_right_recent_activity:
    # Recent User Activity (2x2)
    with st.container(height=360, border=True): # 2x2 ratio (width:height = 1:1)
        st.markdown('<div class="widget-title">Recent User Activity</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        # Use dynamically generated recent_users_data
        for name, grade, expiry, status in recent_users_data:
            st.markdown(f"""
                <div class="user-box">
                    <div class="user-info">
                        <strong>{name}</strong><br>
                        {grade} | {expiry}
                    </div>
                    <div class="user-icon {status}">{status}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
