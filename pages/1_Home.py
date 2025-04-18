import streamlit as st
from llama_cpp import Llama
import os

# Import local LLM models
# You need to change the folder path to the actual path where your models are stored

models = {}
for file in os.listdir(folder_path):
    if file.endswith(".gguf"):
        model_name = file.split(".")[0]
        model_path_act = os.path.join(folder_path, file)
        models[model_name] = Llama(model_path=model_path_act)


st.title(" Welcome to your bot!")
st.markdown(
    '''
Welcome to your chatbot built with LLM models! You can chat with me and ask me anything. 
Besides, you can also upload documents!
'''
)

# Load the models


# Select a LLM model from all the LLM models we have locally(optional)
model_choice = st.selectbox(
    "Choose a model you would like to use",
    list(models.keys()),
    index=0,
    help="The default model is GPT-3.5. You can choose any model from the dropdown list."
)

# Upload multiple files(optional)
''' uploaded_files = st.file_uploader(
    accept_multiple_files=True,
    type=["jpg", "jpeg", "pdf", "txt", "docx", "csv"],
    help="You can upload multiple files. The files will be used to answer your questions. "
         "The files will be stored in the session state and will be used for the chat."
    "Choose your files to be uploaded"
)

for file in uploaded_files:
    bytes_data = file.read()
    st.write(
        "File name: ", file.name, "File type: ", file.type, "File length: ", len(bytes_data))
    st.write(bytes_data)  '''


# redirect to the chat page
if st.button("Start chatting!"):
    st.session_state.modelchoice = model_choice
    st.switch_page("2_Chat.py")
