# https://github.com/fabiomatricardi/Gemma2B-ChatAssistant
import streamlit as st
# Chat with an intelligent assistant in your terminal
from openai import OpenAI
from time import  sleep
import datetime
import random
import string
import tiktoken


encoding = tiktoken.get_encoding("r50k_base") #context_count = len(encoding.encode(yourtext))

modelname = 'Lite-Mistral-150M-v2-Instruct'
modelfile = 'models\Lite-Mistral-150M-v2-Instruct-Q8_0.gguf'


def writehistory(filename,text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

#AVATARS  👷🐦  🥶🌀
av_us = 'user.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = 'assistant65.png'

# Set the webpage title
st.set_page_config(
    page_title=f"Your LocalGPT with 🔲 {modelname}",
    page_icon="🔲",
    layout="wide")

# Create a header element
mytitle = '# LocalGPT with 🔲 Lite-Oute-1-65M-Instruct'
st.markdown(mytitle, unsafe_allow_html=True)
st.markdown('### Context windown: 2048 tokens', unsafe_allow_html=True)
def genRANstring(n):
    """
    n = int number of char to randomize
    """
    N = n
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
    return res

# create THE SESSIoN STATES
if "logfilename" not in st.session_state:
## Logger file
    logfile = f'{genRANstring(5)}_log.txt'
    st.session_state.logfilename = logfile
    #Write in the history the first 2 sessions
    writehistory(st.session_state.logfilename,f'{str(datetime.datetime.now())}\n\nYour own LocalGPT with 🌀 {modelname}\n---\n🧠🫡: You are a helpful assistant.')    
    writehistory(st.session_state.logfilename,f'🌀: How may I help you today?')

if "len_context" not in st.session_state:
    st.session_state.len_context = 0

if "limiter" not in st.session_state:
    st.session_state.limiter = 0

if "repeat" not in st.session_state:
    st.session_state.repeat = 1.35

if "bufstatus" not in st.session_state:
    st.session_state.bufstatus = "**:green[Good]**"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.1

if "maxlength" not in st.session_state:
    st.session_state.maxlength = 500

# Point to the local server
# Change localhost with the IP ADDRESS of the computer acting as a server
# itmay be something like "http://192.168.1.52:8000/v1"
client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed", organization='SelectedModel')
 
# CREATE THE SIDEBAR
with st.sidebar:
    st.image('logo300.png', use_column_width=True)
    st.session_state.temperature = st.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.1, step=0.02)
    #st.session_state.limiter = st.slider('Turns:', min_value=7, max_value=17, value=12, step=1)
    st.session_state.maxlength = st.slider('Length reply:', min_value=150, max_value=2000, 
                                           value=500, step=50)
    st.session_state.repeat = st.slider('Repeat Penalty:', min_value=0.0, max_value=2.0, value=1.35, step=0.01)
    #mytokens = st.markdown(f"""**Context turns** {st.session_state.len_context}""")
    #st.markdown(f"Buffer status: {st.session_state.bufstatus}")
    st.markdown(f"**Logfile**: {st.session_state.logfilename}")
    btnClear = st.button("Clear History",type="primary", use_container_width=True)

# We store the conversation in the session state.
# This will be used to render the chat conversation.
# We initialize it with the first message we want to be greeted with.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Lite-Oute-1-300M-Instruct, a helpful assistant. You reply only to the user questions. You always reply in the language of the instructions.",},
        {"role": "user", "content": "Hi, I am Fabio."},
        {"role": "assistant", "content": "Hi there, I am Lite-Oute-1-300M-Instruct, how may I help you today?"}
    ]

def clearHistory():
    st.session_state.messages = [
        {"role": "system", "content": "You are Lite-Oute-1-300M-Instruct, a helpful assistant. You reply only to the user questions. You always reply in the language of the instructions.",},
        {"role": "user", "content": "Hi, I am Fabio."},
        {"role": "assistant", "content": "Hi there, I am Lite-Oute-1-300M-Instruct, how may I help you today?"}
    ]
    st.session_state.len_context = len(st.session_state.messages)
if btnClear:
      clearHistory()  
      st.session_state.len_context = len(st.session_state.messages)

# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])

# We take questions/instructions from the chat input to pass to the LLM
if user_prompt := st.chat_input("Your message here. Shift+Enter to add a new line", key="user_input"):

    # Add our input to the session state
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # Add our input to the chat window
    with st.chat_message("user", avatar=av_us):
        st.markdown(user_prompt)
        writehistory(st.session_state.logfilename,f'👷: {user_prompt}')

    
    with st.chat_message("assistant",avatar=av_ass):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            response = ''
            conv_messages = []
            #conv_messages.append({"role": "system", "content": "You are a helpful AI assistant."})
            conv_messages.append(st.session_state.messages[-1])
            st.session_state.len_context = len(st.session_state.messages) 
            st.session_state.bufstatus = "**:green[Good]**"
            full_response = ""
            completion = client.chat.completions.create(
                model="local-model", # this field is currently unused
                messages=conv_messages,
                temperature=st.session_state.temperature,
                frequency_penalty  = st.session_state.repeat,
                stop=['</s>'],
                max_tokens=st.session_state.maxlength,
                stream=True,
            )
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "🔲")
            toregister = full_response + f"""
```

prompt tokens: {len(encoding.encode(st.session_state.messages[-1]['content']))}
generated tokens: {len(encoding.encode(full_response))}
```"""
            message_placeholder.markdown(toregister)
            writehistory(st.session_state.logfilename,f'🌟: {toregister}\n\n---\n\n') 

            
    # Add the response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": toregister}
    )
    st.session_state.len_context = len(st.session_state.messages)
