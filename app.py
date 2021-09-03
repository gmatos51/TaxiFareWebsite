import streamlit as st
import datetime
import requests
import urllib
import pandas as pd

#Background
# st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: url("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/1200px-Above_Gotham.jpg")
#     }
#    .sidebar .sidebar-content {
#         background: url("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/1200px-Above_Gotham.jpg")
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

st.set_page_config(
    page_title = 'Vrum Vruuuum',
    page_icon = '🇺🇸',
    layout = 'wide',
    initial_sidebar_state = 'auto' # collapsed
)

#Title

st.title('Taxi Fare Prediction in New York')

st.sidebar.write(' ## Enter some features to predict your fare correctly.')

col1, col2, col3 = st.columns(3)

# Date and Time

date = st.sidebar.date_input(
    "Date:",
    datetime.date(2021, 9, 6))

time = t = st.sidebar.time_input(
    'Time:',
    datetime.time(8, 45))

date_and_time = str(date) + ' ' + str(time)

# Location

start_point = st.sidebar.text_input('Pick-up Point:', "Central Park, New York")

url_location_sp = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(
        start_point) + '?format=json'
response_sp = requests.get(url_location_sp).json()

pickup_latitude = response_sp[0]['lat']
pickup_longitude = response_sp[0]['lon']


end_point = st.sidebar.text_input('Dropoff Point:', "Empire State Building")

url_location_ep = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(
        end_point) + '?format=json'
response_ep = requests.get(url_location_ep).json()

dropoff_latitude = response_ep[0]['lat']
dropoff_longitude  = response_ep[0]['lon']

# Passenger Count

passenger_count = st.sidebar.number_input('How many people?',min_value = 1, max_value = 8,step=1,value=1)

# Prediction

url = 'https://taxifare.lewagon.ai/predict'

if st.sidebar.button('Prediction'):
    parameters = {
        "pickup_datetime": date_and_time,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    x = requests.get(url, params=parameters)
    st.sidebar.write('Estimated fare:', x.json()["prediction"])

def get_map_data():
    return pd.DataFrame([(float(pickup_latitude),float(pickup_longitude)),
                        (float(dropoff_latitude), float(dropoff_longitude))],
                        columns=['lat', 'lon'])

df = get_map_data()

st.map(df)