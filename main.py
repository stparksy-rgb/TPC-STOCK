import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# ============================================================
# 📱 TABLET PRO - AI 트레이딩 시스템
# ============================================================
# 갤럭시탭 S10+ 가로모드 최적화
# Slow Stochastic 8.5.5 전용
# 프로페셔널 HTS 수준 차트
# ============================================================

# 페이지 설정 (비밀번호 체크 전에 설정해야 함)
st.set_page_config(
    layout="wide",
    page_title="TABLET PRO",
    page_icon="📱",
    initial_sidebar_state="collapsed"
)

# 비밀번호 설정 (비공개)
CORRECT_PASSWORD = "****"

# ============================================================
# 스토캐스틱 파라미터 (8.5.5) - 박수영님 지시대로
# ============================================================
K_PERIOD = 8
D_PERIOD = 5
SMOOTH_K = 5
OVERSOLD = 25
OVERBOUGHT = 75

# 비밀번호 확인
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    if st.session_state["password_correct"]:
        return True
    
    st.markdown("""
    <style>
    .stApp { background: #000000; }
    </style>
    <div style='text-align: center; padding: 60px 20px;'>
        <div style='font-size: 60px; margin-bottom: 15px;'>📱</div>
        <h1 style='background: linear-gradient(90deg, #FF416C, #FF4B2B); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-size: 2.5em; font-weight: 900; letter-spacing: 2px;'>
        TABLET PRO
        </h1>
        <p style='color: #555; font-size: 1em; margin-top: 8px; letter-spacing: 4px;'>
        AI TRADING SYSTEM
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        password = st.text_input("", type="password", placeholder="접속 코드", label_visibility="collapsed")
        if st.button("🔓 접속", use_container_width=True, type="primary"):
            if password == CORRECT_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ 코드 오류")
    return False

if not check_password():
    st.stop()

# ============================================================
# CSS 스타일 (프로페셔널 HTS 스타일)
# ============================================================
st.markdown("""
<style>
/* 전체 배경 - 순수 검정 */
.stApp {
    background: #000000 !important;
    color: #E0E0E0;
}

/* 컨테이너 */
.block-container {
    padding: 0.3rem 0.8rem !important;
    max-width: 100% !important;
}

/* 헤더 숨기기 */
header[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stDeployButton { display: none !important; }

/* 신호 카드 - 적극매수 (빨간색 강조) */
.signal-strong-buy {
    background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(200, 0, 0, 0.1) 100%);
    border: 3px solid #FF0000;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    animation: pulse-red 1.5s ease-in-out infinite;
    box-shadow: 0 0 25px rgba(255, 0, 0, 0.4);
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.4); }
    50% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.6); }
}

