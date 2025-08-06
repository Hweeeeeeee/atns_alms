import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 페이지 설정 (한 번만 선언)
st.set_page_config(layout="wide")

# 헤더 및 메뉴바 스타일 정의
st.markdown("""
    <style>
        /* 전체 페이지 기본 폰트 설정 */
        body {
            font-family: 'Inter', sans-serif;
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
            color: #007BFF; /* SAP Blue 계열 */
            border-bottom: 2px solid #007BFF;
        }
        .search-box {
            padding: 4px 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        /* 위젯 공통 스타일 */
        .widget-box {
            background-color: white;
            border: 1px solid #d9d9d9;
            border-radius: 8px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.05);
            padding: 1rem;
            height: 100%; /* 부모 컬럼에 맞춰 높이 조정 */
            display: flex; /* 내부 요소 정렬을 위해 flexbox 사용 */
            flex-direction: column; /* 세로 방향으로 정렬 */
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
        .big-number {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
        }
        .icon {
            font-size: 36px;
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
            border: 1px solid;
            background-color: rgba(0,0,0,0.05); /* 투명한 배경 */
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
        /* Matplotlib 차트 컨테이너 스타일 */
        .chart-container {
            flex-grow: 1; /* 남은 공간을 채우도록 설정 */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        /* Streamlit 기본 패딩 제거 */
        .stApp {
            padding-top: 0px;
        }
        /* 막대 그래프 위에 텍스트를 위한 스타일 추가 */
        .bar-container {
            position: relative;
            width: 100%;
            height: 20px; /* 막대 그래프 높이와 유사하게 설정 */
            margin-top: 10px; /* 막대 그래프와의 간격 조절 */
        }
        .bar-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-weight: bold;
            font-size: 16px; /* 텍스트 크기 조절 */
            z-index: 1; /* 막대 그래프 위에 오도록 설정 */
        }
        /* Composition 위젯의 텍스트와 차트 정렬을 위한 CSS 수정 (롤백) */
        .composition-content {
            display: flex;
            align-items: center; /* HIGHLIGHT: 중앙 정렬로 롤백 */
            justify-content: space-between; /* 텍스트와 차트 사이 공간 분배 */
            flex-grow: 1; /* 남은 공간을 채우도록 설정 */
            padding-top: 10px; /* 상단 여백 추가 */
        }
        .composition-text {
            text-align: left;
            flex-shrink: 0; /* 텍스트가 줄어들지 않도록 */
            margin-right: 10px; /* 텍스트와 차트 사이 간격 */
        }
        .composition-text .percentage {
            font-size: 40px; /* 76% 글자 크기 */
            font-weight: bold;
            color: #007BFF; /* SAP Blue */
        }
        .composition-text .description {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
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

# 섹션 타이틀
st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)





















# 첫 번째 섹션 : Overview
# 첫 줄: 3개 위젯 (2x2, 2x2, 2x1)
col1, col2, col3 = st.columns([2, 2, 2])

# --- 위젯 1: FUE License Status ---
with col1:
    with st.container(height=350, border=True): # st.container를 사용하여 위젯 박스 역할
        st.markdown('<div class="widget-title">FUE License Status</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="stat-block">
                <div><div class="stat-label">Active Licenses</div><div class="stat-value">292</div></div>
                <div><div class="stat-label">Total License</div><div class="stat-value">500</div></div>
                <div><div class="stat-label">Transaction Based</div><div class="stat-value">271</div></div>
            </div>
            <hr style="margin: 1rem 0;">
        """, unsafe_allow_html=True)

        # Figma 디자인에 맞춰 두 개의 파이 차트 대신 하나의 파이 차트로 변경
        active_pct = 292 / 500 * 100
        fig1, ax1 = plt.subplots(figsize=(4, 4)) # 차트 크기 조정
        colors = ['#007BFF', '#FFA500'] # SAP Blue, Orange
        ax1.pie([active_pct, 100 - active_pct], labels=[f'Active ({active_pct:.1f}%)', 'Remaining'], autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.set_aspect('equal') # 원형 유지
        st.pyplot(fig1, use_container_width=True) # 컨테이너 너비에 맞춤


# --- 위젯 2: FUE Active License Variance ---
with col2:
    with st.container(height=350, border=True): # st.container를 사용하여 위젯 박스 역할
        st.markdown('<div class="widget-title">FUE Active License Variance</div>', unsafe_allow_html=True)

        # 최근 4개월 값 생성
        base = 292
        months = ['4월', '5월', '6월', '7월']
        values = [base]
        for _ in range(3):
            base *= np.random.uniform(0.85, 0.95)
            values.insert(0, int(base))

        # 막대그래프
        fig3, ax3 = plt.subplots(figsize=(5, 3)) # 차트 크기 조정
        bar_colors = ['#D3D3D3'] * (len(months) - 1) + ['#007BFF'] # 마지막 막대만 SAP Blue
        ax3.bar(months, values, color=bar_colors)
        ax3.set_ylabel("Licenses")
        ax3.set_title("최근 4개월 Active License 수")
        st.pyplot(fig3, use_container_width=True) # 컨테이너 너비에 맞춤

# --- 위젯 3: My Account ---
with col3:
    with st.container(height=350, border=True): # st.container를 사용하여 위젯 박스 역할
        st.markdown('<div class="widget-title">My Account</div>', unsafe_allow_html=True)
        st.markdown("""
            <table class="my-table">
                <tr><td><strong>License Type</strong></td><td>ATNS ALMS License</td></tr>
                <tr><td><strong>FUE</strong></td><td>500</td></tr>
                <tr><td><strong>Expiration</strong></td><td>2027.12.31</td></tr>
            </table>
        """, unsafe_allow_html=True)
















# 두 번째 섹션 : FUE License
# FUE License 섹션
st.markdown('<div class="section-title">FUE License</div>', unsafe_allow_html=True)

# -------- Row 1: 5개의 위젯 --------
col1_fue, col2_fue, col3_fue, col4_fue, col5_fue = st.columns(5)

with col1_fue:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number">500</div>', unsafe_allow_html=True)

with col2_fue:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">Active License</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number">292</div>', unsafe_allow_html=True)

with col3_fue:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">Remaining Licenses</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number">208</div>', unsafe_allow_html=True)

with col4_fue:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">License Utilization Rate</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 0.5))
        # 막대 그래프 색상 변경 및 텍스트 추가
        ax.barh(0, 58, color='#007BFF', height=0.4) # SAP Blue
        ax.text(58/2, 0, '58%', va='center', ha='center', color='white', fontsize=16, fontweight='bold') # 막대 중앙에 텍스트 추가
        ax.set_xlim(0, 100)
        ax.axis('off')
        st.pyplot(fig, use_container_width=True)
        # 기존 텍스트 제거

with col5_fue:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">License Variance</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number">12 ▲</div>', unsafe_allow_html=True)

# -------- Row 2: 3개의 위젯 --------
col6_fue, col7_fue, col8_fue = st.columns([2, 1, 1]) # 비율 조정

# Widget 6: Composition (2 by 1)
with col6_fue:
    with st.container(height=300, border=True): # 높이 조정
        st.markdown('<div class="widget-title">Composition ratio</div>', unsafe_allow_html=True)
        
        # HIGHLIGHT START: 텍스트와 차트 배치를 위한 HTML 구조 변경 (롤백)
        text_col, chart_col = st.columns([2, 1]) # 텍스트:차트 비율을 2:1로 롤백

        with text_col:
            st.markdown("""
                <div class="composition-text">
                    <div class="percentage">76%</div>
                    <div class="description">GB Advanced use</div>
                </div>
            """, unsafe_allow_html=True)

        with chart_col:
            sizes = [76, 10, 8, 6]
            labels = ['A', 'B', 'C', 'D']
            fig2, ax2 = plt.subplots(figsize=(2, 2)) # HIGHLIGHT: 차트 크기 (figsize)를 (2, 2)로 롤백
            colors_composition = ['#007BFF', '#ADD8E6', '#87CEEB', '#B0E0E6'] # 파란색 계열로 변경
            ax2.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90, colors=colors_composition,
                    wedgeprops={'linewidth': 0, 'edgecolor': 'white'}) # HIGHLIGHT: 텍스트 크기 조정 (textprops) 제거
            ax2.axis('equal')
            st.pyplot(fig2, use_container_width=True) # HIGHLIGHT: bbox_inches='tight' 제거
        # HIGHLIGHT END
            # HIGHLIGHT START: 차트의 y축 위치를 조정하기 위한 CSS 코드 제거
            # .stPlotlyChart { margin-top: -30px; } 스타일 제거
            # HIGHLIGHT END

