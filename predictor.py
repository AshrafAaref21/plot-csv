import requests
import streamlit as st
from utils import read_response, to_date, visual


def output(response, data):
    if str(response.status_code)[0] != '2':
        st.error(f'Bad Request with status code\
                     {response.status_code}\
                          :name_badge:')
        st.error(f"{str(response.content)} :name_badge:")
        if str(response.status_code) == '500':
            st.info(
                'The [market, model, node] combination cannot be retrieved (likely nonexistent)')

    if data['from_date'] > data['to_date']:
        st.warning('(From Date) is greater than (To Date)')
        st.info(
            'The dates range is invalid: end date must be later than start date')

    if str(response.status_code)[0] == '2':
        df = read_response(response=response)
        if len(df) > 0:
            df['date'] = df['date'].apply(to_date)
            st.dataframe(df)

            df["profit_total"] = df["profit_total"].cumsum()
            df["profit_long"] = df["profit_long"].cumsum()
            df["profit_short"] = df["profit_short"].cumsum()

            st.divider()

            visual(df)
        else:
            st.info("There's no Records for this short period. :anchor:")


def single_model(data):
    response = requests.post(
        'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data)

    output(response, data)


def models_comparison(data1, data2):
    cl1, _, cl2 = st.columns([5, 1, 5])

    st.divider()

    with cl1:
        response_1 = requests.post(
            'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data1)

        output(response_1, data1)

    with cl2:
        response_2 = requests.post(
            'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data2)

        output(response_2, data2)
