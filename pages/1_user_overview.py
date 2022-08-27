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
st.set_page_config(page_title="User overview", layout="wide")

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
    fromDb = pd.read_sql("select * from telecom.UserOverview", engine)
    return fromDb


def displayData():
    st.text('Overall Data')
    df = loadDataFromDB()
    st.write(df)


def selectTopHeadsets(num):
    """
    hashtags filter
    """
    st.text('Top handsets')

    df = loadDataFromDB()
    top_headsets_list_df = df["Handset Type"].value_counts().nlargest(n=num)
    st.write(top_headsets_list_df)

    # Generate plot on top 10 handsets
    fig = plt.figure(figsize = (10,10))
    #last_num = len(top_headsets_list_df.values)
    colors = sns.color_palette('muted')[0:num]
    plot = top_headsets_list_df.plot.pie(grid=True, colors=colors, autopct='%.000f%%')
    plt.title('top handset types')
    st.bar_chart(top_headsets_list_df.sort_values(ascending = False))


st.title('User overview analysis')

displayData()

st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Top handsets</p>", unsafe_allow_html=True)

# Some number in the range 0-100
num = st.slider('top headsets', 0, 100, 10)
selectTopHeadsets(num)
