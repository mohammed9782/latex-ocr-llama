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
        if "ocr_result" in st.session_state:
            del st.session_state["ocr_result"]
        st.rerun()


st.markdown('<p style="margin-top: -20px;">Extract LaTeX code from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)
st.markdown('---')

# move upload controls to the side bar

with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image')

        if st.button("Extract LaTeX Code", type="primary"):
            with st.spinner('Processing image...'):
                try:
                    response = ollama.chat(
                        model="llama3.2-vision",
                        messages=[{
                            'role' : 'user',
                            'content' : """derstand the mathematical equation in the provided image and output the corresponding LaTeX code.
                            Here are some guidelines you MUST follow or you will be penalized:
                            - NEVER include any additional text or explanations.
                            - DON'T add dollar signs ($) around the LaTeX code.
                            - DO NOT extract simplified versions of the equations.
                            - NEVER add documentclass, packages or begindocument.
                            - DO NOT explain the symbols used in the equation.
                            - Output only the LaTeX code corresponding to the mathematical equations in the image.""",
                            'images': [uploaded_file.getvalue()]
                        }]
                    )
                    st.session_state["ocr_result"] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")


# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown('### Extracted LaTeX Code:')
    st.code(st.session_state["ocr_result"], language='latex')

    st.markdown('### Latex renderd:')

    cleaned_latex = st.session_state['ocr_result'].replace(r"\[", "").replace(r"\]", "")
    st.latex(cleaned_latex)
else:
    st.info('Upload an image and click "Extract LaTeX Code" to see the results here.')

# Footer
st.markdown('---')
st.markdown('Developed by Your Name. Powered by Streamlit and Ollama.') 

