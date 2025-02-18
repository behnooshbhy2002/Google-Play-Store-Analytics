import streamlit as st
import requests

API_UPDATE_APP = "http://127.0.0.1:8000/apps/{}/update"

def update_app_info(app_id, new_price, update_date, new_desc):
    """Send an update request to the FastAPI backend."""
    update_date_str = update_date.strftime("%Y-%m-%d")  # Convert date to string

    try:
        response = requests.put(
            API_UPDATE_APP.format(app_id),
            json={"price": new_price, "last_updated": update_date_str, "description": new_desc}
        )

        if response.status_code == 200:
            st.success("✅ App updated successfully!")
        else:
            st.error(f"❌ Error: {response.json().get('detail')} {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")

def update_app_form():
    """Streamlit form for updating app details."""
    st.subheader("🔄 Update App Information")

    app_id = st.text_input("App ID:").strip()

    # app_id = int(app_id)  # Convert to integer
    new_price = st.number_input("New Price:")
    update_data = st.date_input("New Update Date:")
    new_desc = st.text_area("New Description:")

    if st.button("Update"):
        update_app_info(app_id, new_price, update_data, new_desc)

if __name__ == "__main__":
    update_app_form()
