import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

def app():
    # Get all data from database
    query = 'SELECT * FROM buildings_table'
    df = pd.read_sql(query, conn)
    X = df.loc[:,~df.columns.isin(['building_id', 'damage_grade'])]
    y = df.loc[:,"damage_grade"]

    # Step 1 - Data Exploration
    st.header("Data Exploration and Analysis")

    # 1. Information of Data Features and Labels
    st.subheader("1. Information of Features and Labels")
    st.write("The shape of features, X is ", X.shape)
    st.write("The shape of labels, y is ", y.shape)
    st.markdown("Features - First 300")
    st.dataframe(X.head(300))
    st.markdown("Labels - First 300")
    st.dataframe(y.head(300))

    #Make a copy of features for data exploration purpose
    EDA_features = X.copy()

    # 2. Frequency Distributions and Summary Statistics
    st.subheader('2. Frequency Distributions and Summary Statistics')
    num_features = ['number_floors','age_building','area_sq_ft','height_ft']
    num_data = EDA_features.loc[:, num_features]

    # Plot histograms
    fig, ax = plt.subplots()
    num_data.hist(grid=True, figsize=(20,16), color='green', bins=5)
    st.pyplot(plt)

    # Summary Statistics
    st.write(num_data.describe().applymap('{:.2f}'.format).transpose())

    # Convert Categorical Feature to Integers
    le = LabelEncoder()
    categorical_columns = ['land_surface_condition','foundation_type','roof_type','ground_floor_type','other_floor_type','position','plan_configuration']
    for c in categorical_columns:
        EDA_features[c] = le.fit_transform(EDA_features[c])

    # 3. Correlation of features
    st.subheader('3. Correlation of features')
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(aspect='equal')
    sns.heatmap(EDA_features.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
    st.write(fig)