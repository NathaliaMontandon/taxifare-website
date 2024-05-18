import streamlit as st
import pandas as pd
from streamlit_date_picker import date_picker, PickerType
import requests


"# Taxifare Prediction"

# First slicers row
pickup_lat, pickup_lon, drop_off_lat, drop_off_lon = st.columns(4)

with pickup_lat:
    pickup_lat_value = st.text_input(
        label="Pickup Latitude", placeholder="Pickup Latitude"
    )

with pickup_lon:
    pickup_lon_value = st.text_input(
        label="Pickup Longitude", placeholder="Pickup Longitude"
    )

with drop_off_lat:
    drop_off_lat_value = st.text_input(
        label="Drop-off Latitude", placeholder="Drop-off Latitude"
    )

with drop_off_lon:
    drop_off_lon_value = st.text_input(
        label="Drop-off Longitude", placeholder="Drop-off Longitude"
    )

# Second slicers row
time, passengers, get_fare = st.columns(3)

with time:
    st.markdown("Pickup Datetime")
    pickup_datetime = date_picker(picker_type=PickerType.time, key="date_picker")

with passengers:
    passenger_count = st.number_input(
        label="Passengers", min_value=1, max_value=8, value=1
    )

with get_fare:
    st.markdown("Calculate Fare")
    get_fare_click = st.button("Get Fare")

# API Call
url = "https://taxifare.lewagon.ai/predict"

params = {
    "pickup_latitude": pickup_lat_value,
    "pickup_longitude": pickup_lon_value,
    "dropoff_latitude": drop_off_lat_value,
    "dropoff_longitude": drop_off_lon_value,
    "passenger_count": passenger_count,
    "pickup_datetime": pickup_datetime,
}

if get_fare_click:
    response = requests.get(url, params=params)
    st.metric("TaxiFare", f'$ {round(response.json()["fare"], 2)}')

    # Map
    coordinates_df = pd.DataFrame(
        {
            "latitude": [float(pickup_lat_value), float(drop_off_lat_value)],
            "longitude": [float(pickup_lon_value), float(drop_off_lon_value)],
        }
    )

    st.map(data=coordinates_df)
