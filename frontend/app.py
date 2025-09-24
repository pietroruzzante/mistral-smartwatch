import requests
import streamlit as st
import time
import pandas as pd
from io import StringIO

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Smartwatch Health Report",
    layout="wide"
)
st.title("Smartwatch Health Report")
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
        response = requests.get(f"{BACKEND_URL}/example")
        if response.status_code == 200:
            csv_data = StringIO(response.text)
            st.session_state.data = pd.read_csv(csv_data)
            files = {"file": ("example.csv", response.text, "text/csv")}
        else:
            st.error("Could not fetch example CSV from backend")

    # analyze data
    if files:
        analyze_response = requests.post(f"{BACKEND_URL}/analyze", files=files)

        if analyze_response.status_code == 200:
            resp = analyze_response.json()
            st.session_state.response = resp

            # first chat message
            first_answer = resp["message"]
            st.session_state.messages = [{"role": "assistant", "content": first_answer}]
            st.session_state.chat_ready = True
        else:
            st.error("Error analyzing dataset")


    # Show results
    if "data" in st.session_state and "response" in st.session_state:
        # --- Heart Rate ---
        st.write("### Heart Rate")
        with st.container():
            st.metric("Average heart rate",
                      f"{st.session_state.response['avg_hr']} bpm",
                      delta="-8", delta_color="inverse")

            st.line_chart(st.session_state.data,
                          y="heart_rate_bpm",
                          height=300,
                          x_label="time",
                          y_label="bpm",
                          color="#d8031c")

        # --- Stress Level ---
        st.write("### Stress Level")
        with st.container():
            cols = st.columns(2)
            with cols[0]:
                st.metric("Average stress level",
                          f"{st.session_state.response['avg_stress_level']}%",
                          delta="-8%", delta_color="inverse")
            with cols[1]:
                st.metric("Maximum stress level",
                          f"{st.session_state.response['max_stress_level']}%",
                          delta="-3%", delta_color="inverse")

            st.line_chart(st.session_state.data,
                          y="stress_level",
                          height=300,
                          x_label="time",
                          y_label="stress level",
                          color="#9fcbee")

        # --- Sleep ---
        st.write("### Sleep")
        with st.container():
            cols = st.columns(4)
            with cols[0]:
                st.metric("Awake",
                          f"{st.session_state.response['sleep_count'][0] // 60}h {st.session_state.response['sleep_count'][0] % 60}m")
            with cols[1]:
                st.metric("Light",
                          f"{st.session_state.response['sleep_count'][1] // 60}h {st.session_state.response['sleep_count'][1] % 60}m")
            with cols[2]:
                st.metric("Deep",
                          f"{st.session_state.response['sleep_count'][2] // 60}h {st.session_state.response['sleep_count'][2] % 60}m")
            with cols[3]:
                st.metric("REM",
                          f"{st.session_state.response['sleep_count'][3] // 60}h {st.session_state.response['sleep_count'][3] % 60}m")

        # --- Physical Activity ---
        st.write("### Physical Activity")
        with st.container():
            cols = st.columns(2)
            with cols[0]:
                st.metric("Total daily calories",
                          f"{st.session_state.response['total_calories']}",
                          delta=-520)
            with cols[1]:
                st.metric("Total daily steps",
                          f"{st.session_state.response['total_steps']}",
                          delta=1154)

# Right column
with col2:
    st.subheader("Chat Health Assistant")

    # initial status
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Drag and drop a .csv or use the example to start the health report"}
        ]
    if "chat_ready" not in st.session_state:
        st.session_state.chat_ready = False

    # show chat
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # enable questions from users
    prompt = st.chat_input("Ask for more insights",
                           disabled=not st.session_state.chat_ready)

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        res = requests.post(f"{BACKEND_URL}/send_message", json={"message": prompt})
        if res.status_code == 200:
            answer = res.json()["message"]

            # Fake typing
            with st.chat_message("assistant"):
                placeholder = st.empty()
                acc = ""
                for ch in answer:
                    acc += ch
                    time.sleep(0.02)
                    placeholder.markdown(acc + "▌")
                placeholder.markdown(acc)

            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("Error contacting backend")

