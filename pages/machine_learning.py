# from numpy.core.numerictypes import maximum_sctype
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from .OrdinalClassifier import OrdinalClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, f1_score
import joblib, sqlite3

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

def app():
    # Default session state of retrain_model_sel set to None
    if 'retrain_model_sel' not in st.session_state:
        st.session_state['retrain_model_sel'] = 'No'

    def retrain_model():
        #Check if user wants to update models
        if (st.session_state['retrain_model_sel']=='Yes'):
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

            # Feature Selection and Engineering
            st.header("Feature Selection and Engineering")

            # Normalise numerical features
            num_features = ['age_building','area_sq_ft','height_ft']
            
            for feature in num_features:
                X.loc[:,feature] = np.log(X.loc[:,feature].replace(0, 1))

            # Mean Encode Geographic Feature
            # geo_features = ['district_id','mun_id','ward_id']

            # Mean of damage grade
            # mean = X.loc[:,'damage_grade'].mean()

            # for var in geo_features:
            #     geo_agg = X.groupby(var)['damage_grade'].agg(['count','mean'])
            #     counts = geo_agg['count']
            #     means = geo_agg['mean']
            #     weight = 100
            #     # Compute the "smoothed" means
            #     smooth = (counts * means + weight * mean) / (counts + weight)
            #     X.loc[:,var+'_weighted_mean'] = X.loc[:,var].map(smooth)
            #     # Save the target mean encoding as dictionary in json file
            #     json.dump(smooth.to_dict(), open("model/"+str(var)+"_map.json", 'w'))

            # Create target dataframe y and drop unused columns for X
            y = X.loc[:,'damage_grade'].copy()
            X = X.loc[:,~X.columns.isin(['district_id','ward_id','mun_id','plan_configuration','damage_grade','number_floors'])]

            # One-hot encode categorical features using get_dummies
            encode_features = ['land_surface_condition','foundation_type','roof_type','ground_floor_type',
                                'other_floor_type','position']
            X = pd.get_dummies(X, columns=encode_features, drop_first=True)
            st.write(X.head(300))

            # Split data into train and test set
            X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=1/3, random_state=42, stratify=y)

            # Normalise training data using sklearn Standard Scalar
            scaler = StandardScaler().fit(X_train)
            X_train = scaler.transform(X_train)
            X_test = scaler.transform(X_test)
            y_train = np.ravel(y_train)
            y_test = np.ravel(y_test)

            scaler_filename = 'model/standard_scaler.joblib'
            joblib.dump(scaler, scaler_filename)

            # Use random forest to check importance of features
            rf_clf = RandomForestClassifier(n_estimators = 100, max_depth = 30, criterion = 'gini', random_state = 42)
            rf_clf_model = rf_clf.fit(X_train, y_train)

            # Plot the feature importance
            sorted_idx = rf_clf.feature_importances_.argsort()
            fig, ax = plt.subplots(figsize=(12,12))
            plt.barh(X.columns[sorted_idx], rf_clf.feature_importances_[sorted_idx])
            plt.xlabel("Random Forest Feature Importance")
            st.pyplot(plt)

            # Model Development and Training
            st.header("Model Development and Training")

            # 1. Logistic Regression (KK)
            st.subheader("Model 1 - Logistic Regression (Baseline)")
            log_reg = LogisticRegression(random_state=42, solver='lbfgs', max_iter=100)
            log_reg_model = log_reg.fit(X_train, y_train)
            y_pred = log_reg_model.predict(X_test)
            st.text('Classification Report for Logistic Regression:\n ' + classification_report(y_test, y_pred))
            st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

            # Save model
            model_filename = 'model/logreg_model.joblib'
            joblib.dump(log_reg_model, model_filename)

            del log_reg_model

            # 2. Linear Discriminant Analysis (WL)
            st.subheader("Model 5 - Linear Discriminant Analysis")
            model_lda = LinearDiscriminantAnalysis(solver='svd')
            # grid_param = {"solver": ["svd", "lsqr", "eigen"], "tol" : [0.0001,0.0002,0.0003]}
            # grid_LDA = GridSearchCV(model_lda, param_grid=grid_param, scoring="f1_micro", cv=5, n_jobs=-1, verbose = 3)
            # grid_LDA.fit(X_train, y_train)
            # st.write("Best parameters:", grid_LDA.best_params_)
            lda_model = model_lda.fit(X_train, y_train)
            y_pred = lda_model.predict(X_test)
            # test_df = pd.DataFrame(np.stack((y_test, y_pred),axis=-1), columns=['y_test', 'y_pred'])
            # st.write(test_df.head(300))
            st.text('Classification Report for Linear Discriminant Analysis:\n ' + classification_report(y_test, y_pred))
            st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

            # Save model
            model_filename = 'model/lda_model.joblib'
            joblib.dump(lda_model, model_filename)

            del lda_model

            # 3. MLP Classifier (Sungmin)
            st.subheader("Model 2 - MLP Classifier")

            # mlp_clf = MLPClassifier(hidden_layer_sizes=(10, 30, 3), max_iter=150)
            # mlpclf_model = mlp_clf.fit(X_train, y_train)
            # y_pred = mlpclf_model.predict(X_test)
            # st.text('Classification Report for MLP Classifier:\n ' + classification_report(y_test, y_pred))
            # st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

            # Save model
            # model_filename = 'model/mlpclf_model.joblib'
            # joblib.dump(mlpclf_model, model_filename)

            # del mlpclf_model

            # 4. Random Forest (Ensemble of Decision Tree) (Sungmin)
            st.subheader("Model 3 - Random Forest Classifier")
            y_pred = rf_clf_model.predict(X_test)
            st.text('Classification Report for Random Forest Classifier:\n ' + classification_report(y_test, y_pred))
            st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

            # Save model
            model_filename = 'model/randomforest_model.joblib'
            joblib.dump(rf_clf_model, model_filename, compress=9)

            del rf_clf_model

            # 5. XGBoost (KK)
            st.subheader("Model 4 - XGBoost Classifier")
            xgb_clf = XGBClassifier(max_depth=7, objective=['multi:softmax', 'eval_metric:merror'], use_label_encoder=False, n_estimators=100)
            xgb_model = xgb_clf.fit(X_train, y_train)
            y_pred = xgb_model.predict(X_test)
            st.text('Classification Report for XGBoost Classifier:\n ' + classification_report(y_test, y_pred))
            st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

            # Save model
            model_filename = 'model/xgboost_model.joblib'
            joblib.dump(xgb_model, model_filename)

            del xgb_model

            # 6. Ordinal Classifier: https://towardsdatascience.com/simple-trick-to-train-an-ordinal-regression-with-any-classifier-6911183d2a3c (Wei Liang)
            #import class from OrdinalClassifier.py
            st.subheader("Ordinal Classifier")
            dt = DecisionTreeClassifier()
            clf = OrdinalClassifier(dt)
            ordclf_model = clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)

            st.text('Classification Report for Ordinal Classifier:\n ' + classification_report(y_test, y_pred))
            st.text("Micro-Averaged F1 Score: " + str(f1_score(y_test, y_pred, average='micro')))

            # Save model
            model_filename = 'model/ordclf_model.joblib'
            joblib.dump(ordclf_model, model_filename)

            del ordclf_model
            
            st.info('Retraining of the models completed.')

        if (st.session_state['retrain_model_sel']=='No'):
            st.info('Models are not retrained.')


    with st.form("update_model"):
        st.header("Retrain Models")

        model_update = st.selectbox("Do you want to retrain the models?", options=('No', 'Yes'), key='retrain_model_sel')

        # Call evaluate_building_risk function
        submit_button = st.form_submit_button("Retrain", on_click=retrain_model)