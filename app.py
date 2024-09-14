import streamlit as st
from src.persona import Persona
from src.gemini_api import GeminiAPI
from src.chat import ChatSession
from src.get_statements import PersonalityStatementFinder
from src.text_to_speech import TTS_Wrapper
from src.get_speech_from_web import VoiceSearch

import base64
import numpy as np


def load_audio(path):
    with open(path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    return audio_b64


gemini_api = GeminiAPI()
statement_finder = PersonalityStatementFinder()
voice_search = VoiceSearch()

if 'tts_wrapper' not in st.session_state:
    st.session_state.tts_wrapper = TTS_Wrapper()

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
            video_url = voice_search.get_speech_from_youtube(persona_name)
            if video_url is None:
                video_url = st.text_input('Enter a video URL to extract audio from')
            if video_url:
                st.session_state.wav_path = voice_search.get_audio_from_youtube(video_url)
                st.session_state.chat_session = chat_session
                st.session_state.relevant_statements = statement_finder.get_personality_statements(persona_name)
                st.write(f"Relevant Statements: {st.session_state.relevant_statements}")
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
            audio_bytes = st.session_state.tts_wrapper.get_speech(response, st.session_state.wav_path)
            audio_bytes_int = (np.array(audio_bytes) * 32767).astype(np.int16)

            audio_base64 = base64.b64encode(audio_bytes_int.tobytes()).decode('utf-8')
            print('Converted')
            st.session_state.messages.append(
            {"role": st.session_state.persona_name, "content": response, "audio": audio_base64}
        )



        except Exception as e:
            print(e)
            st.error(f"An error occurred: {e}")
            response = "Sorry, something went wrong while generating a response."




    if "messages" in st.session_state:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message['role'] == st.session_state.persona_name:
                    audio_data = base64.b64decode(message["audio"])
                    audio_bytes_int = np.frombuffer(audio_data, dtype=np.int16)

                    audio_bytes_float = audio_bytes_int.astype(np.float32) / 32767
                    # Play the audio

                    st.audio(audio_bytes_float, format='audio/wav', start_time=0, sample_rate=25000)
else:
    st.write("Please create a Persona to start the conversation.")
