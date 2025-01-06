import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import datetime as dt

# Read the wildfire data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

years=df['Year'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Build dash app layout
app.layout = html.Div(children=[ html.H1('Australia Wildfire Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),
                                html.Div([html.Div([html.H2('Select Region:', style={'margin-right': '2em'}), 
                                                     dcc.RadioItems([{"label":"New South Wales","value": "NSW"},
                                                                     {"label":"Northern Territory","value": "NT"},
                                                                     {"label":"Queensland","value": "QL"},
                                                                     {"label":"South Australia","value": "SA"},
                                                                     {"label":"Tasmania","value": "TA"},
                                                                     {"label":"Victoria","value": "VI"},
                                                                     {"label":"Western Australia","value": "WA"}], 
                                                                    value = "New South Wales", id='input-region',inline=True)]),
                                        html.Div([html.H2('Select Year:', style={'margin-right': '2em'}),
                                                  dcc.Dropdown(years, value = "2005", id='input-year')
                                                ]),
                                         html.Div([html.Div([ ], id='pie-plot'), #add two empty divisions
                                                   html.Div([ ], id='bar-plot')],
                                                   style={'display': 'flex'}),
    ])
    #outer division ends
])
#layout ends
#TASK 2.4: Add the Ouput and input components inside the app.callback decorator.
#Place to add @app.callback Decorator
@app.callback([Output(component_id='pie-plot', component_property='children'),
               Output(component_id='bar-plot', component_property='children')],
               [Input(component_id='input-region', component_property='value'),
                Input(component_id='input-year', component_property='value')])
   
#TASK 2.5: Add the callback function.
#Place to define the callback function .
def reg_year_display(input_region,input_year):
    
    #data
   region_data = df[df['Region'] == input_region]
   y_r_data = region_data[region_data['Year']==input_year]
    #Plot one - Monthly Average Estimated Fire Area
   
   est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
   fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month', title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year))
   
     #Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
   veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
   fig2 = px.bar(veg_data, x='Month', y='Count', title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year))
    
   return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2) ]

# Run the app
if __name__ == '__main__':
    app.run_server()