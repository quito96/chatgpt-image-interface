import streamlit as st
from chat_bot import ChatBot
from PIL import Image
import io


# Initialize the chatbot session state
def initialize_chatbot():
    if 'chatbot' not in st.session_state:
        st.session_state['chatbot'] = ChatBot()


# Function to handle text submission
def handle_text_submission():
    user_input = st.session_state.user_input  # Get the current user input
    if user_input:  # Check if there is input
        response = None
        if 'image_bytes' in st.session_state and st.session_state.image_bytes is not None:
            response = st.session_state.chatbot.chat(user_input.strip(), image_bytes=st.session_state.image_bytes)
        else:
            response = st.session_state.chatbot.chat(user_input.strip())

        st.session_state.response = response  # Store the response in the session state
        st.session_state.user_input = ""  # Clear the input field


# Function to clear the uploaded image
def clear_uploaded_image():
    if 'image_bytes' in st.session_state:
        del st.session_state.image_bytes
    if 'file_uploader' in st.session_state:
        del st.session_state.file_uploader  # Attempt to clear the file_uploader widget state
    st.rerun()  # Rerun the app to update the state


# Initialize session state for response if not present
if 'response' not in st.session_state:
    st.session_state['response'] = ""

initialize_chatbot()

st.title("Analyze your image ")
#st.sidebar.header("Upload an Image")

# File uploader in the sidebar with a unique key
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="file_uploader")

# Display uploaded image
col1, col2 = st.columns(2)
with col1:
    st.header("Uploaded Image")
    if uploaded_file is not None:
        st.session_state.image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(st.session_state.image_bytes))
        st.image(image, use_column_width=True)

        # Button to clear the uploaded image
        if st.button("Clear Image"):
            clear_uploaded_image()

# Chat interaction
with col2:
    st.header("Chat")
    user_input = st.text_input("Ask a question or type your message...", key="user_input",
                               on_change=handle_text_submission)
    st.text_area("Response", value=st.session_state.response, height=300)

# Clear chat history button (optional)
if st.button("Clear Chat"):
    st.session_state.chatbot.clear_messages()
    st.session_state.response = ""
    st.rerun()
