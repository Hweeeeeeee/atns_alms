import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


import streamlit as st

# 페이지 설정
st.set_page_config(layout="wide")

# 헤더 및 메뉴바 스타일 정의
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
active = "Home"  # 현재 선택된 메뉴

menu_html = '<div class="menu-bar">'
for item in menu_items:
    class_name = "menu-item active" if item == active else "menu-item"
    menu_html += f'<div class="{class_name}">{item}</div>'
menu_html += '</div>'
st.markdown(menu_html, unsafe_allow_html=True)



# 페이지 설정
st.set_page_config(layout="wide")

# CSS 스타일 정의
st.markdown("""
    <style>
        .widget-box {
            background-color: white;
            border: 1px solid #d9d9d9;
            border-radius: 8px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.05);
            padding: 1rem;
            height: 100%;
        }
        .section-title {
            font-size: 24px;
            font-weight: bold;
            margin: 1rem 0;
        }
        .widget-title {
            font-weight: bold;
            font-size: 18px;
            color: black;
            margin-bottom: 0.5rem;
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
        .my-table {
            font-size: 14px;
            width: 100%;
        }
        .my-table td {
            padding: 4px 8px;
        }
    </style>
""", unsafe_allow_html=True)

# 섹션 타이틀
st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

# 첫 줄: 3개 위젯 (2x2, 2x2, 2x1)
col1, col2, col3 = st.columns([2, 2, 2])

# --- 위젯 1: FUE License Status ---
with col1:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">FUE License Status</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="stat-block">
            <div><div class="stat-label">Active Licenses</div><div class="stat-value">292</div></div>
            <div><div class="stat-label">Total License</div><div class="stat-value">500</div></div>
            <div><div class="stat-label">Transaction Based</div><div class="stat-value">271</div></div>
        </div>
        <hr style="margin: 1rem 0;">
    """, unsafe_allow_html=True)

    # 파이 차트 1: Active Licenses
    active_pct = 292 / 500 * 100
    fig1, ax1 = plt.subplots()
    ax1.pie([active_pct, 100 - active_pct], labels=[f'Active ({active_pct:.1f}%)', 'Remaining'], autopct='%1.1f%%')
    st.pyplot(fig1)

    # 파이 차트 2: Transaction Based
    trans_pct = 271 / 500 * 100
    fig2, ax2 = plt.subplots()
    ax2.pie([trans_pct, 100 - trans_pct], labels=[f'Transaction ({trans_pct:.1f}%)', 'Remaining'], autopct='%1.1f%%')
    st.pyplot(fig2)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 위젯 2: FUE Active License Variance ---
with col2:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">FUE Active License Variance</div>', unsafe_allow_html=True)

    # 최근 4개월 값 생성
    base = 292
    months = ['4월', '5월', '6월', '7월']
    values = [base]
    for _ in range(3):
        base *= np.random.uniform(0.85, 0.95)
        values.insert(0, int(base))

    # 막대그래프
    fig3, ax3 = plt.subplots()
    ax3.bar(months, values, color=['gray', 'gray', 'gray', 'blue'])
    ax3.set_ylabel("Licenses")
    ax3.set_title("최근 4개월 Active License 수")
    st.pyplot(fig3)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 위젯 3: My Account ---
with col3:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">My Account</div>', unsafe_allow_html=True)
    st.markdown("""
        <table class="my-table">
            <tr><td><strong>License Type</strong></td><td>ATNS ALMS License</td></tr>
            <tr><td><strong>FUE</strong></td><td>500</td></tr>
            <tr><td><strong>Expiration</strong></td><td>2027.12.31</td></tr>
        </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 두 번째 줄: 위젯 4만 표시
col_user = st.columns([1, 5, 5, 5, 5, 5])[0]
with col_user:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">User</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 28px; font-weight: bold;">902 <span style="color: green;">(+7)</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)




st.set_page_config(layout="wide")

