import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

import app
import app1
import app2
import app3

pages = ["Top 10 Today", "Shop By Season", "People who bought this also bought...", "Search by description"]

page = st.sidebar.selectbox("What kind of recommendations would you like to see?", pages)

if page == pages[0]:
    app.main()

if page == pages[1]:
    app1.main()

if page == pages[2]:
    app2.main()

if page == pages[3]:
    app3.main()

