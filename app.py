import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta

from predictor import single_model, models_comparison


def main():
    # open Logo file
    img = Image.open("logo.png").resize((100, 100))

    # Set up the page configuration
    st.set_page_config(
        page_title="Plot .csv",
        page_icon=img,
        layout="wide",
    )

    _, cl, _ = st.columns([1.1, 6, 1.1])
    with cl:
        # st.title('Data Visualization - Plot data from CSV file')
        st.title('Data Request (MR. Asif Khan) 🏹')
    st.divider()

    cl1, cl2 = st.columns(2)
    with cl1:
        start_date = st.date_input('From Date',
                                   value=datetime.today() - timedelta(weeks=2),
                                   )
    with cl2:
        end_date = st.date_input('To Date',
                                 value=datetime.today(),
                                 )

    market = st.text_input('Input Market Name')
    model = st.text_input('Input Model Name')
    node = st.text_input('Input Node Name')

    show = st.checkbox('Show Data')

    base_data = {
        'from_date': start_date,
        'to_date': end_date,
        'market': market,
        'model': model,
        'node': node,
    }
    st.divider()

    col1, col2 = st.columns([1.5, 2])
    with col1:
        radio = st.radio(
            'Options', ['Single Model', 'Add Model'], index=0)

    # Create buttons
    with col2:

        if radio == 'Single Model':

            if start_date > end_date:
                text = 'Fix the Dates'
            else:
                text = 'Send Request'

            st.write('')
            st.write('')
            btn = st.button(text, type='primary',
                            disabled=start_date > end_date, use_container_width=True)
        else:
            if start_date > end_date:
                text = 'Fix the Dates'
            else:
                text = 'Send Requests'

            data_2 = base_data.copy()

            data_2['model'] = st.text_input('Input Second Model Name')

            btn = st.button(text, type='primary',
                            disabled=start_date > end_date, use_container_width=True)
    if btn:
        if radio == 'Single Model':
            single_model(base_data, show)
        else:
            models_comparison(base_data, data_2, show)


if __name__ == '__main__':
    main()
