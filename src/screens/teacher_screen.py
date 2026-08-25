import streamlit as st
import numpy as np
from datetime import datetime
import pandas as pd

from src.ui.style_base_layout import (
    style_base_layout,
    style_background_dashboard
)
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.share_subject import share_subject_dialog
from src.components.add_photo_dialog import add_photo_dialog
from src.pipelines.facepipeline import predict_attendance
from src.database.config import supabase
from src.components.attendence_log import add_attendence_logs
from src.components.voice_attendece_dialog import voice_attendence_dialog
from src.database.db import get_attendence_for_teacher
from src.database.db import (
    check_teacher_exist,
    create_techer,
    teacher_login,
    get_teacher_subjects
)


# =========================================================
# TEACHER SCREEN
# =========================================================

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    # Decide whether to show Login or Register
    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.subheader(f""" welcome,{teacher_data['name']}""")
    # LEFT COLUMN

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    # LEFT COLUMN
    with c1:
        header_dashboard()

        # RIGHT COLUMN
    with c2:

        # logout
        if st.button("Log out", key="teacher_login_back_btn", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'Take Attendence'

    t1, t2, t3 = st.columns(3)

    with t1:
        type1 = 'primary' if st.session_state.current_teacher_tab == 'Take Attendence' else 'tertiary'
        if st.button("Take Attendence", type=type1, width='stretch',):
            st.session_state.current_teacher_tab = 'Take Attendence'
            st.rerun()

    with t2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'Manage subjects' else 'tertiary'
        if st.button("Manage subjects", type=type2, width='stretch',):
            st.session_state.current_teacher_tab = 'Manage subjects'
            st.rerun()
    with t3:
        type3 = 'primary' if st.session_state.current_teacher_tab == 'Attendence records' else 'tertiary'
        if st.button("Attendence records", type=type3, width='stretch',):
            st.session_state.current_teacher_tab = 'Attendence records'
            st.rerun()
    if st.session_state.current_teacher_tab == 'Take Attendence':
        take_attendence()
    if st.session_state.current_teacher_tab == 'Manage subjects':
        manage_subjects()
    if st.session_state.current_teacher_tab == 'Attendence records':
        attendence_records()

    footer_dashboard()


def take_attendence():
    st.header("Take attendence")
    teacher_id = st.session_state.teacher_data['teacher_id']

    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images = []
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("Please create a subject ")
        return
    subject_options = {
        f"{s['name']}-{s['subject_code']}": s['subject_id'] for s in subjects}
    col1, col2 = st.columns(2)
    with col1:

        selected_subject_label = st.selectbox(
            'select subject', options=list(subject_options.keys()))
    with col2:
        if st.button('ADD photos', type='primary', width='stretch'):
            add_photo_dialog()
    selected_subject_id = subject_options[selected_subject_label]

    if st.session_state.attendence_images:
        st.header("Added photos")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendence_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f"photo{idx+1}")

    c1, c2, c3 = st.columns(3)
    has_photo = bool(st.session_state.attendence_images)
    with c1:

        if st.button("Clear All Photos", width='stretch', type='tertiary'):
            st.session_state.attendence_images = []
            st.rerun()

    with c2:

        if st.button('Run Analysis', width='stretch', type='secondary', disabled=not has_photo):
            with st.spinner('Deep Scanning Class '):
                all_detected_id = {}
                for idx, img in enumerate(st.session_state.attendence_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_id.setdefault(
                                student_id, []).append(f"photo{idx+1}")
                enrolled_res = supabase.table('subject_students').select(
                    "*,students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No Students Enrolled In This Course")
                    return
                else:
                    results, attendence_to_log = [], []
                    current_time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_id.get(
                            int(student['student_id']), [])
                        is_present = len(sources) > 0
                        results.append({
                            "Name": student['name'],
                            "Id": student['student_id'],
                            "Source": ",".join(sources) if is_present else "-",
                            "Status": "Present" if is_present else "Absent"

                        })
                        attendence_to_log.append({
                            "student_id": student['student_id'],
                            "subject_id": selected_subject_id,
                            "timestamp": current_time_stamp,
                            "is_present": bool(is_present)

                        })
                add_attendence_logs(pd.DataFrame(results), attendence_to_log)

    with c3:
        if st.button('voice attendence', type='primary', width='stretch'):
            voice_attendence_dialog(selected_subject_id)


def manage_subjects():

    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage subjects ")
    with col2:
        if st.button("create new subject", width='stretch'):
            create_subject_dialog(teacher_id)

    # list all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🧑‍🎓", "students", sub['total_students']),
                ("📅", "classes", sub['total_classes'])
            ]

        def share_btn():
            if st.button(f"share code:{sub['name']}", key=f"share {sub['subject_code']}"):
                share_subject_dialog(sub['name'], sub['subject_code'])
        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )

    else:
        st.warning("No sunjects found ")


