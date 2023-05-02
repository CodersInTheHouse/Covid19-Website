import streamlit as st 
import pandas as pd
import pyodbc
from datetime import date, timedelta
import numpy as np


st.set_page_config(page_title= "Covid-19 Data", page_icon=":bar_chart:", layout="wide")


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    connected = False
    while (connected==False):
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + st.secrets["server"]
            + ";DATABASE="
            + st.secrets["database"]
            + ";UID="
            + st.secrets["username"]
            + ";PWD="
            + st.secrets["password"],
            timeout=30
        )
        try:
            connected = True
            conn.cursor().execute('select top 1 from DatosCovid')
        except pyodbc.Error as error:
            if error.args[0] == "08S01":
                connected= False
                conn.close()
    return conn




conn = init_connection()

#SIDE BAR 
st.sidebar.header('Please choose the items below:')

#SELECT COUNTRY
country = st.sidebar.multiselect(
    'Select country', ['Argentina','Canada', 'China', 'Colombia','France', 'Germany','Great Britain', 'Italy', 'Mexico', 'United States'], max_selections=4,
)

#SELECT VARIABLES
variables = st.sidebar.selectbox(
    'Variables', ('Confirmed cases', 'Confirmed deaths', 'Fully vaccinated', 'ICU patient', 'Positive test' )
)

match variables:
    case 'Confirmed cases':
        rVar='total_cases'
    case 'Confirmed deaths':
        rVar='total_deaths'
    case 'Fully vaccunated':
        rVar='people_fully_vaccinated'
    case 'ICU patient':
        rVar='icu_patients'
    case 'Positive test':
        rVar='icu_patients'


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

#BUTTON
buttonSearch = st.sidebar.button('Search')

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=300)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

@st.cache_data(ttl=300)
def run_queryDF(query):
    return pd.read_sql(query,conn)

def createSentence(lista: list):
    sentence = f"('{lista[0]}'"
    if len(lista) > 1:
        for c in range(1, len(lista)):
            sentence += ",'" + lista[c] + "'"
    sentence += ")"
    return sentence

def prettySentence(list:list):
    text = ','.join(list)
    if(len(list)>1):
        text = text.replace(f',{list[-1]}',f' and {list[-1]}')
    return text

def isAllCorrect() -> bool:
    return len(country) > 0

#Tabs
tab0, tab1, tab2 = st.tabs(['Query','Line','Bars'])

if buttonSearch:
    if isAllCorrect():
        #Funcion que retorna los paises seleccionados en forma de query
        sentence = createSentence(country)
        pSentence = prettySentence(country)
        
        #rows = run_query(f"select * from DatosCovid as dc where dc.Date >= '{start_date}' and dc.Date <= '{end_date}' and dc.Location IN {sentence};")
        
        # Print results.
        #for row in rows:
        #    st.write(f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}")
        with tab0:
            data = run_queryDF(f"select dc.Location,dc.Date,dc.{rVar} from DatosCovid as dc where dc.Date >= '{start_date}' and dc.Date <= '{end_date}' and dc.Location IN {sentence};")
            st.table(data)

        with tab1:
            st.subheader(f'Linechar for: {pSentence}')

            data1 = run_queryDF(f"select month(dc.Date) as mes,max(dc.{rVar}) as total from DatosCovid dc where dc.Location IN {sentence} group by month(dc.Date) order by  month(dc.Date) asc")
            st.line_chart(data=data1,x='mes', y='total')

        with tab2:
            st.subheader(f'Barchar for: {pSentence}')
            if len(country)>1:
                data2 = run_queryDF(f"select dc.Location, max(dc.{rVar}) as total from DatosCovid dc where dc.Location in {sentence} and dc.Date >= '{start_date}' and  dc.Date <= '{end_date}' group by dc.Location")
                st.bar_chart(data=data2,x='Location', y='total')
            else:
                data2 = run_queryDF(f"select year(dc.Date) as año, max(dc.{rVar}) as total from DatosCovid dc where dc.Location in ('Canada') and dc.Date >= '01/01/2020' and  dc.Date <= '01/01/2023' group by year(dc.Date) order by year(dc.Date) asc")
                st.bar_chart(data=data2,x='año', y='total')

    else:
        st.warning("Sorry, there's been a problem filling those boxes 🧐🧐")
        st.info("Please check and hit that search button again! 🤞")
else:
    with tab0:
        st.info("Welcome to our webpage!")
        st.write("Here you can see really interesenting graphs related to COVID-19")
        st.success("To visualizes the graphics. Fill the boxes on your left 👈")
    
    with tab1:
        st.info("Here you will see a line chart of the query you just performed!")
    
    with tab2:
        st.info("Here you will see a bar chart of the query you just performed!")
    



    

#HIDE LINES MENU AND MADE WITH STREAMLIT 
hide_st_style = """
              <style>
              #MainMenu {visibility:hidden;}
              footer {visibility:hidden;}
              </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
