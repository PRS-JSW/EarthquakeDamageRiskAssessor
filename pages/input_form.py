import streamlit as st
import pandas as pd

def app():
    # File Path
    data = "./data/csv_building_structure.csv"

    # Load the Data
    df = pd.read_csv(data)

    st.header("Add New Entry")

    with st.form("input_form"):
        building_id = df["building_id"].max() + 10
        st.write("Building ID: " + str(building_id))
        

        ward_id = st.selectbox("Ward ID: ", df["ward_id"].sort_values().unique())

        count_floors_pre_eq = st.text_input("Number of floors in building: ", 1)
        age_building = st.slider("Age of building: ", 1, 1000, 1)
        plinth_area_sq_ft = st.text_input("Area of building(in sqft): ", 70)
        height_ft_pre_eq = st.slider("Height of building(in ft): ", 1, 100, 1)

        land_surface_condition = st.selectbox("Land Surface Condition: ", df["land_surface_condition"].sort_values().unique())
        foundation_type = st.selectbox("Type of Land Foundation: ", df["foundation_type"].sort_values().unique())
        roof_type = st.selectbox("Material used for Roof: ", df["roof_type"].sort_values().unique())
        ground_floor_type = st.selectbox("Material used for Gloor Floor: ", df["ground_floor_type"].sort_values().unique())
        other_floor_type = st.selectbox("Material used for Other Floors: ", df["other_floor_type"].sort_values().unique())
        position = st.selectbox("Position of Building: ", df["position"].sort_values().unique())
        plan_configuration = st.selectbox("Plan Configuration of Building: ", df["plan_configuration"].sort_values().unique())


        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        st.success("New Entry Added!")
        st.write(building_id, ward_id, count_floors_pre_eq)