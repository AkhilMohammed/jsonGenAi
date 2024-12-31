import streamlit as st
from langchain_community.chat_models import ChatOpenAI  # Updated import
from langchain.prompts import ChatPromptTemplate
import json
from langchain_groq import ChatGroq

groq_api_key = "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"

# Initialize LangChain Chat Model with Groq API Key
chat_model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Simplified prompt template for debugging
prompt_template = ChatPromptTemplate.from_template(
    "You are a chatbot that extracts structured data from a user's message.\n\nMessage: {message}\n\nExtracted JSON:"
)
print(prompt_template)

# Streamlit App Configuration
st.title("Streamlit Chatbot with Groq and LangChain")
st.markdown("This chatbot converts input strings into structured JSON data.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def process_input(user_input):
    try:
        # Create the formatted prompt
        formatted_prompt = f"""
        You are a chatbot that extracts structured data from a user's message.
        Message: {user_input}
        """
        
        # Use invoke() instead of calling the model directly
        response = chat_model.invoke(formatted_prompt)
        print(response) 
        # Check if the response is an AIMessage and return the content
        if hasattr(response, 'content'):
            return response.content.strip()  # Use the 'content' attribute of AIMessage
        else:
            print(response)
            return f"Unexpected response format: {response}"
        
    except Exception as e:
        return f"Error processing input: {e}"

# User input area
with st.form("chat_form"):
    user_input = st.text_input("Enter your message:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate chatbot response
    chatbot_response = process_input(user_input)
    st.session_state.messages.append({"role": "bot", "content": chatbot_response})

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")
