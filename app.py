import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import assess_risk, input_form, data_analysis, machine_learning

st.set_page_config(
    page_icon="🏢",
    page_title="Earthquake Building Damage Risk Assessor",
    layout='wide')

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("Re-Evaluate Damage Risk of Existing Building", assess_risk.app)
app.add_page("Evaluate Damage Risk of New Building", input_form.app)
app.add_page("Data Exploration", data_analysis.app)
app.add_page("Machine Learning", machine_learning.app)

# The main app
app.run()

# Reference
# https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030