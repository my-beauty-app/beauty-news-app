import streamlit as st
import feedparser
import urllib.parse

# --- デザイン設定 ---
st.set_page_config(page_title="Beauty News Pro", page_icon="💖")
st.markdown("""
    <style>
    .main { background-color: #fff5f7; }
    .stButton>button {
        background-color: #ff85a2; color: white; border-radius: 20px;
        font-weight: bold; width: 100%; border: none; height: 45px;
    }
    .stButton>button:hover {
        background-color: #ff4d7d;
    }
    .news-card {
        background-color: white; padding: 18px; border-radius: 15px;
        border-left: 6px solid #ff85a2; margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    .source-tag {
        background-color: #fee2e2; color: #991b1b;
        padding: 2px 8px; border-radius: 10px; font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ニュース取得関数 ---
def get_beauty_news(keyword, limit=15):
    encoded_keyword = urllib.parse.quote(keyword)
    rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(rss_url)
        return [{"title": e.title, "link": e.link, "date": e.published, "source": e.source.title} for e in feed.entries[:limit]]
    except:
        return []

# --- メイン画面 ---
st.title("🌸 美容医療 News Concierge")
st.write("気になるキーワードやカテゴリーから、最新のトレンドをチェック！")

# 1. カテゴリーボタン（横並び）
st.subheader("🎀 クイック検索")
col1, col2, col3 = st.columns(3)
with col1:
    btn_new = st.button("✨ 新メニュー")
with col2:
    btn_open = st.button("🏥 開院・オープン")
with col3:
    btn_alert = st.button("⚠️ トラブル・注意")

# 2. キーワード自由入力
st.subheader("🔍 キーワードで探す")
user_keyword = st.text_input("例：ポテンツァ、クマ取り、ヒアルロン酸", "美容医療")

# 検索ワードの決定ロジック
search_word = user_keyword
if btn_new: search_word = "美容医療 新メニュー"
if btn_open: search_word = "美容クリニック 開院 オープン"
if btn_alert: search_word = "美容医療 トラブル 消費者庁 注意"

# --- 結果の表示 ---
st.divider()
st.write(f"🔎 **「{search_word}」** の最新ニュースを表示中")

with st.spinner('最新情報を読み込み中...'):
    news_list = get_beauty_news(search_word)
    
    if not news_list:
        st.warning("ニュースが見つかりませんでした 😿")
    else:
        for news in news_list:
            st.markdown(f"""
            <div class="news-card">
                <span class="source-tag">{news['source']}</span>
                <span style="color: #666; font-size: 12px; margin-left: 10px;">📅 {news['date']}</span><br>
                <div style="margin-top: 10px;">
                    <a href="{news['link']}" target="_blank" style="text-decoration: none; color: #d6336c; font-size: 18px; font-weight: bold;">
                        {news['title']}
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.caption("※情報はGoogleニュースからリアルタイムで取得しています。")