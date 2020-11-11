import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
#import urllib3

## https://www.kaggle.com/imdevskp/corona-virus-report?select=covid_19_clean_complete.csv
#response = urllib3.urlopen(url)
#cr = csv.reader(response)
def load_data():
	#data=pd.read_csv('covid_19.csv')
	data = pd.read_csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv')
	return data
	
def local_css(file_name):
	with open(file_name) as f:
		st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

################### CSS  
#local_css("style.css")


# Header
################### 
st.title('Visualizing Covid-19')

# Load Data
################### 
data=load_data()
#st.markdown(data.head()) # check if updated daily
st.markdown("This interactive dashboard is designed to let you explore Covid-19 trends around the world and visualize them in various formats. You can see the daily cases and deaths by selecting a country from the sidebar. *The data is updated daily*.")


# Side Bar
################### 
st.sidebar.title("Select Country")
st.markdown(
"""
<style>
.sidebar .sidebar-content {
	background: rgb(84, 168, 223);
	text-align: left;
	font-size: x-large;
}
</style>
""",
	unsafe_allow_html=True,
)
c = st.sidebar.selectbox('',data.countriesAndTerritories.unique(),key='1')

st.write('***Selected Country: ***',c)
country=pd.DataFrame(data[data['countriesAndTerritories']==c].iloc[::-1])
country['rol'] = country.cases.rolling(20).mean()
country['rolD'] = country.deaths.rolling(20).mean()

# Main Board
###################
### Cases
cases=go.Figure(data=[go.Bar(x=country['dateRep'],y=country['cases'],name='Cases',    marker={'color':'rgb(65,105,225)'},),
	go.Scatter(x=country['dateRep'], y=country.rol,name='R=20')])
cases.update_layout(
	title="Covid-19 Cases",
	xaxis_title="Date",
	yaxis_title="No. of Cases",
	template='plotly_dark',
	height=450,
	width=900
)
#### Deaths
deaths=go.Figure(data=[go.Bar(x=country['dateRep'],y=country['deaths'],name='Deaths'),
	go.Scatter(x=country['dateRep'], y=country.rolD,name='R=20')])
deaths.update_layout(
	title="Covid-19 Deaths",
	xaxis_title="Date",
	yaxis_title="No. of Cases",
	template='plotly_dark',
	height=450,
	width=900,
)

####### add radio selection to sidebar
st.sidebar.text("   ")
radio = st.sidebar.radio("What would you like the graph to display?",['Cases','Deaths'])
if(radio == 'Cases'):
	st.plotly_chart(cases)
elif('Deaths'):
	st.plotly_chart(deaths)

st.sidebar.write("***Total Cases:***",country['cases'].sum())
st.sidebar.write("***Total deaths:***",country['deaths'].sum())
st.sidebar.text("* * *")

#st.sidebar.write("Total Cases: " ,country['cases'].sum())
#st.sidebar.plotly_chart(f,)

######## Cumulative_number_for_14_days_of_COVID
cumulative_14=px.line(x=country['dateRep'],y=country['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000'],
			 template='plotly_dark',color=country['countryterritoryCode'])
cumulative_14.update_layout(
	title="Cumulative Number For 14 days of COVID-19 cases per 100,000",
	xaxis_title="Date",
	yaxis_title="Cumulative Per 100,000",
	template='plotly_dark',
	height=400,	width=900,
)
st.markdown('The below graph displays the cumulative number for 14 days of COVID-19 cases per 100,000 people')
##### Visualize cumulative_14 line chart
st.plotly_chart(cumulative_14)


## Global Cases - Line chart using Plotly Graph Objects
groupedData=data.groupby('month')[['cases']].sum()
groupedData=groupedData[:10]
f=go.Figure(go.Scatter(x=groupedData.index,y=groupedData['cases'],mode='lines+markers',))
f.update_layout(
	title="Global Cases by Month",
	xaxis_title="Month",
	yaxis_title="Cases",
	template='plotly_dark'
)
## Visualize
#st.plotly_chart(f)
st.sidebar.write("***Global Cases:***",groupedData['cases'].sum())

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {920}px;
        padding-top: {1}rem;
        padding-right: {1}rem;
        padding-left: {1}rem;
        padding-bottom: {1}rem;
    }}
    .reportview-container .main {{
        
    }}
</style>
""",
        unsafe_allow_html=True,
    )
#st.sidebar.plotly_chart(f)