# Widget 7: 부서별 현황
with col7_fue:
    with st.container(height=300, border=True): # 높이 조정
        st.markdown('<div class="widget-title">부서별 현황</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon">🏢</div>', unsafe_allow_html=True)

# Widget 8: 직무별 현황
with col8_fue:
    with st.container(height=300, border=True): # 높이 조정
        st.markdown('<div class="widget-title">직무별 현황</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon">🛠️</div>', unsafe_allow_html=True)




















# 세 번쩨 섹션 : User
# User 위젯을 위한 새로운 컬럼 정의 (전체 너비 사용)
st.markdown('<div class="section-title">User</div>', unsafe_allow_html=True)
col_user_total, col_user_variance, col_inactive_users = st.columns(3)

with col_user_total:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number">902 <span style="color: green; font-size: 20px;">(+7)</span></div>', unsafe_allow_html=True)

with col_user_variance:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">User Variance</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number">7 ▲</div>', unsafe_allow_html=True)

with col_inactive_users:
    with st.container(height=150, border=True):
        st.markdown('<div class="widget-title">Inactive Users</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number">19</div>', unsafe_allow_html=True)

# -------- Row 2: Recent Activity (2x2) + License Type (2x1) --------
col4, col5 = st.columns([2, 2]) # 비율을 2:2로 조정하여 두 위젯이 균등하게 배치되도록 함

