import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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
