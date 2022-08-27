# import libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns


sys.path.append('.')
sys.path.append('..')
#sys.path.insert(1, '../scripts')

# import custom libraries
from dataHandler import *

# set the page and title
st.set_page_config(page_title="Telecom data analysis", layout="wide")

@st.cache
def loadData():
    """
    A method to load the data from our data base
    """
    connection = dbConnect(dbName='telecom.db')
    query = "select * from userOverview"
    df = dbExecuteFetch(connection, query, dbName="telecom.db", rdf=True)
    return df


@st.cache
def loadDataFromDB():
    engine = createEngine()
    fromDb = pd.read_sql("select * from telecom.UserSatisfaction", engine)
    return fromDb


def displayData():
    st.text('Overall Data')
    df = loadDataFromDB()
    st.write(df)


st.title('User satisfaction analysis')

displayData()

st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>First visualizer ote goes here</p>", unsafe_allow_html=True)
