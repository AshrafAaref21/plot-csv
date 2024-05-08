import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import requests
import json
from utils import visual


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
                                   value=datetime.today(),
                                   )
    with cl2:
        end_date = st.date_input('To Date',
                                 value=datetime.today(),
                                 )

    market = st.text_input('Input Market Name')
    model = st.text_input('Input Model Name')
    node = st.selectbox('Select Node Name', ['miso', 'nyis'])

    data = {
        'from_date': start_date,
        'to_date': end_date,
        'market': market,
        'model': model,
        'node': node,
    }

    st.divider()
    if start_date > end_date:
        text = 'Fix the Dates'
    else:
        text = 'Send Request'
    btn = st.button(text, type='primary',
                    disabled=start_date > end_date, use_container_width=True)

    if btn:
        response = requests.post(
            'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data)

        if str(response.status_code)[0] != '2':
            st.error(f'Bad Request with status code {response.status_code}')
            st.error(str(response.content))
            if str(response.status_code) == '500':
                st.info(
                    'The [market, model, node] combination cannot be retrieved (likely nonexistent)')

        if start_date > end_date:
            st.warning('(From Date) is greater than (To Date)')
            st.info(
                'The dates range is invalid: end date must be later than start date')

        if str(response.status_code)[0] == '2':
            dic = {}
            for i in json.loads(response.content)['columns']:
                dic[i['name']] = i['values']

            df = pd.DataFrame(dic)
            st.dataframe(df)

            df["profit_total"] = df["profit_total"].cumsum()
            df["profit_long"] = df["profit_long"].cumsum()
            df["profit_short"] = df["profit_short"].cumsum()

            st.divider()

            visual(df)


if __name__ == '__main__':
    main()
