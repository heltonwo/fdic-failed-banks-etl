from src.db import get_engine
import plotly.express as px
import streamlit as st
import pandas as pd


# =============================
# Page Configuration
# =============================
st.set_page_config(
    page_title="Failed Banks Dashboard",
    page_icon="🏦",
    layout="wide",
)


# =============================
# Dashboard Header
# =============================
st.title("Failed Banks Dashboard")
st.caption("Analysis of U.S. bank failures using FDIC data")


# =============================
# Data Loading
# =============================
@st.cache_data
def load_data():
    engine = get_engine()

    query = """
        SELECT *
        FROM failed_banks
    """

    return pd.read_sql(query, engine)


df = load_data()


# =============================
# Year Range Filter
# =============================
min_year = int(df["closing_year"].min())
max_year = int(df["closing_year"].max())

year_range = st.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

start_year, end_year = year_range

df_year_filtered = df[
    df["closing_year"].between(start_year, end_year)
].copy()

st.caption("Click a bar to filter the dashboard. Click it again to clear.")


# =============================
# Retrieve Chart Selections
# =============================
def get_selected_value(chart_key):
    chart_state = st.session_state.get(chart_key)

    if chart_state is None:
        return None

    try:
        points = chart_state.selection.points
    except AttributeError:
        points = chart_state.get("selection", {}).get("points", [])

    if points:
        return points[0].get("y")

    return None


selected_state = get_selected_value("state_chart")
selected_acquiring = get_selected_value("acquiring_chart")


# =============================
# Data for State Chart
# Apply year and acquiring filters
# =============================
df_state_chart = df_year_filtered.copy()

if selected_acquiring:
    df_state_chart = df_state_chart[
        df_state_chart["acquiring_institution"] == selected_acquiring
    ]

states = (
    df_state_chart["state"]
    .value_counts()
    .head(10)
    .rename_axis("state")
    .reset_index(name="failures")
)

fig_state = px.bar(
    states,
    x="failures",
    y="state",
    orientation="h",
    title="Geographic Distribution by State",
    labels={
        "failures": "Number of Bank Failures",
        "state": "U.S. State",
    },
)

fig_state.update_layout(
    xaxis_title="Number of Bank Failures",
    yaxis_title="U.S. State",
    yaxis={
        "categoryorder": "total descending",
        "autorange": "reversed",
    },
)


# =============================
# Data for Acquiring Chart
# Apply year and state filters
# =============================
df_acquiring_chart = df_year_filtered.copy()

if selected_state:
    df_acquiring_chart = df_acquiring_chart[
        df_acquiring_chart["state"] == selected_state
    ]

acquiring_counts = (
    df_acquiring_chart["acquiring_institution"]
    .value_counts()
    .head(10)
    .rename_axis("acquiring_institution")
    .reset_index(name="failures")
)

fig_acquiring = px.bar(
    acquiring_counts,
    x="failures",
    y="acquiring_institution",
    orientation="h",
    title="Top 10 Acquiring Institutions",
    labels={
        "failures": "Number of Bank Failures",
        "acquiring_institution": "Acquiring Institution",
    },
)

fig_acquiring.update_layout(
    xaxis_title="Number of Bank Failures",
    yaxis_title="Acquiring Institution",
    yaxis={
        "categoryorder": "total descending",
        "autorange": "reversed",
    },
)


# =============================
# Display Interactive Charts
# =============================
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.plotly_chart(
        fig_acquiring,
        use_container_width=True,
        on_select="rerun",
        key="acquiring_chart",
    )

with row1_col2:
    st.plotly_chart(
        fig_state,
        use_container_width=True,
        on_select="rerun",
        key="state_chart",
    )


# =============================
# Apply Both Selections
# For KPIs and trend charts
# =============================
df_filtered = df_year_filtered.copy()

if selected_state:
    df_filtered = df_filtered[
        df_filtered["state"] == selected_state
    ]

if selected_acquiring:
    df_filtered = df_filtered[
        df_filtered["acquiring_institution"] == selected_acquiring
    ]


# =============================
# KPIs
# =============================
total_failed_banks = len(df_filtered)
states_affected = df_filtered["state"].nunique()

col1, col2 = st.columns(2)

with col1:
    st.metric("Count of Failed Banks", total_failed_banks)

with col2:
    st.metric("States Affected", states_affected)


# =============================
# Annual Bank Failures
# =============================
annual_failures = (
    df_filtered
    .groupby("closing_year")
    .size()
    .reset_index(name="failures")
)

fig_annual = px.bar(
    annual_failures,
    x="closing_year",
    y="failures",
    title="Annual Bank Failures Trend",
    labels={
        "closing_year": "Year",
        "failures": "Failed Banks",
    },
)

fig_annual.update_layout(
    xaxis=dict(dtick=1),
    xaxis_title="Year",
    yaxis_title="Failed Banks",
)


# =============================
# Monthly Seasonality
# =============================
monthly_failures = (
    df_filtered
    .groupby("closing_month")
    .size()
    .reindex(range(1, 13), fill_value=0)
    .rename_axis("closing_month")
    .reset_index(name="failures")
)

monthly_failures["month"] = pd.to_datetime(
    monthly_failures["closing_month"],
    format="%m",
).dt.strftime("%b")

fig_monthly = px.line(
    monthly_failures,
    x="month",
    y="failures",
    markers=True,
    title="Monthly Seasonality Pattern",
    labels={
        "month": "Month",
        "failures": "Failed Banks",
    },
)


# =============================
# Display Trend Charts
# =============================
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.plotly_chart(
        fig_annual,
        use_container_width=True,
    )

with row2_col2:
    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
    )


# RUN COMMAND:
# uv run python -m streamlit run app/dashboard.py