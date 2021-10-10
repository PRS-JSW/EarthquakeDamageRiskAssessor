from numpy.core.numerictypes import maximum_sctype
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, f1_score
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
    drop_columns = ['count_floors_pre_eq','legal_ownership_status','has_secondary_use']
    encode_features = ['land_surface_condition','foundation_type','roof_type','ground_floor_type','other_floor_type','position','plan_configuration']
    X = X_full.drop(drop_columns,axis = 1)

    # 1. Mean Encoding for geographic ID with smoothing 'geo_level_1_id','geo_level_2_id','geo_level_3_id'
    # Reference: https://www.geeksforgeeks.org/mean-encoding-machine-learning/, https://towardsdatascience.com/all-about-categorical-variable-encoding-305f3361fd02
    df = pd.concat([X[['geo_level_1_id','geo_level_2_id','geo_level_3_id']],y_full],axis=1)
    mean = df['damage_grade'].mean()
    geo_features = ['geo_level_1_id','geo_level_2_id','geo_level_3_id']
    for var in geo_features:
        geo_agg = df.groupby(var)['damage_grade'].agg(['count','mean'])
        counts = geo_agg['count']
        means = geo_agg['mean']
        weight = 100
        smooth = (counts * means + weight * mean) / (counts + weight)
        X[var] = X[var].map(smooth)

    # 2. One-hot encode categorical features using get_dummies
    X = pd.get_dummies(X, columns=encode_features, drop_first=True)
    st.write(X.head(300))

    # 3. Normalise the distribution for continuous variable using log
    int_variables = ["age","area_percentage","height_percentage","count_families"]
    for var in int_variables:
        X[var] = np.log(X[[var]].replace(0, 1))

    # Split data into train and test set
    X_train,X_test,y_train,y_test = train_test_split(X, y_full, test_size=1/3, random_state=42, stratify=y_full)

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
    st.subheader("Random Forest")
    y_pred = rf_clf.predict(X_test)
    test_df = pd.DataFrame(np.stack((y_test, y_pred),axis=-1), columns=['y_test', 'y_pred'])
    st.write(test_df.head(300))
    
    st.text('Classification Report for Ordinal Classifier:\n ' + classification_report(y_test, y_pred))
    st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

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

