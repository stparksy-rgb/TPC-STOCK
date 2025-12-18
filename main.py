import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# ==========================================
# 📱 갤럭시탭 S10+ 전용 AI 트레이딩 시스템
# ==========================================
# - 가로 모드 전용
# - Slow Stochastic 8.5.5
# - 실시간 신호 확인 우선
# - 터치 최적화 UI
# ==========================================

# 비밀번호 설정 (비공개)
CORRECT_PASSWORD = "1248"

# 스토캐스틱 파라미터 (8.5.5)
K_PERIOD = 8
D_PERIOD = 5
SMOOTH_K = 5
OVERSOLD = 25
OVERBOUGHT = 75

# 페이지 설정 (가로 모드 최적화)
st.set_page_config(
    layout="wide",
    page_title="📱 AI 트레이딩",
    page_icon="📱",
    initial_sidebar_state="collapsed"
)

# 비밀번호 확인
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    if st.session_state["password_correct"]:
        return True
    
    st.markdown("""
    <div style='text-align: center; padding: 80px 20px; background: linear-gradient(180deg, #0d0d0d 0%, #1a1a2e 100%); min-height: 100vh;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>📱</div>
        <h1 style='background: linear-gradient(90deg, #00d4ff 0%, #7b2ff7 50%, #f107a3 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8em; font-weight: 800;'>
        AI SIGNAL
        </h1>
        <p style='color: #666; font-size: 1.2em; margin-top: 10px; letter-spacing: 3px;'>TABLET EDITION</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        password = st.text_input("🔐", type="password", placeholder="접속 코드 입력", label_visibility="collapsed")
        if st.button("접속하기", use_container_width=True, type="primary"):
            if password == CORRECT_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ 코드 오류")
    
    return False

if not check_password():
    st.stop()

# 태블릿 전용 CSS (가로 모드 최적화)
st.markdown("""
<style>
/* 기본 배경 - AMOLED 최적화 */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #0d1117 50%, #0a0a0a 100%);
    color: #e0e0e0;
}

/* 컨테이너 패딩 최소화 */
.block-container {
    padding: 0.5rem 1rem !important;
    max-width: 100% !important;
}

/* 헤더 숨기기 */
header[data-testid="stHeader"] {
    display: none !important;
}

/* 사이드바 숨기기 */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* 신호 카드 - 적극매수 */
.signal-strong-buy {
    background: linear-gradient(135deg, rgba(255, 0, 60, 0.25) 0%, rgba(255, 50, 100, 0.15) 100%);
    border: 3px solid #ff003c;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    animation: glow-red 2s ease-in-out infinite;
    box-shadow: 0 0 40px rgba(255, 0, 60, 0.3);
}

@keyframes glow-red {
    0%, 100% { box-shadow: 0 0 40px rgba(255, 0, 60, 0.3); }
    50% { box-shadow: 0 0 60px rgba(255, 0, 60, 0.5); }
}

/* 신호 카드 - 매수 */
.signal-buy {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 150, 255, 0.1) 100%);
    border: 3px solid #00d4ff;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
}

/* 신호 카드 - 관망 */
.signal-neutral {
    background: linear-gradient(135deg, rgba(100, 100, 100, 0.15) 0%, rgba(80, 80, 80, 0.1) 100%);
    border: 2px solid #444;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
}

/* 신호 카드 - 매도 */
.signal-sell {
    background: linear-gradient(135deg, rgba(123, 47, 247, 0.2) 0%, rgba(100, 40, 200, 0.1) 100%);
    border: 3px solid #7b2ff7;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 0 30px rgba(123, 47, 247, 0.2);
}

/* 종목 탭 버튼 */
.stock-tab {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 2px solid #2a2a4a;
    border-radius: 15px;
    padding: 15px 25px;
    margin: 5px;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 120px;
    text-align: center;
}

.stock-tab:hover, .stock-tab.active {
    background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
    border-color: #00d4ff;
    transform: scale(1.05);
}

/* 정보 카드 */
.info-card {
    background: linear-gradient(135deg, rgba(30, 30, 50, 0.8) 0%, rgba(20, 20, 40, 0.8) 100%);
    border: 1px solid rgba(100, 100, 150, 0.3);
    border-radius: 16px;
    padding: 20px;
    margin: 8px 0;
    backdrop-filter: blur(10px);
}

/* 큰 텍스트 (터치 친화적) */
.big-text {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.2;
}

.medium-text {
    font-size: 24px;
    font-weight: 600;
}

.small-text {
    font-size: 14px;
    color: #888;
    letter-spacing: 1px;
}

