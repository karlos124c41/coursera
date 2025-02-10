# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import wget
import webbrowser
from threading import Timer
import os

# Define the port number
port = 8050

def open_browser():
    """
    Opens the web browser to the dashboard
    """
    webbrowser.open_new(f'http://localhost:{port}')

# Download and read the spacex data
if not os.path.exists('spacex_launch_dash.csv'):
    spacex_csv_file = wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get payload range
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    html.Div([
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
        )
    ]),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Add a slider to select payload range
    html.P("Payload range (Kg):"),
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={
                0: '0 kg',
                2500: '2500',
                5000: '5000',
                7500: '7500',
                10000: '10000'
            },
            value=[min_payload, max_payload]
        )
    ]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function for the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Calculate success counts for all sites
        fig = px.pie(
            spacex_df, 
            values='class',
            names='Launch Site', 
            title='Total Success Launches By Site'
        )
    else:
        # Filter data for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        
        # Create pie chart for success vs. failure
        fig = px.pie(
            success_counts, 
            values='count', 
            names='class',
            title=f'Success vs Failure for {entered_site}',
            labels={'class': 'Outcome', '1': 'Success', '0': 'Failure'}
        )
    return fig

# TASK 4: Add a callback function for the scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    # Filter by payload range
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & \
           (spacex_df['Payload Mass (kg)'] <= high)
    df = spacex_df[mask]

    if entered_site == 'ALL':
        # Create scatter plot for all sites
        fig = px.scatter(
            df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Success for All Sites',
            labels={'class': 'Launch Outcome (0=Failure, 1=Success)'}
        )
    else:
        # Filter by site and create scatter plot
        filtered_df = df[df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Success for {entered_site}',
            labels={'class': 'Launch Outcome (0=Failure, 1=Success)'}
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    # Open the browser after a short delay
    Timer(1, open_browser).start()
    
    # Run the server with specific host and port
    app.run_server(debug=True, host='localhost', port=port)