# 위젯 4: Recent User Activity
with col4:
    with st.container(height=300, border=True): # 높이 조정
        st.markdown('<div class="widget-title">Recent User Activity</div>', unsafe_allow_html=True)
        users = [
            ("Kim Hwi-young", "GB Advanced User", "Expires 9999.12.30", "Active"),
            ("Lee Min", "GB Advanced User", "Expires 9999.12.30", "Active"),
            ("Jung Ha-na", "GB Core User", "Expires 2026.11.03", "Expiring"),
            ("Park Soo-bin", "GB Self Service", "Expires 2024.08.10", "Inactive"),
            ("Yoon Tae", "GB Advanced User", "Expires 9999.12.30", "Active")
        ]
        for name, grade, expiry, status in users:
            # 사용자 상태에 따라 user-icon 클래스 동적 적용
            st.markdown(f"""
                <div class="user-box">
                    <div class="user-info">
                        <strong>{name}</strong><br>
                        {grade} | {expiry}
                    </div>
                    <div class="user-icon {status}">{status}</div>
                </div>
            """, unsafe_allow_html=True)

# 위젯 5: User License Type (막대그래프)
with col5:
    with st.container(height=300, border=True): # 높이 조정
        st.markdown('<div class="widget-title">User License Type</div>', unsafe_allow_html=True)

        labels = ['Advance', 'Core', 'Self Service', 'Not Classified']
        values = [189, 84, 371, 42]
        max_value = max(values) * 1.1

        fig, ax = plt.subplots(figsize=(6, 3)) # 차트 크기 조정
        ax.barh(labels, values, color='#007BFF') # 모든 막대를 SAP Blue로
        ax.set_xlim(0, max_value)
        ax.set_xlabel('Users')
        st.pyplot(fig, use_container_width=True) # 컨테이너 너비에 맞춤
