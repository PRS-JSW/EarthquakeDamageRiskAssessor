import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from haversine import haversine, Unit

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

def app():
    df_municipality = pd.read_sql("SELECT * FROM municipality_distance_epicenter ORDER BY municipality", conn)
    # st.dataframe(df_municipality)

    def update_distance():

        if st.session_state['epicenter_loc']=="Nepal 2015 Earthquake":

            for i in range(len(df_municipality)):
                epicenter_lat = df_municipality2.loc[(df_municipality2['municipality']=='Nepal 2015 Earthquake'),'latitude'].values[0]
                epicenter_long = df_municipality2.loc[(df_municipality2['municipality']=='Nepal 2015 Earthquake'),'longitude'].values[0]
                epicenter_loc = (epicenter_lat, epicenter_long)

                distance = haversine(epicenter_loc, (df_municipality.loc[i,'latitude'], df_municipality.loc[i,'longitude']))
                df_municipality.loc[i,'distanceto_epicenter'] = round(distance, 4)

        if st.session_state['epicenter_loc']!="Nepal 2015 Earthquake":
            
            epicenter_lat = df_municipality2.loc[(df_municipality2['municipality']==st.session_state['epicenter_loc']),'latitude'].values[0]
            epicenter_long = df_municipality2.loc[(df_municipality2['municipality']==st.session_state['epicenter_loc']),'longitude'].values[0]
            epicenter_loc = (epicenter_lat, epicenter_long)

            for i in range(len(df_municipality)):
                distance = haversine(epicenter_loc, (df_municipality.loc[i,'latitude'], df_municipality.loc[i,'longitude']))
                df_municipality.loc[i,'distanceto_epicenter'] = round(distance, 4)

        # Update distance to epicenter in database
        # st.dataframe(df_municipality)
        df_municipality.to_sql('municipality_distance_epicenter', conn, if_exists='replace', index=False)

        st.success('Distance to epicentre updated successfully.')

    st.header("Update Location of Epicentre")
    
    with st.form("update_epicenter"):
        nepal_epicenter = {'municipality':'Nepal 2015 Earthquake', 'latitude':28.23, 'longitude':84.731, 'distanceto_epicenter':0}
        df_municipality2 = df_municipality.append(nepal_epicenter, ignore_index=True).copy()
        df_municipality_list = df_municipality2.loc[:,'municipality']

        # index=position_index,
        epicenter_location = st.selectbox("Location of New Epicentre (Nearest Municipality): ", df_municipality_list, index=112, key='epicenter_loc')

        submit_button = st.form_submit_button("Submit", on_click=update_distance)