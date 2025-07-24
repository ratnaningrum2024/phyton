import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ====================================================================
# MUAT API KEY DARI FILE .env UNTUK KEAMANAN
# ====================================================================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-flash"

# ====================================================================
# KONTEKS AWAL CHATBOT: KONSULTASI TUMBUH KEMBANG ANAK
# ====================================================================
INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": [
            "Saya adalah TumbuhCeriaBot, asisten digital Anda untuk membantu memahami dan memantau tumbuh kembang anak usia 0 sampai 12 tahun. Saya siap memberikan informasi mengenai perkembangan anak, saran stimulasi, dan menjawab pertanyaan seputar perawatan, gizi, serta kebiasaan anak berdasarkan usia mereka."
        ],
    },
    {
        "role": "model",
        "parts": ["Baik! Berikan usia anak dan pertanyaan Anda."],
    },
]

# ====================================================================
# KONFIGURASI GEMINI API
# ====================================================================
if not API_KEY:
    st.error("API Key belum diatur. Buat file .env dan tambahkan GEMINI_API_KEY=...")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,
            max_output_tokens=500,
        ),
    )
except Exception as e:
    st.error(f"Gagal menginisialisasi model Gemini: {e}")
    st.stop()

# ====================================================================
# STREAMLIT UI
# ====================================================================
st.title("🤖 TumbuhCeriaBot")
st.markdown("Chatbot untuk konsultasi tumbuh kembang anak usia 0–12 tahun.")
st.divider()

# Inisialisasi session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)
    st.session_state.messages = [
        {"role": "assistant", "text": INITIAL_CHATBOT_CONTEXT[1]["parts"][0]}
    ]

# Tampilkan riwayat obrolan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Input pengguna
user_input = st.chat_input("Tulis pertanyaan Anda di sini...")
if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("TumbuhCeriaBot sedang mengetik..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                reply = response.text
            except Exception as e:
                reply = f"⚠️ Maaf, terjadi kesalahan: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "text": reply})
