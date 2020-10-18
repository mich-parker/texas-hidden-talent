import streamlit as st
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

countylist = []
fipslist = []

# ONLY TX PLEASE
list1 = counties.get('features')
# print(list1)
for i in list(list1):
    prop = i.get('properties')
    curr = prop.get('STATE')
    fip = prop.get('STATE') + prop.get('COUNTY')
    county = prop.get('NAME')
    countylist.append(county)
    fipslist.append(fip)
    if curr != '48':
        list1.remove(i)

counties['features'] = list1

import pandas as pd
names = pd.DataFrame()
names['County Name'] = countylist
names['fips'] = fipslist


df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

df = pd.merge(names, df, on='fips', how='right')
print(df.head())

import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 31.9686, "lon": -99.9018},
                           opacity=0.5,
                           labels={'unemp':'Value'}, hover_data=['County Name']
                          )

# fig.update_traces(hovertemplate='County: ' + df['County Name'] + '<br>Michaela\'s Awesomeness: {}')

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig)