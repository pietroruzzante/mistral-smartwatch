import requests
import streamlit as st
import time

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Smartwatch Health Report",
    layout="wide"
)
col1, col2 = st.columns([2, 1])

with col1:
    #file uploader
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        # post request with dataframe
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{BACKEND_URL}/analyze", files={"file": uploaded_file})

        if response.status_code == 200:
            # save json to app state
            st.session_state.response = response.json()

            st.subheader("Metrics")
            # TODO estrarre e plottare metriche

        else:
            st.error("Error in analysis request")

with col2:

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": ""}]

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
