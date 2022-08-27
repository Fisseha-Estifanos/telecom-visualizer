# import libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px

# import custom libraries
from dataHandler import *

# set the page and title
st.set_page_config(page_title="Twitter data analysis", layout="wide")