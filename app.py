import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Setup
st.set_page_config(page_title="Country Finder v5", layout="centered")
st.title("🌍 Country Information Finder")
st.write("Search for any country globally using the updated REST Countries v5 API.")

# 1. Setup API Key and Headers
# It's best practice to keep keys in a .env file as REST_COUNTRIES_KEY=your_key
API_KEY = os.getenv("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")
headers = {"Authorization": f"Bearer {API_KEY}"}


def fetch_country_data(query):
    """Fetches country data from the v5 API based on user search."""
    url = f"https://api.restcountries.com/v5/countries?q={query}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 401:
            return None, "Unauthorized: Please verify your v5 API Key."
        elif response.status_code == 404:
            return None, "Country not found. Try a different spelling."
        else:
            return None, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"


# 2. User UI Input
country_query = st.text_input(
    "Enter a country name (e.g., India, Canada, Japan):"
)

if country_query:
    with st.spinner(f"Searching for '{country_query}'..."):
        data, error = fetch_country_data(country_query)

    if error:
        st.error(error)
    elif data:
        st.success("Data fetched successfully!")

        # The v5 API typically returns a list of results matching the search query
        # Let's inspect and parse the first match safely
        if isinstance(data, list) and len(data) > 0:
            country = data[0]
        elif isinstance(data, dict) and "data" in data:
            # Handle if the payload is wrapped inside a {'data': [...]} object
            country = (
                data["data"][0]
                if isinstance(data["data"], list)
                else data["data"]
            )
        else:
            country = data

        # 3. Render Parsed JSON Fields Nicely on Screen
        st.subheader(f"Results for {country_query.title()}")

        # Display raw response safely in an expandable widget for debugging
        with st.expander("Show Raw API JSON Payload"):
            st.json(country)

        # Dynamic Extraction Example based on common REST countries fields
        # (Adjust keys if your custom v5 endpoint names them slightly differently)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Common Name:** {country.get('name', 'N/A')}")
            st.markdown(f"**Region:** {country.get('region', 'N/A')}")
            st.markdown(f"**Subregion:** {country.get('subregion', 'N/A')}")

        with col2:
            st.markdown(f"**Capital:** {country.get('capital', 'N/A')}")

            pop = country.get("population", "N/A")
            if isinstance(pop, (int, float)):
                st.markdown(f"**Population:** {pop:,}")
            else:
                st.markdown(f"**Population:** {pop}")

            area = country.get("area", "N/A")
            if isinstance(area, (int, float)):
                st.markdown(f"**Area:** {area:,} sq km")
            else:
                st.markdown(f"**Area:** {area}")