/* 스토캐스틱 수치 */
.stoch-value {
    font-family: 'SF Mono', 'Monaco', monospace;
    font-size: 32px;
    font-weight: 700;
}

/* 조건 체크 */
.condition-check {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 25px;
    font-size: 16px;
    font-weight: 600;
    margin: 5px;
}

.condition-pass {
    background: rgba(0, 255, 100, 0.2);
    border: 2px solid #00ff64;
    color: #00ff64;
}

.condition-fail {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid #444;
    color: #666;
}

/* Streamlit 버튼 커스텀 */
.stButton > button {
    background: linear-gradient(135deg, #1e1e3f 0%, #2a2a5a 100%) !important;
    border: 2px solid #3a3a6a !important;
    border-radius: 15px !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    padding: 15px 30px !important;
    min-height: 60px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%) !important;
    border-color: #00d4ff !important;
    transform: scale(1.02) !important;
}

/* 새로고침 버튼 특별 스타일 */
.refresh-btn > button {
    background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%) !important;
    min-width: 150px !important;
}

/* 입력 필드 */
.stTextInput > div > div > input {
    background: #1a1a2e !important;
    border: 2px solid #2a2a4a !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 18px !important;
    padding: 15px !important;
}

/* selectbox */
.stSelectbox > div > div {
    background: #1a1a2e !important;
    border: 2px solid #2a2a4a !important;
    border-radius: 12px !important;
}

/* 차트 컨테이너 */
.chart-container {
    background: rgba(15, 15, 25, 0.9);
    border-radius: 20px;
    padding: 15px;
    border: 1px solid rgba(100, 100, 150, 0.2);
}

/* 스크롤바 숨기기 (태블릿) */
::-webkit-scrollbar {
    width: 0px;
    height: 0px;
}

