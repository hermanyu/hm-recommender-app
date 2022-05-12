import streamlit as st
from torchvision.io import read_image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import torchvision
from torchvision.utils import save_image
from PIL import Image

import os
import pandas as pd
import numpy as np
import matplotlib.image as mpimg

from sklearn.metrics.pairwise import cosine_similarity
import joblib


def get_image(article_code):
    path = './images_dresses/'+article_code+'.jpg'
    return mpimg.imread(path)


@st.cache
def load_model():
    return joblib.load('./models/vgg16_feature_extractor.pkl')


@st.cache
def load_embeddings():
    return pd.concat([joblib.load('./models/dress_encodings'+str(i)+'.pkl') for i in range(1,12)])

resizer = transforms.Compose([transforms.Resize((320,224))])
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
flatten = nn.Flatten()
convert_to_tensor = transforms.ToTensor()


def main():
    with st.form(key='Image Uploader Form'):
        query = st.file_uploader(type=['png', 'jpg', 'jpeg'], label='Image Uploader')
        number_of_results = st.number_input('Number of Search Results to Display: ', min_value=1, max_value=5_000, value=10)
        submit_button = st.form_submit_button(label='Search')
    
    if submit_button:
        query = Image.open(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write('Searching for matches to the uploaded dress...')
        with col2:
            st.image(query, caption='Uploaded Image.', width=224)    
        
        query = convert_to_tensor(query)

        model = load_model()
        model.to('cpu')

        query = resizer(query)
        query = normalize(query).to('cpu')
        query = model(query)
        query = query.view(1, query.shape[0], query.shape[1], query.shape[2])
        query = flatten(query)[0].numpy()

        embeddings = load_embeddings()

        data = []

        for i in range(embeddings.shape[0]):
            article_id = embeddings.iloc[i,0]
            latent = np.array(embeddings.iloc[i, 1:])
            sim = cosine_similarity(query.reshape(1, query.shape[0]), latent.reshape(1, latent.shape[0]))[0][0]
            data.append([article_id, sim])

        df = pd.DataFrame(data, columns=['article_id','similarity'])
        df.sort_values(by='similarity', ascending=False, inplace=True)

        for i in range(number_of_results):
            article_id = df.iloc[i,0]
            col1, col2 = st.columns(2)
        
            with col1:
                st.write(article_id)
            with col2:
                st.image(get_image(article_id), width=224)





