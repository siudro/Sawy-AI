import openai
import streamlit as st
from streamlit_extras.let_it_rain import rain
from PIL import Image
import os
import base64

openai_access_token = st.secrets["api_key"]

def camel_rain():
    rain(
        emoji="🐪",
        font_size=54,
        falling_speed=5
    )

def detect_topics(response_text):
    topics = {
        "Numou": ["numou education center", "numou", "the center", "location", "الموقع","المركز", "مركز نمو", "نمو"],
        "Sawy": ["sawy","سوي", "سوّي","camel", "camels", "mascot", "جمل", "ناقة", "ناقه"],
        "Sawa": ["sawa","son","small camel", "سوا"],
        #"The Team": ["the team", "Sedra", "Jax", "Sulaiman", "Khuzama", "Roaa", "Asma", "Yousef"],
        #"The Projects": ["the projects", "sofa", "tables", "furniture", "sculpture", "the hand", "hand", "metal hand", "art piece", "SawySawa", "line-follower", "The Saqar"],
        #"The Stations": ["the stations", "sawysawy", "sawy-sawy", "سوي-سوي", "سوي سوي", "3D printing", "laser cutting", "arduino"],
        "The Machines": ["machine","machines","equipment", "tools","laser cutter", "welding", "metal work", "3D printers", "vinyl", "vinyl cutter", "press heat", "3D pens"]
    }
    detected_topics = []
    for topic, keywords in topics.items():
        for keyword in keywords:
            if keyword.lower() in response_text.lower():
                detected_topics.append(topic)
                break
    return detected_topics

def display_images(topic):
    images = []
    captions = []
    
    if topic == "Numou":
        images = ["Numou/numou.jpeg", "Numou/visits.jpeg"]
        captions = ["Numou Education Center", "One of the school visits at S3"]
    elif topic == "Sawy":
        images = ["Sawy/sawy1.jpeg", "Sawy/sawy2.jpeg", "Sawy/sawy3.jpeg"]
        captions = ["Sawy", "Sawy", "Sawy at the DAS book fair"]
        camel_rain()
    elif topic == "Sawa":
        images = ["Sawa/sawa1.jpeg", "Sawa/sawa2.jpeg", "Sawa/sawysawa.jpeg"]
        captions = ["Sawa", "Sawa", "Sawa", "Sawa"]
        camel_rain()
    elif topic == "The Machines":
        images = ["Machines/3D-printer.jpeg", "Machines/laser-cutter.jpeg","Machines/vinyle-cutter.jpeg","Machines/welder.jpeg","Machines/press-heat.jpeg"]
        captions = ["One of the 3D Printers at S3", "The Laser Cutter", "Vinyle Cutter", "The Welding Machine", "The Press Heat"]
    else:
        pass

    if images and captions:
        cols = st.columns(len(images))
        for col, img, caption in zip(cols, images, captions):
            with col:
                st.markdown(
                    f"""
                    <div class="image-container">
                        <img src="data:image/jpeg;base64,{get_base64_encoded_image(img)}" class="image">
                        <p>{caption}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Custom CSS
st.markdown("""
    <style>
    .image-container {
        border: 1px solid #d3d3d3;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        max-width: 100%;
        height: auto;
    }
    .image-container img {
        border-radius: 10px;
        max-width: 100%;
        height: auto;
        cursor: pointer;
    }
    .image-container p {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Talk to Sawy🐪")
st.title("اتكلم مع سوّي🐪")
"""
Are you interested in knowing who Sawy is?
What does her name mean?
Who made her and Why?
All your questions will be answered by the AI personality Sawy!🐪
"""
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets["sawy"] }
    ]

if prompt := st.chat_input():
    openai.api_key = openai_access_token
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    msg = response.choices[0]['message']
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])
    
    detected_topics = detect_topics(msg['content'])
    for topic in detected_topics:
        display_images(topic)
