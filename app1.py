import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def get_image(prod_code):
    prod_string = '0'+str(prod_code)
    path = './images/'+prod_string[0:3]+'/'+prod_string+'.jpg'
    return mpimg.imread(path)

@st.cache
def load_product_desc():
    filepath = './data/product_desc_'+cat_abbr[cat]+'.csv'
    return pd.read_csv(filepath, index_col='product_code')


def main():

    seasons=['Fall', 'Winter', 'Spring', 'Summer']

    with st.form(key='Season Form'):
        season = st.selectbox("Season ", seasons)
        number_of_results = st.number_input('Number of Results ', min_value=1, max_value=5_000, value=10)
        submit_button = st.form_submit_button(label='View')

    df = pd.read_csv('./data/top_sellers_'+season.lower()+'.csv')

    for i in range(number_of_results):
        prod_code = df.loc[i,'product_code']
        col1, col2 = st.columns(2)

        with col1:
            st.write(str(prod_code))

        with col2:
            try:
                st.image(get_image(prod_code))
            except:
                st.write("Image not available :(")



