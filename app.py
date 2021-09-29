import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
apptitle = 'Earthquake Damage Predictor'

st.set_page_config(page_title=apptitle)

# App Title
st.title('Earthquake Damage Predictor')

# Sub Title
st.markdown("""
Based on aspects of building location and construction, this app predicts the level of damage to buildings caused by the 2015 Gorkha earthquake in Nepal.
* **Python libraries: ** Streamlit, Pandas, Numpy, Matplotlib, Seaborn
* **Data Source: ** [Driven Data Competition - Richter's Predictor: Modeling Earthquake Damage ](https://www.drivendata.org/competitions/57/nepal-earthquake/)
""")

# File Path
TRAINFEATURES_FILE = "./data/train_values.csv"
TRAINLABELS_FILE = "./data/train_labels.csv"
TESTFEATURES_FILE = "./data/test_values.csv"

# Load the Data
X_full = pd.read_csv(TRAINFEATURES_FILE)
y_full = pd.read_csv(TRAINLABELS_FILE)

# Sidebar
st.sidebar.header("User Input Features")

# Step 1 - Data Exploration
st.header("Step 1 - Data Exploration")

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
st.subheader('2. Analysis of Geographic Region Variables - Relationship of Geographic Variable 1, 2 and 3')
geo_df = X_full.groupby(['geo_level_1_id','geo_level_2_id','geo_level_3_id']).size().reset_index().rename(columns={0:'count'})
geo_df = geo_df.sort_values(['geo_level_1_id','geo_level_2_id','geo_level_3_id'])
st.write(geo_df)
st.markdown("""
There are no duplicates observed for geographic variable 3 and geographic variable 2. 
Each geograhic variable 3 value corresponds to a geographic 2 value and therefore correspond to a geographic 1 value.
""")

# 3. Frequency Distributions and Summary Statistics
st.subheader('3. Frequency Distributions and Summary Statistics')
vis_data = X_full.loc[:, ~X_full.columns.isin(['geo_level_1_id','geo_level_2_id','geo_level_3_id'])]

# Plot histograms
fig, ax = plt.subplots()
vis_data.hist(grid=True, figsize=(20,16), color='green', bins=5)
st.pyplot(plt)

# Summary Statistics
st.write(X_full.describe().applymap('{:.2f}'.format).transpose())

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

# 4. Correlation of features
st.subheader('4. Correlation of features')
fig = plt.figure(figsize=(18, 18))
ax = plt.subplot(aspect='equal')
sns.heatmap(X_full.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
st.write(fig)
st.markdown("""
Features with correlation >= 0.7
* count_floors_pre_eq: height_percentage (0.8)
* has_secondary_use: has_secondary_use_agriculture (0.7)
Therefore, it is likely that majority of buildings are also used for agriculture.
""")

# 5. Count of buildings with secondary uses
st.subheader('5. Count of buildings with secondary uses')
secondaryuse_df = X_full.iloc[:, 20:]
st.write(secondaryuse_df)
# st.write(secondaryuse_df[secondaryuse_df != 0].count())

# 6. Observation of damage to building among geographic region
st.subheader('6. Observation of damage to building among geographic region')
geo1_dmg_chart = y_full.join(X_full['geo_level_1_id'])
st.write(geo1_dmg_chart)
fig, ax = plt.subplots(figsize=(12,12))
sns.countplot(y="geo_level_1_id", hue="damage_grade", data=geo1_dmg_chart)
st.pyplot(fig)

# Step 2 - Feature Selection and Engineering
st.header("Step 2 - Feature Selection and Engineering")

# Use random forest to check importance of features
# 33 features, to encode categorical features and check for correlation

# Normalise any numerical data required

# Step 3 - Model Development and Training
st.header("Step 3 - Model Development and Training")

# Agenda for Model Development
# 1. Logistic Regression (KK)
# 2. Decision Tree (Sungmin)
# 3. Random Forest (Ensemble of Decision Tree) (Sungmin)
# 4. AdaBoost (KK)
# 5. Ordinal Classifier: https://towardsdatascience.com/simple-trick-to-train-an-ordinal-regression-with-any-classifier-6911183d2a3c (Wei Liang)

# Step 4 - Model Validation and Evaluation
st.header("Step 4 - Model Validation and Evaluation")




# Step 5 - Model Selection
st.header("Step 5 - Model Selection")



# Step 6 - Model Deployment
st.header("Step 6 - Model Deployment")


