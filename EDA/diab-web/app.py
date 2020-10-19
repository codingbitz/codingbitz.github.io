import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pickle,joblib
from datetime import date

# Calling the model we saved before

diabmdl = joblib.load('diab_web.sav')

st.sidebar.header('Diabetes Prediction')
today = date.today()
date = today.strftime("%d-%b-%Y")

select = st.sidebar.selectbox('Select Form', ['Diabetics Check - Q & A Form'], key='1')
if not st.sidebar.checkbox("Hide", True, key='1'):
    st.title('🎲 Diabetes Prediction - Females')
    #st.markdown("### 🎲 Diabetes Prediction - Females")
    st.markdown("This application is a Streamlit form that can be used"
            " to get user input & based on that predict whether the user has possibly diabetes or not with 73% accuracy as on "+date)
    name = st.text_input("Name:")
    ethnicGroup = st.multiselect("Do you belong to any of the ethnic group?", 
                         ["Black", "White",
                         "Hispanic", "Asian"])
    #age = st.slider("What is your age?", 21, 80)
    #bp = st.number_input("Diastolic Blood Pressure:")
    dpf = st.number_input("Diabetes Pedigree Function:")
    #glu = st.number_input("Glucose:")
    #bmi = st.number_input("Body Mass Index:")
    preg = st.number_input("Number of times pregnant:")
    #skth = st.number_input("skth:")
    test = st.number_input("2-Hour serum insulin (mu U/ml):")
# 'preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age'
    submit = st.button('Predict')
    if submit:
        #prediction = diabmdl.predict([[bmi,age,bp,dpf,glu]])
        prediction = diabmdl.predict([[test,preg,dpf]])
        if prediction == 0:
            st.write('Congrats',name,',You are not diabetic')
        else:
            st.write(name," ,we are really sorry to say but it seems like you are Diabetic.")