/* 신호 카드 - 매수 */
.signal-buy {
    background: linear-gradient(135deg, rgba(255, 107, 53, 0.2) 0%, rgba(200, 80, 40, 0.1) 100%);
    border: 3px solid #FF6B35;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}

/* 신호 카드 - 관망 */
.signal-neutral {
    background: rgba(60, 60, 60, 0.3);
    border: 2px solid #555555;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}

/* 신호 카드 - 매도 */
.signal-sell {
    background: linear-gradient(135deg, rgba(41, 121, 255, 0.2) 0%, rgba(30, 90, 200, 0.1) 100%);
    border: 3px solid #2979FF;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}

/* 정보 박스 */
.info-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
    border: 1px solid #333;
    border-radius: 10px;
    padding: 15px;
    margin: 6px 0;
}

/* 종목 버튼 */
.stButton > button {
    background: #1a1a1a !important;
    border: 2px solid #333 !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #FF416C, #FF4B2B) !important;
    border-color: #FF416C !important;
}

/* 입력 필드 */
.stTextInput > div > div > input {
    background: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-size: 16px !important;
}

/* selectbox */
.stSelectbox > div > div {
    background: #111 !important;
    border: 1px solid #333 !important;
}

/* 스크롤바 숨기기 */
::-webkit-scrollbar { width: 0; height: 0; }

/* 조건 체크 태그 */
.tag-pass {
    display: inline-block;
    background: rgba(0, 255, 0, 0.15);
    border: 1px solid #00FF00;
    color: #00FF00;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 13px;
    font-weight: 600;
    margin: 3px;
}

.tag-fail {
    display: inline-block;
    background: rgba(100, 100, 100, 0.1);
    border: 1px solid #444;
    color: #666;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 13px;
    margin: 3px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 데이터 함수
# ============================================================

@st.cache_data(ttl=180)
def get_stock_data(ticker, period="1y"):
    """일봉 데이터 가져오기 (1년치 - 스크롤로 과거 볼 수 있게)"""
    try:
        clean_ticker = ticker.strip()
        if not clean_ticker.isdigit() or len(clean_ticker) != 6:
            return None, None
        
        # 코스피 시도
        ticker_symbol = clean_ticker + ".KS"
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=period, interval="1d")
        
        # 코스닥 시도
        if df.empty:
            ticker_symbol = clean_ticker + ".KQ"
            stock = yf.Ticker(ticker_symbol)
            df = stock.history(period=period, interval="1d")
        
        if df.empty:
            return None, None
        
        # 종목명
        try:
            info = stock.info
            name = info.get('longName', info.get('shortName', clean_ticker))
            if name and len(name) > 20:
                name = name[:20]
        except:
            name = clean_ticker
        
        return df, name
    except Exception as e:
        return None, None

def calculate_stochastic(df):
    """Slow Stochastic 8.5.5 계산"""
    low_min = df['Low'].rolling(window=K_PERIOD).min()
    high_max = df['High'].rolling(window=K_PERIOD).max()
    
    # Fast %K
    fast_k = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    
    # Slow %K = Fast %K의 이동평균
    df['%K'] = fast_k.rolling(window=SMOOTH_K).mean()
    
    # Slow %D = Slow %K의 이동평균
    df['%D'] = df['%K'].rolling(window=D_PERIOD).mean()
    
    return df

def generate_signals(df):
    """매매 신호 생성"""
    df['Buy_Signal'] = None
    df['Sell_Signal'] = None
    df['Strong_Buy'] = False
    
    for i in range(1, len(df)):
        prev_k = df['%K'].iloc[i-1]
        prev_d = df['%D'].iloc[i-1]
        curr_k = df['%K'].iloc[i]
        curr_d = df['%D'].iloc[i]
        
        # 적극매수: 골든크로스 + %K, %D 모두 과매도
        if (prev_k < prev_d and curr_k > curr_d and 
            curr_k <= OVERSOLD and curr_d <= OVERSOLD):
            df.at[df.index[i], 'Buy_Signal'] = df['Low'].iloc[i] * 0.97
            df.at[df.index[i], 'Strong_Buy'] = True
        
        # 일반 매수: 골든크로스 + %K만 과매도
        elif (prev_k < prev_d and curr_k > curr_d and curr_k <= OVERSOLD):
            df.at[df.index[i], 'Buy_Signal'] = df['Low'].iloc[i] * 0.97
        
        # 매도: 데드크로스 + 과매수
        elif (prev_k > prev_d and curr_k < curr_d and curr_k >= OVERBOUGHT):
            df.at[df.index[i], 'Sell_Signal'] = df['High'].iloc[i] * 1.03
    
    return df

def analyze_current_signal(df):
    """현재 신호 분석"""
    if len(df) < 2:
        return "⏸️ 관망", "neutral", {}
    
    curr = df.iloc[-1]
    prev = df.iloc[-2]
    
    k_val = curr['%K'] if not pd.isna(curr['%K']) else 50
    d_val = curr['%D'] if not pd.isna(curr['%D']) else 50
    
    conditions = {
        'golden_cross': prev['%K'] < prev['%D'] and k_val > d_val,
        'dead_cross': prev['%K'] > prev['%D'] and k_val < d_val,
        'oversold_k': k_val <= OVERSOLD,
        'oversold_d': d_val <= OVERSOLD,
        'overbought': k_val >= OVERBOUGHT
    }
    
    if conditions['golden_cross'] and conditions['oversold_k'] and conditions['oversold_d']:
        return "🚀 적극매수", "strong-buy", conditions
    elif conditions['golden_cross'] and conditions['oversold_k']:
        return "📈 매수", "buy", conditions
    elif conditions['dead_cross'] and conditions['overbought']:
        return "📉 매도", "sell", conditions
    else:
        return "⏸️ 관망", "neutral", conditions

# ============================================================
# 차트 생성 (프로페셔널 HTS 수준)
# ============================================================

def create_pro_chart(df, name, initial_view_days=65):
    """프로페셔널 수준 차트 생성 - 전체 데이터 + 좌우 스크롤 가능"""
    
    # 전체 데이터 사용 (스크롤로 과거 차트 볼 수 있게)
    chart_df = df.copy()
    
    # 서브플롯: 캔들(70%) + 스토캐스틱(30%)
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.72, 0.28]
    )
    
    # ========== 1. 캔들스틱 (HTS 스타일) ==========
    fig.add_trace(go.Candlestick(
        x=chart_df.index,
        open=chart_df['Open'],
        high=chart_df['High'],
        low=chart_df['Low'],
        close=chart_df['Close'],
        increasing=dict(line=dict(color='#FF3333', width=1), fillcolor='#FF3333'),
        decreasing=dict(line=dict(color='#3366FF', width=1), fillcolor='#3366FF'),
        name='',
        showlegend=False
    ), row=1, col=1)
    
    # ========== 2. 매매 신호 마커 (수정됨) ==========
    # 적극매수 신호 (Strong_Buy == True)
    strong_buy_mask = chart_df['Strong_Buy'] == True
    strong_buy = chart_df[strong_buy_mask]
    
    # 일반 매수 신호 (Buy_Signal이 있고 Strong_Buy가 아닌 것)
    normal_buy_mask = (~chart_df['Buy_Signal'].isna()) & (chart_df['Strong_Buy'] == False)
    normal_buy = chart_df[normal_buy_mask]
    
    # 매도 신호
    sell_mask = ~chart_df['Sell_Signal'].isna()
    sell = chart_df[sell_mask]
    
    # 적극매수 마커 (빨간 삼각형 + 노란 테두리) - 먼저 그리기
    if len(strong_buy) > 0:
        fig.add_trace(go.Scatter(
            x=strong_buy.index,
            y=strong_buy['Buy_Signal'],
            mode='markers+text',
            marker=dict(
                symbol='triangle-up',
                size=24,
                color='#FF0000',
                line=dict(width=3, color='#FFFF00')
            ),
            text=['적극매수'] * len(strong_buy),
            textposition='bottom center',
            textfont=dict(size=12, color='#FF0000', family='Arial Black'),
            name='적극매수',
            showlegend=False
        ), row=1, col=1)
    
    # 일반 매수 마커
    if len(normal_buy) > 0:
        fig.add_trace(go.Scatter(
            x=normal_buy.index,
            y=normal_buy['Buy_Signal'],
            mode='markers+text',
            marker=dict(symbol='triangle-up', size=18, color='#FF6B35'),
            text=['매수'] * len(normal_buy),
            textposition='bottom center',
            textfont=dict(size=11, color='#FF6B35'),
            name='매수',
            showlegend=False
        ), row=1, col=1)
    
    # 매도 마커
    if len(sell) > 0:
        fig.add_trace(go.Scatter(
            x=sell.index,
            y=sell['Sell_Signal'],
            mode='markers+text',
            marker=dict(symbol='triangle-down', size=20, color='#2979FF'),
            text=['매도'] * len(sell),
            textposition='top center',
            textfont=dict(size=11, color='#2979FF'),
            name='매도',
            showlegend=False
        ), row=1, col=1)
    
    # ========== 3. 스토캐스틱 8.5.5 ==========
    # %K 라인 (하늘색)
    fig.add_trace(go.Scatter(
        x=chart_df.index,
        y=chart_df['%K'],
        mode='lines',
        line=dict(color='#00BFFF', width=2),
        name='%K',
        showlegend=False
    ), row=2, col=1)
    
    # %D 라인 (주황색)
    fig.add_trace(go.Scatter(
        x=chart_df.index,
        y=chart_df['%D'],
        mode='lines',
        line=dict(color='#FFA500', width=2),
        name='%D',
        showlegend=False
    ), row=2, col=1)
    
    # 과매수/과매도 영역 표시
    fig.add_hrect(y0=OVERBOUGHT, y1=100, fillcolor="rgba(255,0,0,0.1)", 
                  line_width=0, row=2, col=1)
    fig.add_hrect(y0=0, y1=OVERSOLD, fillcolor="rgba(0,255,0,0.1)", 
                  line_width=0, row=2, col=1)
    
    # 기준선
    fig.add_hline(y=OVERBOUGHT, line_dash="dash", line_color="#FF6666", 
                  line_width=1, opacity=0.8, row=2, col=1)
    fig.add_hline(y=OVERSOLD, line_dash="dash", line_color="#66FF66", 
                  line_width=1, opacity=0.8, row=2, col=1)
    fig.add_hline(y=50, line_dash="dot", line_color="#666666", 
                  line_width=1, opacity=0.5, row=2, col=1)
    
    # ========== 초기 표시 범위 설정 (최근 65일) ==========
    if len(chart_df) > initial_view_days:
        end_date = chart_df.index[-1]
        start_date = chart_df.index[-initial_view_days]
    else:
        end_date = chart_df.index[-1]
        start_date = chart_df.index[0]
    
    # ========== 레이아웃 설정 ==========
    fig.update_layout(
        height=520,
        template="plotly_dark",
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        margin=dict(l=10, r=70, t=10, b=30),
        xaxis_rangeslider_visible=False,
        showlegend=False,
        hovermode='x unified',
        dragmode='pan'
    )
    
    # X축 설정 (날짜) - 초기 범위 설정 + 스크롤 가능
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.15)',
        showticklabels=False,
        range=[start_date, end_date],  # 초기 표시 범위
        row=1, col=1
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.15)',
        tickfont=dict(size=11, color='#888'),
        tickformat='%m/%d',
        range=[start_date, end_date],  # 초기 표시 범위
        row=2, col=1
    )
    
    # Y축 설정 - 가격
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.15)',
        side='right',
        tickformat=',',
        tickfont=dict(size=12, color='#AAAAAA'),
        row=1, col=1
    )
    
    # Y축 설정 - 스토캐스틱
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.15)',
        side='right',
        range=[-5, 105],
        tickvals=[0, 25, 50, 75, 100],
        tickfont=dict(size=11, color='#888'),
        row=2, col=1
    )
    
    return fig

