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


# TODO
@st.cache
def loadDataFromDB():
    engine = createEngine(local=False)
    df = pd.read_sql("select * from telecom.UserOverview", engine)
    #df = pd.csv('name', engine)
    return df


@st.cache
def loadDataFromCSV():
    df = pd.read_csv('data/sample_overview_data.csv.bz2')
    return df

# TODO : replace with loadDataFromDB
baseDF = loadDataFromCSV()


def displayData(baseDF):
    st.text('Overall Data')
    st.write(baseDF)


def selectTopHeadsets(num, baseDF):
    """
    hashtags filter
    """
    st.text('Top handsets')
    
    top_headsets_list_df = baseDF["Handset Type"].value_counts().nlargest(n=num)
    st.write(top_headsets_list_df)

    # Generate plot on top 10 handsets
    fig = plt.figure(figsize = (10,10))
    #last_num = len(top_headsets_list_df.values)
    colors = sns.color_palette('muted')[0:num]
    plot = top_headsets_list_df.plot.pie(grid=True, colors=colors, autopct='%.000f%%')
    plt.title('top handset types')
    st.bar_chart(top_headsets_list_df.sort_values(ascending = False))


def topHandsetsByManufacturers(handset, handsetManufac, baseDF):
    apple_manufacturer = baseDF.loc[baseDF['Handset Manufacturer'] == 'Apple', ['Handset Type']].value_counts().nlargest(handset)
    samsung_manufacturer = baseDF.loc[baseDF['Handset Manufacturer'] == 'Samsung', ['Handset Type']].value_counts().nlargest(handset)
    huawei_manufacturer = baseDF.loc[baseDF['Handset Manufacturer'] == 'Huawei', ['Handset Type']].value_counts().nlargest(handset)

    st.title('Apple')
    st.write(apple_manufacturer)
    
    st.title('Samsung')
    st.write(samsung_manufacturer)

    st.title('Huawei')
    st.write(huawei_manufacturer)


def manufacturerPie(manufacturer_Num, baseDF):
    dfLangCount = baseDF['Handset Manufacturer'].value_counts().nlargest(n=manufacturer_Num)
    st.title("Top head sets per manufacturer")
    fig1, ax1 = plt.subplots()
    ax1.pie(dfLangCount.values, labels=dfLangCount.keys(), autopct='%.000f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)


def aggregatePerUser(baseDF):
    """
    """
    cols_list = ['Bearer Id', 'Dur. (ms)', 'total_data']
    source = st.selectbox("choose aggregate feature", cols_list)
    df_ = baseDF.groupby('MSISDN/Number')[source].sum()
    st.title("User aggregate per " + str(source))
    st.write(df_)
    st.bar_chart(data=df_)

st.title('User overview analysis')

displayData(baseDF)

st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Top handsets</p>", unsafe_allow_html=True)

# Some number in the range 0-100
num = st.slider('top headsets', 0, 100, 10)
selectTopHeadsets(num, baseDF)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Top handsets per top handset manufactures</p>", unsafe_allow_html=True)

handsetNum = st.slider('top headsets', 0, 20, 5)
man_Num = st.slider('top headset manufacturer', 0, 20, 3)
topHandsetsByManufacturers(handsetNum, man_Num, baseDF)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Top handset manufactures</p>", unsafe_allow_html=True)

manufacturer_Num = st.slider('top headset manufacturer', 0, 20, 3, key='manufacturer_Num')
manufacturerPie(manufacturer_Num, baseDF)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Aggregates per user</p>", unsafe_allow_html=True)

aggregatePerUser(baseDF)


