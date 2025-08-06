import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 페이지 설정
st.set_page_config(layout="wide")

# ✅ CSS 스타일 정의
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

# ======================== ROW 1: LICENSE 요약 ========================
st.markdown("### FUE License")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Total</div><div class="big-number">500</div></div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Active</div><div class="big-number">292</div></div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Remaining</div><div class="big-number">208</div></div>', unsafe_allow_html=True)

with col4:
    with st.container():
        st.markdown('<div class="widget-box">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Utilization</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 0.5))
        ax.barh(0, 58, color='blue', height=0.4)
        ax.set_xlim(0, 100)
        ax.axis('off')
        st.pyplot(fig)
        st.markdown('<div class="big-number">58%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col5:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Variance</div><div class="big-number">+12</div></div>', unsafe_allow_html=True)

# ======================== ROW 2: License 상세 ========================
col6, col7, col8 = st.columns([2, 1, 1])

with col6:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Composition</div>', unsafe_allow_html=True)
        sizes = [76, 10, 8, 6]
        labels = ['A', 'B', 'C', 'D']
        fig2, ax2 = plt.subplots()
        ax2.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)
        st.markdown('</div>', unsafe_allow_html=True)

with col7:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">부서별 현황</div><div class="big-number">🏢</div></div>', unsafe_allow_html=True)

with col8:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">직무별 현황</div><div class="big-number">🛠️</div></div>', unsafe_allow_html=True)

# ======================== ROW 3: User 요약 ========================
st.markdown("### User")
col9, col10, col11 = st.columns(3)

with col9:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Total Users</div><div class="big-number">902</div></div>', unsafe_allow_html=True)

with col10:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Variance</div><div class="big-number">+7</div></div>', unsafe_allow_html=True)

with col11:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Inactive</div><div class="big-number">19</div></div>', unsafe_allow_html=True)

# ======================== ROW 4: User 상세 ========================
col12, col13 = st.columns([2, 2])

with col12:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">Recent Activity</div>', unsafe_allow_html=True)
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

with col13:
    with st.container():
        st.markdown('<div class="widget-box"><div class="widget-title">User License Type</div>', unsafe_allow_html=True)
        labels = ['Advance', 'Core', 'Self Service', 'Not Classified']
        values = [189, 84, 371, 42]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.barh(labels, values, color='skyblue')
        ax.set_xlim(0, max(values)*1.1)
        ax.set_xlabel('Users')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
