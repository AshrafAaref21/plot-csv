import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px

from utils import miso, CSS


# open Logo file
img = Image.open("logo.png").resize((100, 100))

# Set up the page configuration
st.set_page_config(
    page_title="Plot .csv",
    page_icon=img,
    layout="wide",
)


_, cl, _ = st.columns([1.5, 6, 1.5])
with cl:
    st.title('Data Visualization - Plot data from CSV file')
st.divider()

data_uploader = st.file_uploader("Upload datasets", type=['csv', 'xlsx'])

if data_uploader is not None:
    if data_uploader.name[-3:] == 'csv':
        df = pd.read_csv(data_uploader)
    else:
        df = pd.read_excel(data_uploader)

    st.write('')
    st.success('Your Data Successfully Uploaded')

    st.divider()

    miso(df)
