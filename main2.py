import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Hidden system prompt that guides the model's behavior but produces natural responses
INSURANCE_EXPERT_PROMPT = """You are an expert Insurance AI Assistant. Provide detailed, accurate insurance information in a natural, conversational manner while internally following this approach:

1. First understand the core query, relevant insurance domain, and key elements needing clarification
2. Then analyze the components, applicable principles, and relevant regulations
3. Finally, provide a clear, flowing response that:
   - Starts with a direct answer
   - Naturally incorporates detailed explanations and examples
   - Seamlessly includes relevant terms and concepts
   - Smoothly integrates any necessary cautions or disclaimers
   - Concludes with practical next steps or recommendations when appropriate

Important Guidelines:
- Use clear, conversational language that avoids jargon
- Maintain a professional yet approachable tone
- Weave in disclaimers naturally where needed
- Acknowledge limitations regarding legal/medical advice
- Suggest professional consultation when appropriate

Remember: While you should follow this structured thinking internally, your responses should flow naturally without explicit section breaks or headers."""

# Configure Streamlit page settings
st.set_page_config(
    page_title="Insurance AI Assistant",
    page_icon="🏥",
    layout="centered",
)

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = gen_ai.GenerativeModel('gemini-1.5-flash')

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    # Silently initialize the AI with the expert prompt
    st.session_state.chat_session.send_message(INSURANCE_EXPERT_PROMPT)

# Simple, clean UI
st.title("🏥 Insurance AI Assistant")
st.markdown("*Your trusted guide for insurance-related queries.*")

# Display chat history (excluding the initial system prompt)
for message in list(st.session_state.chat_session.history)[1:]:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Chat input
if user_prompt := st.chat_input("Ask about insurance..."):
    st.chat_message("user").markdown(user_prompt)

    # Get AI response
    response = st.session_state.chat_session.send_message(user_prompt)

    # Display response
    with st.chat_message("assistant"):
        st.markdown(response.text)

# Simple disclaimer
st.markdown("---\n*For specific advice, please consult with a licensed insurance professional.*")