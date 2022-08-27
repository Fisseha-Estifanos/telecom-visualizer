import streamlit as st

st.set_page_config(
    page_title="Telecom data analysis",
    #page_icon="👋",
)

st.write("# Welcome to telecom data analysis👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    ## This is a data visualizer dashboard made for the Telecom data analysis project.

    **👈 Select a page from the sidebar** to see some demonstrations!

    ### To learn more about the project you can see more at GitHub?
    - Check out the [Project](https://github.com/fisseha-estifanos/telecom)

    ### Contact me at
    - Email [Fisseha Estifanos](mailto:fisseha.137@gmail.com)
    - GitHub [Fisseha Estifanos](https://github.com/fisseha-estifanos)
    - LinkedIn [Fisseha Estifanos](https://www.linkedin.com/in/fisseha-estifanos-109ba6199/)
"""
)