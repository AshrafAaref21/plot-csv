import requests
import streamlit as st
from pandas import concat

from utils import read_response, to_date, visual, visual_compare, models_visualizer


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

            # st.dataframe(df)

            df["profit_total"] = df["profit_total"].cumsum()
            df["profit_long"] = df["profit_long"].cumsum()
            df["profit_short"] = df["profit_short"].cumsum()

            # if callback is not None:
            #     st.divider()
            #     callback(df)
        else:
            st.info("There's no Records for this short period. :anchor:")

        return df


def single_model(data, show=False):
    response = requests.post(
        'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data)

    df = output(response, data)
    visual(df)

    if show:
        st.dataframe(df, use_container_width=True)


def models_comparison(data1, data2, show=False):
    response_1 = requests.post(
        'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data1)
    df1 = output(response_1, data1)

    if ',' in data2['model']:
        models = data2.pop('model')
        models = models.split(',')
        models = [i.strip() for i in models]
        df1['model'] = data1['model']
        ls = []
        for i in models:
            data2['model'] = i
            response = requests.post(
                'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data2)

            df2 = output(response, data2)
            df2['model'] = i
            ls.append(df2)

            # df2.set_index('date', inplace=True)
            # df2.columns = [f"{i} ({data2['model']})" for i in df2.columns]

            # df = df1.join(df2, how='left')
        df = concat([df1, *ls], axis=0)
        models_visualizer(df)
        # visual_compare(df, models=[data1['model'], *models])

    else:

        df1.set_index('date', inplace=True)
        df1.columns = [f"{i} ({data1['model']})" for i in df1.columns]

        response_2 = requests.post(
            'https://quantum-zero-bayfm.ondigitalocean.app/report', data=data2)

        df2 = output(response_2, data2)
        df2.set_index('date', inplace=True)
        df2.columns = [f"{i} ({data2['model']})" for i in df2.columns]

        df = df1.join(df2)

        visual_compare(df, models=[data1['model'], data2['model']])

    if show:
        st.divider()
        st.dataframe(df, use_container_width=True)
