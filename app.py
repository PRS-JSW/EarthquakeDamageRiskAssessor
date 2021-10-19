import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import assess_risk, input_form, data_analysis, machine_learning

st.set_page_config(layout='wide')

# Title of the main page
st.title("Earthquake Damage Predictor")

# Sub Title
st.markdown("""
Based on aspects of building location and construction, this app predicts the level of damage to buildings caused by the 2015 Gorkha earthquake in Nepal.
* **Python libraries: ** Streamlit, Pandas, Numpy, Matplotlib, Seaborn, sqlite3, sklearn, joblib
* **Data Source: ** [Kathmandu Living Labs’s Open Data Portal](https://eq2015.npc.gov.np/)
""")

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("Search Building Data", assess_risk.app)
app.add_page("Add New Building Data", input_form.app)
app.add_page("Data Exploration", data_analysis.app)
app.add_page("Machine Learning", machine_learning.app)

# The main app
app.run()

# Reference
# https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030