import streamlit as st
import re

def load_questions(prompt_file="prompt.md"):
    """
    Loads and parses the questions from the prompt file.
    """
    try:
        with open(prompt_file, 'r') as f:
            text = f.read()

        # Isolate the questioning section to avoid parsing other parts of the file
        questioning_section = text.split('COMPLETE QUESTIONING SEQUENCE', 1)[1]

        # Correctly split the text by newline characters
        lines = questioning_section.split('\n')
        questions = []
        for line in lines:
            line = line.strip()
            # Regex to capture content within quotes on lines that look like questions
            match = re.search(r'^(?:\d+\.\s*)?"([^"]*)"', line)
            if match:
                questions.append(match.group(1))

        # The first captured "question" is the opening script, so we remove it
        if questions:
            questions.pop(0)

        return questions
    except (FileNotFoundError, IndexError):
        return []

# --- Page Configuration ---
st.set_page_config(page_title="Ava - AI Receptionist", layout="centered")

# --- Styling ---
st.markdown("""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: sans-serif;
        }
        .stApp {
            background-color: #f4f4f4;
        }
        .stChatMessage {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border: 1px solid #ddd;
            max-width: 80%;
            margin-left: auto;
            margin-right: auto;
        }
        h1 {
            text-align: center;
            color: #4a4a4a;
        }
        .stChatInput {
            background-color: #fff;
            border-top: 1px solid #ddd;
            padding: 10px;
        }
        .stTextInput > div > div > input {
            border-radius: 20px;
            border: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Initialization ---
if 'questions' not in st.session_state:
    st.session_state.questions = load_questions()

if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- App Body ---
st.title("Ava - Your Elite Events Planning Assistant")

# Display initial greeting if the conversation has just started
if not st.session_state.messages:
    initial_greeting = "Hello! I'm Ava, the receptionist assistant for Elite Events Planning. My job is to ask all the right questions so our expert planners have everything they need to create your perfect event. Let's start with the basics!"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Logic ---
if prompt := st.chat_input("Your response..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display bot response
    with st.chat_message("assistant"):
        response = ""
        questions = st.session_state.questions
        index = st.session_state.current_question_index

        if not questions:
            response = "I'm sorry, I'm having trouble loading my questions at the moment. Please try again later."
        elif index < len(questions):
            # Acknowledge previous answer before asking the next question
            acknowledgement = "Got it, thank you. " if index > 0 else ""
            response = f"{acknowledgement}{questions[index]}"
            st.session_state.current_question_index += 1
        else:
            response = "Thank you for providing all the information. Our event planners will be in touch with you shortly!"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