/* 터치 영역 최적화 */
* {
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
}
</style>
""", unsafe_allow_html=True)

# 30분봉 데이터 가져오기
@st.cache_data(ttl=180)
def get_intraday_data(ticker, days=10):
    try:
        clean_ticker = ticker.strip()
        if not clean_ticker.isdigit() or len(clean_ticker) != 6:
            return None, None
        
        ticker_symbol = clean_ticker + ".KS"
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=f"{days}d", interval="30m")
        
        if df.empty:
            ticker_symbol = clean_ticker + ".KQ"
            stock = yf.Ticker(ticker_symbol)
            df = stock.history(period=f"{days}d", interval="30m")
        
        if df.empty:
            return None, None
        
        try:
            info = stock.info
            name = info.get('longName', info.get('shortName', clean_ticker))
            # 이름이 너무 길면 자르기
            if len(name) > 15:
                name = name[:15] + "..."
        except:
            name = clean_ticker
        
        return df, name
    except:
        return None, None

# Slow Stochastic 8.5.5 계산
def calculate_stochastic_855(df):
    low_min = df['Low'].rolling(window=K_PERIOD).min()
    high_max = df['High'].rolling(window=K_PERIOD).max()
    k = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['%K'] = k.rolling(window=SMOOTH_K).mean()
    df['%D'] = df['%K'].rolling(window=D_PERIOD).mean()
    return df

# 신호 생성
def generate_signals(df):
    df['Buy_Signal'] = None
    df['Sell_Signal'] = None
    df['Strong_Buy'] = False
    
    for i in range(1, len(df)):
        prev_k = df['%K'].iloc[i-1]
        prev_d = df['%D'].iloc[i-1]
        curr_k = df['%K'].iloc[i]
        curr_d = df['%D'].iloc[i]
        
        # 골든크로스 (적극매수): %K, %D 모두 과매도 구간에서 골든크로스
        if (prev_k < prev_d and curr_k > curr_d and 
            curr_k <= OVERSOLD and curr_d <= OVERSOLD):
            df.at[df.index[i], 'Buy_Signal'] = df['Low'].iloc[i] * 0.98
            df.at[df.index[i], 'Strong_Buy'] = True
        
        # 일반 매수: %K만 과매도 구간에서 골든크로스
        elif (prev_k < prev_d and curr_k > curr_d and curr_k <= OVERSOLD):
            df.at[df.index[i], 'Buy_Signal'] = df['Low'].iloc[i] * 0.98
        
        # 매도: 과매수 구간에서 데드크로스
        elif (prev_k > prev_d and curr_k < curr_d and curr_k >= OVERBOUGHT):
            df.at[df.index[i], 'Sell_Signal'] = df['High'].iloc[i] * 1.02
    
    return df

# 현재 신호 분석
def analyze_current_signal(df):
    if len(df) < 2:
        return "⏸️ 데이터 부족", "neutral", {}
    
    current = df.iloc[-1]
    prev = df.iloc[-2]
    
    k_val = current['%K']
    d_val = current['%D']
    
    # 조건 체크
    conditions = {
        'golden_cross': prev['%K'] < prev['%D'] and k_val > d_val,
        'dead_cross': prev['%K'] > prev['%D'] and k_val < d_val,
        'oversold_k': k_val <= OVERSOLD,
        'oversold_d': d_val <= OVERSOLD,
        'overbought': k_val >= OVERBOUGHT
    }
    
    # 신호 판정
    if conditions['golden_cross'] and conditions['oversold_k'] and conditions['oversold_d']:
        return "🚀 적극매수", "strong-buy", conditions
    elif conditions['golden_cross'] and conditions['oversold_k']:
        return "📈 매수", "buy", conditions
    elif conditions['dead_cross'] and conditions['overbought']:
        return "📉 매도", "sell", conditions
    else:
        return "⏸️ 관망", "neutral", conditions

# 차트 생성 (3개월치, 큰 캔들, HTS 스타일)
def create_tablet_chart(df, name):
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.05,
        shared_xaxes=True
    )
    
    # 3개월치만 표시 (약 60개 캔들) - 30분봉 기준 최근 60개
    recent_df = df.tail(60)
    
    # 캔들스틱 - HTS 스타일 (빨간 양봉, 파란 음봉)
    fig.add_trace(go.Candlestick(
        x=recent_df.index,
        open=recent_df['Open'],
        high=recent_df['High'],
        low=recent_df['Low'],
        close=recent_df['Close'],
        increasing=dict(
            line=dict(color='#FF3333', width=1.5), 
            fillcolor='#FF3333'
        ),
        decreasing=dict(
            line=dict(color='#3366FF', width=1.5), 
            fillcolor='#3366FF'
        ),
        name='Price',
        showlegend=False
    ), row=1, col=1)
    
    # 매매 신호 마커
    strong_buy = recent_df[recent_df['Strong_Buy'] == True]
    normal_buy = recent_df[(~recent_df['Buy_Signal'].isna()) & (recent_df['Strong_Buy'] == False)]
    sell = recent_df[~recent_df['Sell_Signal'].isna()]
    
    if len(strong_buy) > 0:
        fig.add_trace(go.Scatter(
            x=strong_buy.index,
            y=strong_buy['Buy_Signal'],
            mode='markers+text',
            marker=dict(symbol='triangle-up', size=25, color='#FF0000',
                       line=dict(width=2, color='#FFFF00')),
            text=['적극매수'] * len(strong_buy),
            textposition='bottom center',
            textfont=dict(size=12, color='#FF0000', family='Arial Black'),
            name='적극매수',
            showlegend=False
        ), row=1, col=1)
    
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
    
    # 스토캐스틱 8.5.5
    fig.add_trace(go.Scatter(
        x=recent_df.index,
        y=recent_df['%K'],
        line=dict(color='#00BFFF', width=2.5),
        name='%K',
        showlegend=False
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=recent_df.index,
        y=recent_df['%D'],
        line=dict(color='#FFA500', width=2.5),
        name='%D',
        showlegend=False
    ), row=2, col=1)
    
    # 과매도/과매수 라인
    fig.add_hline(y=OVERBOUGHT, line_dash="dash", line_color="#FF6666", 
                  opacity=0.7, row=2, col=1)
    fig.add_hline(y=OVERSOLD, line_dash="dash", line_color="#66FF66", 
                  opacity=0.7, row=2, col=1)
    
    # 레이아웃 (태블릿 최적화 - 차트 크게)
    fig.update_layout(
        height=500,
        template="plotly_dark",
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#0a0a0a',
        margin=dict(l=10, r=70, t=20, b=20),
        xaxis_rangeslider_visible=False,
        showlegend=False,
        hovermode='x unified',
        dragmode='pan'
    )
    
    # X축 설정
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(80, 80, 80, 0.3)',
        showticklabels=False,
        row=1, col=1
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(80, 80, 80, 0.3)',
        tickfont=dict(size=12, color='#888'),
        row=2, col=1
    )
    
    # Y축 설정 - 가격 (오른쪽, 원 단위)
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(80, 80, 80, 0.3)',
        side='right',
        tickformat=',',
        ticksuffix='',
        tickfont=dict(size=13, color='#AAAAAA'),
        row=1, col=1
    )
    
    # Y축 설정 - 스토캐스틱
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(80, 80, 80, 0.3)',
        side='right',
        range=[0, 100],
        tickvals=[0, 25, 50, 75, 100],
        tickfont=dict(size=12, color='#888'),
        row=2, col=1
    )
    
    return fig

# ==========================================
# 메인 UI (가로 모드 최적화)
# ==========================================

# 상단 헤더
col_header1, col_header2, col_header3 = st.columns([2, 4, 2])

with col_header1:
    st.markdown("""
    <div style='padding: 10px 0;'>
        <span style='font-size: 28px; font-weight: 800; 
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        📱 AI SIGNAL
        </span>
        <span style='color: #444; font-size: 14px; margin-left: 10px;'>8.5.5</span>
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    # 관심종목 입력
    tickers_input = st.text_input(
        "종목코드",
        value="005930, 000660, 035420",
        placeholder="종목코드 입력 (쉼표 구분)",
        label_visibility="collapsed"
    )

