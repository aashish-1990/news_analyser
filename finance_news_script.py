import streamlit as st
import feedparser
import openai
import os

st.set_page_config(page_title="Finance News Script Generator", layout="centered")
st.title("📈 Indian Finance News – Video Script Generator")

st.markdown("Get a YouTube/video-ready script from today's top Indian finance news headlines in one click!")

# --- OpenAI API Key ---
api_key = st.text_input("Enter your OpenAI API key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
if not api_key:
    st.warning("Please enter your OpenAI API key to use this app.")

# --- Fetch Finance News ---
def fetch_finance_news():
    rss_url = "https://news.google.com/rss/search?q=finance+india&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    headlines = []
    for entry in feed.entries[:8]:  # Get top 8 stories
        headlines.append(f"{entry.title} - {entry.link}")
    return headlines

# --- Generate Video Script ---
def create_summary(headlines, api_key):
    summary_prompt = (
        "You are an expert finance news analyst in India. "
        "Summarize the following headlines into a crisp, engaging, and informative video script, "
        "suitable for a 2-3 minute YouTube finance news update. "
        "Structure with intro, top stories, quick explanations, and a CTA at the end:\n\n"
        + "\n".join(headlines)
    )
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or "gpt-3.5-turbo" if you prefer
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=900,
        temperature=0.5,
    )
    return response.choices[0].message['content']

# --- App Workflow ---
if api_key:
    if st.button("Generate Today's Finance News Script"):
        with st.spinner("Fetching news and generating script..."):
            news = fetch_finance_news()
            st.subheader("Today's Top Finance News Headlines")
            for h in news:
                st.markdown(f"- {h}")
            script = create_summary(news, api_key)
            st.subheader("Generated Video Script")
            st.text_area("Script Output", script, height=300)
            st.success("Script ready! Copy and use for your video.")
            st.download_button("Download Script as TXT", data=script, file_name="finance_news_script.txt")
else:
    st.info("Enter your OpenAI API key to get started.")

st.caption("Created by Aashish Sharma | Powered by Streamlit + OpenAI")
