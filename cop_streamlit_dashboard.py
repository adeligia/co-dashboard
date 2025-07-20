
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load Excel file
df = pd.read_excel("cop_power_interest_scored.xlsx", sheet_name="Χαρτογράφηση")

# Handle quadrant classification
df["Quadrant"] = df.apply(
    lambda row: (
        "Key Players" if row["Power"] >= 3 and row["Interest (projected)"] >= 3 else
        "Satisfy" if row["Power"] >= 3 else
        "Involve" if row["Interest (projected)"] >= 3 else
        "Monitor"
    ), axis=1
)

# Sidebar filters
st.sidebar.header("Filters")
domain_filter = st.sidebar.multiselect("Select Domain(s):", df["Domain"].dropna().unique(), default=df["Domain"].dropna().unique())
type_filter = st.sidebar.multiselect("Select Type(s):", df["Type"].dropna().unique(), default=df["Type"].dropna().unique())
city_filter = st.sidebar.multiselect("Select Location(s):", df["Location (City)"].dropna().unique(), default=df["Location (City)"].dropna().unique())

# Apply filters
filtered_df = df[
    df["Domain"].isin(domain_filter) &
    df["Type"].isin(type_filter) &
    df["Location (City)"].isin(city_filter)
]

st.title("Power-Interest Matrix Dashboard for CoP Stakeholders")
st.markdown("Filtered data: **{}** stakeholders shown".format(len(filtered_df)))

# Create scatter plot
fig = px.scatter(
    filtered_df,
    x="Power",
    y="Interest (projected)",
    color="Domain",
    symbol="Type",
    hover_name="Organization Name",
    hover_data=["Type", "Location (City)", "Quadrant"],
    labels={"Power": "Power", "Interest (projected)": "Interest"},
    title="Power vs Interest of Stakeholders"
)

# Add quadrant lines and labels
fig.add_shape(type="line", x0=3, x1=3, y0=0, y1=5, line=dict(dash="dot"))
fig.add_shape(type="line", x0=0, x1=5, y0=3, y1=3, line=dict(dash="dot"))
fig.add_annotation(x=4.5, y=4.5, text="Key Players", showarrow=False)
fig.add_annotation(x=1.5, y=4.5, text="Involve", showarrow=False)
fig.add_annotation(x=4.5, y=1.5, text="Satisfy", showarrow=False)
fig.add_annotation(x=1.5, y=1.5, text="Monitor", showarrow=False)

st.plotly_chart(fig, use_container_width=True)

# Show filtered data table
st.markdown("### Stakeholder Data")
st.dataframe(filtered_df.reset_index(drop=True))
