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
    with st.container():
        st.markdown("""
            <div class="widget-box">
                <div class="widget-title">FUE License Status</div>
                <div class="stat-block">
                    <div><div class="stat-label">Active Licenses</div><div class="stat-value">292</div></div>
                    <div><div class="stat-label">Total License</div><div class="stat-value">500</div></div>
                    <div><div class="stat-label">Transaction Based</div><div class="stat-value">271</div></div>
                </div>
                <hr style="margin: 1rem 0;">
        """, unsafe_allow_html=True)

        col_pie1, col_pie2 = st.columns(2)
        with col_pie1:
            fig1, ax1 = plt.subplots()
            ax1.pie([292, 208], labels=['Active', 'Remaining'], autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col_pie2:
            fig2, ax2 = plt.subplots()
            ax2.pie([271, 229], labels=['Transaction Based', 'Other'], autopct='%1.1f%%', startangle=90)
            ax2.axis('equal')
            st.pyplot(fig2)

        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="widget-box">
            <div class="widget-title">My Account</div>
            <div class="stat-block" style="grid-template-columns: 1fr 1fr;">
                <div><div class="stat-label">License Type</div><div class="stat-value">FUE</div></div>
                <div><div class="stat-label">License</div><div class="stat-value">500</div></div>
                <div><div class="stat-label">ATNS ALMS</div><div class="stat-value">Expiration</div></div>
                <div><div class="stat-value">2027.12.31</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---------------- FUE Active License Variance ----------------
st.markdown("<h3>FUE Active License Variance</h3>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='widget-box'><div class='widget-title'>Active License (최근 4개월)</div>", unsafe_allow_html=True)
    months = ['May', 'June', 'July', 'August']
    values = [345, 310, 278, 292]
    fig_line, ax_line = plt.subplots()
    ax_line.plot(months, values, marker='o', color='#1673ff')
    ax_line.set_title("Active License Variance")
    ax_line.grid(True)
    st.pyplot(fig_line)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- User License Type ----------------
st.markdown("<h3>User License Type</h3>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='widget-box'><div class='widget-title'>User License Type</div>", unsafe_allow_html=True)
    license_types = ['Advance', 'Core', 'Self Service', 'Not Classified']
    values = [189, 84, 371, 42]
    colors = ['#1673ff', '#69aaf5', '#aecdfc', '#d0e0fa']
    fig_bar, ax_bar = plt.subplots()
    ax_bar.barh(license_types, values, color=colors)
    ax_bar.set_xlim([0, max(values) * 1.1])
    ax_bar.invert_yaxis()
    ax_bar.set_xlabel("Users")
    st.pyplot(fig_bar)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Composition Pie ----------------
st.markdown("<h3>Composition</h3>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='widget-box'><div class='widget-title'>Composition</div>", unsafe_allow_html=True)
    comp_labels = ['Type A', 'Type B', 'Type C', 'Type D']
    comp_sizes = [76, 12, 7, 5]
    fig_comp, ax_comp = plt.subplots()
    ax_comp.pie(comp_sizes, labels=comp_labels, autopct='%1.1f%%', startangle=140)
    ax_comp.axis('equal')
    st.pyplot(fig_comp)
    st.markdown("</div>", unsafe_allow_html=True)
