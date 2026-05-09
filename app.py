import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.database.config import DatabaseConfigError, DatabaseConnectionError


def show_database_error(error):
    st.error("Database connection failed")
    st.warning(
        "SnapClass could not reach Supabase. Check your internet connection, DNS, "
        "and `.streamlit/secrets.toml` values for `SUPABASE_URL` and `SUPABASE_KEY`."
    )

    with st.expander("Technical details"):
        st.code(str(error))
        if error.__cause__:
            st.code(f"{type(error.__cause__).__name__}: {error.__cause__}")

    if st.button("Retry connection", type="primary"):
        st.rerun()

def main():

    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon= "https://i.ibb.co/YTYGn5qV/logo.png"
    )

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    try:
        match st.session_state['login_type']:
            case 'teacher':
                teacher_screen()

            case 'student':
                student_screen()
            
            case None:
                home_screen()


        join_code = st.query_params.get('join-code')
        if join_code:
            if st.session_state.login_type != 'student':
                st.session_state.login_type = 'student' # shift to student portal if join code is present in url    
                st.rerun()
            if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student': # only show enroll dialog if user is logged in as student
                auto_enroll_dialog(join_code) # open enroll dialog if join code is present in url and user is logged in as student
    except (DatabaseConfigError, DatabaseConnectionError) as error:
        show_database_error(error)
    
main()

