import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.header("📊 Interactive Sales Dashboard")

#Load data
df = pd.read_csv("Sales_data.csv")
st.success("✅ CSV loaded successfully")

# Region filter
st.sidebar.header("Filter Data")
Region_filter = st.sidebar.multiselect("Select Region(s)", options=df['Region'].unique(), default=df['Region'].unique())
Product_filter = st.sidebar.multiselect("Select Product(s)", options=df['Category'].unique(), default=df['Category'].unique())

# Filter data
filtered_df = df[
    (df['Region'].isin(Region_filter))&
    (df['Category'].isin(Product_filter))
]

st.markdown(f"#### Region selected: {Region_filter} \n #### Product_selected: {Product_filter}")

col1,col2=st.columns(2)
with col1:
        Total_sales = filtered_df["Revenue"].sum()
        st.metric('Revenue', f' ${Total_sales: 2f}')

with col1:
        Average_sales = filtered_df["Revenue"].mean()
        st.metric('Average Revenue', f' ${Average_sales: 2f}')

tab1,tab2=st.tabs(['Sales by Product', 'Sales by Region'])
with tab1:
    st.subheader('Sales by Product')
    product_data=filtered_df.groupby('Category')['Revenue'].sum().reset_index()
    fig1 = px.bar(product_data, x='Category', y='Revenue', color='Category', text='Revenue')
    st.plotly_chart(fig1)
                  
with tab2:
    st.subheader('Sales by Region')
    Region_data=filtered_df.groupby('Region')['Revenue'].sum().reset_index()
    fig2 = px.pie(Region_data, names='Region', values='Revenue', title='Sales by Region')
    st.plotly_chart(fig2)
                  

def generate_insight(df):
    if df.empty:
        return "No data available for this region."

    top_category = df.groupby("Category")["Revenue"].sum().idxmax()
    total = df["Revenue"].sum()
    avg_order = df["Revenue"].mean()

    options = [
        f"💰 Revenue in this region: ${total:.2f}",
        f"🔥 Best-category: {top_category}",
        f"📦 Average order value: ${avg_order:.2f}"
    ]
    return random.choice(options)


st.info(generate_insight(filtered_df))



