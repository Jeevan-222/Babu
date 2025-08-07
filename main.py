import streamlit as st
import wikipedia
import requests

# -------------------- CONFIG --------------------
st.set_page_config(page_title="DJ BAK Chatbot", layout="wide")
st.title("📚 DJ BAK Chatbot")

GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # 🔐 Replace this

# -------------------- SESSION INIT --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- FUNCTIONS --------------------
def get_wikipedia_summary(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "Sorry, I couldn't find anything on that topic."
        summary = wikipedia.summary(results[0], sentences=2, auto_suggest=False, redirect=True)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Your query is ambiguous. Did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.PageError:
        return "Sorry, I couldn't find a page matching your query."
    except Exception:
        return "Oops, something went wrong."

def get_coordinates(location):
    """Get lat/lon from Google Maps Geocoding API"""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            latlon = results[0]["geometry"]["location"]
            return latlon["lat"], latlon["lng"]
    return None, None

# -------------------- CHATBOT INPUT --------------------
user_input = st.text_input("🧠 What's on your mind!?", key="chat_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = get_wikipedia_summary(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    st.session_state.chat_input = ""
    st.experimental_rerun()

# -------------------- LOCATION SEARCH --------------------
location_input = st.text_input("📍 Search a location on Google Maps", key="location_input")

if location_input:
    lat, lon = get_coordinates(location_input)
    if lat and lon:
        st.success(f"Found location: {location_input} ({lat}, {lon})")
        st.map(data={"lat": [lat], "lon": [lon]})
    else:
        st.error("❌ Location not found.")

# -------------------- CHAT HISTORY --------------------
st.markdown("## 💬 Chat History")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")

# -------------------- ABOUT / FEATURES BUTTONS --------------------
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("About Me"):
        st.info("👋 Hi! I'm DJ BAK Chatbot, your Wikipedia-powered assistant.")
with col2:
    if st.button("Features"):
        st.info("🔍 Ask me anything! I search Wikipedia and show locations on Google Maps.")
