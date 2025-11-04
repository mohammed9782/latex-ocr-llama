import streamlit as st
import ollama
from PIL import Image
import io   


# page configuration
st.set_page_config(
    page_title="Latex OCR with Llama 3.2 version",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("🦙 Latex OCR with Llama 3.2 version")


# Add clear bottons to the top-right corner
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        if "OCR_result" in st.session_state:
            del st.session_state["OCR_result"]
        st.rerun()


st.markdown('Extract latx code from images using Llama 3.2 version model. Upload an image containing mathematical expressions, and the app will extract the LaTeX code for you.')
st.markdown('---')

# move upload controls to the side bar

with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    st.markdown('---')