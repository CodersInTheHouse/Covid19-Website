import streamlit as st 
import datetime as dt
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import date, timedelta
import plotly.express as px

st.set_page_config(page_title= "Covid-19 Data", page_icon=":bar_chart:", layout="wide")

#READ EXCEL
df= pd.read_excel(
    io='DatosCovid19.xlsx',
    engine='openpyxl',
    sheet_name='DatosCovid',
    skiprows=0,
    usecols='A:M',
    nrows=15,
)
st.dataframe(df)

#SIDE BAR 
st.sidebar.header('Please choose the items below:')

#SELECT COUNTRY
country=st.sidebar.multiselect(
    'Select country', ['Argentina','Canada', 'China', 'Colombia','France', 'Germany','Great Britain', 'Italy', 'Mexico', 'United States'], max_selections=4,
)
#SELECT VARIABLES
variables=st.sidebar.selectbox(
    'Variables', ('confirmed cases', 'confirmed deaths', 'fully vaccinated', 'ICU patient', 'positive test' )
)

today = date.today()
default_date_yesterday = today - timedelta(days=1)
#SELECT DATAS
start_date = st.sidebar.date_input('Start Date', default_date_yesterday)
end_date = st.sidebar.date_input('End Date', default_date_yesterday)

#BUTTON
boton=st.sidebar.button('Search')

#HIDE LINES MENU AND MADE WITH STREAMLIT 
hide_st_style = """
              <style>
              #MainMenu {visibility:hidden;}
              footer {visibility:hidden;}
              </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

