import streamlit as st
import random
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import time
import uuid
import os

st.set_page_config(page_title='GAMSIT by amawan',
                   layout='centered',
                   menu_items={
                        'About' : '**I am a .... !**'
                       })

if 'player' not in st.session_state:
    st.session_state.player = 'start-button'
    st.session_state.playerScore = 0
if 'computer' not in st.session_state:
    st.session_state.computer = 'start-button'
    st.session_state.computerScore = 0
if 'totalRound' not in st.session_state:
    st.session_state.totalRound = 100/2
if 'progBar' not in st.session_state:
    st.session_state.progBar = 0
if 'buttonDisable' not in st.session_state:
    st.session_state.buttonDisable = False
if 'celebrate' not in st.session_state:
    st.session_state.celebrate = False
if "rock" not in st.session_state:
    st.session_state.rock = False
if "paper" not in st.session_state:
    st.session_state.paper = False
if "scissor" not in st.session_state:
    st.session_state.scissor = False


st.markdown('''
<style>
.css-1xarl3l.e16fv1kl1 {
color : blue;
padding-left : 20px;
}
</style>
''',unsafe_allow_html=True)


st.markdown('''
<style>
.css-1cpxqw2.edgvbvh9 {
height : 77px;
font-size : 50px;
border : solid;
border-radius : 15px;
box-shadow : 2px 2px #aaaaaa;
margin-left : 17px;
}
</style>
''',unsafe_allow_html=True)

st.sidebar.markdown('''
<style>
.css-15tx938.effi0qh3 {
font-weight : bold;
font-size : 20px;
}
</style>
''',unsafe_allow_html=True)

st.sidebar.markdown('''
<h1 style='font-size:30px;font-weight:bold;'>
GAMSIT
<i style='font-size:15px;'>by amawan</i>
</h1>
<hr>
''',unsafe_allow_html=True)

st.markdown('''
<style>
.css-50ug3q.e16fv1kl3 {
font-size : 30px;
font-weight : bold;
padding-top : 5px;
padding-left : 90px;
}
</style>
''',unsafe_allow_html=True)

st.markdown('''
<style>
.css-1qrvfrg.edgvbvh9 {
font-weight : bold;
width : 100%;
height : 50px;
}
</style>
''',unsafe_allow_html=True)


# title
st.markdown('''
<hr>
<h1 style='text-align:center;font-size:70px;'>
GAMSIT
</h1>
<hr>
''',unsafe_allow_html=True)


directory = "static/"
model = load_model('models/model.h5', compile=False)
with open('labels.txt', 'r') as file:
    labels = file.read().splitlines()

def score():
    p = st.session_state.player
    c = st.session_state.computer
    if p == c :
        return None
    elif (p == "rock") and (c == "paper"):
        st.session_state.computerScore += 1
    elif (p == "rock") and (c == "scissor"):
        st.session_state.playerScore += 1
    elif (p == "paper") and (c == "rock"):
        st.session_state.playerScore += 1
    elif (p == "paper") and (c == "scissor"):
        st.session_state.computerScore += 1
    elif (p == "scissor") and (c == "rock"):
        st.session_state.computerScore += 1
    elif (p == "scissor") and (c == "paper"):
        st.session_state.playerScore += 1

def computer_move():
    x = ["rock", "paper", "scissor"]*5
    st.session_state.computer = random.choice(x)

def numInputButton():
    st.session_state.buttonDisable = True

numOfRounds = st.sidebar.number_input('Enter number of rounds : ', min_value=2, step=1,on_change=numInputButton)

def restart():
    global numOfRounds 
    st.session_state.buttonDisable = False
    st.session_state.player =  'start-button'
    st.session_state.computer = 'start-button'
    st.session_state.playerScore = 0
    st.session_state.computerScore = 0
    st.session_state.progBar = 0
    st.session_state.totalRound = 100/numOfRounds

image = st.camera_input("Take a picture of your hand gesture", disabled=st.session_state.buttonDisable)
if image:
    img = Image.open(image).convert("RGB")
    img = img.resize((150, 150))
    filename = f"player_{time.strftime('%Y%m%d_%H%M%S_')}{uuid.uuid4()}.png"
    image = img.save(os.path.join(directory, filename))
    image_path = os.path.join(directory, filename)
    img_array = np.asarray(img)
    if img_array is not None:
        img_array = np.expand_dims(img_array, axis=0)
        normalized_image_array = img_array.astype(np.float32)*(1./225) 
        data = np.ndarray(shape=(1, 150, 150, 3), dtype=np.float32)
        data[0] = normalized_image_array
        predictions = model.predict(data)
        index = np.argmax(predictions)
        class_name = labels[index]
        confidence_score = predictions[0][index]

        if class_name[2:] == 'rock':
            st.session_state.rock = True
            st.session_state.paper = False
            st.session_state.scissor = False
        elif class_name[2:] == 'paper':
            st.session_state.paper = True
            st.session_state.rock = False
            st.session_state.scissor = False
        elif class_name[2:] == 'scissor':
            st.session_state.scissor = True
            st.session_state.paper = False
            st.session_state.rock = False
                    
        if st.session_state.rock:
            st.session_state.player = 'rock'
        elif st.session_state.paper:
            st.session_state.player = 'paper'
        elif st.session_state.scissor:
            st.session_state.player = 'scissor'
        st.session_state.progBar += st.session_state.totalRound
        computer_move()
        score()

        st.text(class_name[2:])
        st.text(f"Score: {float(confidence_score)}")
            
        if st.session_state.progBar >= 100:
            st.session_state.buttonDisable = True
            if st.session_state.playerScore > st.session_state.computerScore:
                st.balloons()
                st.session_state.player = 'win'
                st.session_state.computer = 'lose'
            elif st.session_state.computerScore > st.session_state.playerScore:
                st.session_state.player = 'lose'
                st.session_state.computer = 'win'
            elif st.session_state.computerScore == st.session_state.playerScore:
                st.session_state.player = 'draw'
                st.session_state.computer = 'draw'
    else:
        st.warning("No hand detected in the image. Please try again.")


left, right , result = st.columns([2,2,1])
left.metric('YOU', f'{st.session_state.playerScore}')
right.metric('COM', f'{st.session_state.computerScore}')
result.markdown('''
<p style='font-weight:bold;font-size:30px;height:50px;padding-left:7px;'>
ROUND
</p>
''',unsafe_allow_html=True)
result.progress(int(st.session_state.progBar))
st.markdown('<hr>',unsafe_allow_html=True)
you, com , sc = st.columns([2,2,1])

you.image(f'{st.session_state.player}.png')
com.image(f'{st.session_state.computer}.png')


st.markdown('<hr>',unsafe_allow_html=True)

st.sidebar.button('PLAY \U0001F503', on_click=restart)