import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import random

def get_image(prod_code):
    prod_string = '0'+str(prod_code)
    path = './images/'+prod_string[0:3]+'/'+prod_string+'.jpg'
    return mpimg.imread(path)

@st.cache
def load_co_occurrence():
    return pd.concat([
                    pd.read_csv('./data/current-week-co-occurrence-1.csv', index_col='product_code'), 
                    pd.read_csv('./data/current-week-co-occurrence-2.csv', index_col='product_code') 
                ])

def main():
    
    co_occurrence = load_co_occurrence()

    random_index = random.randint(0, 9830)

    st.write('Here is a randomly selected product code: ' +str(co_occurrence.index[random_index]))

    with st.form(key='user form'):
        user_input = st.text_input('What is the product code of your most recent purchase? ')
        submit_button = st.form_submit_button(label='Get Recommendations')

    if submit_button:
        recommended_products = co_occurrence[user_input].sort_values(ascending=False)[0:7]
        recommendations = [str(idx) for idx in recommended_products.index if str(idx) != user_input]

        st.write("People who bought: ", user_input)
        st.image(get_image(user_input))

        st.write("also bought... ")
        col1, col2, col3 = st.columns(3)

        with col1:
            try:
                st.image(get_image(recommendations[0]))
            except:
                st.write("Image not found in repository :( ")
        
        with col2:
            try:
                st.image(get_image(recommendations[1]))
            except:
                st.write("Image not found in repository :( ")

        with col3:
            try:
                st.image(get_image(recommendations[2]))
            except:
                st.write("Image not found in repository :( ")

        col4, col5, col6 = st.columns(3)

        with col4:
            try:
                st.image(get_image(recommendations[3]))
            except:
                st.write("Image not found in repository :( ")

        with col5:
            try:
                st.image(get_image(recommendations[4]))
            except:
                st.write("Image not found in repository :( ")

        with col6:
            try:
                st.image(get_image(recommendations[5]))
            except:
                st.write("Image not found in repository :( ")




