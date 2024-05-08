import streamlit as st
import numpy as np
import plotly.express as px


def visual(df):
    tab1, tab2 = st.tabs(["Plot Profit Cumulative", "Wins VS Losses"])
    with tab1:
        fig = px.line(
            df,
            x='date',
            y=['profit_short', 'profit_long', 'profit_total'],
            labels={'value': 'Profit Cumulative', 'variable': ''},
        )

        newnames = {"profit_total": "Total",
                    "profit_long": "Long",
                    "profit_short": "Short"
                    }

        fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))
        # fig.update_layout(
        #     hovermode="x"
        # )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        y_max = np.ceil(df.win_count.max() / 5) * 5 + 5
        if df.win_count.max() < df.loss_count.max():
            y_max = np.ceil(df.loss_count.max() / 5) * 5 + 5
        y_min = np.floor(df.win_count.min() / 5) * 5 - 5
        if df.win_count.min() < df.loss_count.min():
            y_min = np.floor(df.loss_count.min() / 5) * 5 - 5

        fig = px.line(
            df,
            x='date',
            y=['mwh_total', 'win_count'],
            # color_discrete_sequence=px.colors.qualitative.Antique,
            range_y=[y_min, y_max],
            labels={'value': 'Wins and Losses',
                    'variable': ''}
        )
        newnames = {
            "mwh_total": "# Economics",
            "win_count": "# Wins"}

        fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))
        # fig.update_layout(
        #     hovermode="x"
        # )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def CSS():
    st.markdown("""<style>
            .st-id {
            gap: 18px;
            margin-top:15px;
            }
            .st-ib {
            -webkit-box-orient: vertical;
            -webkit-box-direction: normal;
            flex-direction: row;
                
        }


              
            </style>""", unsafe_allow_html=True)
