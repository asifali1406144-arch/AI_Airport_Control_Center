
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="AI Airport Control Center",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: white;
}
[data-testid="stMetric"] {
    background: #17243a;
    padding: 20px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

st.title("✈️ AI AIRPORT CONTROL CENTER")
st.caption("SMART AIRPORT MANAGEMENT SYSTEM")

st.divider()

st.subheader("AIRPORT OVERVIEW")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Flights", 128)
c2.metric("Arrivals", 54)
c3.metric("Departures", 74)
c4.metric("Active Alerts", 3)

st.divider()

data = pd.DataFrame({
    "Flight": ["PK301", "EK600", "QR620", "PK305", "TK710"],
    "Airline": ["PIA", "Emirates", "Qatar Airways",
                "PIA", "Turkish Airlines"],
    "Destination": ["Lahore", "Dubai", "Doha",
                    "Islamabad", "Istanbul"],
    "Status": ["On Time", "Delayed", "On Time",
               "Boarding", "Scheduled"],
    "Gate": ["A1", "B2", "A3", "C1", "B4"]
})

st.subheader("✈️ FLIGHT OPERATIONS")

st.dataframe(data, use_container_width=True, hide_index=True)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("FLIGHT STATISTICS")

    chart_data = pd.DataFrame({
        "Category": ["Arrivals", "Departures"],
        "Flights": [54, 74]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Flights",
        color="Category",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("FLIGHT DISTRIBUTION")

    fig2 = px.pie(
        chart_data,
        names="Category",
        values="Flights",
        hole=0.5,
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("🚨 AIRPORT ALERTS")

st.error("EK600 - Flight Delayed")
st.warning("Gate C3 - Security Inspection")
st.success("PK301 - Operating Normally")

st.divider()

st.subheader("🔍 SEARCH FLIGHT")

search = st.text_input("Enter Flight Number")

if search:
    result = data[
        data["Flight"].str.contains(search, case=False)
    ]

    if len(result) > 0:
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("No Flight Found")

st.divider()

st.subheader("🤖 AI AIRPORT ASSISTANT")

question = st.text_input("Ask about airport operations")

if st.button("Analyze"):
    if question:
        st.info(
            "Airport analysis: Please review flight "
            "status, delays and active alerts."
        )

st.caption("AI Airport Control Center | Academic Project")
st.caption(
    "Last Updated: " +
    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

