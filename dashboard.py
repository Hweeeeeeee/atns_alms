import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd # HIGHLIGHT: pandas 라이브러리 임포트

# 페이지 설정 (한 번만 선언)
st.set_page_config(layout="wide")

# 헤더 및 메뉴바 스타일 정의
st.markdown("""
    <style>
        /* 전체 페이지 기본 폰트 설정 */
        body {
            font-family: 'Inter', sans-serif;
        }
        /* 컨텐츠 영역 배경색 변경 */
        .stApp {
            padding-top: 0px;
            background-color: #FFFFFF; /* 컨텐츠 영역 배경색 흰색으로 지정 */
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
        /* 위젯 공통 스타일 - 그림자 적용 및 스크롤 방지 */
        div[data-testid="stVerticalBlock"] > div.st-emotion-cache-ocqkzj {
            box-shadow: 0 8px 16px rgba(0,0,0,0.35) !important; /* 그림자를 더 진하게 적용 */
            overflow: hidden !important; /* 내부 스크롤 방지 */
        }
        .section-title {
            font-size: 24px;
            font-weight: bold;
            margin: 2rem 0; /* 섹션 타이틀 상단 여백 2배 증가 */
        }
        .widget-title {
            font-weight: bold;
            font-size: 18px;
            color: black;
            margin-bottom: 1.5rem; /* 타이틀 하단 여백 증가 */
        }
        /* 위젯 내부 콘텐츠를 감싸는 div 스타일 */
        .widget-content {
            flex-grow: 1; /* 남은 공간을 모두 차지 */
            display: flex;
            flex-direction: column;
            justify-content: center; /* 수직 중앙 정렬 */
            align-items: flex-start; /* 좌측 정렬 */
            padding-bottom: 1.5rem; /* 하단 여백 추가 */
        }
        .stat-block {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            text-align: left;
            margin-bottom: 1rem;
            width: 100%; /* stat-block이 전체 너비를 사용하도록 */
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
            margin-top: 0; /* Flexbox가 정렬하므로 마진 초기화 */
        }
        .icon {
            font-size: 36px;
            text-align: left;
            margin-top: 0; /* Flexbox가 정렬하므로 마진 초기화 */
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
        /* Composition 위젯의 텍스트와 차트 정렬을 위한 CSS 수정 */
        .composition-content {
            display: flex;
            align-items: center;
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

# Overview 섹션 위젯 배치 및 크기 조정
cols_overview_row1 = st.columns([2, 2, 2]) 

# 위젯 1: FUE License Status (2x2 크기)
with cols_overview_row1[0]:
    with st.container(height=360, border=True): # 2x2 비율 (가로:세로 = 1:1)
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
        fig1, ax1 = plt.subplots(figsize=(3, 3)) # 1:1 비율 유지
        colors = ['#007BFF', '#FFA500']
        ax1.pie([active_pct, 100 - active_pct], labels=[f'Active ({active_pct:.1f}%)', 'Remaining'], autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.set_aspect('equal')
        st.pyplot(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 위젯 2: FUE Active License Variance (2x2 크기)
with cols_overview_row1[1]:
    with st.container(height=360, border=True): # 2x2 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">FUE Active License Variance</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)

        base = 292
        months = ['4월', '5월', '6월', '7월']
        values = [base]
        for _ in range(3):
            base *= np.random.uniform(0.85, 0.95)
            values.insert(0, int(base))

        fig3, ax3 = plt.subplots(figsize=(4, 3)) # 1:1 비율에 가깝게 조정
        bar_colors = ['#D3D3D3'] * (len(months) - 1) + ['#007BFF']
        ax3.bar(months, values, color=bar_colors)
        ax3.set_ylabel("Licenses")
        ax3.set_title("최근 4개월 Active License 수")
        st.pyplot(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 위젯 3: My Account (2x1 크기) - 첫 번째 줄에 배치
with cols_overview_row1[2]:
    with st.container(height=180, border=True): # 2x1 비율 (가로:세로 = 2:1)
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


# FUE License 섹션 (순서 변경 및 크기/위치 조정)
st.markdown('<div class="section-title">FUE License</div>', unsafe_allow_html=True)

# 첫 번째 줄: 1x1 위젯 5개 (총 5단위) + 1단위 여백
cols_fue_row1 = st.columns([1, 1, 1, 1, 1, 1]) # 1+1+1+1+1+1 = 6단위. 마지막은 여백

with cols_fue_row1[0]: # 1단위
    with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="big-number">500</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[1]: # 1단위
    with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">Active License</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="big-number">292</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[2]: # 1단위
    with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">Remaining Licenses</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="big-number">208</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[3]: # 1단위
    with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">License Utilization Rate</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 0.5)) # 위젯 높이에 맞게 조정
        ax.barh(0, 58, color='#007BFF', height=0.4)
        ax.text(58/2, 0, '58%', va='center', ha='center', color='white', fontsize=16, fontweight='bold')
        ax.set_xlim(0, 100)
        ax.axis('off')
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with cols_fue_row1[4]: # 1단위
    with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">License Variance</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="big-number">12 ▲</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 두 번째 줄: Composition Ratio (2x1), 부서별 현황 (1x1), 직무별 현황 (1x1)
cols_fue_row2 = st.columns([2, 1, 1, 2]) # 2(위젯) + 1(위젯) + 1(위젯) + 2(여백) = 6단위

# Widget 6: Composition (2x1 크기)
with cols_fue_row2[0]:
    with st.container(height=180, border=True): # 2x1 비율 (가로:세로 = 2:1)
        st.markdown('<div class="widget-title">Composition ratio</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        
        text_col, chart_col = st.columns([2, 1])

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
            fig2, ax2 = plt.subplots(figsize=(1.5, 1.5)) # 위젯 높이에 맞게 조정
            colors_composition = ['#007BFF', '#ADD8E6', '#87CEEB', '#B0E0E6']
            ax2.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90, colors=colors_composition,
                    wedgeprops={'linewidth': 0, 'edgecolor': 'white'})
            ax2.axis('equal')
            st.pyplot(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Widget 7: 부서별 현황 (1x1 크기)
with cols_fue_row2[1]: # 두 번째 컬럼
    with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">부서별 현황</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="icon">🏢</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Widget 8: 직무별 현황 (1x1 크기)
with cols_fue_row2[2]: # 세 번째 컬럼
    with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">직무별 현황</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
        st.markdown('<div class="icon">🛠️</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# User 섹션 (순서 변경 및 크기/위치 조정)
st.markdown('<div class="section-title">User</div>', unsafe_allow_html=True)

# Main columns for User section: col_left_widgets (for 1x1s and 2x1), col_right_recent_activity (for 2x2)
col_left_widgets, col_right_recent_activity, _ = st.columns([3, 2, 1])

# HIGHLIGHT START: CSV 파일에서 USERID 수 계산
user_count = 0
try:
    df_users = pd.read_csv('zalmt0020.csv')
    if 'USERID' in df_users.columns:
        user_count = df_users['USERID'].nunique()
    else:
        st.warning("zalmt0020.csv 파일에 'USERID' 열이 없습니다. 기본값 902를 사용합니다.")
        user_count = 902 # 기본값
except FileNotFoundError:
    st.error("zalmt0020.csv 파일을 찾을 수 없습니다. 기본값 902를 사용합니다.")
    user_count = 902 # 기본값
except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}. 기본값 902를 사용합니다.")
    user_count = 902 # 기본값
# HIGHLIGHT END

with col_left_widgets:
    # Row for Total, User Variance, Inactive Users (1x1 each)
    cols_1x1_user = st.columns(3) # col_left_widgets의 3단위를 3등분 (각 1단위)
    
    with cols_1x1_user[0]:
        with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
            st.markdown('<div class="widget-title">Total</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content">', unsafe_allow_html=True)
            # HIGHLIGHT: user_count 값 동적 전달
            st.markdown(f'<div class="big-number">{user_count} <span style="color: green; font-size: 20px;">(+7)</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with cols_1x1_user[1]:
        with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
            st.markdown('<div class="widget-title">User Variance</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content">', unsafe_allow_html=True)
            st.markdown('<div class="big-number">7 ▲</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with cols_1x1_user[2]:
        with st.container(height=180, border=True): # 1x1 비율 (가로:세로 = 1:1)
            st.markdown('<div class="widget-title">Inactive Users</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content">', unsafe_allow_html=True)
            st.markdown('<div class="big-number">19</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # User License Type (2x1) below the 1x1s.
    cols_user_license_type = st.columns([2, 1]) 
    with cols_user_license_type[0]:
        with st.container(height=180, border=True): # 2x1 비율 (가로:세로 = 2:1)
            st.markdown('<div class="widget-title">User License Type</div>', unsafe_allow_html=True)
            st.markdown('<div class="widget-content">', unsafe_allow_html=True)
            
            labels = ['Advance', 'Core', 'Self Service', 'Not Classified']
            values = [189, 84, 371, 42]
            max_value = max(values) * 1.1 # 막대 길이 조절을 위한 최대값

            for i in range(len(labels)):
                label = labels[i]
                value = values[i]

                label_col, bar_col = st.columns([1, 3]) 

                with label_col:
                    st.markdown(f'<div style="font-size: 14px; margin-top: 8px;"><strong>{label}</strong></div>', unsafe_allow_html=True)

                with bar_col:
                    fig, ax = plt.subplots(figsize=(4, 0.15)) 
                    ax.barh(0, value, color='#007BFF', height=0.4) 
                    ax.text(value/2, 0, f'{value}', va='center', ha='center', color='white', fontsize=10, fontweight='bold') 
                    ax.set_xlim(0, max_value) 
                    ax.axis('off')
                    st.pyplot(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

with col_right_recent_activity:
    # Recent User Activity (2x2)
    with st.container(height=360, border=True): # 2x2 비율 (가로:세로 = 1:1)
        st.markdown('<div class="widget-title">Recent User Activity</div>', unsafe_allow_html=True)
        st.markdown('<div class="widget-content">', unsafe_allow_html=True)
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
                    <div class="user-icon {status}">{status}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
