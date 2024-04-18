import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

from utils import miso


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
    # st.title('Data Visualization - Plot data from CSV file')
    st.title('Plot data from CSV file (MR. Asif Khan)')
st.divider()

data_uploader = st.file_uploader("Upload datasets", type=['csv', 'xlsx'])

if data_uploader is not None:
    if data_uploader.name[-3:] == 'csv':
        df = pd.read_csv(data_uploader)
    else:
        df = pd.read_excel(data_uploader)

    df["profit_total"] = df["profit_total"].cumsum()
    df["profit_long"] = df["profit_long"].cumsum()
    df["profit_short"] = df["profit_short"].cumsum()

    st.dataframe(df.cumsum())
    st.write('')
    st.success('Your Data Successfully Uploaded')

    st.divider()

    miso(df)
