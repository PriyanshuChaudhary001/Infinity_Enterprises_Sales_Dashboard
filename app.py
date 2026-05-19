import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load DataSet
cus = pd.read_csv("dataset/customer.csv")
order = pd.read_csv("dataset/orders.csv")
df = pd.merge(order, cus, on='CustomerID', how='inner')
df['Month'] = pd.to_datetime(df['Order Date']).dt.month

st.set_page_config(layout='wide')
st.title("Infinity_Enterprises_Sales_Dashboard")

filtered_df = df.copy()

# Filters
col1,col2,col3,col4 = st.columns(4)
with col1:
    cat = st.selectbox("Select Product",["All"]+list(df['Product Category'].unique()))
    if cat is not 'All':
        filtered_df = filtered_df[filtered_df['Product Category']==cat]
with col2:
    state = st.selectbox("Select State",["All"]+list(df['State or Province'].unique()))
    if state is not 'All':
        filtered_df = filtered_df[filtered_df['State or Province']==state]
with col3:
    city = st.selectbox("Select City",["All"]+list(filtered_df['City'].unique()))
    if city is not 'All':
        filtered_df = filtered_df[filtered_df['City']==city]
with col4:
    gender = st.radio("Select Gender",["All"]+list(df['Gender'].unique()) , horizontal=True)
    if gender is not 'All':
        filtered_df = filtered_df[filtered_df['Gender']==gender]


st.text("All Payment Modes :"+str(filtered_df['Payment Mode'].unique()))


# KPIs
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric("Total Sales",round(filtered_df['Amount'].sum(),2))
with col3:
    st.metric("Total Profit",round(filtered_df['Profit'].sum(),2))
with col2:
    st.metric("Sold Quantity",round(filtered_df['Qty'].sum(),0))
with col4:
    fig, ax = plt.subplots(figsize=(8,2))
    sns.lineplot(x='Product Sub-Category',y='Profit',data=filtered_df , ax=ax)
    plt.axis('off')
    # plt.title("Profit By Product Sub-Category")
    st.pyplot(fig)

col1 , col2 = st.columns([2,1])
with col1:
    fig, ax = plt.subplots(figsize=(6,1))
    sns.lineplot( x='Month' , y='Profit' , data=filtered_df , ax=ax )
    st.pyplot(fig)
with col2:
    fig , ax = plt.subplots(figsize=(3,1))
    sns.barplot(x='Payment Mode',y='Profit' , data=filtered_df,ax=ax)
    st.pyplot(fig)

if cat=='All':
    fig , ax = plt.subplots(figsize=(8,1))
    sns.barplot( x='Product Category' , y='Profit' , data=filtered_df , ax=ax  )
    st.pyplot(fig)
else:
    fig , ax = plt.subplots(figsize=(12,3))
    pbp = filtered_df.groupby('Product Sub-Category')['Profit'].sum().reset_index()
    plt.barh( pbp['Product Sub-Category'] ,pbp['Profit'])
    st.pyplot(fig)

st.dataframe(filtered_df , height=300)