# CSS 스타일 정의
st.markdown("""
    <style>
        .widget-box {
            background-color: white;
            border: 1px solid #d9d9d9;
            border-radius: 8px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.05);
            padding: 1rem;
            text-align: center;
        }
        .widget-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 0.5rem;
        }
        .big-number {
            font-size: 32px;
            font-weight: bold;
        }
        .icon {
            font-size: 36px;
        }
    </style>
""", unsafe_allow_html=True)

# 섹션 제목
st.markdown('<h3>FUE License</h3>', unsafe_allow_html=True)

# -------- Row 1: 5개의 위젯 --------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-number">500</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Active License</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-number">292</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Remaining Licenses</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-number">208</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">License Utilization Rate</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4, 0.5))
    ax.barh(0, 58, color='blue', height=0.4)
    ax.set_xlim(0, 100)
    ax.axis('off')
    st.pyplot(fig)
    st.markdown('<div class="big-number">58%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">License Variance</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-number">12 ▲</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------- Row 2: 3개의 위젯 --------
col6, col7, col8 = st.columns([2, 1, 1])

# Widget 6: Composition (2 by 1)
with col6:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Composition</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: left; font-size: 20px; font-weight: bold; margin-top: 30px;">76%</div>', unsafe_allow_html=True)
    sizes = [76, 10, 8, 6]
    labels = ['A', 'B', 'C', 'D']
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

# Widget 7: 부서별 현황
with col7:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">부서별 현황</div>', unsafe_allow_html=True)
    st.markdown('<div class="icon">🏢</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Widget 8: 직무별 현황
with col8:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">직무별 현황</div>', unsafe_allow_html=True)
    st.markdown('<div class="icon">🛠️</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)





st.set_page_config(layout="wide")

# 스타일 정의
st.markdown("""
    <style>
        .widget-box {
            background-color: white;
            border: 1px solid #d9d9d9;
            border-radius: 8px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.05);
            padding: 1rem;
        }
        .widget-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 0.5rem;
        }
        .big-number {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
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
        .user-info {
            font-size: 13px;
        }
        .user-icon {
            border: 1px solid #007BFF;
            background-color: rgba(0,123,255,0.1);
            color: #007BFF;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 12px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 섹션 제목
st.markdown('<h3>User</h3>', unsafe_allow_html=True)

# -------- Row 1: 위젯 1~3 --------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-number">902</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">User Variance</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-number">7 ▲</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Inactive Users</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-number">19</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------- Row 2: Recent Activity (2x2) + License Type (2x1) --------
col4, col5 = st.columns([2, 2])

# 위젯 4: Recent User Activity
with col4:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Recent User Activity</div>', unsafe_allow_html=True)
    users = [
        ("Kim Hwi-young", "GB Advanced User", "Expires 9999.12.30", "Active"),
        ("Lee Min", "GB Advanced User", "Expires 9999.12.30", "Active"),
        ("Jung Ha-na", "GB Core User", "Expires 2026.11.03", "Expiring"),
        ("Park Soo-bin", "GB Self Service", "Expires 2024.08.10", "Inactive"),
        ("Yoon Tae", "GB Advanced User", "Expires 9999.12.30", "Active")
    ]
    for name, grade, expiry, status in users:
        st.markdown(f"""
            <div class="user-box">
                <div class="user-info">
                    <strong>{name}</strong><br>
                    {grade} | {expiry}
                </div>
                <div class="user-icon">{status}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 위젯 5: User License Type (막대그래프)
with col5:
    st.markdown('<div class="widget-box">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">User License Type</div>', unsafe_allow_html=True)

    labels = ['Advance', 'Core', 'Self Service', 'Not Classified']
    values = [189, 84, 371, 42]
    max_value = max(values) * 1.1

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.barh(labels, values, color='skyblue')
    ax.set_xlim(0, max_value)
    ax.set_xlabel('Users')
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
