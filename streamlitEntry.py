# import libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
import sys
import os

sys.path.append('.')
sys.path.append('..')
#sys.path.insert(1, '../scripts')

# import custom libraries
from dataHandler import *

# set the page and title
st.set_page_config(page_title="Twitter data analysis", layout="wide")


def loadData():
    """
    A method to load the data from our data base
    """
    connection = DBConnect(dbName='tweets.db')
    query = "select * from TweetInformation"
    df = db_execute_fetch(connection, query, dbName="tweets.db", rdf=True)
    return df