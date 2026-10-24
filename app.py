import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="E-Commerce Sales & Customer Segmentation Dashboard",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ E-Commerce Sales & Customer Segmentation Dashboard")
st.markdown("An interactive web application analyzing transaction behavior, sales performance, and RFM customer segmentation.")

# 2. Load Data with Caching
@st.cache_data
def load_data():
    segmented_df = pd.read_csv('segmented_customers.csv')
    cleaned_df = pd.read_csv('cleaned_online_retail.csv')
    cleaned_df['InvoiceDate'] = pd.to_datetime(cleaned_df['InvoiceDate'])
    return segmented_df, cleaned_df

try:
    segmented_df, cleaned_df = load_data()
except FileNotFoundError:
    st.error("⚠️ Dataset files not found! Ensure 'segmented_customers.csv' and 'cleaned_online_retail.csv' are in the same directory as 'app.py'.")
    st.stop()

# 3. Sidebar Filters
st.sidebar.header("🔍 Dashboard Filters")
selected_segments = st.sidebar.multiselect(
    "Filter by Customer Segment(s):",
    options=segmented_df['Segment'].unique(),
    default=segmented_df['Segment'].unique()
)

# Filter data based on sidebar selection
filtered_segmented = segmented_df[segmented_df['Segment'].isin(selected_segments)]

# 4. Top Key Performance Indicator (KPI) Cards
st.markdown("### 📊 Key Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

total_revenue = cleaned_df['TotalPrice'].sum()
total_orders = cleaned_df['InvoiceNo'].nunique()
total_customers = len(segmented_df)
avg_order_value = total_revenue / total_orders

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Active Customers", f"{total_customers:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# 5. Row 1: Visualizations (Segment Distribution & Revenue by Segment)
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Customer Distribution by Segment")
    segment_counts = filtered_segmented['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Customer Count']
    fig_pie = px.pie(
        segment_counts, 
        names='Segment', 
        values='Customer Count', 
        hole=0.4, 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_b:
    st.subheader("Monetary Value Contribution by Segment")
    segment_revenue = filtered_segmented.groupby('Segment')['Monetary'].sum().reset_index()
    fig_bar = px.bar(
        segment_revenue, 
        x='Segment', 
        y='Monetary', 
        color='Segment', 
        text_auto='.2s', 
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_layout(showlegend=False, xaxis_title="Segment", yaxis_title="Total Revenue ($)")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# 6. Row 2: Time Series Trend (Monthly Revenue)
st.subheader("📈 Monthly Revenue Trend")
cleaned_df['YearMonth'] = cleaned_df['InvoiceDate'].dt.to_period('M').astype(str)
monthly_sales = cleaned_df.groupby('YearMonth')['TotalPrice'].sum().reset_index()

fig_line = px.line(
    monthly_sales, 
    x='YearMonth', 
    y='TotalPrice', 
    markers=True, 
    title="Revenue Growth Over Time"
)
fig_line.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)")
st.plotly_chart(fig_line, use_container_width=True)

# 7. Raw Data Preview Dropdown
with st.expander("🔍 Preview Filtered Customer Segmentation Data"):
    st.dataframe(filtered_segmented)