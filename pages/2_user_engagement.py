# import libraries
import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import altair as alt
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt


sys.path.append('.')
sys.path.append('..')
#sys.path.insert(1, '../scripts')

# import custom libraries
from dataHandler import *

# set the page and title
st.set_page_config(page_title="User engagement", layout="wide")

@st.cache
def loadData():
    """
    A method to load the data from our data base
    """
    connection = dbConnect(dbName='telecom.db')
    query = "select * from userOverview"
    df = dbExecuteFetch(connection, query, dbName="telecom.db", rdf=True)
    return df


# TODO
@st.cache
def loadDataFromDB():
    engine = createEngine(local= True)
    userEng = pd.read_sql("select * from telecom.UserEngagement", engine)
    userAppEng = pd.read_sql("select * from telecom.UserAppEngagement", engine)
    return userEng, userAppEng

@st.cache
def loadDataFromCSV():
    df1 = pd.read_csv('data/user_engagement.csv.bz2')
    df2 = pd.read_csv('data/user_app_engagement.csv.bz2')
    return df1, df2

# TODO : replace with loadDataFromDB
df, df2 = loadDataFromCSV()

def displayData(df, df2):
    st.text('Overall Data')
    st.title('User engagement')
    st.write(df)
    st.title('User application engagement')
    st.write(df2)

def topCustomersPerEngagement(numberOfCustomers, df, df2):
    """
    """
    df = df[['MSISDN/Number', 'XDR Sessions', 'Dur. (ms)', 'total_data']]
    cols_list = ['XDR Sessions', 'Dur. (ms)', 'total_data']
    source = st.selectbox("choose aggregate feature", cols_list)
    df_ = df.nlargest(numberOfCustomers, source)
    st.title("User aggregate per " + str(source))
    st.bar_chart(data=df_)
    st.write(df_)

def showCluster(df, df2):
    # visualizing the 3 clusters in the dataframe
    # for 20, 000 samples only
    fig = px.scatter(df, x='total_data', y='Dur. (ms)',
                    color='cluster', size='XDR Sessions')
    fig.update_traces(marker_size=8)
    fig.update(layout_yaxis_range = [0, 800000])
    fig.update(layout_xaxis_range = [0, 4000000000])
    fig.show()
    # Plot!
    st.plotly_chart(fig, use_container_width=True)

st.title('User engagement analysis')

displayData(df, df2)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Top customers per engagement metric</p>", unsafe_allow_html=True)

numberOfCustomers = st.slider('top customers', 0, 100, 10)
topCustomersPerEngagement(numberOfCustomers, df, df2)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Engagement clusters</p>", unsafe_allow_html=True)
showCluster(df, df2)
