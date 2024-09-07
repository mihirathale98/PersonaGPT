import streamlit as st
from persona import Persona
from gemini_api import GeminiAPI
from chat import ChatSession


gemini_api = GeminiAPI()

st.title("Persona GPT")


with st.sidebar:
    persona_name = st.text_input(
        "Who do you want to talk with?", key="persona_name_input"
    )

    if st.button("Create Persona"):
        if persona_name.strip() == "":
            st.warning("Please enter a valid persona name.")
        else:
            chat_session = ChatSession(persona_name)
            st.session_state.chat_session = chat_session
            st.session_state.persona_name = persona_name
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": f"You are now chatting with {persona_name}.",
                }
            ]
            st.success(f"Persona '{persona_name}' created successfully!")
    else:
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = None

if st.session_state.chat_session:
    st.write(f"Chatting with **{st.session_state.persona_name}**.")

    prompt = st.chat_input("Say something")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        chat_session = st.session_state.chat_session

        try:
            response = chat_session.converse(prompt)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            response = "Sorry, something went wrong while generating a response."

        st.session_state.messages.append(
            {"role": st.session_state.persona_name, "content": response}
        )

    if "messages" in st.session_state:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
else:
    st.write("Please create a Persona to start the conversation.")
