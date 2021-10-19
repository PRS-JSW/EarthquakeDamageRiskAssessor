import streamlit as st
import pandas as pd
import sqlite3

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

def form_callback():
    # Columns required to insert entry to database
    df_insert = pd.DataFrame(columns=['building_id','ward_id','number_floors','age_building','area_sq_ft','height_ft',
                                        'land_surface_condition','foundation_type','roof_type','ground_floor_type','other_floor_type',
                                        'position','plan_configuration','has_superstructure_adobe_mud','has_superstructure_mud_mortar_stone',
                                        'has_superstructure_stone_flag','has_superstructure_cement_mortar_stone','has_superstructure_mud_mortar_brick',
                                        'has_superstructure_cement_mortar_brick','has_superstructure_timber','has_superstructure_bamboo',
                                        'has_superstructure_rein_concrete_non_engineered','has_superstructure_rein_concrete_engineered',
                                        'has_superstructure_other'])

    # Assign values to columns
    df_insert = df_insert.append({'building_id':st.session_state.building_id,
                                    'ward_id':st.session_state.ward_id,
                                    'number_floors':st.session_state.number_floors,
                                    'age_building':st.session_state.age_building,
                                    'area_sq_ft':st.session_state.area_sq_ft,
                                    'height_ft':st.session_state.height_ft,
                                    'land_surface_condition':st.session_state.land_surface_condition,
                                    'foundation_type':st.session_state.foundation_type,
                                    'roof_type':st.session_state.roof_type,
                                    'ground_floor_type':st.session_state.ground_floor_type,
                                    'other_floor_type':st.session_state.other_floor_type,
                                    'position':st.session_state.position,
                                    'plan_configuration':st.session_state.plan_configuration,
                                    # Convert boolean to int
                                    'has_superstructure_adobe_mud':st.session_state.has_superstructure_adobe_mud*1,
                                    'has_superstructure_mud_mortar_stone':st.session_state.has_superstructure_mud_mortar_stone*1,
                                    'has_superstructure_stone_flag':st.session_state.has_superstructure_stone_flag*1,
                                    'has_superstructure_cement_mortar_stone':st.session_state.has_superstructure_cement_mortar_stone*1,
                                    'has_superstructure_mud_mortar_brick':st.session_state.has_superstructure_mud_mortar_brick*1,
                                    'has_superstructure_cement_mortar_brick':st.session_state.has_superstructure_cement_mortar_brick*1,
                                    'has_superstructure_timber':st.session_state.has_superstructure_timber*1,
                                    'has_superstructure_bamboo':st.session_state.has_superstructure_bamboo*1,
                                    'has_superstructure_rein_concrete_non_engineered':st.session_state.has_superstructure_rein_concrete_non_engineered*1,
                                    'has_superstructure_rein_concrete_engineered':st.session_state.has_superstructure_rein_concrete_engineered*1,
                                    'has_superstructure_other':st.session_state.has_superstructure_other*1
    }, ignore_index=True)

    # Insert entry to database
    df_insert.to_sql('buildings_table', conn, if_exists='append', index=False)
    st.success("New Entry Added!")

def app():
    # Get all data from database
    df_buildings = pd.read_sql('SELECT * FROM buildings_table ORDER BY building_id DESC LIMIT 1', conn)
    df_ward_id = pd.read_sql('SELECT * FROM ward_id_table', conn)
    df_land_surface_condition = pd.read_sql('SELECT * FROM land_surface_condition_table', conn)
    df_foundation_type = pd.read_sql('SELECT * FROM foundation_type_table', conn)
    df_roof_type = pd.read_sql('SELECT * FROM roof_type_table', conn)
    df_ground_floor_type = pd.read_sql('SELECT * FROM ground_floor_type_table', conn)
    df_other_floor_type = pd.read_sql('SELECT * FROM other_floor_type_table', conn)
    df_position = pd.read_sql('SELECT * FROM position_table', conn)
    df_plan_configuration = pd.read_sql('SELECT * FROM plan_configuration_table', conn)

    st.header("Add New Building Data")

    with st.form("input_form", clear_on_submit=True):
        building_id = df_buildings["building_id"][0] + 10

        # Building ID and Ward ID
        st.write("Building ID: " + str(building_id))
        st.session_state.building_id = building_id
        ward_id = st.selectbox("Ward ID: ", df_ward_id, key='ward_id')

        # Position and Plan configuration
        plan_configuration = st.selectbox("Plan Configuration of Building: ", df_plan_configuration, key='plan_configuration')
        position = st.selectbox("Position of Building: ", df_position, key='position')

        # Age of building
        age_building = st.slider("Age of building: ", 1, 1000, 1, key='age_building')

        # Create 2 columns
        col1, col2 = st.columns(2)
        
        # Number of floors and Height
        number_floors = col1.text_input("Number of floors in building: ", 1, key='number_floors')
        height_ft = col2.text_input("Height of building (in ft): ", 20, key='height_ft')

        # Area
        area_sq_ft = col1.text_input("Area of building (in sqft): ", 70, key='area_sq_ft')

        # Land surface 
        land_surface_condition = col2.selectbox("Land Surface Condition: ", df_land_surface_condition, key='land_surface_condition')

        # Foundation
        foundation_type = col1.selectbox("Type of Land Foundation: ", df_foundation_type, key='foundation_type')

        # Material used for Roof
        roof_type = col2.selectbox("Material used for Roof: ", df_roof_type, key='roof_type')

        # Material used for Ground floor and Other Floor
        ground_floor_type = col1.selectbox("Material used for Ground Floor: ", df_ground_floor_type, key='ground_floor_type')
        other_floor_type = col2.selectbox("Material used for Other Floors: ", df_other_floor_type, key='other_floor_type')

        # Material used for Superstructure
        st.write("Materials used for superstructure of the building (Select all that applies): ")
        has_superstructure_adobe_mud = st.checkbox('Adobe/Mud', key='has_superstructure_adobe_mud')
        has_superstructure_timber = st.checkbox('Timber', key='has_superstructure_timber')
        has_superstructure_bamboo = st.checkbox('Bamboo', key='has_superstructure_bamboo')
        has_superstructure_stone_flag = st.checkbox('Stone', key='has_superstructure_stone_flag')
        has_superstructure_mud_mortar_stone = st.checkbox('Mud Mortar - Stone', key='has_superstructure_mud_mortar_stone')
        has_superstructure_mud_mortar_brick = st.checkbox('Mud Mortar - Brick', key='has_superstructure_mud_mortar_brick')
        has_superstructure_cement_mortar_stone = st.checkbox('Cement Mortar - Stone', key='has_superstructure_cement_mortar_stone')
        has_superstructure_cement_mortar_brick = st.checkbox('Cement Mortar - Brick', key='has_superstructure_cement_mortar_brick')
        has_superstructure_rein_concrete_non_engineered = st.checkbox('Non-Engineered Reinforced Concrete', key='has_superstructure_rein_concrete_non_engineered')
        has_superstructure_rein_concrete_engineered = st.checkbox('Engineered Reinforced Concrete', key='has_superstructure_rein_concrete_engineered')
        has_superstructure_other = st.checkbox('Other Materials', key='has_superstructure_other')

        submit_button = st.form_submit_button("Submit", on_click=form_callback)