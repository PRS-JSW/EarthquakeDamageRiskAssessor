import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import assess_existing, assess_reconstructed, data_analysis, machine_learning, update_epicenter, model_performance

st.set_page_config(
    page_icon="🏢",
    page_title="Earthquake Building Damage Risk Assessor",
    layout='wide')

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("Assess Damage Risk of Reconstructed Building", assess_reconstructed.app)
app.add_page("Assess Damage Risk of Existing Building", assess_existing.app)
app.add_page("Data Exploration", data_analysis.app)
app.add_page("Machine Learning", machine_learning.app)
app.add_page("Model Performance and Evaluation", model_performance.app)
app.add_page("Update Epicenter Location", update_epicenter.app)

# The main app
app.run()

# Reference
# https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030