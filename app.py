import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page config
apptitle = 'Earthquake Damage Predictor'

st.set_page_config(page_title=apptitle)

# App Title
st.title('Earthquake Damage Predictor')

# File Path
TRAINFEATURES_FILE = "./data/train_values.csv"
TRAINLABELS_FILE = "./data/train_labels.csv"
TESTFEATURES_FILE = "./data/test_values.csv"


# Load the Data
X_full = pd.read_csv(TRAINFEATURES_FILE)
y_full = pd.read_csv(TRAINLABELS_FILE)


# EDA
st.subheader("Data Exploration")
st.write("The shape of training data, X is ", X_full.shape)
st.write("The shape of training label, y is ", y_full.shape)
st.write("")
st.subheader("Additional Information")
st.write("Features - First 500")
st.dataframe(X_full.head(500))
st.write("Labels - First 500")
st.dataframe(y_full.head(500))
X_full.set_index(["building_id"], inplace=True)
y_full.set_index(["building_id"], inplace=True)
