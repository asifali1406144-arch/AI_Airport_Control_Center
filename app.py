
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="AI Airport Control Center",
    page_icon="✈️",
    layout="wide"
)

# =========================
# DESIGN
# =========================
st.markdown("""
<style>
.stApp {
    background: #081426;
    color: white;
}
[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stSidebar"] {
    background: #101f35;
}
[data-testid="stMetric"] {
    background: #172b45;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #294666;
}
h1, h2, h3 {
    color: #65c7ff;
}
p, label {
    color: #dce8f5;
}
div.stButton > button {
    background: #087fba;
    color: white;
    border-radius: 8px;
    border: none;
}
div.stButton > button:hover {
    background: #06a6e8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SAMPLE AIRPORT DATA
# =========================
flights = pd.DataFrame({
    "Flight": ["PK301", "EK600", "QR620", "PK305", "TK710",
               "EY221", "SV720", "QR611", "PK309", "EK602"],
    "Airline": ["PIA", "Emirates", "Qatar Airways", "PIA",
                "Turkish Airlines", "Etihad", "Saudia",
                "Qatar Airways", "PIA", "Emirates"],
    "Destination": ["London", "Dubai", "Doha", "Lahore",
                    "Istanbul", "Abu Dhabi", "Jeddah",
                    "Doha", "Islamabad", "Dubai"],
    "Type": ["Departure", "Arrival", "Departure", "Arrival",
             "Departure", "Arrival", "Departure",
             "Arrival", "Departure", "Arrival"],
    "Status": ["On Time", "Landed", "Boarding", "Delayed",
               "On Time", "Landed", "Boarding",
               "Delayed", "On Time", "Landed"],
    "Gate": ["A1", "B2", "A3", "C1", "B4",
             "A2", "C2", "B1", "A4", "C3"],
    "Terminal": ["T1", "T2", "T1", "T3", "T2",
                 "T1", "T3", "T2", "T1", "T3"],
    "Delay": [0, 0, 0, 25, 0, 0, 0, 15, 0, 0]
})

# =========================
# SIDEBAR
# =========================
st.sidebar.title("✈️ AIRPORT CONTROL")
st.sidebar.caption("AI Operations Management System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Airport Overview",
        "🛫 Flight Operations",
        "🛬 Arrivals & Departures",
        "🛣️ Runway Management",
        "🚪 Gate Management",
        "🧳 Baggage Tracking",
        "🏢 Terminal Monitoring",
        "🌦️ Weather Monitoring",
        "🚨 Airport Alerts",
        "📊 Analytics & Reports",
        "🤖 AI Airport Assistant"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("● Airport System Online")
st.sidebar.caption("Demo Data | Not a live operational feed")
st.sidebar.write("Updated:", datetime.now().strftime("%H:%M:%S"))

# =========================
# HEADER
# =========================
st.title("✈️ AI AIRPORT CONTROL CENTER")
st.caption("Smart Airport Operations | Monitoring | Analytics")
st.markdown("---")

# =========================
# OVERVIEW
# =========================
if page == "🏠 Airport Overview":

    st.subheader("Airport Operations Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Flights", "128", "+8")
    c2.metric("Arrivals", "54", "+4")
    c3.metric("Departures", "74", "+6")
    c4.metric("Active Alerts", "3", "-1")

    st.markdown("### 📡 Airport Live Status")

    a, b, c = st.columns(3)
    a.success("Runway: Operational")
    b.success("Terminal: Operational")
    c.warning("3 Active Alerts")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("Flight Distribution")
        fig = px.pie(
            values=[54, 74],
            names=["Arrivals", "Departures"],
            hole=0.55,
            color_discrete_sequence=["#00b4d8", "#4361ee"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Flight Status")
        status = flights["Status"].value_counts().reset_index()
        status.columns = ["Status", "Count"]
        fig = px.bar(
            status,
            x="Status",
            y="Count",
            color="Status",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("✈️ Recent Flight Operations")
    st.dataframe(flights.head(6), use_container_width=True)

    st.info("Dashboard uses sample airport data for demonstration.")

# =========================
# FLIGHT OPERATIONS
# =========================
elif page == "🛫 Flight Operations":

    st.subheader("Flight Operations Management")

    search = st.text_input("🔍 Search Flight Number")

    filtered = flights.copy()

    if search:
        filtered = filtered[
            filtered["Flight"].str.contains(search, case=False)
        ]

    st.dataframe(filtered, use_container_width=True)

    st.subheader("Flight Status Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("On Time", len(flights[flights.Status == "On Time"]))
    col2.metric("Delayed", len(flights[flights.Status == "Delayed"]))
    col3.metric("Boarding", len(flights[flights.Status == "Boarding"]))

    st.subheader("Flight Filters")

    selected_status = st.selectbox(
        "Select Status",
        ["All"] + list(flights["Status"].unique())
    )

    if selected_status != "All":
        st.dataframe(
            flights[flights.Status == selected_status],
            use_container_width=True
        )

# =========================
# ARRIVALS AND DEPARTURES
# =========================
elif page == "🛬 Arrivals & Departures":

    st.subheader("Arrivals and Departures")

    tab1, tab2 = st.tabs(["🛬 Arrivals", "🛫 Departures"])

    with tab1:
        st.dataframe(
            flights[flights.Type == "Arrival"],
            use_container_width=True
        )

    with tab2:
        st.dataframe(
            flights[flights.Type == "Departure"],
            use_container_width=True
        )

    fig = px.bar(
        flights,
        x="Flight",
        y="Delay",
        color="Type",
        barmode="group",
        title="Flight Delay Analysis",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# RUNWAY MANAGEMENT
# =========================
elif page == "🛣️ Runway Management":

    st.subheader("Runway Monitoring System")

    r1, r2, r3 = st.columns(3)

    r1.metric("Total Runways", "3")
    r2.metric("Operational", "2")
    r3.metric("Under Maintenance", "1")

    runway_data = pd.DataFrame({
        "Runway": ["RWY 09/27", "RWY 18/36", "RWY 12/30"],
        "Status": ["Operational", "Operational", "Maintenance"],
        "Condition": ["Good", "Good", "Inspection"],
        "Activity": ["Active", "Active", "Closed"]
    })

    st.dataframe(runway_data, use_container_width=True)

    st.subheader("Runway Safety Status")

    st.success("RWY 09/27 — Operational")
    st.success("RWY 18/36 — Operational")
    st.warning("RWY 12/30 — Maintenance")

    st.info("Runway statuses are demonstration values, not live sensor readings.")

# =========================
# GATE MANAGEMENT
# =========================
elif page == "🚪 Gate Management":

    st.subheader("Airport Gate Management")

    gates = pd.DataFrame({
        "Gate": ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2"],
        "Terminal": ["T1", "T1", "T1", "T2", "T2", "T2", "T3", "T3"],
        "Status": ["Occupied", "Available", "Boarding",
                   "Available", "Occupied", "Available",
                   "Boarding", "Available"]
    })

    st.dataframe(gates, use_container_width=True)

    g1, g2, g3 = st.columns(3)
    g1.metric("Total Gates", len(gates))
    g2.metric("Available", len(gates[gates.Status == "Available"]))
    g3.metric("Occupied", len(gates[gates.Status == "Occupied"]))

    gate_choice = st.selectbox("Select Gate", gates["Gate"])
    st.write("Selected Gate:", gate_choice)

# =========================
# BAGGAGE TRACKING
# =========================
elif page == "🧳 Baggage Tracking":

    st.subheader("Smart Baggage Management")

    b1, b2, b3 = st.columns(3)
    b1.metric("Total Bags", "1,240")
    b2.metric("Processed", "1,180")
    b3.metric("Pending", "60")

    baggage = pd.DataFrame({
        "Bag ID": ["BG101", "BG102", "BG103", "BG104", "BG105"],
        "Flight": ["PK301", "EK600", "QR620", "PK305", "TK710"],
        "Status": ["Loaded", "Processing", "Delivered",
                   "Pending", "Loaded"],
        "Belt": ["B1", "B2", "B3", "B1", "B2"]
    })

    st.dataframe(baggage, use_container_width=True)

    bag_id = st.text_input("Enter Baggage ID")

    if st.button("Track Baggage"):
        result = baggage[baggage["Bag ID"] == bag_id.upper()]

        if not result.empty:
            st.success("Baggage Record Found")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("Baggage ID not found in demo records.")

# =========================
# TERMINAL MONITORING
# =========================
elif page == "🏢 Terminal Monitoring":

    st.subheader("Terminal Management")

    terminals = pd.DataFrame({
        "Terminal": ["T1", "T2", "T3"],
        "Capacity": [500, 450, 350],
        "Passengers": [320, 280, 190],
        "Status": ["Operational", "Operational", "Operational"]
    })

    terminals["Occupancy %"] = (
        terminals["Passengers"] / terminals["Capacity"] * 100
    ).round(1)

    st.dataframe(terminals, use_container_width=True)

    fig = px.bar(
        terminals,
        x="Terminal",
        y="Occupancy %",
        color="Terminal",
        title="Terminal Occupancy",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# WEATHER MONITORING
# =========================
elif page == "🌦️ Weather Monitoring":

    st.subheader("Airport Weather Monitoring")

    w1, w2, w3 = st.columns(3)

    w1.metric("Temperature", "28 °C")
    w2.metric("Wind Speed", "14 km/h")
    w3.metric("Visibility", "8 km")

    st.info("Weather values below are sample data, not live weather.")

    weather = pd.DataFrame({
        "Condition": ["Clear", "Cloudy", "Windy", "Rain"],
        "Hours": [10, 6, 5, 3]
    })

    fig = px.bar(
        weather,
        x="Condition",
        y="Hours",
        color="Condition",
        title="Sample Weather Conditions",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success("Demo weather monitoring panel is active.")

# =========================
# ALERTS
# =========================
elif page == "🚨 Airport Alerts":

    st.subheader("Airport Alert Center")

    alerts = [
        ("🔴 HIGH", "Runway 12/30 maintenance", "Runway"),
        ("🟠 MEDIUM", "Flight PK305 delayed by 25 minutes", "Flight"),
        ("🟡 LOW", "Gate A3 boarding in progress", "Gate")
    ]

    for level, message, category in alerts:
        with st.container(border=True):
            st.markdown(f"**{level} — {category}**")
            st.write(message)

    st.subheader("Alert Statistics")

    fig = px.pie(
        names=["High", "Medium", "Low"],
        values=[1, 1, 1],
        hole=0.5,
        title="Alert Distribution",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# ANALYTICS AND REPORTS
# =========================
elif page == "📊 Analytics & Reports":

    st.subheader("Airport Analytics Center")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Flights", "128")
        st.metric("Average Delay", "4.0 min")

    with col2:
        st.metric("Passenger Count", "2,450")
        st.metric("Airport Efficiency", "94%")

    fig = px.bar(
        flights,
        x="Flight",
        y="Delay",
        color="Status",
        title="Flight Delay Report",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Download Flight Report")

    csv = flights.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download CSV Report",
        csv,
        "airport_flight_report.csv",
        "text/csv"
    )

# =========================
# AI AIRPORT ASSISTANT
# =========================
elif page == "🤖 AI Airport Assistant":

    st.subheader("🤖 AI Airport Operations Assistant")

    st.write(
        "Ask questions about flights, delays, runways, gates and airport operations."
    )

    question = st.text_input(
        "Ask your airport question:",
        placeholder="Example: Which flights are delayed?"
    )

    if st.button("Analyze Airport Data"):

        if question.strip():

            q = question.lower()

            if "delay" in q:
                delayed = flights[flights.Status == "Delayed"]
                st.warning(f"{len(delayed)} delayed flights found.")
                st.dataframe(delayed, use_container_width=True)

            elif "arrival" in q:
                st.dataframe(
                    flights[flights.Type == "Arrival"],
                    use_container_width=True
                )

            elif "departure" in q:
                st.dataframe(
                    flights[flights.Type == "Departure"],
                    use_container_width=True
                )

            elif "runway" in q:
                st.info(
                    "Two runways are operational and one is under maintenance (demo data)."
                )

            elif "gate" in q:
                st.info("Gate information is available in Gate Management.")

            elif "baggage" in q or "bag" in q:
                st.info("Open Baggage Tracking to search baggage records.")

            elif "weather" in q:
                st.info("Open Weather Monitoring for sample weather information.")

            elif "flight" in q:
                st.dataframe(flights, use_container_width=True)

            else:
                st.info(
                    "Try asking about flights, arrivals, departures, delays, "
                    "runways, gates, baggage or weather."
                )

        else:
            st.warning("Please enter a question.")

    st.markdown("---")
    st.subheader("AI Operational Insights")

    delayed_count = len(flights[flights.Status == "Delayed"])
    ontime_count = len(flights[flights.Status == "On Time"])

    st.write(f"✈️ {ontime_count} flights are currently marked On Time.")
    st.write(f"⚠️ {delayed_count} flights are marked Delayed.")
    st.write("🛣️ One runway is listed under maintenance.")
    st.write("🚪 Gate availability can be reviewed in Gate Management.")

    st.caption("Rule-based demonstration assistant; not an external AI model.")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<center>✈️ AI AIRPORT CONTROL CENTER | Smart Airport Management System</center>",
    unsafe_allow_html=True
)