def attendence_records():
    st.header("Manage records ")
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendence_for_teacher(teacher_id)
    if not records:
        return
    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M%p") if ts else "N'A",
            "subject": r['subjects']['name'],
            "subject_code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })
    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'time', 'subject', 'subject_code']).agg(
            present_count=('is_present', 'sum'),
            total_count=('is_present', 'count')


        ).reset_index()
    )
    summary['Attendence stats'] = (
        "✅️"+summary['present_count'].astype(str)+"/"
        + summary['total_count'].astype(str)+' students'
    )

    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [['time', 'subject', 'subject_code', 'Attendence stats']]
                  )
    st.dataframe(display_df, width='stretch', hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


# =========================================================
# TEACHER LOGIN SCREEN
# =========================================================

def teacher_screen_login():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    # LEFT COLUMN
    with c1:
        header_dashboard()

    # RIGHT COLUMN
    with c2:

        # GO BACK TO HOME
        if st.button(
            "Go back to Home",
            key="teacher_login_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state.login_type = None
            st.rerun()

        st.header(
            "Login using password",
            text_alignment="center"
        )

        st.space()

        # USERNAME
        teacher_username = st.text_input(
            "Enter Username",
            placeholder="shaik zabi"
        )

        st.space()

        # PASSWORD
        teacher_password = st.text_input(
            "Enter password",
            type="password",
            placeholder="enter password"
        )

        st.divider()

        # LOGIN AND REGISTER BUTTONS
        btnc1, btnc2 = st.columns(
            [1, 1],
            gap="small"
        )

        with btnc1:
            login_clicked = st.button(
                "Login",
                icon=":material/passkey:",
                width="stretch"
            )

        with btnc2:
            register_clicked = st.button(
                "Register",
                type="primary",
                icon=":material/person_add:",
                width="stretch"
            )

        # LOGIN ACTION
        if login_clicked:

            if login_teacher(teacher_username, teacher_password):

                st.toast("Welcome back!")

                import time
                time.sleep(1)

                st.rerun()

            else:
                st.error("Invalid username or password")

        # REGISTER ACTION
        if register_clicked:
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


# =========================================================
# REGISTER TEACHER
# =========================================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_password,
    teacher_pass_confirm
):

    # Check empty fields
    if (
        not teacher_username
        or not teacher_name
        or not teacher_password
        or not teacher_pass_confirm
    ):
        return False, "All fields are required"

    # Check username
    if check_teacher_exist(teacher_username):
        return False, "Username already exists"

    # Check password confirmation
    if teacher_password != teacher_pass_confirm:
        return False, "Passwords don't match"

    # Create teacher
    try:

        create_techer(
            teacher_username,
            teacher_password,
            teacher_name
        )

        return True, "Successfully created"

    except Exception as e:

        print("Registration error:", e)

        return False, f"Registration error: {e}"


# =========================================================
# TEACHER REGISTER SCREEN
# =========================================================

def teacher_screen_register():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    # LEFT COLUMN
    with c1:
        header_dashboard()

    # RIGHT COLUMN
    with c2:

        # GO BACK TO HOME
        if st.button(
            "Go back to Home",
            key="teacher_register_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state.login_type = None
            st.rerun()

        st.header(
            "Register your teacher profile",
            text_alignment="center"
        )

        st.space()

        # USERNAME
        teacher_username = st.text_input(
            "Enter Username",

        )

        st.space()

        # NAME
        teacher_name = st.text_input(
            "Enter name",

        )

        st.space()

        # PASSWORD
        teacher_password = st.text_input(
            "Enter password",
            type="password",

        )

        st.space()

        # CONFIRM PASSWORD
        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="enter password"
        )

        st.divider()

        # REGISTER AND LOGIN BUTTONS
        btnc1, btnc2 = st.columns(
            [1, 1],
            gap="small"
        )

        with btnc1:
            register_clicked = st.button(
                "Register now",
                icon=":material/person_add:",
                width="stretch"
            )

        with btnc2:
            login_clicked = st.button(
                "Login instead",
                type="primary",
                icon=":material/passkey:",
                width="stretch"
            )

        # REGISTER ACTION
        if register_clicked:

            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_password,
                confirm_password
            )

            if success:

                st.success(message)

                import time
                time.sleep(2)

                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

        # LOGIN ACTION
        if login_clicked:
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()
