import streamlit as st
import requests

API_KEY = "Svf76eKbNaiczYmWzlaYLQwe36o1t1l0umNfvd8v"  # Replace with your own NASA key if rate-limited
BASE_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers"

# Streamlit config
st.set_page_config(page_title="🚗 NASA Mars Rover Explorer", layout="wide")
st.title("🚗 Mars Rover Photo Explorer")

# Rover selector
rover = st.selectbox("Select Rover", ["Curiosity", "Opportunity", "Spirit"]).lower()

# Choose search method
search_by = st.radio("Search By", ["Martian Sol", "Earth Date"])

if search_by == "Martian Sol":
    sol = st.number_input("Enter Martian Sol (e.g. 1000)", min_value=0, max_value=5000, value=1000)
    params = {"sol": sol, "api_key": API_KEY}
else:
    earth_date = st.date_input("Pick an Earth Date")
    params = {"earth_date": earth_date.isoformat(), "api_key": API_KEY}

# Optional camera filter
camera_options = {
    "": "All Cameras",
    "FHAZ": "Front Hazard Avoidance Camera",
    "RHAZ": "Rear Hazard Avoidance Camera",
    "NAVCAM": "Navigation Camera",
    "MAST": "Mast Camera",
    "CHEMCAM": "Chemistry Camera",
    "MAHLI": "Hand Lens Imager",
    "MARDI": "Mars Descent Imager",
    "PANCAM": "Panoramic Camera",
    "MINITES": "Mini-TES"
}

selected_camera = st.selectbox("Camera (optional)", list(camera_options.keys()), format_func=lambda x: camera_options[x])
if selected_camera:
    params["camera"] = selected_camera.lower()

# Search
if st.button("Search Photos"):
    url = f"{BASE_URL}/{rover}/photos"
    st.info(f"Searching {rover.title()} images...")
    res = requests.get(url, params=params)

    if res.status_code == 200:
        photos = res.json().get("photos", [])
        if photos:
            st.success(f"Found {len(photos)} images")
            for photo in photos[:15]:  # limit results
                st.image(photo["img_src"], caption=f"{photo['camera']['full_name']} on {photo['earth_date']}", use_column_width=True)
                st.caption(f"Rover: {photo['rover']['name']} | Sol: {photo['sol']} | Camera: {photo['camera']['name']}")
        else:
            st.warning("No photos found for that query.")
    else:
        st.error("Error fetching Mars Rover photos.")
