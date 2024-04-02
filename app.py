import os
import streamlit as st
import shutil
from PIL import Image
from lyzr import QABot

os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

st.set_page_config(
    page_title="Lyzr",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Grammar Analyzer🔎 ")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Step into the world of flawless writing with our Grammar Analyzer app. Effortlessly elevate your document to perfection, showcasing precision and clarity with every sentence")

def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")


# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Streamlit app header
# st.title("Word File Uploader")

# File upload widget
uploaded_file = st.file_uploader("Choose Word file", type=["docx"])

if uploaded_file is not None:
    # Save the uploaded Word file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success(f"File successfully saved")


def get_files_in_directory(directory="data"):
    # This function helps us get the file path along with the filename.
    files_list = []

    # Ensure the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Check if the path points to a file (not a directory)
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list


def rag_implementation():
    # This function will implement RAG Lyzr QA bot
    path = get_files_in_directory()
    path = path[0]

    rag = QABot.docx_qa(
        input_files=[str(path)],
        llm_params={"model": "gpt-3.5-turbo"},
        # vector_store_params=vector_store_params
    )

    return rag


def resume_response():
    rag = rag_implementation()
    prompt = """  Follow the intructions as given below ,
                    - Run spell check to identify misspelled words. Correct each flagged word, ensuring accurate spelling and context.
                    - Carefully review for grammar and sentence structure errors. Correct subject-verb agreement, tense misuse, and punctuation errors.
                    - Proofread line by line, focusing on syntax, coherence, and clarity. Rectify awkward phrasing, unclear language, and inconsistencies in writing style. Rewrite or rephrase sentences for enhanced readability.
                    - Keep the corrected document and print it. Start printing the corrected version from the next line after this statement: "Correct version:".
                    - Errors : Show the errors in the document and it has been changed."""

    
    response = rag.query(prompt)
    return response.response

if uploaded_file is not None:
    automatice_response = resume_response()
    st.markdown(f"""{automatice_response}""")


# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's QABot as you refine your documents with ease.For any inquiries or issues, please contact Lyzr.

    """
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
