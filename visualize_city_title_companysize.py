import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="City, Title, Company Size Visualizations", layout="wide")
st.title("City, Title, Company Size Visualizations")

# Load the CSV file
df = pd.read_csv('Passionfruit-_All-Replies-positives-+-DNC_-Default-View-export-1747218941610.csv')

# Extract City from 'Location Name' (first part before comma)
df['City'] = df['Location Name'].astype(str).str.split(',').str[0].str.strip()

# Clean up columns
city_col = 'City'
title_col = 'Title'
size_col = 'Employee Count'

# Drop rows with missing values in key columns
df = df.dropna(subset=[city_col, title_col, size_col])

# Convert company size to numeric (if not already)
df[size_col] = pd.to_numeric(df[size_col], errors='coerce')
df = df.dropna(subset=[size_col])

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    selected_cities = st.multiselect("Select Cities", options=sorted(df[city_col].unique()), default=None)
    selected_titles = st.multiselect("Select Titles", options=sorted(df[title_col].unique()), default=None)

# Apply filters
filtered_df = df.copy()
if selected_cities:
    filtered_df = filtered_df[filtered_df[city_col].isin(selected_cities)]
if selected_titles:
    filtered_df = filtered_df[filtered_df[title_col].isin(selected_titles)]

# 1. Bar chart: Number of people per city
city_counts = filtered_df[city_col].value_counts().reset_index()
city_counts.columns = ['City', 'Count']
fig1 = px.bar(city_counts, x='City', y='Count',
              labels={'City': 'City', 'Count': 'Count'},
              title='Number of People per City')
st.plotly_chart(fig1, use_container_width=True)

# 2. Box plot: Company size distribution by title (top 20 titles)
top_titles = filtered_df[title_col].value_counts().head(20).index
filtered_top_titles = filtered_df[filtered_df[title_col].isin(top_titles)]
fig2 = px.box(filtered_top_titles, x=title_col, y=size_col,
              title='Company Size Distribution by Title (Top 20 Titles)',
              labels={title_col: 'Title', size_col: 'Employee Count'})
st.plotly_chart(fig2, use_container_width=True)

# 3. Heatmap: Count of titles by city and company size (binned)
filtered_df['Company Size Bin'] = pd.cut(filtered_df[size_col], bins=[0, 50, 200, 500, 1000, 5000, 100000],
                                labels=['1-50', '51-200', '201-500', '501-1k', '1k-5k', '5k+'])
heatmap_data = filtered_df.groupby([city_col, 'Company Size Bin'])[title_col].count().reset_index()
fig3 = px.density_heatmap(heatmap_data, x=city_col, y='Company Size Bin', z=title_col,
                         color_continuous_scale='Viridis',
                         title='Heatmap: Titles by City and Company Size',
                         labels={city_col: 'City', 'Company Size Bin': 'Company Size', title_col: 'Count'})
st.plotly_chart(fig3, use_container_width=True) 