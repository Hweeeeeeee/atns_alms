import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
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
        color: #1673ff;
        border-bottom: 2px solid #1673ff;
    }
    .search-box {
        padding: 4px 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    .widget-box {
        background-color: white;
        border: 1px solid #d9d9d9;
        border-radius: 8px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
        padding: 1rem;
        height: 100%;
    }
    .widget-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 1rem;
    }
    .stat-block {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-label {
        font-size: 14px;
        color: #666;
    }
    .stat-value {
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
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

# ---------------- Menu Bar ----------------
menu_items = ["Home", "FUE License", "User", "My Account"]
active = "Home"
menu_html = '<div class="menu-bar">'
for item in menu_items:
    class_name = "menu-item active" if item == active else "menu-item"
    menu_html += f'<div class="{class_name}">{item}</div>'
menu_html += '</div>'
st.markdown(menu_html, unsafe_allow_html=True)

# ---------------- Overview Section ----------------
st.markdown("<h3>Overview</h3>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 2])
with col1:
    st.markdown("""
        <div class="widget-box">
            <div class="widget-title">FUE License Status</div>
            <div class="stat-block">
                <div>
                    <div class="stat-label">Active Licenses</div>
                    <div class="stat-value">292</div>
                </div>
                <div>
                    <div class="stat-label">Total License</div>
                    <div class="stat-value">500</div>
                </div>
                <div>
                    <div class="stat-label">Transaction Based</div>
                    <div class="stat-value">271</div>
                </div>
            </div>
            <div> 
                <div> 
                    # 파이 차트 1: Active Licenses
                    active_pct = 292 / 500 * 100
                    fig1, ax1 = plt.subplots()
                    ax1.pie([active_pct, 100 - active_pct], labels=[f'Active ({active_pct:.1f}%)', 'Remaining'], autopct='%1.1f%%')
                    st.pyplot(fig1)
                </div>
                <div>      
                    # 파이 차트 2: Transaction Based
                    trans_pct = 271 / 500 * 100
                    fig2, ax2 = plt.subplots()
                    ax2.pie([trans_pct, 100 - trans_pct], labels=[f'Transaction ({trans_pct:.1f}%)', 'Remaining'], autopct='%1.1f%%')
                    st.pyplot(fig2)
                </div>
            </div>
            <hr style="margin: 1rem 0;">
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="widget-box">
            <div class="widget-title">My Account</div>
            <div class="stat-block" style="grid-template-columns: 1fr 1fr;">
                <div>
                    <div class="stat-label">License Type</div>
                    <div class="stat-value">FUE</div>
                </div>
                <div>
                    <div class="stat-label">License</div>
                    <div class="stat-value">500</div>
                </div>
                <div>
                    <div class="stat-label">ATNS ALMS</div>
                    <div class="stat-value">Expiration</div>
                </div>
                <div>
                    <div class="stat-value">2027.12.31</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---------------- FUE License Section ----------------
st.markdown("<h3>FUE License</h3>", unsafe_allow_html=True)
fue1, fue2, fue3, fue4, fue5 = st.columns(5)
with fue1:
    st.markdown("<div class='widget-box'><div class='widget-title'>Total</div><div class='stat-value'>500</div></div>", unsafe_allow_html=True)
with fue2:
    st.markdown("<div class='widget-box'><div class='widget-title'>Active License</div><div class='stat-value'>292</div></div>", unsafe_allow_html=True)
with fue3:
    st.markdown("<div class='widget-box'><div class='widget-title'>Remaining Licenses</div><div class='stat-value'>208</div></div>", unsafe_allow_html=True)
with fue4:
    st.markdown("<div class='widget-box'><div class='widget-title'>Utilization Rate</div><div class='stat-value'>58%</div><div style='background:#eee; height:10px; border-radius:5px;'><div style='width:58%; background:#1673ff; height:10px; border-radius:5px;'></div></div></div>", unsafe_allow_html=True)
with fue5:
    st.markdown("<div class='widget-box'><div class='widget-title'>License Variance</div><div class='stat-value'>12 ▲</div></div>", unsafe_allow_html=True)

# ---------------- User Section ----------------
st.markdown("<h3>User</h3>", unsafe_allow_html=True)
user1, user2, user3, user4, user5 = st.columns([1, 1, 1, 2, 2])
with user1:
    st.markdown("<div class='widget-box'><div class='widget-title'>Total</div><div class='stat-value'>902</div></div>", unsafe_allow_html=True)
with user2:
    st.markdown("<div class='widget-box'><div class='widget-title'>User Variance</div><div class='stat-value'>7 ▲</div></div>", unsafe_allow_html=True)
with user3:
    st.markdown("<div class='widget-box'><div class='widget-title'>Inactive Users</div><div class='stat-value'>19</div></div>", unsafe_allow_html=True)
with user4:
    st.markdown("""
        <div class='widget-box'>
            <div class='widget-title'>Recent User Activity</div>
            <div class='user-box'><div class='user-info'>Kim Hyeon<br>GB Advanced use | Expires 9999.12.30</div><div class='user-icon'>Active</div></div>
            <div class='user-box'><div class='user-info'>Lee Min<br>GB Basic use | Expires 2026.01.15</div><div class='user-icon'>Active</div></div>
        </div>
    """, unsafe_allow_html=True)
with user5:
    st.markdown("""
        <div class='widget-box'>
            <div class='widget-title'>User License Type</div>
            <div class='stat-block' style='grid-template-columns: 1fr;'>
                <div class='stat-label'>Advance</div>
                <div style='background:#eee; height:10px;'><div style='width:21%; background:#1673ff; height:10px;'></div></div>
                <div class='stat-label'>Core</div>
                <div style='background:#eee; height:10px;'><div style='width:9%; background:#1673ff; height:10px;'></div></div>
                <div class='stat-label'>Self Service</div>
                <div style='background:#eee; height:10px;'><div style='width:42%; background:#1673ff; height:10px;'></div></div>
                <div class='stat-label'>Not Classified</div>
                <div style='background:#eee; height:10px;'><div style='width:5%; background:#1673ff; height:10px;'></div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
