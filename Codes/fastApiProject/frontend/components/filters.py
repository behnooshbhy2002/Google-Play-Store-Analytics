import re

import streamlit as st
import requests
import pandas as pd
from streamlit.errors import StreamlitDuplicateElementKey


def get_categories():
    """Fetch the list of categories from the API"""
    try:
        response = requests.get("http://127.0.0.1:8000/categories/")
        if response.status_code == 200:
            categories = response.json()
            return {category["id"]: category["category_name"] for category in categories}
        else:
            return {}
    except requests.exceptions.RequestException:
        return {}


def get_content_ratings():
    """Fetch the list of content ratings from the API"""
    try:
        response = requests.get("http://127.0.0.1:8000/content_ratings/")
        if response.status_code == 200:
            return {rating["id"]: rating["content_rating"] for rating in response.json()}
        else:
            return []
    except requests.exceptions.RequestException:
        return []


def fetch_apps(params):
    """Fetch apps from API based on filters"""
    try:
        response = requests.get("http://127.0.0.1:8000/search/", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.exceptions.RequestException:
        return []


import time  # Import the time module

def search_apps():
    try:
        # Initialize session state variables
        if "categories" not in st.session_state:
            st.session_state.categories = get_categories()

        if "selected_categories" not in st.session_state:
            st.session_state.selected_categories = []

        if "content_ratings" not in st.session_state:
            st.session_state.content_ratings = get_content_ratings()

        if "selected_content_ratings" not in st.session_state:
            st.session_state.selected_content_ratings = []

        if "apps_data" not in st.session_state:
            st.session_state.apps_data = []

        if "filtered" not in st.session_state:
            st.session_state.filtered = False

        if "current_page" not in st.session_state:
            st.session_state.current_page = 1

        # Fetch categories and content ratings
        categories = st.session_state.categories
        content_ratings = st.session_state.content_ratings

        # Allow multiple category selection
        selected_categories = st.sidebar.multiselect(
            "Select Categories",
            list(categories.values()),
            default=st.session_state.selected_categories,
            key="category_multiselect_unique_key"
        )

        # Allow multiple content rating selection
        selected_content_ratings = st.sidebar.multiselect(
            "Select Content Ratings",
            list(content_ratings.values()),
            default=st.session_state.selected_content_ratings,
            key="content_rating_multiselect_unique_key"
        )

        # Set the range for rating
        rating_range = st.sidebar.slider(
            "Rating Range", 0.0, 5.0, (0.0, 5.0), key="rating_slider_unique_key"
        )
        min_rating, max_rating = rating_range

        # Set the range for price
        min_price = st.sidebar.number_input(
            "Minimum Price", 0.0, 100.0, 0.0, key="min_price_input_unique_key"
        )
        max_price = st.sidebar.number_input(
            "Maximum Price", 0.0, 100.0, 1.0, key="max_price_input_unique_key"
        )

        # Rule: Check if max_price is lower than min_price and max_price is not 0
        if max_price < min_price and max_price != 0:
            st.sidebar.error("❌ Maximum price cannot be lower than minimum price unless it is 0.")
            disable_filter_button = True
        else:
            disable_filter_button = False

        # Add sorting options
        sort_by = st.sidebar.selectbox(
            "Sort By", ["Rating", "Price", "Category"], key="sort_by_filter_unique_key"
        )
        sort_order = st.sidebar.selectbox(
            "Sort Order", ["Ascending", "Descending"], key="sort_order_filter_unique_key"
        )

        # Add the search bar for app name
        app_name = st.sidebar.text_input(
            "Search by App Name", key="app_name_input_unique_key"
        )
        # Add a checkbox to toggle execution time display
        show_execution_time = st.sidebar.checkbox("Show Execution Time", value=True)

        # Apply Filter button
        if st.sidebar.button("Apply Filter", key="apply_filter_btn_unique_key", disabled=disable_filter_button):
            # Convert the selected categories into multiple query parameters
            params = []
            for category in selected_categories:
                params.append(("category_name", category))
            for rating in selected_content_ratings:
                params.append(("content_rating", rating))

            query_params = {
                "min_rating": min_rating,
                "max_rating": max_rating,
                "min_price": min_price,
                "max_price": max_price,
                "app_name": app_name,
                "sort_by": sort_by.lower(),
                "show_execution_time": show_execution_time,
                "sort_order": "asc" if sort_order == "Ascending" else "desc",
            }

            # Make API request with proper query parameter formatting
            response = requests.get("http://127.0.0.1:8000/search/", params=params + list(query_params.items()))
            if response.status_code == 200:
                data = response.json()
                st.session_state.apps_data = data["results"]
                st.session_state.execution_time_before = data["explain_before_indexing"]
                st.session_state.execution_time_after = data["explain_after_indexing"]
                st.session_state.filtered = True
                st.session_state.current_page = 1
            else:
                st.error("Failed to fetch data from the API.")

        if not st.session_state.filtered or not st.session_state.apps_data:
            st.write("🔍 Apply filters to search for apps!")
            return

        # Convert API response to DataFrame
        app_data = pd.DataFrame(st.session_state.apps_data)

        if app_data.empty:
            st.write("🚫 No results found!")
            return

        # Map category_id to category_name
        app_data['category_name'] = app_data['category_id'].map(categories)
        app_data['content rating'] = app_data['content_rating'].map(content_ratings)

        # Display important columns first
        important_columns = ["app_name", "rating", "price", "category_name", "content rating"]
        app_data = app_data[important_columns + [col for col in app_data.columns if col not in important_columns]]

        # Sort data based on user selection
        if sort_by == "Rating":
            app_data = app_data.sort_values(by="rating", ascending=(sort_order == "Ascending"))
        elif sort_by == "Price":
            app_data = app_data.sort_values(by="price", ascending=(sort_order == "Ascending"))
        elif sort_by == "Category":
            app_data = app_data.sort_values(by="category_name", ascending=(sort_order == "Ascending"))

        # Pagination
        page_size = 10
        total_pages = len(app_data) // page_size + (1 if len(app_data) % page_size > 0 else 0)

        if total_pages == 0:
            st.write("🚫 No results to display!")
            return

        # Select page number
        page = st.selectbox(
            "Select page", range(1, total_pages + 1), index=st.session_state.current_page - 1, key="page_selector_unique_key"
        )

        # Update session state with the selected page
        st.session_state.current_page = page

        # Display the apps for the selected page
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_apps = app_data.iloc[start_idx:end_idx]

        # Display the execution time and plan
        # Display the execution time and plan if the checkbox is checked
        if show_execution_time and st.session_state.execution_time_before and st.session_state.execution_time_after:
            explain_text_before = " ".join(st.session_state.execution_time_before)
            match1 = re.search(r"Execution Time:\s*(\d+\.\d+)\s*ms", explain_text_before)
            execution_time_before = match1.group(1)
            st.write(" **Execution Time Before Indexing:**")
            st.code(f"{execution_time_before} ms")

            explain_text_after = " ".join(st.session_state.execution_time_after)
            match2 = re.search(r"Execution Time:\s*(\d+\.\d+)\s*ms", explain_text_after)
            execution_time_after = match2.group(1)
            st.write(" **Execution Time After Indexing:**")
            st.code(f"{execution_time_after} ms")

        st.dataframe(page_apps)

    except StreamlitDuplicateElementKey as e:
        st.rerun()


# Run the search function
search_apps()
