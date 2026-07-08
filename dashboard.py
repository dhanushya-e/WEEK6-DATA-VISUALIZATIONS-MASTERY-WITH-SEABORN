import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Corporate Sales Dashboard", layout="wide")
st.markdown("# 📊 Interactive Corporate Sales Analytics Dashboard")
st.markdown("---")

# Load file directly without dangerous None assignments
df = pd.read_csv('sales_data(100).csv')
df['Date'] = pd.to_datetime(df['Date'])

st.sidebar.markdown("### 📊 Interactive Filters Workspace")
available_regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect("Select Regions:", options=available_regions, default=available_regions)

filtered_df = df[df['Region'].isin(selected_regions)]

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    st.subheader("📈 Regional Sales Volume Timeline (Plotly)")
    grouped_timeline = filtered_df.groupby(['Date', 'Region'])['Total Sales'].sum().reset_index()
    fig_line = px.line(grouped_timeline.sort_values('Date'), x='Date', y='Total Sales', color='Region', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with row1_col2:
    st.subheader("🛒 Quantity Performance Mix (Plotly)")
    fig_bar = px.bar(filtered_df, x='Product', y='Quantity', color='Region', barmode='group')
    st.plotly_chart(fig_bar, use_container_width=True)

with row2_col1:
    st.subheader("📦 Price Spread Outliers (Seaborn)")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.boxplot(data=filtered_df, x='Product', y='Price', palette='Set2', hue='Product', legend=False, ax=ax)
    plt.xticks(rotation=25)
    st.pyplot(fig)

with row2_col2:
    st.subheader("🔗 Numeric Metric Correlation Heatmap (Seaborn)")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    corr_matrix = filtered_df[['Quantity', 'Price', 'Total Sales']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig)
