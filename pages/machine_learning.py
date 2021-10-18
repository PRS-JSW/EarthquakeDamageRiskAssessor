from numpy.core.numerictypes import maximum_sctype
import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, f1_score
import joblib
from .OrdinalClassifier import OrdinalClassifier

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

def app():
    # Get all data from database
    query = 'SELECT * FROM buildings_table'
    df = pd.read_sql(query, conn)
    # df.loc[:,'district_id'] = df.loc[:,'ward_id'].astype(str).str[:2].astype(int)
    df.loc[:,'mun_id'] = df.loc[:,'ward_id'].astype(str).str[:4].astype(int)
    df.loc[:,'damage_grade'] = df.loc[:,'damage_grade'].astype(int) - 1

    # Duplicate dataframe as X without building_id, ward_id and number_floors
    X = df.loc[:,~df.columns.isin(['building_id','ward_id','number_floors'])].copy()
    # print(X.head(100))
    # print(X.info())
    # print(X.describe())

    # Step 1 - Feature Selection and Engineering
    st.header("Feature Selection and Engineering")

    # 1. Normalise numerical features
    num_features = ['age_building','area_sq_ft','height_ft']
    
    for feature in num_features:
        X.loc[:,feature] = np.log(X.loc[:,feature].replace(0, 1))

    # 2. Mean Encode Geographic Feature
    geo_features = ['mun_id']
    # 'district_id','ward_id'

    # Mean of damage grade
    mean = X.loc[:,'damage_grade'].mean()

    for var in geo_features:
        geo_agg = X.groupby(var)['damage_grade'].agg(['count','mean'])
        counts = geo_agg['count']
        means = geo_agg['mean']
        weight = 100
        smooth = (counts * means + weight * mean) / (counts + weight)
        X.loc[:,var+'_weighted_mean'] = X.loc[:,var].map(smooth)

    # Create target dataframe y and drop unused columns for X
    y = X.loc[:,'damage_grade'].copy()
    X = X.loc[:,~X.columns.isin(['mun_id','plan_configuration','damage_grade'])]

    # 3. One-hot encode categorical features using get_dummies
    encode_features = ['land_surface_condition','foundation_type','roof_type','ground_floor_type',
                        'other_floor_type','position']
    X = pd.get_dummies(X, columns=encode_features, drop_first=True)
    st.write(X.head(300))

    # Split data into train and test set
    X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=1/3, random_state=42, stratify=y)

    # 4. Normalise training data using sklearn Standard Scalar
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)    
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)

    scaler_filename = './utils/features_scaler.joblib'
    joblib.dump(scaler, scaler_filename)

    # 4. Use random forest to check importance of features
    rf_clf = RandomForestClassifier(n_estimators = 10, criterion = 'gini', random_state = 42)
    rf_clf.fit(X_train, y_train)
    
    # Plot the feature importance
    sorted_idx = rf_clf.feature_importances_.argsort()
    fig, ax = plt.subplots(figsize=(12,12))
    plt.barh(X.columns[sorted_idx], rf_clf.feature_importances_[sorted_idx])
    plt.xlabel("Random Forest Feature Importance")
    st.pyplot(plt)

    # Step 3 - Model Development and Training
    st.header("Step 3 - Model Development and Training")

    # Agenda for Model Development
    # 1. Logistic Regression (KK)
    st.subheader("Logistic Regression")


    # 2. Decision Tree (Sungmin)
    st.subheader("Decision Tree")

    # 3. Random Forest (Ensemble of Decision Tree) (Sungmin)
    # st.subheader("Random Forest")
    # y_pred = rf_clf.predict(X_test)
    # test_df = pd.DataFrame(np.stack((y_test, y_pred),axis=-1), columns=['y_test', 'y_pred'])
    # st.write(test_df.head(300))
    
    # st.text('Classification Report for Ordinal Classifier:\n ' + classification_report(y_test, y_pred))
    # st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

    # 4. AdaBoost (KK)
    st.subheader("AdaBoost")


    # 5. Ordinal Classifier: https://towardsdatascience.com/simple-trick-to-train-an-ordinal-regression-with-any-classifier-6911183d2a3c (Wei Liang)
    # import class from OrdinalClassifier.py
    st.subheader("Ordinal Classifier")
    dt = DecisionTreeClassifier()
    clf = OrdinalClassifier(dt)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    test_df = pd.DataFrame(np.stack((y_test, y_pred),axis=-1), columns=['y_test', 'y_pred'])
    st.write(test_df.head(300))

    st.text('Classification Report for Ordinal Classifier:\n ' + classification_report(y_test, y_pred))
    st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

    # Step 4 - Model Validation and Evaluation
    st.header("Step 4 - Model Validation and Evaluation")




    # Step 5 - Model Selection
    st.header("Step 5 - Model Selection")



    # Step 6 - Model Deployment
    st.header("Step 6 - Model Deployment")

