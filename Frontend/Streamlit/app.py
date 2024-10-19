import streamlit as st
from PIL import Image

if 'welcome_page' not in st.session_state:
    st.session_state.welcome_page = True

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazir&display=swap');
    body, h1, p {
        font-family: 'Vazir', sans-serif;
    }
    .button {
        background-color: #4CAF50; /* سبز */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
    }
    .button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.welcome_page:
    st.title("Welcome to the eKYC System")
    st.write("This is the user interface for uploading and verifying documents.")
    if st.button("شروع کنید"):
        st.session_state.welcome_page = False

else:
    gifs = [
        ('face_recognition.gif', 'این تصویر اول است و درباره پروژه تشخیص چهره است.'),
    ]
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    current_gif, description = gifs[st.session_state.current_index]
    gif = Image.open(current_gif)
    st.image(gif, caption=description, use_column_width=True)

    st.markdown('<div class="centered">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button('⬅️ قبلی', key='previous'):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1

    with col3:
        if st.session_state.current_index < len(gifs) - 1:
            if st.button('➡️ بعدی', key='next'):
                st.session_state.current_index += 1
        else:
            if st.button('شروع کن', key='restart'):
                st.session_state.welcome_page = True
                st.session_state.current_index = 0

    st.markdown('</div>', unsafe_allow_html=True)
