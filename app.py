import streamlit as st


# DB Mgmt
import sqlite3 
conn = sqlite3.connect('data/buildingsdata.db')
c = conn.cursor()

# Custom imports 
from multipage import MultiPage
from pages import input_form, data_analysis, machine_learning

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Earthquake Damage Predictor")

# Sub Title
st.markdown("""
Based on aspects of building location and construction, this app predicts the level of damage to buildings caused by the 2015 Gorkha earthquake in Nepal.
* **Python libraries: ** Streamlit, Pandas, Numpy, Matplotlib, Seaborn, sklearn, joblib
* **Data Source: ** [Driven Data Competition - Richter's Predictor: Modeling Earthquake Damage ](https://www.drivendata.org/competitions/57/nepal-earthquake/)
""")

# Add all your applications (pages) here
app.add_page("Input Form", input_form.app)
app.add_page("Data Exploration", data_analysis.app)
app.add_page("Machine Learning", machine_learning.app)

# The main app
app.run()

# Reference
# https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030