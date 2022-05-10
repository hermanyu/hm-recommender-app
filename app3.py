import streamlit as st

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

categories = ['Babies Sizes 50-98', 'Chilren Accessories & Swim', 'Children Sizes 92-140',
             'Children Sizes 134-170', 'Divided', 'Ladies Accessories', 'Ladieswear',
             'Lingeries/Tights', 'Menswear', 'Sport']

cat_abbr = {'Babies Sizes 50-98':'babies', 'Chilren Accessories & Swim':'child_acc', 'Children Sizes 92-140':'child1',
             'Children Sizes 134-170':'child2', 'Divided':'divided', 'Ladies Accessories':'ladies_acc', 'Ladieswear':'ladies',
             'Lingeries/Tights':'lingerie_tights', 'Menswear':'mens', 'Sport':'sport'}
           

def get_image(prod_code):
    prod_string = '0'+str(prod_code)
    path = './images/'+prod_string[0:3]+'/'+prod_string+'.jpg'
    return mpimg.imread(path)

def main():

    with open('./models/pretrained-sbert.pkl', 'rb') as model_in:
        model = joblib.load(model_in)

    with st.form(key='user form'):
        user_input = st.text_input('Hello, what are you looking for? ')
        cat = st.selectbox("Category: ", categories)
        number_of_results = st.number_input('Number of Search Results to Display: ', min_value=1, max_value=40_000, value=10)
        submit_button = st.form_submit_button(label='Search')

    user_embedding = model.encode([user_input])

    filepath = './data/desc_embeddings_'+cat_abbr[cat]+'.csv'
    
    @st.cache
    def load_embeddings():
        if cat == 'Ladieswear':
            df1 = pd.read_csv('./data/desc_embeddings_ladies1.csv', index_col='product_code')
            df2 = pd.read_csv('./data/desc_embeddings_ladies2.csv', index_col='product_code')
            return pd.concat([df1, df2])
        else:
            filepath = './data/desc_embeddings_'+cat_abbr[cat]+'.csv'
            return pd.read_csv(filepath, index_col='product_code')

    @st.cache
    def load_product_desc():
        filepath = './data/product_desc_'+cat_abbr[cat]+'.csv'
        return pd.read_csv(filepath, index_col='product_code')

    product_embeddings = load_embeddings()
    product_desc = load_product_desc()


    similarities = []

    for product in product_embeddings.index:
        similarities.append([product]+ list(cosine_similarity(user_embedding, np.array(product_embeddings.loc[product]).reshape(1,384))[0]))

    df = pd.DataFrame(similarities, columns=['product_code', 'similarity'])
    df.sort_values(by='similarity', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)



    for i in range(number_of_results):
        prod_code = df.iloc[i,0]
        col1, mid, col2 = st.columns(3)
        
        with col1:
            st.write(prod_code)
        with mid:
            try:
                st.image(get_image(df.iloc[i,0]))
            except:
                st.write('Image not currently available.')
        with col2:
            st.write(product_desc.loc[prod_code, 'detail_desc'])