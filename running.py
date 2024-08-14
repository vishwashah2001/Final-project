


import openai
import streamlit as st
import json
import logging

# Set up logging to capture process details
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace this with your actual OpenAI API key (consider using environment variables for security)
openai.api_key = st.secrets["api_key"]

# Function to run a prompt-based customization using gpt-3.5-turbo
def run_custom_prompt(user_input, chat_history):
    try:
        # Append the user message to chat history
        chat_history.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0.7,
            max_tokens=150
        )

        # Append the assistant's response to chat history
        assistant_response = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_response})

        # Return the assistant's response
        return assistant_response

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None

# Function to save chat history to a file
def save_chat_history(chat_history):
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f, indent=4)
    st.success("Chat history saved!")

# Initialize the chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Title of the Streamlit app
st.title("Chatbot with Fine-Tuning")

# Display the chat history
if st.session_state["chat_history"]:
    for i, chat in enumerate(st.session_state["chat_history"]):
        if chat["role"] == "user":
            st.write(f"**You:** {chat['content']}")
        elif chat["role"] == "assistant":
            st.write(f"**Bot:** {chat['content']}")

# Text input for user to enter their query
user_input = st.text_input("Enter your message:", "")

# Buttons for interaction
enter_button = st.button("Enter")
save_button = st.button("Save History")
clear_button = st.button("Clear Conversation")

# Handle the Enter button
if enter_button and user_input:
    response = run_custom_prompt(user_input, st.session_state["chat_history"])
    if response:
        # Display the response immediately, but ensure it's only displayed once
        st.write(f"**You:** {user_input}")
        st.write(f"**Bot:** {response}")

# Handle the Save History button
if save_button:
    save_chat_history(st.session_state["chat_history"])

# Handle the Clear Conversation button
if clear_button:
    st.session_state["chat_history"] = []
    st.query_params.clear()  # This reloads the page and clears the session state
