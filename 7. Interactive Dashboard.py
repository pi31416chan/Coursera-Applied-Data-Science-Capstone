# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
path = "C:\\Users\\pi314\Learning\\Data Science\\IBM Data Science Professional Certificate\\10 Applied Data Science Capstone\\Project\\"
spacex_df = pd.read_csv(path+"7. spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

dropdownoptions = [{'label':'All Sites','value':'ALL'}]
[dropdownoptions.append({'label':x,'value':x}) for x in sorted(set(spacex_df['Launch Site']))]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=dropdownoptions,
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'),
)
def compute_graphs(site):
    if site == 'ALL':
        df_temp = spacex_df[spacex_df['class']==1]['Launch Site'].value_counts()
    else:
        df_temp = spacex_df[spacex_df['Launch Site'] == site].groupby('class')['Launch Site'].count()

    fig = px.pie(df_temp,
                names=df_temp.index,
                values=df_temp.values,
                color=df_temp.index,
                title='Total Success Launches By Site',)

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property='value')],
)
def compute_graphs(site,slidervalues):
    min = slidervalues[0]
    max = slidervalues[1]

    if site == 'ALL':
        df_temp = spacex_df[['Launch Site','Booster Version Category','Payload Mass (kg)','class']]
    else:
        df_temp = spacex_df[spacex_df["Launch Site"] == site][['Launch Site','Booster Version Category','Payload Mass (kg)','class']]
    df_temp = df_temp[(df_temp['Payload Mass (kg)'] > int(min)) & (df_temp['Payload Mass (kg)'] < int(max))]

    fig = px.scatter(df_temp,
                    x='Payload Mass (kg)',
                    y='class',
                    # color='Launch Site' if site == 'ALL' else df_temp['class'].apply(str).sort_values(),
                    color='Booster Version Category',
                    title='Correlation between Payload and Success for all Sites',)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()