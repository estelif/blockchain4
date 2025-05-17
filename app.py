import streamlit as st
from utils.api_connectors import CryptoPanicAPI, CoinMarketCapAPI
from utils.data_processor import process_coin_data, process_news_data
from utils.ollama_integration import generate_ai_response
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize APIs
try:
    crypto_panic = CryptoPanicAPI()
    cmc = CoinMarketCapAPI()
except Exception as e:
    st.error(f"Failed to initialize APIs: {str(e)}")
    st.stop()

st.set_page_config(
    page_title="AI Crypto Assistant",
    page_icon="💲",
    layout="wide"
)

#CSS
def load_css():
    st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stTextInput input {
            background-color: #1E2130;
            color: white;
        }
        .stSelectbox select {
            background-color: #1E2130;
            color: white;
        }
        .coin-header {
            font-size: 24px;
            font-weight: bold;
            color: #00D1B2;
            margin-bottom: 10px;
        }
        .news-card {
            background-color: #1E2130;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .news-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .news-source {
            color: #888;
            font-size: 12px;
        }
        .positive {
            color: #00D1B2;
        }
        .negative {
            color: #FF3860;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# App header
st.title("💰 AI Crypto Assistant")
st.markdown("""
Get real-time cryptocurrency data, news, and AI-powered insights for the top 50 coins by market cap.
""")

# Sidebar coin selection
st.sidebar.header("Coin Selection")
top_coins = cmc.get_top_coins()
coin_symbols = [coin["symbol"] for coin in top_coins]
selected_coin = st.sidebar.selectbox("Select a cryptocurrency", coin_symbols)

# Main content
if selected_coin:
    coin_data = cmc.get_coin_data(selected_coin)
    processed_data = process_coin_data(coin_data)
    
    if processed_data:
        # Coin overview section
        st.markdown(f'<div class="coin-header">{processed_data["name"]} ({processed_data["symbol"]})</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Price", f"${processed_data['price']:,.2f}")
        with col2:
            st.metric("Market Cap", f"${processed_data['market_cap']:,.0f}")
        with col3:
            st.metric("Rank", f"#{processed_data['rank']}")
        
        # Price change indicators
        cols = st.columns(4)
        with cols[0]:
            delta = f"{processed_data['percent_change_1h']:.2f}%"
            st.metric("1h Change", delta, delta, delta_color="inverse")
        with cols[1]:
            delta = f"{processed_data['percent_change_24h']:.2f}%"
            st.metric("24h Change", delta, delta, delta_color="inverse")
        with cols[2]:
            delta = f"{processed_data['percent_change_7d']:.2f}%"
            st.metric("7d Change", delta, delta, delta_color="inverse")
        with cols[3]:
            last_updated = datetime.strptime(processed_data['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
            st.metric("Last Updated", last_updated.strftime("%Y-%m-%d %H:%M:%S"))
        
        # AI query section
        st.subheader("Ask About This Coin")
        user_query = st.text_input(f"What would you like to know about {processed_data['name']}?", 
                                  placeholder=f"E.g., 'What's the latest development for {processed_data['name']}?'")
        
        if user_query:
            # Get relevant news for context
            news_items = crypto_panic.get_news(processed_data["symbol"])
            processed_news = process_news_data(news_items)
            
            # Prepare context for ai
            context = f"""
            Current {processed_data['name']} ({processed_data['symbol']}) Data:
            - Price: ${processed_data['price']:,.2f}
            - Market Cap: ${processed_data['market_cap']:,.0f} (Rank #{processed_data['rank']})
            - 24h Change: {processed_data['percent_change_24h']:.2f}%
            
            Latest News:
            {'. '.join([n['title'] for n in processed_news[:3]])}
            """
            
            with st.spinner("Generating AI response..."):
                ai_response = generate_ai_response(user_query, context)
                st.markdown(f"**Response:**\n\n{ai_response}")
        
        # News Section
        st.subheader("Latest News")
        news_items = crypto_panic.get_news(processed_data["symbol"])
        processed_news = process_news_data(news_items)
        
        if not processed_news:
            st.info("No recent news found for this cryptocurrency.")
        else:
            for news in processed_news[:5]:  # Show top 5 news items
                with st.container():
                    st.markdown(f"""
                    <div class="news-card">
                        <div class="news-title">{news["title"]}</div>
                        <div class="news-source">
                            {news["source"]} • {news["published_at"]} • 
                            <span class="positive">👍 {news["votes"]}</span>
                        </div>
                        <a href="{news["url"]}" target="_blank">Read more</a>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("Failed to fetch data for the selected coin. Please try another one.")
else:
    st.warning("Please select a cryptocurrency from the sidebar.")

# Footer
st.markdown("---")
st.markdown("""
**Data Sources:** - Market Data: CoinMarketCap - News: CryptoPanic - AI: Ollama (Llama3:8b)
""")