import requests
import streamlit as st
from pandas import concat

from utils import read_response, to_date, visual, visual_compare


def output(response, data, callback=None):
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
        df = df[['date', 'profit_short', 'profit_long', 'profit_total',
                 'mwh_total', 'win_count']]
        if len(df) > 0:
            df['date'] = df['date'].apply(to_date)

            st.dataframe(df)

            df["profit_total"] = df["profit_total"].cumsum()
            df["profit_long"] = df["profit_long"].cumsum()
            df["profit_short"] = df["profit_short"].cumsum()

            st.divider()

            if callback is not None:
                callback(df)
        else:
            st.info("There's no Records for this short period. :anchor:")

        return df


def single_model(data):
    response = requests.post(
        'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data)

    output(response, data, visual)


def models_comparison(data1, data2):
    response_1 = requests.post(
        'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data1)

    response_2 = requests.post(
        'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data2)

    cl1, _, cl2 = st.columns([5, 1, 5])

    st.divider()

    with cl1:
        st.subheader(f"Model {data1['model']}")
        df1 = output(response_1, data1)
        df1.set_index('date', inplace=True)
        df1.columns = [f"{i} ({data1['model']})" for i in df1.columns]
    with cl2:
        st.subheader(f"Model {data2['model']}")
        df2 = output(response_2, data2)
        df2.set_index('date', inplace=True)
        df2.columns = [f"{i} ({data2['model']})" for i in df2.columns]

    df = df1.join(df2)
    st.dataframe(df)
    visual_compare(df, data1, data2)
