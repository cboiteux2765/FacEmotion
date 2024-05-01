import os
import streamlit as st
import google.generativeai as genai
import PIL
from PIL import Image
import pandas as pd
from camera_input_live import camera_input_live
st.title("FacEmotion")

genai.configure(api_key="AIzaSyCwxxyZ-STyGrdLfGSSc1eqGF7vn4RVJ5A")

#Default configuration for model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 500,
} 

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                safety_settings=safety_settings,
                                system_instruction = "You will be given an image and your goal is to recognize the emotion the person is displaying on their face and to recommend products, items, services, or actions to improve the person's emotion. If you see any items in the image that could be useful in accomplishing this task, tell them so as well. If the image does not contain a human face or expression always respond with \"Sorry, I don't see any faces or expressions in this image. Please give me an image that has a facial expression.\" All of your output should be in Markdown. If the prompt is not some sort of question like \"What emotion is this\" simply engage in covnersation with the user.")
uploaded_file = st.file_uploader("Upload an image", type=("png", "jpg", "heic", "heif"))
image = ""
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask me anything!"
        }
    ]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
webcam_used = st.toggle("Use webcam")
temp = uploaded_file
if webcam_used:
    uploaded_file = st.camera_input("Take a photo!")
else:
    uploaded_file = temp
def llm_function(query):
    response = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        response = model.generate_content([query, image])
        st.image(image)
    with st.chat_message("assistant"):
        st.markdown(response.text)
    
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response.text
        }
    )

query = st.chat_input("Talk to FacEmotion!")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    
    llm_function(query)