# ============================================================
# 메인 UI (가로 모드 최적화)
# ============================================================

# 상단 헤더
col_h1, col_h2, col_h3 = st.columns([1.5, 4, 1.5])

with col_h1:
    st.markdown("""
    <div style='padding: 8px 0;'>
        <span style='font-size: 22px; font-weight: 900; color: #FF416C;'>📱 TABLET PRO</span>
        <span style='color: #444; font-size: 12px; margin-left: 8px;'>8.5.5</span>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    tickers_input = st.text_input(
        "종목코드",
        value="005930, 000660, 035420",
        placeholder="종목코드 (쉼표로 구분)",
        label_visibility="collapsed"
    )

with col_h3:
    analyze_btn = st.button("🔍 분석", type="primary", use_container_width=True)

# 분석 실행
if analyze_btn or 'stocks_data' not in st.session_state:
    tickers = [t.strip() for t in tickers_input.split(',') if t.strip()]
    
    if tickers:
        stocks_data = []
        
        for ticker in tickers:
            df, name = get_stock_data(ticker, period="1y")
            if df is not None and not df.empty:
                df = calculate_stochastic(df)
                df = generate_signals(df)
                signal_text, signal_type, conditions = analyze_current_signal(df)
                
                curr = df.iloc[-1]
                prev = df.iloc[-2] if len(df) > 1 else curr
                change = ((curr['Close'] - prev['Close']) / prev['Close'] * 100) if len(df) > 1 else 0
                
                stocks_data.append({
                    'ticker': ticker,
                    'name': name if name else ticker,
                    'df': df,
                    'signal_text': signal_text,
                    'signal_type': signal_type,
                    'conditions': conditions,
                    'price': curr['Close'],
                    'change': change,
                    'k_val': curr['%K'] if not pd.isna(curr['%K']) else 50,
                    'd_val': curr['%D'] if not pd.isna(curr['%D']) else 50
                })
        
        if stocks_data:
            st.session_state['stocks_data'] = stocks_data
            st.session_state['selected_idx'] = 0

# 데이터 표시
if 'stocks_data' in st.session_state and st.session_state['stocks_data']:
    stocks = st.session_state['stocks_data']
    
    # 종목 선택 버튼
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    
    btn_cols = st.columns(len(stocks))
    for i, stock in enumerate(stocks):
        with btn_cols[i]:
            # 신호 아이콘
            if stock['signal_type'] == 'strong-buy':
                icon = "🔴"
            elif stock['signal_type'] == 'buy':
                icon = "🟠"
            elif stock['signal_type'] == 'sell':
                icon = "🔵"
            else:
                icon = "⚪"
            
            btn_label = f"{icon} {stock['name'][:6]}" if len(stock['name']) > 6 else f"{icon} {stock['name']}"
            
            if st.button(btn_label, key=f"btn_{i}", use_container_width=True):
                st.session_state['selected_idx'] = i
                st.rerun()
    
    # 현재 선택된 종목
    idx = st.session_state.get('selected_idx', 0)
    if idx >= len(stocks):
        idx = 0
    
    stock = stocks[idx]
    
    # 구분선
    st.markdown("<hr style='border: 1px solid #222; margin: 8px 0;'>", unsafe_allow_html=True)
    
    # 메인 레이아웃: 좌측 정보 | 우측 차트
    col_info, col_chart = st.columns([1, 2.5])
    
    # ========== 좌측: 정보 패널 ==========
    with col_info:
        # 종목명 & 코드
        st.markdown(f"""
        <div style='margin-bottom: 8px;'>
            <div style='font-size: 20px; font-weight: 800; color: #FFF;'>{stock['name']}</div>
            <div style='font-size: 13px; color: #666;'>{stock['ticker']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 현재가
        change_color = "#FF3333" if stock['change'] >= 0 else "#3366FF"
        change_sign = "+" if stock['change'] >= 0 else ""
        
        st.markdown(f"""
        <div class='info-box'>
            <div style='color: #888; font-size: 12px;'>현재가</div>
            <div style='font-size: 32px; font-weight: 800; color: {change_color};'>
                {stock['price']:,.0f}<span style='font-size: 14px; color: #666;'>원</span>
            </div>
            <div style='font-size: 16px; color: {change_color};'>{change_sign}{stock['change']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI 신호
        signal_class = f"signal-{stock['signal_type']}"
        st.markdown(f"""
        <div class='{signal_class}'>
            <div style='font-size: 28px; font-weight: 800;'>{stock['signal_text']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 스토캐스틱 수치
        k_val = stock['k_val']
        d_val = stock['d_val']
        k_color = "#00FF00" if k_val <= OVERSOLD else "#FF3333" if k_val >= OVERBOUGHT else "#00BFFF"
        d_color = "#00FF00" if d_val <= OVERSOLD else "#FF3333" if d_val >= OVERBOUGHT else "#FFA500"
        
        st.markdown(f"""
        <div class='info-box'>
            <div style='color: #888; font-size: 12px; margin-bottom: 8px;'>STOCHASTIC 8.5.5</div>
            <div style='display: flex; justify-content: space-around;'>
                <div style='text-align: center;'>
                    <div style='color: #666; font-size: 11px;'>%K</div>
                    <div style='font-size: 26px; font-weight: 800; color: {k_color};'>{k_val:.1f}</div>
                </div>
                <div style='text-align: center;'>
                    <div style='color: #666; font-size: 11px;'>%D</div>
                    <div style='font-size: 26px; font-weight: 800; color: {d_color};'>{d_val:.1f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 매수 조건 체크
        cond = stock['conditions']
        gc = "tag-pass" if cond.get('golden_cross') else "tag-fail"
        ok = "tag-pass" if cond.get('oversold_k') else "tag-fail"
        od = "tag-pass" if cond.get('oversold_d') else "tag-fail"
        
        st.markdown(f"""
        <div class='info-box'>
            <div style='color: #888; font-size: 12px; margin-bottom: 6px;'>매수 조건</div>
            <span class='{gc}'>골든크로스</span>
            <span class='{ok}'>%K≤25</span>
            <span class='{od}'>%D≤25</span>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== 우측: 차트 ==========
    with col_chart:
        fig = create_pro_chart(stock['df'], stock['name'], show_days=65)
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': False,
            'scrollZoom': True
        })
        
        # 차트 범례
        st.markdown("""
        <div style='display: flex; justify-content: center; gap: 25px; margin-top: 3px;'>
            <span style='color: #00BFFF; font-size: 13px; font-weight: 600;'>━ %K</span>
            <span style='color: #FFA500; font-size: 13px; font-weight: 600;'>━ %D</span>
            <span style='color: #66FF66; font-size: 13px;'>┄ 25</span>
            <span style='color: #FF6666; font-size: 13px;'>┄ 75</span>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== 하단: 요약 ==========
    st.markdown("<hr style='border: 1px solid #222; margin: 10px 0;'>", unsafe_allow_html=True)
    
    strong_buy_cnt = sum(1 for s in stocks if s['signal_type'] == 'strong-buy')
    buy_cnt = sum(1 for s in stocks if s['signal_type'] == 'buy')
    sell_cnt = sum(1 for s in stocks if s['signal_type'] == 'sell')
    neutral_cnt = sum(1 for s in stocks if s['signal_type'] == 'neutral')
    
    sum_cols = st.columns(5)
    
    with sum_cols[0]:
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: rgba(255,0,0,0.1); 
        border-radius: 8px; border: 1px solid rgba(255,0,0,0.3);'>
            <div style='color: #888; font-size: 11px;'>적극매수</div>
            <div style='font-size: 26px; font-weight: 800; color: #FF0000;'>{strong_buy_cnt}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sum_cols[1]:
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: rgba(255,107,53,0.1); 
        border-radius: 8px; border: 1px solid rgba(255,107,53,0.3);'>
            <div style='color: #888; font-size: 11px;'>매수</div>
            <div style='font-size: 26px; font-weight: 800; color: #FF6B35;'>{buy_cnt}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sum_cols[2]:
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: rgba(41,121,255,0.1); 
        border-radius: 8px; border: 1px solid rgba(41,121,255,0.3);'>
            <div style='color: #888; font-size: 11px;'>매도</div>
            <div style='font-size: 26px; font-weight: 800; color: #2979FF;'>{sell_cnt}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sum_cols[3]:
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: rgba(100,100,100,0.1); 
        border-radius: 8px; border: 1px solid rgba(100,100,100,0.3);'>
            <div style='color: #888; font-size: 11px;'>관망</div>
            <div style='font-size: 26px; font-weight: 800; color: #888;'>{neutral_cnt}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sum_cols[4]:
        now = datetime.now()
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: rgba(50,50,50,0.3); 
        border-radius: 8px; border: 1px solid #333;'>
            <div style='color: #888; font-size: 11px;'>업데이트</div>
            <div style='font-size: 18px; font-weight: 600; color: #666;'>{now.strftime("%H:%M")}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("🔍 종목코드를 입력하고 '분석' 버튼을 눌러주세요")