import streamlit as st
from streamlit_js_eval import get_geolocation
import pandas as pd
from geopy.distance import geodesic

# Function to calculate the distance to each rest area
def calculate_distances(rest_areas_df, user_location):
    user_lat, user_lon = user_location
    distances = rest_areas_df.apply(lambda row: geodesic((user_lat, user_lon), (row['latitude'], row['longitude'])).kilometers, axis=1)
    rest_areas_df['distance_to_user_km'] = distances
    return rest_areas_df

def main():
    st.title("NSW Rest Area Finder")

    # Load CSV data
    rest_areas_df = pd.read_csv('nsw_rest_areas_all.csv')

    # Obtain user's geolocation
    loc = get_geolocation()
    if loc:
        user_coords = (loc['coords']['latitude'], loc['coords']['longitude'])
        st.write(f"Your coordinates are {user_coords[0]}, {user_coords[1]}")

        # Calculate distances
        rest_areas_with_distances = calculate_distances(rest_areas_df, user_coords)

        # Find the closest rest area
        closest_rest_area = rest_areas_with_distances.loc[rest_areas_with_distances['distance_to_user_km'].idxmin()]
        st.write("Closest Rest Area:")
        st.write(closest_rest_area)

    else:
        st.write("Unable to retrieve your location. Please press 'ALLOW' giving browser location permission.")

    # Ask the user type
    user_type = st.radio("Are you a truck driver or a car driver?", ('Truck Driver', 'Car Driver'))

    with st.form(key='review_form'):
        st.write("Rest Area Review")
        
        # Common questions for all users
        cleanliness_rating = st.slider("Rate the cleanliness of the rest area:", 1, 5, 3)
        safety_rating = st.slider("Rate the safety of the rest area:", 1, 5, 3)
        amenities_rating = st.slider("Rate the amenities available:", 1, 5, 3)
        comments = st.text_area("Additional comments:")

        # Specific questions for truck drivers
        if user_type == 'Truck Driver':
            parking_space = st.slider("Rate the adequacy of parking space for trucks:", 1, 5, 3)
            accessibility = st.slider("Rate the accessibility for large vehicles:", 1, 5, 3)

        # Specific questions for car drivers
        if user_type == 'Car Driver':
            family_friendly = st.slider("Rate how family-friendly the rest area is:", 1, 5, 3)
            pet_facilities = st.slider("Rate the facilities for pets, if any:", 1, 5, 3)

        # Submit button
        submit_button = st.form_submit_button(label='Submit Review')
    if submit_button:
        st.success("Thank you for your review!")
if __name__ == "__main__":
    main()