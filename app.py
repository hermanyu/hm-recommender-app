import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from datetime import date

def get_image(prod_code):
    prod_string = '0'+str(prod_code)
    path = './images/'+prod_string[0:3]+'/'+prod_string+'.jpg'
    return mpimg.imread(path)


def main():

    months_dict = {'09':'2019-09', '10':'2019-10', '11':'2019-11', '12':'2019-12', '01':'2020-01', '02':'2020-02',
                    '03':'2020-03', '04':'2020-04', '05':'2020-05', '06':'2020-06', '07':'2020-07', '08':'2020-08'}

    current_month = date.today().strftime('%m')
    current_day = date.today().strftime('%d')

    filepath = './data/transactions_'+months_dict[current_month]+'.csv'
    df = pd.read_csv(filepath, date_parser='t_dat')
    df = df[ df['t_dat']==months_dict[current_month]+'-'+current_day ]
    top10 = list(df.value_counts(subset='product_code')[0:10].index)

    st.write("Today's Top 10 ")
    st.write(str(date.today()))

    for i in range(10):
        prod_code = top10[i]
        col1, mid, col2 = st.columns(3)
        with col1:
            st.write(f'#{i}) '+ str(prod_code))
        with mid:
            try:
                st.image(get_image(prod_code))
            except:
                st.write('Image not currently available.')


