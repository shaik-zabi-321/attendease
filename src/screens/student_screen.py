import numpy as np
import streamlit as st
from src.ui.style_base_layout import (
    style_base_layout,
    style_background_dashboard
)
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from PIL import Image
from src.pipelines.facepipeline import predict_attendance, get_face_embeddings, train_classifier
from src.database.db import get_all_students, create_students, get_student_attendence, get_student_subjects, unenroll_student_subject
from src.pipelines.voice_pipeline import get_voice_embedding
import time
from src.components.enrolldialog import enroll_dialog
from src.components.registration_dialog import registration_dialog


def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    st.subheader(f""" welcome,{student_data['name']}""")

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()

    with c2:
        if st.button("Log out", key="teacher_login_back_btn", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

        st.space()

    col1, col2 = st.columns(2)
    with col1:
        st.header("Your Enrolled Subjects")
    with col2:
        if st.button("Enroll in subjects"):
            enroll_dialog()
    st.divider()

    with st.spinner("Loading your enrolled subjects"):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendence(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {'total': 0, 'attended': 0})

        def unenroll_btn():
            if st.button("unenroll from this subject ", type='tertiary', key=f"unenroll_{sid}"):
                unenroll_student_subject(student_id, sid)
                st.toast("Sucessfully unenrolled")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ("", 'total', stats['total']),
                    ("", 'attended', stats['attended']),
                ],
                footer_callback=unenroll_btn
            )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type='secondary',
            key="teacher_login_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state.login_type = None
            st.rerun()

    st.header('Login using face id ', text_alignment='center')
    st.space()
    st.space()

    photo_source = st.camera_input("position your face in the center")
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning"):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('face not found')
            elif num_faces > 1:
                st.warning("multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'welcome back {student["name"]}')
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.info('face not recogized you might be a new student ')
                        registration_dialog(img)
                else:
                    st.info('face not recogized you might be a new student ')
                    registration_dialog(img)

    footer_dashboard()
