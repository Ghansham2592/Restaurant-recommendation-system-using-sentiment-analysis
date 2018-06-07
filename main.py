######################################################################################################################
##                                                                                                                  ##  
## This is main bokeh application file which imports business_data.txt file which has all the necessary data        ##
## Run this file using the command: bokeh serve --show main.py                                                      ##
##                                                                                                                  ##
######################################################################################################################

# Importing libraries
from bokeh.layouts import widgetbox, column, layout, row
from bokeh.models.widgets import Select
from bokeh.plotting import curdoc

from bokeh.models import ColumnDataSource, GMapOptions, WheelZoomTool, HoverTool
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.plotting import gmap

import pandas as pd
import json

# Select box data
select_data = json.load(open('./data/select_data.json'))

# Load business data, which is a exported tsv version of sql table
df = pd.read_csv('./data/business_data.txt', sep='\t', na_filter = False)
# Set the df as a working set, data in working set changes as per preferences
working_set = df

# Set up a google map
map_options = GMapOptions(lat=0, lng=0, map_type="roadmap", zoom=10)
google_mapview = gmap("AIzaSyDngsc8Jmb2EmBa6v6Sjiu-lDpVWQGgnr8", map_options, title="Restaurants", width= 500, height= 450)
map_source = ColumnDataSource(data=dict(lat=[],lon=[],name=[]))

# Set up a nested bar graph
nested_bar_source = ColumnDataSource(data=dict(x=[], counts=[]))
nested_bar = figure()

# Data source for table
source = ColumnDataSource(data=dict())

table = {
    'name': [],
    'address': [],
    'categories': [],
    'stars': [],
    'total_reviews': [],
    'lat': [],
    'long': []
}

def load():
    # Initial load
    country_select.value = "USA"
    updateCountry("", "", "")


def updateCountry(attr, old, new):
    # Update the values in the state select box as per the country selected
    if (country_select.value == 'USA'):
        state_select.options = select_data['country']['USA']
    elif (country_select.value == 'Canada'):
        state_select.options = select_data['country']['Canada']
    elif (country_select.value == 'Germany'):
        state_select.options = select_data['country']['Germany']
    elif (country_select.value == 'Scotland'):
        state_select.options = select_data['country']['Scotland']

    state_select.value = state_select.options[0];
    updateState("value", "", "")


def updateState(attr, old, new):
    # Update the values in the city select box as per the state selected
    value = state_select.value;
    cities = df.loc[df['state'] == select_data['state'][value]]
    cities = cities['city'].unique()
    city_select.options = list(cities)
    city_select.value = city_select.options[0]
    updateCity("", "", "")


def updateCity(attr, old, new):
    # Update the working set and load fields in the category select box
    global working_set
    value = city_select.value
    business = df.loc[df['city'] == value]

    business = business.sort_values(by=['score'], ascending = False)
    # Update categories
    category_list = set()
    for index, row in business.iterrows():
        cat = json.loads(row['categories'])
        row['categories'] = cat
        for i in range(len(cat)):
            if (cat[i] in select_data['categories']):
                category_list.add(cat[i])

    category_select.options = list(category_list)
    category_select.value = "Restaurants"
    working_set = business
    updateCategory("", "", "")


def updateCategory(attr, old, new):
    # Populate the table and graph with the preferences selected by the user
    global working_set
    value = category_select.value
    data = working_set[working_set['categories'].map(lambda x: value in x)]
    setTableData(data[:10])
    generateGraphData(data[:10])
    updateSource()
    updateMap()

def updateSource():
    # Update the table data source
    source.data = {
        'name': table['name'],
        'address': table['address'],
        'categories': table['categories'],
        'stars': table['stars'],
        'total_reviews': table['total_reviews']
    }


def updateNestedBar(data):
    # Update the nested bar graph source
    nested_bar_source.data = data


def updateMap():
    # Update the map, also change the view to selected city
    map_source.data = {
        'lat': table['lat'],
        'lon': table['long'],
        'name': table['name']
    }
    if (len(table['lat']) != 0):
        map_options.lat = table['lat'][0]
    if (len(table['long']) != 0):
        map_options.lng = table['long'][0]


