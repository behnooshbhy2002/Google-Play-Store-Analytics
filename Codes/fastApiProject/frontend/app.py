import streamlit as st
from components.filters import search_apps
from components.charts import show_charts
from components.update_form import update_app_form

st.title("📊 App Dashboard")

tab1, tab2, tab3 = st.tabs(["🔍 Advanced Search", "📈 Data Analysis", "🛠 Developer Management"])

with tab1:
    search_apps()

with tab2:
    show_charts()

with tab3:
    update_app_form()
