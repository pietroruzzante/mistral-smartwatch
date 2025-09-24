import requests
import streamlit as st
import time
import pandas as pd
import altair as alt

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Smartwatch Health Report",
    layout="wide"
)
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Smartwatch Health Report")
    #file uploader
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        st.session_state.data = pd.read_csv(uploaded_file)

        # post request with dataframe
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response = requests.post(f"{BACKEND_URL}/analyze", files=files)

        if response.status_code == 200:
            # save json to app state
            st.session_state.response = response.json()

            #hr_tab, = st.tabs(["Heart Rate"])
            "### Heart Rate"
            st.line_chart(data=st.session_state.data, height=300, y = "heart_rate_bpm", x_label="time", y_label="bpm", color="#d8031c")
            "### Stress"
            st.line_chart(data=st.session_state.data, height=300, y = "stress_level", x_label="time", y_label="stress_level", color="#9fcbee" )
            "### Sleep"
            with st.container(height=100):
                cols = st.columns(spec=4)
                with cols[0]:
                    st.metric("Awake", st.session_state.response["sleep_count"][3])
                with cols[1]:
                    st.metric("Light", st.session_state.response["sleep_count"][2])
                with cols[2]:
                    st.metric("Deep", st.session_state.response["sleep_count"][1])
                with cols[3]:
                    st.metric("REM", st.session_state.response["sleep_count"][0])

        else:
            st.error("Error in analysis request")

with col2:

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Drag and drop a .csv to start health report"}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if "response" in st.session_state:

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate stream of response with milliseconds delay
            for chunk in st.session_state.response['message'].split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
