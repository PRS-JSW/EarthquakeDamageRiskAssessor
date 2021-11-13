import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, precision_score, log_loss
import joblib, sqlite3
from collections import Counter

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

def app():
    # Get all data from database
    query = 'SELECT * FROM buildings_table'
    df = pd.read_sql(query, conn)
    df.loc[:,'district_id'] = df.loc[:,'ward_id'].astype(str).str[:2].astype(int)
    df.loc[:,'mun_id'] = df.loc[:,'ward_id'].astype(str).str[:4].astype(int)
    df.loc[:,'damage_grade'] = df.loc[:,'damage_grade'].astype(int)
    
    # Get municipality distance to epicenter
    df_distance = pd.read_sql("SELECT municipality_codes, distanceto_epicenter FROM municipality_distance_epicenter", conn)

    # Merge dataframes based on municipality codes
    df2 = pd.merge(df, df_distance, how='left', left_on='mun_id', right_on='municipality_codes')

    # Duplicate dataframe as X without building_id and number_floors
    X = df2.loc[:,~df2.columns.isin(['building_id','number_floors','municipality_codes'])].copy()

    # Normalise numerical features
    num_features = ['age_building','area_sq_ft','height_ft']
    
    for feature in num_features:
        X.loc[:,feature] = np.log(X.loc[:,feature].replace(0, 1))

    # Create target dataframe y and drop unused columns for X
    y = X.loc[:,'damage_grade'].copy()
    X = X.loc[:,~X.columns.isin(['district_id','ward_id','mun_id','plan_configuration','damage_grade','number_floors'])]

    # One-hot encode categorical features using get_dummies
    encode_features = ['land_surface_condition','foundation_type','roof_type','ground_floor_type',
                        'other_floor_type','position']
    X = pd.get_dummies(X, columns=encode_features, drop_first=True)

    # Split data into train and test set
    X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=1/3, random_state=42, stratify=y)

    # Load scaler
    scaler_filename = "model/standard_scaler.joblib"
    loaded_scaler = joblib.load(scaler_filename)

    # Normalise training data using sklearn Standard Scalar
    X_train = loaded_scaler.transform(X_train)
    X_test = loaded_scaler.transform(X_test)
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)

    # Model Peformance and Evaluation
    st.header("Model Performance and Evaluation")

    # 1. Logistic Regression
    st.subheader("Model 1 - Logistic Regression (Baseline)")
    model_filename = 'model/logreg_model.joblib'
    log_reg_model = joblib.load(model_filename)
    y_pred = log_reg_model.predict(X_test)
    st.text('Classification Report for Logistic Regression:\n ' + classification_report(y_test, y_pred))
    st.text("Precision (micro): {0}, F1 score (micro): {1}".format(str(precision_score(y_test, y_pred, average='micro').round(4)), 
                                                                               str(f1_score(y_test, y_pred, average='micro').round(4)) ))
    del log_reg_model
    
    # 2. Linear Discriminant Analysis
    st.subheader("Model 5 - Linear Discriminant Analysis")
    model_filename = 'model/lda_model.joblib'
    lda_model = joblib.load(model_filename)
    y_pred = lda_model.predict(X_test)
    st.text('Classification Report for Linear Discriminant Analysis:\n ' + classification_report(y_test, y_pred))
    st.text("Precision (micro): {0}, F1 score (micro): {1}".format(str(precision_score(y_test, y_pred, average='micro').round(4)), 
                                                                                  str(f1_score(y_test, y_pred, average='micro').round(4)) ))

    del lda_model
    
    # 3. MLP Classifier (Neural Net)
    st.subheader("Model 2 - MLP Classifier")
    # model_filename = 'model/mlpclf_model.joblib'
    # mlpclf_model = joblib.load(model_filename)
    # y_pred = mlpclf_model.predict(X_test)
    # st.text('Classification Report for MLP Classifier:\n ' + classification_report(y_test, y_pred))
    # st.text("Precision (micro): {0}, F1 score (micro): {1}".format(str(precision_score(y_test, y_pred, average='micro').round(4)), 
    #                                                                               str(f1_score(y_test, y_pred, average='micro').round(4)) ))

    # del mlpclf_model
    
    # 4. Random Forest (Ensemble of Decision Tree)
    st.subheader("Model 3 - Random Forest Classifier")
    model_filename = 'model/randomforest_model.joblib'
    rf_clf_model = joblib.load(model_filename)
    y_pred = rf_clf_model.predict(X_test)
    st.text('Classification Report for Random Forest Classifier:\n ' + classification_report(y_test, y_pred))
    st.text("Precision (micro): {0}, F1 score (micro): {1}".format(str(precision_score(y_test, y_pred, average='micro').round(4)), 
                                                                                  str(f1_score(y_test, y_pred, average='micro').round(4)) ))
    del rf_clf_model
    
    # 5. XGBoost
    st.subheader("Model 4 - XGBoost Classifier")
    model_filename = 'model/xgboost_model.joblib'
    xgb_model = joblib.load(model_filename)
    y_pred = xgb_model.predict(X_test)
    st.text('Classification Report for XGBoost Classifier:\n ' + classification_report(y_test, y_pred))
    st.text("Precision (micro): {0}, F1 score (micro): {1}".format(str(precision_score(y_test, y_pred, average='micro').round(4)), 
                                                                                  str(f1_score(y_test, y_pred, average='micro').round(4)) ))
    del xgb_model

    # 6. Ordinal Classifier
    # st.subheader("Model 7 - Ordinal Classifier")
    # model_filename = 'model/ordclf_model.joblib'
    # ordclf_model = joblib.load(model_filename)
    # y_pred = ordclf_model.predict(X_test)
    # st.text('Classification Report for Ordinal Classifier:\n ' + classification_report(y_test, y_pred))
    # st.text("Precision (micro): {0}, F1 score (micro): {1}".format(str(precision_score(y_test, y_pred, average='micro').round(4)), 
    #                                                                               str(f1_score(y_test, y_pred, average='micro').round(4)) ))
    # del ordclf_model