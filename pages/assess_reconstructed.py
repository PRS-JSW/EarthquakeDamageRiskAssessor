import streamlit as st
import pandas as pd
import numpy as np
import sqlite3, joblib

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

# Evaluate new building structure for damage grade risk
def app():

    # Get all data from database
    df_ward_id = pd.read_sql('SELECT * FROM ward_id_table', conn)
    df_land_surface_condition = pd.read_sql('SELECT * FROM land_surface_condition_table', conn)
    df_foundation_type = pd.read_sql('SELECT * FROM foundation_type_table', conn)
    df_roof_type = pd.read_sql('SELECT * FROM roof_type_table', conn)
    df_ground_floor_type = pd.read_sql('SELECT * FROM ground_floor_type_table', conn)
    df_other_floor_type = pd.read_sql('SELECT * FROM other_floor_type_table', conn)
    df_position = pd.read_sql('SELECT * FROM position_table', conn)
    df_distance = pd.read_sql("SELECT municipality_codes, distanceto_epicenter FROM municipality_distance_epicenter", conn)

    def check_risk():
        # Load prediction model
        model_filename = "model/xgboost_model.joblib"
        loaded_model = joblib.load(model_filename)
        scaler_filename = "model/standard_scaler.joblib"
        loaded_scaler = joblib.load(scaler_filename)
        # district_ID_map = json.load(open( "model/district_id_map.json"))
        # ward_id_map = json.load(open( "model/ward_id_map.json"))
        # mun_id_map = json.load(open( "model/mun_id_map.json"))

        ward_id = int(st.session_state.ward_id)
        # district_id = int(str(ward_id)[:2])
        mun_id = int(str(ward_id)[:4])

        # Normalise numerical features
        age_building = np.log(int(str(st.session_state.age_building).replace("0", "1")))
        area_sq_ft = np.log(int(str(st.session_state.area_sq_ft).replace("0", "1")))
        height_ft = np.log(int(str(st.session_state.height_ft).replace("0", "1")))

        # Target mean encoding for district_id, ward_id, mun_id
        # district_id_weighted_mean = district_ID_map.get(str(district_id))
        # ward_id_weighted_mean = ward_id_map.get(str(ward_id))
        # mun_id_weighted_mean = mun_id_map.get(str(mun_id))
        distanceto_epicenter = df_distance.loc[(df_distance["municipality_codes"] == mun_id), "distanceto_epicenter"].values[0]

        # Get values of building structure
        has_superstructure_adobe_mud = st.session_state.has_superstructure_adobe_mud*1
        has_superstructure_mud_mortar_stone = st.session_state.has_superstructure_mud_mortar_stone*1
        has_superstructure_stone_flag = st.session_state.has_superstructure_stone_flag*1
        has_superstructure_cement_mortar_stone = st.session_state.has_superstructure_cement_mortar_stone*1
        has_superstructure_mud_mortar_brick = st.session_state.has_superstructure_mud_mortar_brick*1
        has_superstructure_cement_mortar_brick = st.session_state.has_superstructure_cement_mortar_brick*1
        has_superstructure_timber = st.session_state.has_superstructure_timber*1
        has_superstructure_bamboo = st.session_state.has_superstructure_bamboo*1
        has_superstructure_rein_concrete_non_engineered = st.session_state.has_superstructure_rein_concrete_non_engineered*1
        has_superstructure_rein_concrete_engineered = st.session_state.has_superstructure_rein_concrete_engineered*1
        has_superstructure_other = st.session_state.has_superstructure_other*1
        land_surface_Moderate_slope = 1 if (st.session_state.land_surface_condition == 'Moderate slope') else 0
        land_surface_Steep_slope = 1 if (st.session_state.land_surface_condition == 'Steep slope') else 0
        foundation_type_CementStone_Brick = 1 if (st.session_state.foundation_type == 'Cement-Stone/Brick') else 0
        foundation_type_MudmortarStone_Brick = 1 if (st.session_state.foundation_type == 'Mud mortar-Stone/Brick') else 0
        foundation_type_Other = 1 if (st.session_state.foundation_type == 'Other') else 0
        foundation_type_Reinforcedconcrete = 1 if (st.session_state.foundation_type == 'Reinforced concrete') else 0
        roof_type_Bamboo_TimberLight = 1 if (st.session_state.roof_type == 'Bamboo/Timber-Light roof') else 0
        roof_type_ReinforcedCementConcrete_ReinforcedBrick_ReinforcedBrickConcrete = 1 if (st.session_state.roof_type == 'Reinforced Cement Concrete/Reinforced Brick/Reinforced Brick Concrete') else 0
        ground_floor_type_Mud = 1 if (st.session_state.ground_floor_type == 'Mud') else 0
        ground_floor_type_Other = 1 if (st.session_state.ground_floor_type == 'Other') else 0
        ground_floor_type_Reinforcedconcrete = 1 if (st.session_state.ground_floor_type == 'Reinforced concrete') else 0
        ground_floor_type_Timber = 1 if (st.session_state.ground_floor_type == 'Timber') else 0
        other_floor_type_ReinforcedCementConcrete_ReinforcedBrick_ReinforcedBrickConcrete = 1 if (st.session_state.other_floor_type == 'Reinforced Cement Concrete/Reinforced Brick/Reinforced Brick Concrete') else 0
        other_floor_type_TimberPlank = 1 if (st.session_state.other_floor_type == 'Timber-Plank') else 0
        other_floor_type_Timber_BambooMud = 1 if (st.session_state.other_floor_type == 'Timber/Bamboo-Mud') else 0
        position_Attached2side = 1 if (st.session_state.position == 'Attached-2 side') else 0
        position_Attached3side = 1 if (st.session_state.position == 'Attached-3 side') else 0
        position_Notattached = 1 if (st.session_state.position == 'Not attached') else 0

        # Make into list
        df_predict = [[age_building,area_sq_ft,height_ft,has_superstructure_adobe_mud,has_superstructure_mud_mortar_stone,has_superstructure_stone_flag,
                        has_superstructure_cement_mortar_stone,has_superstructure_mud_mortar_brick,has_superstructure_cement_mortar_brick,
                        has_superstructure_timber,has_superstructure_bamboo,has_superstructure_rein_concrete_non_engineered,has_superstructure_rein_concrete_engineered,
                        has_superstructure_other,distanceto_epicenter,land_surface_Moderate_slope,land_surface_Steep_slope,
                        foundation_type_CementStone_Brick,foundation_type_MudmortarStone_Brick,foundation_type_Other,foundation_type_Reinforcedconcrete,
                        roof_type_Bamboo_TimberLight,roof_type_ReinforcedCementConcrete_ReinforcedBrick_ReinforcedBrickConcrete,ground_floor_type_Mud,
                        ground_floor_type_Other,ground_floor_type_Reinforcedconcrete,ground_floor_type_Timber,other_floor_type_ReinforcedCementConcrete_ReinforcedBrick_ReinforcedBrickConcrete,
                        other_floor_type_TimberPlank,other_floor_type_Timber_BambooMud,position_Attached2side,position_Attached3side,position_Notattached]]

        # Use saved scaler to rescale data
        df_predict = loaded_scaler.transform(df_predict)

        # Use model to predict damage grade
        dmg_grade = loaded_model.predict(df_predict)[0]

        if (dmg_grade == 0):
            grade_text = " (Minor repair required)"
        if (dmg_grade == 1):
            grade_text = " (Major repair required)"
        if (dmg_grade == 2):
            grade_text = " (Total reconstruction required)"
        st.info("Assessed Damage Risk of Reconstructed Building: " + str(dmg_grade) + grade_text + ".")

    st.header("Assess Damage Risk of Reconstructed Building")

    with st.form("input_form"):
        # Ward ID
        ward_id = st.selectbox("Ward ID: ", df_ward_id, key='ward_id')

        # Position and Plan configuration
        position = st.selectbox("Position of Building: ", df_position, key='position')

        # Age of building
        age_building = st.slider("Age of building: ", 1, 1000, 1, key='age_building')

        # Create 2 columns
        col1, col2 = st.columns(2)
        
        # Number of floors and Height
        height_ft = col1.text_input("Height of building (in ft): ", 20, key='height_ft')

        # Area
        area_sq_ft = col2.text_input("Area of building (in sqft): ", 70, key='area_sq_ft')

        # Land surface and foundation
        land_surface_condition = col1.selectbox("Land Surface Condition: ", df_land_surface_condition, key='land_surface_condition')
        foundation_type = col2.selectbox("Type of Land Foundation: ", df_foundation_type, key='foundation_type')

        # Material used for Ground floor and Other Floor
        ground_floor_type = col2.selectbox("Material used for Ground Floor: ", df_ground_floor_type, key='ground_floor_type')
        other_floor_type = col1.selectbox("Material used for Other Floors: ", df_other_floor_type, key='other_floor_type')

        # Material used for Roof
        roof_type = col1.selectbox("Material used for Roof: ", df_roof_type, key='roof_type')

        # Material used for Superstructure
        st.write("Materials used for superstructure of the building (Select all that applies): ")
        col21, col22, col23 = st.columns(3)

        has_superstructure_adobe_mud = col21.checkbox('Adobe/Mud', key='has_superstructure_adobe_mud')
        has_superstructure_timber = col22.checkbox('Timber', key='has_superstructure_timber')
        has_superstructure_bamboo = col23.checkbox('Bamboo', key='has_superstructure_bamboo')
        has_superstructure_stone_flag = col21.checkbox('Stone', key='has_superstructure_stone_flag')
        has_superstructure_mud_mortar_stone = col22.checkbox('Mud Mortar - Stone', key='has_superstructure_mud_mortar_stone')
        has_superstructure_mud_mortar_brick = col23.checkbox('Mud Mortar - Brick', key='has_superstructure_mud_mortar_brick')
        has_superstructure_cement_mortar_stone = col21.checkbox('Cement Mortar - Stone', key='has_superstructure_cement_mortar_stone')
        has_superstructure_cement_mortar_brick = col22.checkbox('Cement Mortar - Brick', key='has_superstructure_cement_mortar_brick')
        has_superstructure_rein_concrete_non_engineered = col23.checkbox('Non-Engineered Reinforced Concrete', key='has_superstructure_rein_concrete_non_engineered')
        has_superstructure_rein_concrete_engineered = col21.checkbox('Engineered Reinforced Concrete', key='has_superstructure_rein_concrete_engineered')
        has_superstructure_other = col22.checkbox('Other Materials', key='has_superstructure_other')

        submit_button = st.form_submit_button("Submit", on_click=check_risk)