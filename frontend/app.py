import requests
import streamlit as st
import time
import pandas as pd
from io import StringIO

backend_url = "http://localhost:8000"

st.set_page_config(
    page_title="Smartwatch Health Report",
    layout="wide"
)
st.title("Smartwatch Data Analyzer")
st.write("This app provide a complete overview of daily health status, based on smartwatch data")

first_answer = ""
if "chat_ready" not in st.session_state:
    st.session_state.chat_ready = False

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ask me more about your health status!"}]


# Two-columns layout
col1, col2 = st.columns([2, 1])

# Left column
with col1:
    st.subheader("Upload data")

    files = None

    # manual upload
    uploaded_file = st.file_uploader("Load your CSV here", type=["csv"])
    st.write("Or try with an example dataset:")

    if uploaded_file:
        st.session_state.data = pd.read_csv(uploaded_file)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}

    # use example CSV
    if st.button("Use example CSV"):
        response = requests.get(f"{backend_url}/example")
        if response.status_code == 200:
            csv_data = StringIO(response.text)
            st.session_state.data = pd.read_csv(csv_data)
            files = {"file": ("example.csv", response.text, "text/csv")}
        else:
            st.error("Could not fetch example CSV from backend")

    # analyze data
    if files:
        analyze_response = requests.post(f"{backend_url}/analyze", files=files)

        if analyze_response.status_code == 200:
            resp = analyze_response.json()
            st.session_state.response = resp

            st.session_state.first_answer = resp["message"]
            st.session_state.first_answer_animated = False

            st.session_state.messages = []
            st.session_state.chat_ready = True
        else:
            st.error("Error analyzing dataset")

    # Show results
    if "data" in st.session_state and "response" in st.session_state:

        # --- Heart Rate & Stress side by side ---
        col3, col4 = st.columns(2)
        with col3:
            st.write("### Heart Rate")
            st.metric("Average heart rate",
                      f"{st.session_state.response['avg_hr']} bpm",
                      delta="-8", delta_color="inverse")
            st.line_chart(st.session_state.data,
                          y="heart_rate_bpm",
                          height=300,
                          x_label="time",
                          y_label="bpm",
                          color="#d8031c")
        with col4:
            st.write("### Stress Level")
            st.metric("Average stress level",
                      f"{st.session_state.response['avg_stress_level']}%",
                      delta="-8%", delta_color="inverse")

            st.line_chart(st.session_state.data,
                          y="stress_level",
                          height=300,
                          x_label="time",
                          y_label="stress level",
                          color="#9fcbee")

        # --- Sleep ---
        st.write("### Sleep")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Awake",
                      f"{st.session_state.response['sleep_count'][0] // 60}h {st.session_state.response['sleep_count'][0] % 60}m")
        with c2:
            st.metric("Light",
                      f"{st.session_state.response['sleep_count'][1] // 60}h {st.session_state.response['sleep_count'][1] % 60}m")
        with c3:
            st.metric("Deep",
                      f"{st.session_state.response['sleep_count'][2] // 60}h {st.session_state.response['sleep_count'][2] % 60}m")
        with c4:
            st.metric("REM",
                      f"{st.session_state.response['sleep_count'][3] // 60}h {st.session_state.response['sleep_count'][3] % 60}m")

        # --- Physical Activity ---
        st.write("### Physical Activity")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Total daily calories",
                      f"{st.session_state.response['total_calories']}",
                      delta=-520)
        with c2:
            st.metric("Total daily steps",
                      f"{st.session_state.response['total_steps']}",
                      delta=1154)

# Right column
with col2:
    st.subheader("Mistral Assistant Report")

    if not st.session_state.chat_ready:
        st.caption("Load a CSV to get an overview about your health status")

    # mostra SEMPRE il primo report se presente
    if "first_answer" in st.session_state:
        if not st.session_state.get("first_answer_animated", False):
            # anima SOLO la prima volta
            placeholder = st.empty()
            acc = ""
            for ch in st.session_state.first_answer:
                acc += ch
                time.sleep(0.01)
                placeholder.markdown(acc + "▌")
            placeholder.markdown(acc)
            st.session_state.first_answer_animated = True
        else:
            # dai rerun in poi: niente animazione
            st.markdown(st.session_state.first_answer)


# --- CHAT DI FOLLOW-UP (fuori dalle colonne) ---
if st.session_state.get("chat_ready", False):
    st.markdown("### More insights")

    # mostra solo i messaggi di follow-up (il primo report NON è qui)
    for m in st.session_state.get("messages", []):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    prompt = st.chat_input("Ask for more insights")
    if prompt:
        # append messaggio utente
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # invia al backend
        res = requests.post(f"{backend_url}/send_message", json={"message": prompt})
        if res.status_code == 200:
            answer = res.json()["message"]

            # typing finto
            with st.chat_message("assistant"):
                ph = st.empty()
                acc = ""
                for ch in answer:
                    acc += ch
                    time.sleep(0.01)
                    ph.markdown(acc + "▌")
                ph.markdown(acc)

            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("Error contacting backend")
