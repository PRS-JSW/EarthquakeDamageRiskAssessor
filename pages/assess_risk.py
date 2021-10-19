import streamlit as st
import pandas as pd
import sqlite3

# Connect to Database
conn = sqlite3.connect('data/buildingsdata.db', check_same_thread=False)

def assess_building_risk():
    st.success("Hi")

def search_building():
    # Get all data from database
    # df_ward_id = pd.read_sql('SELECT * FROM ward_id_table', conn)
    df_land_surface_condition = pd.read_sql('SELECT * FROM land_surface_condition_table', conn)
    df_foundation_type = pd.read_sql('SELECT * FROM foundation_type_table', conn)
    df_roof_type = pd.read_sql('SELECT * FROM roof_type_table', conn)
    df_ground_floor_type = pd.read_sql('SELECT * FROM ground_floor_type_table', conn)
    df_other_floor_type = pd.read_sql('SELECT * FROM other_floor_type_table', conn)
    df_position = pd.read_sql('SELECT * FROM position_table', conn)
    df_plan_configuration = pd.read_sql('SELECT * FROM plan_configuration_table', conn)

    # Get list of building ID from database
    search_building_ID = st.session_state.search_building_ID

    query = 'SELECT * FROM buildings_table where building_id=' + search_building_ID
    df_search = pd.read_sql(query, conn)

    if(len(df_search) > 0):
        with st.form("reevaluate_risk_form"):
            # Building ID and Ward ID
            st.write("Building ID: " + str(df_search["building_id"][0]))
            st.write("Ward ID: " + str(df_search["ward_id"][0]))

            # Position and Plan configuration
            plan_index = df_plan_configuration[(df_plan_configuration['plan_configuration']==df_search["plan_configuration"][0])].index[0].item()
            plan_configuration = st.selectbox("Plan Configuration of Building: ", df_plan_configuration, index=plan_index, key='plan_configuration')
            position_index = df_position[(df_position['position']==df_search["position"][0])].index[0].item()
            position = st.selectbox("Position of Building: ", df_position, index=position_index, key='position')

            # Age of building
            age_building = st.slider("Age of building: ", min_value=1, max_value=1000, step=1, value=df_search["age_building"][0].item(), key='age_building')

            # Create 2 columns
            col1, col2 = st.columns(2)

            # Number of floors and Height
            number_floors = col1.text_input("Number of floors in building: ", str(df_search["number_floors"][0]), key='number_floors')
            height_ft = col2.text_input("Height of building (in ft): ", str(df_search["height_ft"][0]), key='height_ft')

            # Area
            area_sq_ft = col1.text_input("Area of building (in sqft): ", str(df_search["area_sq_ft"][0]), key='area_sq_ft')

            # Land surface
            land_surface_condition_index = df_land_surface_condition[(df_land_surface_condition['land_surface_condition']==df_search["land_surface_condition"][0])].index[0].item()
            land_surface_condition = col2.selectbox("Land Surface Condition: ", df_land_surface_condition, index=land_surface_condition_index, key='land_surface_condition')

            # Foundation
            foundation_type_index = df_foundation_type[(df_foundation_type['foundation_type']==df_search["foundation_type"][0])].index[0].item()
            foundation_type = col1.selectbox("Type of Land Foundation: ", df_foundation_type, index=foundation_type_index, key='foundation_type')

            # Material used for Roof
            roof_type_index = df_roof_type[(df_roof_type['roof_type']==df_search["roof_type"][0])].index[0].item()
            roof_type = col2.selectbox("Material used for Roof: ", df_roof_type, index=roof_type_index, key='roof_type')

            # Material used for Ground floor and Other Floor
            ground_floor_type_index = df_ground_floor_type[(df_ground_floor_type['ground_floor_type']==df_search["ground_floor_type"][0])].index[0].item()
            ground_floor_type = col1.selectbox("Material used for Ground Floor: ", df_ground_floor_type, index=ground_floor_type_index, key='ground_floor_type')
            other_floor_type_index = df_other_floor_type[(df_other_floor_type['other_floor_type']==df_search["other_floor_type"][0])].index[0].item()
            other_floor_type = col2.selectbox("Material used for Other Floors: ", df_other_floor_type, index=other_floor_type_index, key='other_floor_type')

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

            submit_button = st.form_submit_button("Re-evaluate Building Damage", on_click=assess_building_risk)
    else:
        st.warning("No record found for building ID " + st.session_state.search_building_ID + ".")

def app():
    with st.form("search_form"):
        building_id = st.text_input("Search Building ID: ", 120101000011, key='search_building_ID')
        submit_button = st.form_submit_button("Search", on_click=search_building)