import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

def app():
    # File Path
    TRAINFEATURES_FILE = "./data/train_values.csv"
    TRAINLABELS_FILE = "./data/train_labels.csv"
    TESTFEATURES_FILE = "./data/test_values.csv"

    # Load the Data
    X_full = pd.read_csv(TRAINFEATURES_FILE)
    y_full = pd.read_csv(TRAINLABELS_FILE)

    # Step 1 - Data Exploration
    st.header("Data Exploration and Analysis")

    # 1. Information of Training Data Features and Labels
    st.subheader("1. Information of Training Data Features and Labels")
    st.write("The shape of training data, X is ", X_full.shape)
    st.write("The shape of training label, y is ", y_full.shape)
    st.markdown("Features of Training Data - First 300")
    st.dataframe(X_full.head(300))
    st.markdown("Labels of Training Data - First 300")
    st.dataframe(y_full.head(300))
    X_full.set_index(["building_id"], inplace=True)
    y_full.set_index(["building_id"], inplace=True)

    # 2. Analysis of Geographic Region Variables

    #Make a copy of features for data exploration purpose
    EDA_features = X_full.copy()

    st.subheader('2. Analysis of Geographic Region Variables - Relationship of Geographic Variable 1, 2 and 3')
    geo_df = EDA_features.groupby(['geo_level_1_id','geo_level_2_id','geo_level_3_id']).size().reset_index().rename(columns={0:'count'})
    geo_df = geo_df.sort_values(['geo_level_1_id','geo_level_2_id','geo_level_3_id'])
    st.write(geo_df)
    st.markdown("""
    There are no duplicates observed for geographic variable 3 and geographic variable 2. 
    Each geograhic variable 3 value corresponds to a geographic 2 value and therefore correspond to a geographic 1 value.
    """)

    # 3. Frequency Distributions and Summary Statistics
    st.subheader('3. Frequency Distributions and Summary Statistics')
    vis_data = EDA_features.loc[:, ~X_full.columns.isin(['geo_level_1_id','geo_level_2_id','geo_level_3_id'])]

    # Plot histograms
    fig, ax = plt.subplots()
    vis_data.hist(grid=True, figsize=(20,16), color='green', bins=5)
    st.pyplot(plt)

    # Summary Statistics
    st.write(EDA_features.describe().applymap('{:.2f}'.format).transpose())

    st.markdown("""
    From the histograms and summary, it can be observed that the following binary variables denoting secondary uses of buildings have a mean close to 0:
    * has_secondary_use_rental
    * has_secondary_use_institution
    * has_secondary_use_school
    * has_secondary_use_industry
    * has_secondary_use_health_post
    * has_secondary_use_gov_office
    * has_secondary_use_use_police
    * has_secondary_use_other
    """)

    # Convert Categorical Feature to Integers
    le = LabelEncoder()
    categorical_columns = ['land_surface_condition','foundation_type','roof_type','ground_floor_type','other_floor_type','position','plan_configuration','legal_ownership_status']
    for c in categorical_columns:
        EDA_features[c] = le.fit_transform(EDA_features[c])

    # 4. Correlation of features
    st.subheader('4. Correlation of features')
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(aspect='equal')
    sns.heatmap(EDA_features.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
    st.write(fig)
    st.markdown("""
    _To enlarge image: Right click and select Open Image in New Tab._

    Features with correlation >= 0.7
    * count_floors_pre_eq: height_percentage (0.8) is correlated as buildings with higher number of floors will likely be higher
    * has_secondary_use: feature has_secondary_use_agriculture (0.7) is a subset of has_secondary_use
    """)

    # 5. Count of buildings with secondary uses
    st.subheader('5. Count of buildings with secondary uses')
    secondaryuse_df = EDA_features.iloc[:, 27:]
    st.write(secondaryuse_df.astype(bool).sum(axis=0))
    st.markdown("""
    Total of 29,156 buildings with secondary uses with majority being used as agriculture and hotel.
    """)

    # 6. Observation of damage to building among geographic region
    st.subheader('6. Observation of damage to building among geographic region')
    geo1_dmg_chart = y_full.join(EDA_features['geo_level_1_id'])
    st.write(geo1_dmg_chart)
    fig, ax = plt.subplots(figsize=(12,12))
    sns.countplot(y="geo_level_1_id", hue="damage_grade", data=geo1_dmg_chart)
    st.pyplot(fig)
    st.markdown("""
    Observed that some regions have fewer damaged buildings, possibly rural regions. Area denoted as "17" have the most building with grade 3 damage, 
    possibly the region struck by the earthquake.
    """)