with col_header3:
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        days = st.selectbox("기간", [5, 10, 15], index=1, label_visibility="collapsed")
    with col_btn2:
        refresh_btn = st.button("🔄 분석", type="primary", use_container_width=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# 종목 분석 및 표시
if refresh_btn or 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    
    tickers = [t.strip() for t in tickers_input.split(',') if t.strip()]
    
    if not tickers:
        st.warning("종목코드를 입력해주세요")
        st.stop()
    
    # 선택된 종목 인덱스
    if 'selected_idx' not in st.session_state:
        st.session_state['selected_idx'] = 0
    
    # 모든 종목 데이터 수집
    all_stocks = []
    for ticker in tickers:
        df, name = get_intraday_data(ticker, days)
        if df is not None and not df.empty:
            df = calculate_stochastic_855(df)
            df = generate_signals(df)
            signal_text, signal_type, conditions = analyze_current_signal(df)
            
            all_stocks.append({
                'ticker': ticker,
                'name': name,
                'df': df,
                'signal_text': signal_text,
                'signal_type': signal_type,
                'conditions': conditions,
                'price': df.iloc[-1]['Close'],
                'k_val': df.iloc[-1]['%K'],
                'd_val': df.iloc[-1]['%D'],
                'change': ((df.iloc[-1]['Close'] - df.iloc[-2]['Close']) / df.iloc[-2]['Close'] * 100) if len(df) > 1 else 0
            })
    
    if not all_stocks:
        st.error("유효한 종목 데이터가 없습니다")
        st.stop()
    
    st.session_state['all_stocks'] = all_stocks

# 저장된 데이터 사용
if 'all_stocks' in st.session_state:
    all_stocks = st.session_state['all_stocks']
    
    # 종목 탭 (하단 고정 스타일)
    st.markdown("---")
    
    tab_cols = st.columns(len(all_stocks))
    for i, stock in enumerate(all_stocks):
        with tab_cols[i]:
            # 신호에 따른 색상
            if stock['signal_type'] == 'strong-buy':
                btn_style = "🔴"
            elif stock['signal_type'] == 'buy':
                btn_style = "🔵"
            elif stock['signal_type'] == 'sell':
                btn_style = "🟣"
            else:
                btn_style = "⚪"
            
            if st.button(f"{btn_style} {stock['name'][:8]}", key=f"tab_{i}", use_container_width=True):
                st.session_state['selected_idx'] = i
                st.rerun()
    
    st.markdown("---")
    
    # 현재 선택된 종목
    idx = st.session_state.get('selected_idx', 0)
    if idx >= len(all_stocks):
        idx = 0
    
    stock = all_stocks[idx]
    
    # 메인 레이아웃 (가로 모드: 좌측 신호 | 우측 차트 - 차트 더 크게)
    col_signal, col_chart = st.columns([1, 2.2])
    
    # 좌측: 신호 패널
    with col_signal:
        # 종목명 & 가격
        change_color = "#ff3366" if stock['change'] >= 0 else "#3366ff"
        change_sign = "+" if stock['change'] >= 0 else ""
        
        st.markdown(f"""
        <div class='info-card'>
            <div class='small-text'>현재가</div>
            <div class='big-text' style='color: {change_color};'>
                {stock['price']:,.0f}<span style='font-size: 20px; color: #666;'>원</span>
            </div>
            <div style='font-size: 22px; color: {change_color}; margin-top: 5px;'>
                {change_sign}{stock['change']:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI 신호
        signal_class = f"signal-{stock['signal_type']}"
        signal_text = stock['signal_text']
        
        st.markdown(f"""
        <div class='{signal_class}'>
            <div style='font-size: 38px; font-weight: 800;'>{signal_text}</div>
            <div style='font-size: 16px; margin-top: 10px; color: #888;'>
                {stock['name']} ({stock['ticker']})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 스토캐스틱 수치
        k_color = "#00ff64" if stock['k_val'] <= OVERSOLD else "#ff3366" if stock['k_val'] >= OVERBOUGHT else "#00d4ff"
        d_color = "#00ff64" if stock['d_val'] <= OVERSOLD else "#ff3366" if stock['d_val'] >= OVERBOUGHT else "#ff8c00"
        
        st.markdown(f"""
        <div class='info-card'>
            <div class='small-text'>STOCHASTIC 8.5.5</div>
            <div style='display: flex; justify-content: space-around; margin-top: 15px;'>
                <div style='text-align: center;'>
                    <div style='color: #666; font-size: 14px;'>%K</div>
                    <div class='stoch-value' style='color: {k_color};'>{stock['k_val']:.1f}</div>
                </div>
                <div style='text-align: center;'>
                    <div style='color: #666; font-size: 14px;'>%D</div>
                    <div class='stoch-value' style='color: {d_color};'>{stock['d_val']:.1f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 조건 체크
        conditions = stock['conditions']
        
        gc_class = "condition-pass" if conditions.get('golden_cross') else "condition-fail"
        os_k_class = "condition-pass" if conditions.get('oversold_k') else "condition-fail"
        os_d_class = "condition-pass" if conditions.get('oversold_d') else "condition-fail"
        
        st.markdown(f"""
        <div class='info-card'>
            <div class='small-text'>매수 조건</div>
            <div style='margin-top: 12px;'>
                <span class='condition-check {gc_class}'>골든크로스</span>
                <span class='condition-check {os_k_class}'>%K≤25</span>
                <span class='condition-check {os_d_class}'>%D≤25</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 우측: 차트 (크고 선명하게)
    with col_chart:
        fig = create_tablet_chart(stock['df'], stock['name'])
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': False,
            'scrollZoom': True
        })
        
        # 범례
        st.markdown("""
        <div style='display: flex; justify-content: center; gap: 40px; margin-top: 5px;'>
            <span style='color: #00BFFF; font-size: 15px; font-weight: bold;'>━ %K</span>
            <span style='color: #FFA500; font-size: 15px; font-weight: bold;'>━ %D</span>
            <span style='color: #66FF66; font-size: 15px;'>-- 25</span>
            <span style='color: #FF6666; font-size: 15px;'>-- 75</span>
        </div>
        """, unsafe_allow_html=True)

# 신호 요약 (하단)
if 'all_stocks' in st.session_state:
    all_stocks = st.session_state['all_stocks']
    
    strong_buy_count = sum(1 for s in all_stocks if s['signal_type'] == 'strong-buy')
    buy_count = sum(1 for s in all_stocks if s['signal_type'] == 'buy')
    sell_count = sum(1 for s in all_stocks if s['signal_type'] == 'sell')
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    summary_cols = st.columns(4)
    with summary_cols[0]:
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: rgba(255,0,60,0.1); 
        border-radius: 15px; border: 2px solid rgba(255,0,60,0.3);'>
            <div style='color: #888; font-size: 13px;'>적극매수</div>
            <div style='font-size: 32px; font-weight: 800; color: #ff003c;'>{strong_buy_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_cols[1]:
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: rgba(0,212,255,0.1); 
        border-radius: 15px; border: 2px solid rgba(0,212,255,0.3);'>
            <div style='color: #888; font-size: 13px;'>매수</div>
            <div style='font-size: 32px; font-weight: 800; color: #00d4ff;'>{buy_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_cols[2]:
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: rgba(123,47,247,0.1); 
        border-radius: 15px; border: 2px solid rgba(123,47,247,0.3);'>
            <div style='color: #888; font-size: 13px;'>매도</div>
            <div style='font-size: 32px; font-weight: 800; color: #7b2ff7;'>{sell_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_cols[3]:
        now = datetime.now()
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: rgba(50,50,70,0.3); 
        border-radius: 15px; border: 2px solid rgba(80,80,100,0.3);'>
            <div style='color: #888; font-size: 13px;'>업데이트</div>
            <div style='font-size: 20px; font-weight: 600; color: #666;'>{now.strftime("%H:%M")}</div>
        </div>
        """, unsafe_allow_html=True)