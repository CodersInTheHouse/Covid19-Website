import streamlit as st 
import pandas as pd
import pyodbc
from datetime import date, timedelta


st.set_page_config(page_title= "Covid-19 Data", page_icon=":bar_chart:", layout="wide")


#SIDE BAR 
st.sidebar.header('Please choose the items below:')

#SELECT COUNTRY
country = st.sidebar.multiselect(
    'Select country', ['Argentina','Canada', 'China', 'Colombia','France', 'Germany','Great Britain', 'Italy', 'Mexico', 'United States'], max_selections=4,
)

#SELECT VARIABLES
variables = st.sidebar.selectbox(
    'Variables', ('Confirmed cases', 'Confirmed deaths', 'Fully vaccunated', 'ICU patient', 'Positive test' )
)

today = date.today()
default_date_yesterday = today - timedelta(days=1)

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

conn = init_connection()

#SELECT DATAS
start_date = st.sidebar.date_input('Start Date', default_date_yesterday)
end_date = st.sidebar.date_input('End Date', default_date_yesterday)

#BUTTON
buttonSearch = st.sidebar.button('Search')

def createQuery():
    pass


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=300)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


if buttonSearch:
    print("Button")
    rows = run_query("select * from DatosCovid as dc where dc.Date >= '2020-01-12' and dc.Date < '2020-01-13';")
    # Print results.
    for row in rows:
        for i in range(row):
            st.write(row[i], end="")
        st.write("")
        #st.write(f"{row[0]}{row[1]}{row[2]}{row[3]}:")
        




#HIDE LINES MENU AND MADE WITH STREAMLIT 
hide_st_style = """
              <style>
              #MainMenu {visibility:hidden;}
              footer {visibility:hidden;}
              </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
