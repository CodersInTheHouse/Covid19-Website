import streamlit as st 
import pandas as pd
import pyodbc
from datetime import date, timedelta


st.set_page_config(page_title= "Covid-19 Data", page_icon=":bar_chart:", layout="wide")


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

#BUTTON
buttonSearch = st.sidebar.button('Search')

date_inicio = date(2020, 3, 10) #date inicio pandemia
date_fin = date(2023,1,21) #date fin pandemia

#SELECT DATAS
start_date = st.sidebar.date_input('Start Date', 
                                   value= date_inicio, 
                                   min_value= date_inicio, 
                                   max_value= date_fin)

end_date = st.sidebar.date_input('End Date', 
                                 value = date_fin,
                                 min_value= date_inicio, 
                                 max_value= date_fin)


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=300)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def createSentence(lista: list):
    sentence = f"('{lista[0]}'"
    if len(lista) > 1:
        for c in range(1, len(lista)):
            sentence += ",'" + lista[c] + "'"
    sentence += ")"
    return sentence

def isAllCorrect() -> bool:
    return len(country) > 0


if buttonSearch:
    if isAllCorrect():
        #Funcion que retorna los paises seleccionados en forma de query
        sentence = createSentence(country)
        
        rows = run_query(f"select * from DatosCovid as dc where dc.Date >= '{start_date}' and dc.Date <= '{end_date}' and dc.Location IN {sentence};")
        # Print results.
        for row in rows:
            st.write(f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}")
    else:
        st.warning("Sorry, there's been a problem filling those boxes 🧐🧐")
        st.info("Please check and hit that search button again! 🤞")
else:
    st.info("Welcome to our webpage!")
    st.write("Here you can see really interesenting graphs related to COVID-19")
    st.success("To visualizes the graphics. Fill the boxes on your left 👈")

#HIDE LINES MENU AND MADE WITH STREAMLIT 
hide_st_style = """
              <style>
              #MainMenu {visibility:hidden;}
              footer {visibility:hidden;}
              </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
