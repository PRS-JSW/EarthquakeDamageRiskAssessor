from numpy.core.fromnumeric import shape
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3, joblib, json

def app():
    # Initialize session state of reevaluate_building_risk
    if 'retrain_model_sel' not in st.session_state:
        st.session_state['reevaluate_building_risk'] = False

    def evaluate_building_risk():
        # Connect to Database
        conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

        # Get all data from database
        df_land_surface_condition = pd.read_sql('SELECT * FROM land_surface_condition_table', conn)
        df_foundation_type = pd.read_sql('SELECT * FROM foundation_type_table', conn)
        df_roof_type = pd.read_sql('SELECT * FROM roof_type_table', conn)
        df_ground_floor_type = pd.read_sql('SELECT * FROM ground_floor_type_table', conn)
        df_other_floor_type = pd.read_sql('SELECT * FROM other_floor_type_table', conn)
        df_position = pd.read_sql('SELECT * FROM position_table', conn)
        df_distance = pd.read_sql("SELECT municipality_codes, distanceto_epicenter FROM municipality_distance_epicenter", conn)

        # Get list of building ID from database
        search_building_ID = st.session_state.search_building_ID

        query = 'SELECT * FROM buildings_table where building_id=' + search_building_ID
        df_search = pd.read_sql(query, conn)

        if(len(df_search) > 0):
            st.header("Assess Damage Risk of Existing Building")

            col1, col2 = st.columns(2)

            with col1:
                with st.form("reevaluate_risk_form", clear_on_submit=True):
                    st.markdown("#### Current Building Configuration")

                    # Building ID and Ward ID
                    st.write("Building ID: " + str(df_search["building_id"][0]))
                    st.write("Ward ID: " + str(df_search["ward_id"][0]))
                    current_damage_grade = df_search["damage_grade"][0]

                    # Position
                    position_index = df_position[(df_position['position']==df_search["position"][0])].index[0].item()
                    position = st.selectbox("Position of Building: ", df_position, index=position_index, key='position')

                    # Age of building
                    age_building = st.slider("Age of building: ", min_value=1, max_value=1000, step=1, value=df_search["age_building"][0].item(), key='age_building')

                    # Height
                    height_ft = st.text_input("Height of building (in ft): ", str(df_search["height_ft"][0]), key='height_ft')

                    # Area
                    area_sq_ft = st.text_input("Area of building (in sqft): ", str(df_search["area_sq_ft"][0]), key='area_sq_ft')

                    # Land surface
                    land_surface_condition_index = df_land_surface_condition[(df_land_surface_condition['land_surface_condition']==df_search["land_surface_condition"][0])].index[0].item()
                    land_surface_condition = st.selectbox("Land Surface Condition: ", df_land_surface_condition, index=land_surface_condition_index, key='land_surface_condition')

                    # Foundation
                    foundation_type_index = df_foundation_type[(df_foundation_type['foundation_type']==df_search["foundation_type"][0])].index[0].item()
                    foundation_type = st.selectbox("Type of Land Foundation: ", df_foundation_type, index=foundation_type_index, key='foundation_type')

                    # Material used for Roof
                    roof_type_index = df_roof_type[(df_roof_type['roof_type']==df_search["roof_type"][0])].index[0].item()
                    roof_type = st.selectbox("Material used for Roof: ", df_roof_type, index=roof_type_index, key='roof_type')

                    # Material used for Ground floor and Other Floor
                    ground_floor_type_index = df_ground_floor_type[(df_ground_floor_type['ground_floor_type']==df_search["ground_floor_type"][0])].index[0].item()
                    ground_floor_type = st.selectbox("Material used for Ground Floor: ", df_ground_floor_type, index=ground_floor_type_index, key='ground_floor_type')
                    other_floor_type_index = df_other_floor_type[(df_other_floor_type['other_floor_type']==df_search["other_floor_type"][0])].index[0].item()
                    other_floor_type = st.selectbox("Material used for Other Floors: ", df_other_floor_type, index=other_floor_type_index, key='other_floor_type')

                    # Material used for Superstructure
                    st.write("Materials used for superstructure of the building (Select all that applies): ")
                    has_superstructure_adobe_mud = st.checkbox('Adobe/Mud', key='has_superstructure_adobe_mud', value=df_search["has_superstructure_adobe_mud"][0].item())
                    has_superstructure_timber = st.checkbox('Timber', key='has_superstructure_timber', value=df_search["has_superstructure_timber"][0].item())
                    has_superstructure_bamboo = st.checkbox('Bamboo', key='has_superstructure_bamboo', value=df_search["has_superstructure_bamboo"][0].item())
                    has_superstructure_stone_flag = st.checkbox('Stone', key='has_superstructure_stone_flag', value=df_search["has_superstructure_stone_flag"][0].item())
                    has_superstructure_mud_mortar_stone = st.checkbox('Mud Mortar - Stone', key='has_superstructure_mud_mortar_stone', value=df_search["has_superstructure_mud_mortar_stone"][0].item())
                    has_superstructure_mud_mortar_brick = st.checkbox('Mud Mortar - Brick', key='has_superstructure_mud_mortar_brick', value=df_search["has_superstructure_mud_mortar_brick"][0].item())
                    has_superstructure_cement_mortar_stone = st.checkbox('Cement Mortar - Stone', key='has_superstructure_cement_mortar_stone', value=df_search["has_superstructure_cement_mortar_stone"][0].item())
                    has_superstructure_cement_mortar_brick = st.checkbox('Cement Mortar - Brick', key='has_superstructure_cement_mortar_brick', value=df_search["has_superstructure_cement_mortar_brick"][0].item())
                    has_superstructure_rein_concrete_non_engineered = st.checkbox('Non-Engineered Reinforced Concrete', key='has_superstructure_rein_concrete_non_engineered', value=df_search["has_superstructure_rein_concrete_non_engineered"][0].item())
                    has_superstructure_rein_concrete_engineered = st.checkbox('Engineered Reinforced Concrete', key='has_superstructure_rein_concrete_engineered', value=df_search["has_superstructure_rein_concrete_engineered"][0].item())
                    has_superstructure_other = st.checkbox('Other Materials', key='has_superstructure_other', value=df_search["has_superstructure_other"][0].item())

                    # Call reevaluate_building_risk function to set session state of reevaluate_building_risk to True
                    submit_button = st.form_submit_button("Assess Existing Building Damage Risk", on_click=reevaluate_building_risk)

            with col2:
                with st.container():
                    # Check to see if session state of reevaluate_building_risk is set to True
                    if st.session_state['reevaluate_building_risk']:

                        # Load prediction model
                        model_filename = "model/xgboost_model.joblib"
                        loaded_model = joblib.load(model_filename)
                        scaler_filename = "model/standard_scaler.joblib"
                        loaded_scaler = joblib.load(scaler_filename)
                        # district_ID_map = json.load(open( "model/district_id_map.json"))
                        # ward_id_map = json.load(open( "model/ward_id_map.json"))
                        # mun_id_map = json.load(open( "model/mun_id_map.json"))

                        ward_id = int(df_search["ward_id"][0])
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

                        st.write("")
                        st.markdown("#### New Building Configuration")

                        # Building ID and Ward ID
                        st.markdown("Building ID: " + str(df_search["building_id"][0]) + "  \n")
                        st.markdown("Ward ID: " + str(df_search["ward_id"][0]) + "  \n")

                        # Position
                        position_index = df_position[(df_position['position']==st.session_state.position)].index[0].item()
                        position = st.selectbox("Position of Building: ", df_position, index=position_index)

                        # Age of building
                        age_building = st.slider("Age of building: ", min_value=1, max_value=1000, step=1, value=st.session_state.age_building)

                        # Height
                        height_ft = st.text_input("Height of building (in ft): ", st.session_state.height_ft)

                        # Area
                        area_sq_ft = st.text_input("Area of building (in sqft): ", st.session_state.area_sq_ft)

                        # Land surface
                        land_surface_condition_index = df_land_surface_condition[(df_land_surface_condition['land_surface_condition']==st.session_state.land_surface_condition)].index[0].item()
                        land_surface_condition = st.selectbox("Land Surface Condition: ", df_land_surface_condition, index=land_surface_condition_index)

                        # Foundation
                        foundation_type_index = df_foundation_type[(df_foundation_type['foundation_type']==st.session_state.foundation_type)].index[0].item()
                        foundation_type = st.selectbox("Type of Land Foundation: ", df_foundation_type, index=foundation_type_index)

                        # Material used for Roof
                        roof_type_index = df_roof_type[(df_roof_type['roof_type']==st.session_state.roof_type)].index[0].item()
                        roof_type = st.selectbox("Material used for Roof: ", df_roof_type, index=roof_type_index)

                        # Material used for Ground floor and Other Floor
                        ground_floor_type_index = df_ground_floor_type[(df_ground_floor_type['ground_floor_type']==st.session_state.ground_floor_type)].index[0].item()
                        ground_floor_type = st.selectbox("Material used for Ground Floor: ", df_ground_floor_type, index=ground_floor_type_index)
                        other_floor_type_index = df_other_floor_type[(df_other_floor_type['other_floor_type']==st.session_state.other_floor_type)].index[0].item()
                        other_floor_type = st.selectbox("Material used for Other Floors: ", df_other_floor_type, index=other_floor_type_index)

                        # Material used for Superstructure
                        st.write("Materials used for superstructure of the building: ")
                        has_superstructure_adobe_mud = st.checkbox('Adobe/Mud', value=st.session_state.has_superstructure_adobe_mud)
                        has_superstructure_timber = st.checkbox('Timber', value=st.session_state.has_superstructure_timber)
                        has_superstructure_bamboo = st.checkbox('Bamboo', value=st.session_state.has_superstructure_bamboo)
                        has_superstructure_stone_flag = st.checkbox('Stone', value=st.session_state.has_superstructure_stone_flag)
                        has_superstructure_mud_mortar_stone = st.checkbox('Mud Mortar - Stone', value=st.session_state.has_superstructure_mud_mortar_stone)
                        has_superstructure_mud_mortar_brick = st.checkbox('Mud Mortar - Brick', value=st.session_state.has_superstructure_mud_mortar_brick)
                        has_superstructure_cement_mortar_stone = st.checkbox('Cement Mortar - Stone', value=st.session_state.has_superstructure_cement_mortar_stone)
                        has_superstructure_cement_mortar_brick = st.checkbox('Cement Mortar - Brick', value=st.session_state.has_superstructure_cement_mortar_brick)
                        has_superstructure_rein_concrete_non_engineered = st.checkbox('Non-Engineered Reinforced Concrete', value=st.session_state.has_superstructure_rein_concrete_non_engineered)
                        has_superstructure_rein_concrete_engineered = st.checkbox('Engineered Reinforced Concrete', value=st.session_state.has_superstructure_rein_concrete_engineered)
                        has_superstructure_other = st.checkbox('Other Materials', value=st.session_state.has_superstructure_other)

                        # Predicted Damage to New Building Configuration
                        # Message for damage to building
                        if (dmg_grade == 0):
                            grade_text = " (Minor repair required)"
                        if (dmg_grade == 1):
                            grade_text = " (Major repair required)"
                        if (dmg_grade == 2):
                            grade_text = " (Total reconstruction required)"
                        # Up or down, comments of damage grade
                        if (dmg_grade > int(current_damage_grade)):
                            st.markdown("** Assessed Damage Risk of Existing Building: " + str(dmg_grade) + "**" + " :arrow_up:" + grade_text)
                        if (dmg_grade < int(current_damage_grade)):
                            st.markdown("** Assessed Damage Risk of Existing Building: " + str(dmg_grade) + "**" + " :arrow_down:" + grade_text)
                        if (dmg_grade == int(current_damage_grade)):
                            st.markdown("** Assessed Damage Risk of Existing Building: " + str(dmg_grade) + "**" + grade_text)

        else:
            st.warning("No record found for building ID " + st.session_state.search_building_ID + ".")

    def reevaluate_building_risk():
        # Set session state of reevaluate_building_risk to True
        st.session_state['reevaluate_building_risk'] = True

        # Call evaluate_building_risk function
        evaluate_building_risk()

    with st.form("search_form"):
        st.header("Retrieve Existing Building Record")

        building_id = st.text_input("Search Building ID: ", 120101000011, key='search_building_ID')

        # Call evaluate_building_risk function
        submit_button = st.form_submit_button("Search", on_click=evaluate_building_risk)