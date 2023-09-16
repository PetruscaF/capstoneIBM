# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site_dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC', 'value': 'CCAFS SLC-40'},
                                ],
                                value='ALL',
                                placeholder="Select a launch site",
                                searchable=True
                                ),
                                html.Br(),
                                                                                                
                                # return the outcomes piechart for a selected site
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(0, 10000, 1000, id='payload_slider', value=[0, 10000])
                                ,

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    
    filtered_df = spacex_df.loc[spacex_df['Launch Site'].isin([site_dropdown])]
    
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
    else:
        fig = px.pie(filtered_df, 
        names= 'class', 
        title=f'Total success launches for site {site_dropdown}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'), 
    Input(component_id='site_dropdown', component_property='value'),
    Input(component_id="payload_slider", component_property="value"))
def get_scatter_chart(site_dropdown,payload_slider):
    
    filtered_df = spacex_df.loc[spacex_df['Launch Site'].isin([site_dropdown])] 
    
    low, high = payload_slider
    mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
    mask2 = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    if site_dropdown == 'ALL':
        fig = px.scatter(
        spacex_df[mask2], x='Payload Mass (kg)', y='class', 
        color="Booster Version Category", 
        title='Corralation between Payload and Success for all sites',
        hover_data=['Payload Mass (kg)'])
        return fig
    else:
        fig = px.scatter(
        filtered_df[mask], x='Payload Mass (kg)', y='class', 
        color="Booster Version Category",
        title=f'Corralation between Payload and Success for {site_dropdown}',
        hover_data=['Payload Mass (kg)'])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
