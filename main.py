#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    # Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast' : 'center'}
        )
    ]),
    
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast' : 'center'}
        )),
    
    # Add an inner division to display the output
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ]),
])

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

# Define the callback function to update the output container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Automobile sales fluctuate over Recession Period (year wise)"))
        
        #Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        # Calculate average number of vehicles sold by vehicle type
        average_num = recession_data.groupby('Vehicle_Type')['Number_Sold'].mean().reset_index()
        Av_chart2 = dcc.Graph(
            figure=px.Bar(average_num, 
                x='Vehicle_Type', 
                y='Number_Sold',  # Corrected x-axis
                title="Average Vehicle Sales by Type (Recession Period)")
)


        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1)]),
            # Rest of your code for other plots...
        ]
    elif selected_statistics == 'Yearly Statistics':
        # Filter the data for the selected year
        yearly_data = data[data['Year'] == selected_year]
        
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, 
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile sales for the whole period"))
        
        # Rest of your code for other plots...
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1)]),
            # Rest of your code for other plots...
        ]

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
