# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

options_list = [{'label': 'All Sites', 'value': 'ALL'}] + \
               [{'label': i, 'value': i} for i in spacex_df['Launch Site'].drop_duplicates()]
# Create dropdown options
options_list = [{'label': i, 'value': i} for i in spacex_df['Launch Site'].drop_duplicates()]
options_list.insert(0, {'label': 'All Sites', 'value': 'ALL'})


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=options_list,
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload],
                                                marks={i: str(i) for i in range(0, 10001, 2500)},
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = filtered_df[filtered_df['class'] == 1]
        fig = px.pie(filtered_df, values='class',
            names='Launch Site',
            title='Fraction of Launch Success By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        filtered_df = filtered_df['class'].value_counts()
        fig = px.pie(filtered_df, values='class',
                     names=filtered_df.index,
                     title='Success of ' + entered_site)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")],
              )
def get_scatter_chart(site, payload_range):
    filtered_df = spacex_df
    filtered_df = filtered_df[filtered_df["Payload Mass (kg)"] >= payload_range[0]]
    filtered_df = filtered_df[filtered_df["Payload Mass (kg)"] <= payload_range[1]]
    if site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title='Payload Mass (kg) vs. Success: All Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df["Launch Site"] == site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title='Payload vs. Success: ' + site)
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