def setTableData(business):
    # Update the local table dictionary which is eveuntually used to update table source
    table['name'] = []
    table['address'] = []
    table['categories'] = []
    table['stars'] = []
    table['total_reviews'] = []
    table['lat'] = []
    table['long'] = []
    for index, row in business.iterrows():
        table['name'].append(row['name'])
        table['address'].append(row['address'])
        table['categories'].append(', '.join(map(str, json.loads(row['categories']))))
        table['stars'].append(row['score'])
        table['total_reviews'].append(row['pos_count'] + row['neg_count'] + row['neutral_count'])
        table['lat'].append(row['latitude'])
        table['long'].append(row['longitude'])


def generateGraph(business_data = None):
    # Create a nested bar graph object 
    global nested_bar, nested_bar_source
    palette = ["#9FFF0F", "#E21500", "#FFDE0F"]
    sentiments = ['Pos', 'Neg', 'Neutral']
    graph_data = dict(x=[], counts=())
    updateNestedBar(graph_data)
    nested_bar = figure(x_range=[], plot_height=400, plot_width=800, title="% Sentiments for Restaurants",
               toolbar_location=None, tools="")

    nested_bar.vbar(x='x', top='counts', width=0.9, source=nested_bar_source, line_color="white",
           fill_color=factor_cmap('x', palette=palette, factors=sentiments, start=1, end=2))

    nested_bar.y_range.start = 0
    nested_bar.x_range.range_padding = 0.05
    nested_bar.xaxis.major_label_orientation = 1
    nested_bar.xgrid.grid_line_color = None


def generateGraphData(business_data):
    # Update the nested bar graph data
    sentiments = ['Pos', 'Neg', 'Neutral']
    business = []
    data = {
        'business' : business,
        'Positive'   : [],
        'Negative'   : [],
        'Neutral'   : []
    }
    i = 0
    for index, row in business_data.iterrows():
        total_reviews = row['pos_count'] + row['neg_count'] + row['neutral_count']
        business.append(str(i))
        i += 1
        data['Positive'].append((row['pos_count'] / total_reviews * 100))
        data['Negative'].append((row['neg_count'] / total_reviews * 100))
        data['Neutral'].append((row['neutral_count'] / total_reviews * 100))

    x = [ (b, sentiment) for b in business for sentiment in sentiments ]
    counts = sum(zip(data['Positive'], data['Negative'], data['Neutral']), ())
    nested_bar.x_range.factors = x
    updateNestedBar(dict(x=x, counts=counts))


# Select boxes for country, state, city and category
country_select = Select(title="Select the Country:", name="country", value="USA", options=["USA", "Canada", "Germany", "Scotland"])
country_select.on_change('value', updateCountry)

state_select = Select(title="Select the State:", name="state", value="All", options=["All"])
state_select.on_change('value', updateState)

city_select = Select(title="Select the City:", name="city", value="All", options=["All"])
city_select.on_change('value', updateCity)

category_select = Select(title="Select the Category:", name="Resturant", value="Restaurants", options=["Restaurants"])
category_select.on_change('value', updateCategory)


# Code to create table columns
columns = [
    TableColumn(field="name", title="Name", width=300),
    TableColumn(field="address", title="Address"),
    TableColumn(field="categories", title="Categories", width=1000),
    TableColumn(field="stars", title="Score", formatter = NumberFormatter(format= "0.[000]")),
    TableColumn(field="total_reviews", title="Total Reviews")
]

data_table = DataTable(source = source, columns=columns, width=900, height=280)

# Map location dots and hovertool
google_mapview.circle(x="lon", y="lat", size=11, fill_color="red", fill_alpha=0.8, source= map_source)
hover = HoverTool(tooltips=[
    ("Rank", "$index"),
    ("Name", "@name")
])

wheel_zoom = WheelZoomTool()
google_mapview.add_tools(wheel_zoom, hover)
google_mapview.toolbar.active_scroll = wheel_zoom

# Instantiate graph before using it in the layout
generateGraph()

# Create a layout
sizing_mode = 'fixed'
l = layout([
    row([column([country_select,state_select,city_select, category_select, ]),widgetbox(data_table)]),
    row([nested_bar,google_mapview])
], sizing_mode=sizing_mode)

# Initial load
load()

# Add the layout in the root of the application
curdoc().add_root(l)
curdoc().title = "Recommendation"
