import streamlit as st
from utils import get_response, load_training_data
from langchain_core.messages import AIMessage, HumanMessage


st.set_page_config(page_title="AI Shopping Assistant", page_icon=":speech_balloon:")

training_data = load_training_data("training_data.json")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Hey, How can I help you?")]
if "preferences" not in st.session_state:
    st.session_state.preferences = {"language": "English", "tone": "Friendly"}


with st.sidebar:
    st.header("Options")
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
    
    st.subheader("User Preferences")
    language = st.selectbox("Language", ["English", "Spanish", "French"], index=0)
    tone = st.selectbox("Tone", ["Friendly", "Professional"], index=0)
    st.session_state.preferences["language"] = language
    st.session_state.preferences["tone"] = tone

    st.subheader("FAQs")
    if st.button("Show FAQs"):
        faqs = [
            {"question": "What is this app?", "answer": "This app helps you with smartphone shopping queries."},
            {"question": "How can I contact support?", "answer": "You can contact support via email at support@example.com."}
        ]
        for faq in faqs:
            st.write(f"**{faq['question']}**")
            st.write(faq['answer'])
    
    st.subheader("Feedback")
    feedback = st.text_area("Your feedback", "")
    if st.button("Submit Feedback"):
        if feedback:
            st.write("Thank you for your feedback!")
            
        else:
            st.write("Please enter your feedback before submitting.")

    st.subheader("Response Logs")
    if st.button("Show Response Logs"):
        if "response_logs" not in st.session_state:
            st.session_state.response_logs = []
        for log in st.session_state.response_logs:
            st.write(f"- {log}")

st.title("AI Shopping Assistant")


for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message")
if user_query and user_query.strip():
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        try:
            response = get_response(user_query, training_data)
            st.markdown(response)
            st.session_state.chat_history.append(AIMessage(content=response))

            if "response_logs" not in st.session_state:
                st.session_state.response_logs = []
            st.session_state.response_logs.append(response)
        except Exception as e:
            st.markdown(f"Error processing your query: {e}")
