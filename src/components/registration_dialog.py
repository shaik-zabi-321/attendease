# Add this new function near the top of student_screen.py (or in its own file,
# e.g. src/components/registration_dialog.py, and import it)
import streamlit as st
from src.pipelines.facepipeline import get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import create_students
import time


@st.dialog("Register New Profile")
def registration_dialog(img):
    new_name = st.text_input('enter your name ', placeholder="eg. shaik zabi")

    st.subheader("optional: voice enrollment")
    st.info("enroll for voice only attendance")

    audio_data = None
    try:
        audio_data = st.audio_input(
            "record a short phrase like iam present, my name is zabi")
    except Exception as e:
        st.error('audio data failed')

    if st.button('create account', type='primary'):
        if new_name:
            with st.spinner("in progress"):
                embeddings = get_face_embeddings(img)
                if embeddings:
                    face_emb = embeddings[0].tolist()

                    voice_emb = None
                    if audio_data:
                        voice_emb = get_voice_embedding(audio_data.read())

                    response_data = create_students(
                        new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                    if response_data:
                        train_classifier()
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = response_data[0]
                        st.toast(f'profile created hi {new_name}')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error(
                        "couldnt capture your facial features for registration")
        else:
            st.warning('please enter your name ')


# --- Then in student_screen(), replace the old inline block ---
# OLD:
#   if student:
#       ...
#   else:
#       st.info('face not recogized you might be a new student ')
#   show_registration = True
#   if show_registration:
#       with st.container(border=True):
#           st.header("register new profile")
#           ... (all the old inline code)

# NEW:
