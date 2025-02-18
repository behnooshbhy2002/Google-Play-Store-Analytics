import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

API_RELEASES = "http://127.0.0.1:8000/trends/releases-per-year"
API_UPDATES = "http://127.0.0.1:8000/trends/updates-per-year"
API_RATINGS = "http://127.0.0.1:8000/trends/rating-distribution"

def fetch_categories():
    """Fetch categories from the API."""
    try:
        response = requests.get("http://127.0.0.1:8000/categories/")
        if response.status_code == 200:
            return [cat["category_name"] for cat in response.json()]
    except requests.exceptions.RequestException:
        return []
    return []

def fetch_trends(api_url, category_name):
    """Fetch trend data (releases, updates, or ratings) for a selected category."""
    try:
        response = requests.get(api_url, params={"category_name": category_name})
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return []
    return []


def fetch_avg_ratings():
    """Fetch average ratings per category from the API."""
    try:
        response = requests.get("http://127.0.0.1:8000/trends/avg-rating-per-category")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return []
    return []


def show_avg_ratings_chart():
    st.subheader("⭐ Average Rating per Category")

    data = fetch_avg_ratings()

    if data:
        df = pd.DataFrame(data)
        fig = px.bar(df, x="category_name", y="avg_rating",
                     title="Average Rating per Category",
                     labels={"category_name": "Category", "avg_rating": "Average Rating"},
                     height=600)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig)
    else:
        st.warning("No data available.")
def plot_trends(df, title, y_label):
    """Helper function to plot trends."""
    if not df.empty:
        fig = px.bar(df, x="year", y="count", title=title,
                     labels={"year": "Year", "count": y_label},
                     height=500)
        fig.update_traces(text=df["count"], textposition="outside")
        fig.update_xaxes(type='category')
        st.plotly_chart(fig)
    else:
        st.warning("No data available for the selected category.")

def plot_rating_distribution(df, category):
    if not df.empty:
        df = df[df["bin"] > 1]  # Ensure bins are valid
        ratings = df["bin"].dropna().tolist()

        if ratings:
            fig = ff.create_distplot(
                [ratings], group_labels=[f"Ratings - {category}"],
                show_hist=True, show_rug=False, curve_type='kde',
                bin_size=0.2
            )
            fig.update_layout(title=f"Rating Distribution for {category}",
                              xaxis_title="Rating", yaxis_title="Density")
            st.plotly_chart(fig)
        else:
            st.warning("No valid rating data available.")
    else:
        st.warning("No rating data available for the selected category.")

def show_charts():
    st.subheader("📊 Application Trends Analysis")

    # Load categories
    categories = fetch_categories()

    # Select category
    selected_category = st.selectbox("Select a Category", categories)

    if selected_category:
        st.write(f"📅 Showing trends for **{selected_category}**")

        # Fetch release trends
        release_data = fetch_trends(API_RELEASES, selected_category)
        if release_data:
            df_releases = pd.DataFrame(release_data)
            plot_trends(df_releases, f"Number of App Releases per Year ({selected_category})", "Number of Releases")

        # Fetch update trends
        update_data = fetch_trends(API_UPDATES, selected_category)
        if update_data:
            df_updates = pd.DataFrame(update_data)
            plot_trends(df_updates, f"Number of App Updates per Year ({selected_category})", "Number of Updates")


    show_avg_ratings_chart()
        # Fetch rating distribution
        # rating_data = fetch_trends(API_RATINGS, selected_category)
        # if rating_data:
        #     df_ratings = pd.DataFrame(rating_data)
        #     plot_rating_distribution(df_ratings, selected_category)
