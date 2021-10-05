from numpy.core.numerictypes import maximum_sctype
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
import joblib
from .OrdinalClassifier import OrdinalClassifier

def app():
    # File Path
    TRAINFEATURES_FILE = "./data/train_values.csv"
    TRAINLABELS_FILE = "./data/train_labels.csv"
    TESTFEATURES_FILE = "./data/test_values.csv"

    # Load the Data
    X_full = pd.read_csv(TRAINFEATURES_FILE)
    y_full = pd.read_csv(TRAINLABELS_FILE)
    X_full.set_index(["building_id"], inplace=True)
    y_full.set_index(["building_id"], inplace=True)

    # Step 2 - Feature Selection and Engineering
    st.header("Feature Selection and Engineering")
    drop_columns = ['geo_level_1_id','geo_level_2_id','count_floors_pre_eq','legal_ownership_status','has_secondary_use']
    encode_features = ['land_surface_condition','foundation_type','roof_type','ground_floor_type','other_floor_type','position','plan_configuration', \
                        'has_superstructure_adobe_mud','has_superstructure_mud_mortar_stone','has_superstructure_stone_flag','has_superstructure_cement_mortar_stone', \
                        'has_superstructure_mud_mortar_brick','has_superstructure_cement_mortar_brick','has_superstructure_timber','has_superstructure_bamboo', \
                        'has_superstructure_rc_non_engineered','has_superstructure_rc_engineered','has_superstructure_other','has_secondary_use_agriculture', \
                        'has_secondary_use_hotel','has_secondary_use_rental','has_secondary_use_institution','has_secondary_use_school','has_secondary_use_industry', \
                        'has_secondary_use_health_post','has_secondary_use_gov_office','has_secondary_use_use_police','has_secondary_use_other']
    X = X_full.drop(drop_columns,axis = 1)
    # 1. One-hot encode categorical features using get_dummies
    X = pd.get_dummies(X, columns=encode_features, drop_first=True)
    st.write(X.head(300))

    # 2. Inspect distribution of target variable
    st.markdown("""
    Value Counts of Damage Grade
    """)
    st.write(y_full.value_counts())

    st.markdown("""
    One-hot encode categorical features using get_dummies and inspect distribution of target variable.
    """)

    # Split data into train and test set
    X_train,X_test,y_train,y_test = train_test_split(X, y_full, test_size=1/3, random_state=42, stratify=y_full)

    # 3. Normalise training data using sklearn Standard Scalar
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    scaler_filename = './utils/features_scaler.joblib'
    joblib.dump(scaler, scaler_filename)

    # 4. Use random forest to check importance of features
    model = RandomForestClassifier(n_estimators = 10, criterion = 'gini', random_state = 42)
    model.fit(X_train, np.ravel(y_train))

    # Plot the feature importance
    sorted_idx = model.feature_importances_.argsort()
    fig, ax = plt.subplots(figsize=(12,12))
    plt.barh(X.columns[sorted_idx], model.feature_importances_[sorted_idx])
    plt.xlabel("Random Forest Feature Importance")
    st.pyplot(plt)

    # Step 3 - Model Development and Training
    st.header("Step 3 - Model Development and Training")

    # Agenda for Model Development
    # 1. Logistic Regression (KK)


    # 2. Decision Tree (Sungmin)
    # 3. Random Forest (Ensemble of Decision Tree) (Sungmin)
    # 4. AdaBoost (KK)


    # 5. Ordinal Classifier: https://towardsdatascience.com/simple-trick-to-train-an-ordinal-regression-with-any-classifier-6911183d2a3c (Wei Liang)
    # import class from OrdinalClassifier.py
    st.subheader("Ordinal Classifier (Credit: Muhammad)")
    clf = OrdinalClassifier(DecisionTreeClassifier(max_depth=3))
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    st.markdown("""
    Micro-Averaged F1 Score:
    """)
    st.write(f1_score(y_test, y_pred, average='micro'))

    # Step 4 - Model Validation and Evaluation
    st.header("Step 4 - Model Validation and Evaluation")




    # Step 5 - Model Selection
    st.header("Step 5 - Model Selection")



    # Step 6 - Model Deployment
    st.header("Step 6 - Model Deployment")

