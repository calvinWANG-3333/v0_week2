import streamlit as st
from llama_cpp import Llama

st.set_page_config(page_title="Chat", layout="wide")
st.title("💬 Chat with LLM")
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.imgur.com/j6CjBvn.jpeg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .title {
            font-size: 40px;
            font-weight: bold;
            color: #ffecec;
            text-shadow: 2px 2px 4px #000000;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #fff0f0 !important;
            text-shadow: 1px 1px 2px #000;
        }

        .stAlert-success {
            color: #004d00 !important;
            background-color: rgba(232, 255, 232, 0.95) !important;
        }

        button[kind="primary"] {
            background-color: #ff6699 !important;
            color: white !important;
            border: None;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

models = {}
folder_path = "/Users/apple/.lmstudio/models"

for file in os.listdir(folder_path):
    if file.endswith(".gguf"):
        model_name = file.split(".")[0]
        model_path = os.path.join(folder_path, file)
        models[model_name] = Llama(
            model_path=model_path
        )


# Initialization
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Session 1": []}
    st.session_state.active_session = "Session 1"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # Model selection
    model = st.selectbox(
        "🤖 Choose Model",
        ["deepseek-r1-distill-qwen-7b", "another-model-id"],
        index=0,
        key="model_choice"
    )

    # Display session selector
    session_names = list(st.session_state.chat_sessions.keys())
    selected_session = st.selectbox("🕘 Chat History", session_names)

    if selected_session != st.session_state.active_session:
        st.session_state.active_session = selected_session
        st.session_state.messages = st.session_state.chat_sessions[selected_session]

    # Clear current chat
    if st.button("🧹 Clear This Chat"):
        st.session_state.messages = []
        st.session_state.chat_sessions[st.session_state.active_session] = []
        st.success("Chat cleared.")

# New Chat Button (top of main area)
if st.button("➕ New Chat"):
    new_name = f"Session {len(st.session_state.chat_sessions) + 1}"
    st.session_state.chat_sessions[new_name] = []
    st.session_state.active_session = new_name
    st.session_state.messages = []
    st.experimental_rerun()

#  Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#  Call local downloaded LM Studio


def call_local_llm(prompt: str) -> str:
    llm = models[st.session_state.current_model_name]
    response = llm.create_completion(
        prompt=prompt
    )
    return response["choices"][0]["text"].strip()


# User Input + Response
if user_input := st.chat_input("Type your message here..."):
    user_msg = {"role": "user", "content": user_input}
    st.session_state.messages.append(user_msg)
    st.session_state.chat_sessions[st.session_state.active_session].append(
        user_msg)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_local_llm(
                user_input, st.session_state.model_choice)
            st.markdown(response)
            assistant_msg = {"role": "assistant", "content": response}
            st.session_state.messages.append(assistant_msg)
            st.session_state.chat_sessions[st.session_state.active_session].append(
                assistant_msg)
