import pandas as pd
import plotly as pl
import plotly.express as px
import chart_studio.plotly as py
import plotly.graph_objects as go
import streamlit as st
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

###############################

uploaded_file= st.sidebar.file_uploader("Drop Here")
if uploaded_file:
    df=pd.read_csv(uploaded_file)

###############################

df=pd.read_csv("ds_salaries.csv")
df["company_size"].replace(["S", "M", "L"], ["Small", "Medium", "Large"], inplace=True)
df.drop("Unnamed: 0",axis=1,inplace=True)

###############################

st.title("MSBA 325 Assignment")
st.text("Building Interactive Visualization with Streamlit")
st.markdown("201803271 **Rami Haidar**")

###############################

def data_head(dataframe):
    st.header("Data Head")
    st.write(dataframe.head())

def stats(dataframe):
    st.header("Data Statistics")
    st.write(dataframe.describe())

df_experience=df.groupby("experience_level")["salary_in_usd"].mean().reset_index().sort_values("salary_in_usd")
def fig1(dataframe):
    #Bar plot of Average DS Salaries Based on Experience Level (EDA)
    ex_salary = px.bar(dataframe, x='experience_level', y='salary_in_usd',color='experience_level', title="Average DS Salaries Based on Experience Level",
        labels={"experience_level": "Experience Level"})

    ex_salary.update_layout(
    xaxis_title="Experience Level",
    yaxis_title="Mean Salary ($)",
    font = dict(size=17),height=600,width=700)

    st.plotly_chart(ex_salary)
    st.write("Figure 1: Average Data Scientist Salaries Based on Experience Level.")

def interactive(dataframe):
    
    #y_axis_value = st.selectbox("Select Y-axis value",options=df.columns)
    x_axis_value = st.selectbox("Select X-axis value",options=("remote_ratio","job_title","experience_level","employment_type","salary_currency","employee_residence","company_size"))
    st.write("You selected :",x_axis_value)
    joker_hist = px.histogram(dataframe, x=x_axis_value,color=x_axis_value, title='Count of Different '+x_axis_value.upper())

    joker_hist.update_layout(
    xaxis_title=x_axis_value,
    yaxis_title="Count",
    font = dict(size=17),height=600)

    st.plotly_chart(joker_hist)
    st.write("Figure 2:'Count of Different" +x_axis_value.upper())

def box(dataframe):
    year = st.slider("What year would you like to visualize ?",min_value=2020,max_value=2022,value=2020,step=1)
    dataframe=dataframe[dataframe["work_year"]==year]

    #Box plot representing the  Salary Relative to the Comapny Size by Employees
    data_csize = px.box(dataframe, x="company_size", y="salary_in_usd",color="remote_ratio",range_y=[0,500000],width=1000,height=600,
        title="Salary\nRelative to the Comapany Size by Employees ",
        labels={"company_size":"Company Size [S<50 / 50<M<250/ L>250] (Employees)",
        "salary_in_usd":"Salary ($)","remote_ratio": "Remote Ratio"},
        category_orders={"company_size": ["Small", "Medium", "Large"]})

    st.plotly_chart(data_csize)
    st.write("Figure 3: Salary\nRelative to the Comapany Size by Employees")
###############################

st.sidebar.title("Navigation")
st.sidebar.markdown("Select the Data/Plots accordingly:")
user_options= st.sidebar.radio("Visualizations",options=["Home",
"Data Head",
"Data Statistics",
"Salaries vs Experience",
"Interactive Count",
"Box Plot"])

###############################

if user_options == "Home":
    st.markdown("Hello !!! The following app displays some of insights gained from exploring a **Data Scientist Salary** dataset obtained from Kaggle. ")

if user_options == "Data Statistics":
    stats(df)

if user_options == "Data Head":
    data_head(df)

if user_options == "Salaries vs Experience":
    fig1(df_experience)

if user_options == "Interactive Count":
    interactive(df)

if user_options == "Box Plot":
    box(df)
    
###############################