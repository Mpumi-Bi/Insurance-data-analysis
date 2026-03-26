import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Insurance Dashboard", layout="wide")
st.title("Interactive Insurance Dashboard")
st.write("Explore dummy insurance data with interactive charts and filters")

# Dummy insurance data
df = pd.DataFrame({
    'Age': [25, 30, 45, 50, 35, 60],
    'Gender': ['M', 'F', 'F', 'M', 'F', 'M'],
    'Premium': [200, 300, 250, 400, 320, 500],
    'ClaimAmount': [1000, 1500, 1200, 2000, 1600, 2200]
})

# --- Filters ---
st.sidebar.header("Filters")

# Age filter
age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df['Age'].min()),
    max_value=int(df['Age'].max()),
    value=(25, 60)
)

# Gender filter
gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Apply filters
filtered_df = df[
    (df['Age'] >= age_range[0]) &
    (df['Age'] <= age_range[1]) &
    (df['Gender'].isin(gender_filter))
]

# --- Display filtered data ---
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# --- Scatter plot: Premium vs ClaimAmount ---
st.subheader("Premium vs Claim Amount")
fig = px.scatter(
    filtered_df,
    x='Premium',
    y='ClaimAmount',
    color='Gender',
    size='Age',
    hover_data=['Age']
)
st.plotly_chart(fig, width='stretch')

# --- Bar chart: Average Claim Amount by Gender ---
st.subheader("Average Claim Amount by Gender")
avg_claim = filtered_df.groupby('Gender')['ClaimAmount'].mean().reset_index()
st.bar_chart(avg_claim.set_index('Gender'))

# --- Summary KPIs ---
st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(filtered_df))
with col2:
    st.metric("Average Premium", round(filtered_df['Premium'].mean(), 2))
with col3:
    st.metric("Average Claim Amount", round(filtered_df['ClaimAmount'].mean(), 2))