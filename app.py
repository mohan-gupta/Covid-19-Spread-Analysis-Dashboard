import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
import plotly.express as px
from dash.dependencies import Input,Output
import datetime
import plotly.graph_objects as go

#----------------------------------------------------------------------------------------------------------
#Reading the data
link = r'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(link)
print('data set extracted')

#Data Pre-Processing
def data_preProcess(df):
    # extracting useful columns
    cols = ['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases',
            'total_deaths', 'new_deaths', 'population']
    df = df[cols]

    # Extracting records where continent is not missing
    df2 = df[~df['continent'].isnull()]

    #filling null data with 0
    df3 = df2.fillna(0)

    #renaming colums
    df3.rename(columns={'location':'country',
                        'new_cases':'cases','new_deaths':'deaths'},inplace=True)

    #converting date to datetime
    df3['date'] = pd.to_datetime(df3['date'])


    return df3

df = data_preProcess(df)

#----------------------------------------------------------------------------------------------------------
#Reading unique countries and generating list of options
countries_option = [{'label':i,'value':i} for i in df['country'].unique()]

#----------------------------------------------------------------------------------------------------------

####-------------------------- FUNCTIONS TO PLOT GRAPHS----------------------------------------------------

#----------------------------Function to plot world map---------------------------------------------------
def map_cases_deaths(df,feature):
    country_cases = df.groupby(['iso_code',
                                'country'],
                               as_index=False)[feature].sum()

    fig = px.choropleth(country_cases,
                        locations="iso_code",
                        color=feature,
                        hover_name="country",color_continuous_scale=px.colors.sequential.Jet)

    fig.update_layout(title = {'text':'Total {}'.format(feature.title()),
                                   'y':0.95,
                                   'x':0.5,
                                   'xanchor': 'center',
                                   'yanchor': 'top'})
    return fig

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------- Function to bar plots ------------------------------------------------

def plot_pct(df,feature,show_all=False):
    feature_each = df.groupby('country',as_index=False)[feature].sum()
    feature_each[feature] = round(100*feature_each[feature]/feature_each[feature].sum(),2)

    feature_each = feature_each.sort_values(by=feature,ascending=False)
    if show_all:
        fig = px.bar(feature_each,x='country',y=feature,
                 color=feature,title='{}'.format(feature.title()))
    else:
        fig = px.bar(feature_each.iloc[:10],x='country',y=feature,
                     color=feature,title='{}'.format(feature.title()))
    fig.update_layout(xaxis_title='Countries',
                     yaxis_title='Percent {} (%)'.format(feature))
    return fig

#----------------------------------------------------------------------------------------------------------
##----------------------------------- function to get dataFrame for days ----------------------------------
def get_data(df,period):
    '''date can be 0,1,7,14
                0: for Total,
                1: for 24 hrs,
                7: for last 7 days,
                14: for last 14 days'''
    last_rcrd_date = df['date'].max()
    if period == 0:
        df_date = df
    elif period == 1:
        last_24hrs = pd.to_datetime(last_rcrd_date - datetime.timedelta(1))
        df_date = df[df['date'] == last_24hrs]

    else:
        dates = pd.date_range(end=last_rcrd_date, periods=period, freq='1D')
        df_date = df[df['date'].isin(dates)]

    new_df = df_date.groupby('country', as_index=False).agg({'cases': 'sum', 'deaths': 'sum'})
    new_df = new_df.sort_values(by='cases', ascending=False)

    master_df = pd.merge(new_df, df_date.loc[:, ['iso_code', 'country', 'continent', 'population']], on='country',
                         how='right')
    master_df = master_df.drop_duplicates()
    master_df = master_df.reset_index(drop=True)

    master_df = master_df.sort_values(by='cases', ascending=False, ignore_index=True)
    master_df.insert(loc=0, column='#', value=master_df.index + 1)

    return master_df

#-----------------------------------------------------------------------------------------------------------------
####---------------------------------Function for DF to  data Table-----------------------------------------------

def to_dataTable(df,idt):
    data_table = dt.DataTable(
                            id=idt,
                            style_cell={
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'textAlign': 'center',
                                        'minwidth':95,
                                        'maxwidth':95,
                                        'width':95
                                    },
                            fixed_rows={'headers': True},
                            style_table={'height': '333px'},
                            style_header={
                                'fontWeight': 'bold',
                                'height':40,
                                'fontSize':20
                            },
                            data=df.to_dict('records'),
                            columns=[{"name": i.title(), "id": i} for i in df.columns],
                            sort_action="native",
                            page_action='none'
                        )
    return data_table

#----------------------------------------------------------------------------------------------------------
##------------------------------------------------ MarkDown------------------------------------------------

title = """# Covid-19 Spread Analysis"""

fmt_case =format(df['cases'].sum(),',')
fmt_death =format(df['deaths'].sum(),',')

cas_dth = """#### Globally There have been ```{} confirmed Cases``` and ```{} confirmed Deaths``` """.format(
    fmt_case,fmt_death)



#----------------------------------------------------------------------------------------------------------
#---------------------------------------------- Data frames -----------------------------------------------
df_total  =get_data(df,0)
df_24 = get_data(df,1)
df_7 = get_data(df,7)
df_14 = get_data(df,14)

#----------------------------------------------------------------------------------------------------------
#--------------------------------------------- Data Table -------------------------------------------------
dt_total = to_dataTable(df_total,'0')
dt_24 = to_dataTable(df_24,'24')
dt_7 = to_dataTable(df_7,'7')
dt_14 = to_dataTable(df_14,'14')


#----------------------------------------------------------------------------------------------------------
#---------------------------------------------- BOOTSTRAP CARDS--------------------------------------------

#------------------------------------------Card for World Maps---------------------------------------------

world_cases = dbc.Card(dcc.Graph(id = 'wordMap_cases',figure = map_cases_deaths(df,'cases')))
world_deaths = dbc.Card(dcc.Graph(id = 'wordMap_deaths',figure = map_cases_deaths(df,'deaths')))

#----------------------------------------------------------------------------------------------------------
#----------------------------------- Card For Cases (Barplot) ---------------------------------------------

cd_grph_cases = dbc.Card(dcc.Graph(
                                id='wordBar_cases',
                                figure = plot_pct(df,'cases')),
                                body=True)
#----------------------------------------------------------------------------------------------------------
# --------------------------------- Card For Deaths (Barplot) ---------------------------------------------

cd_grph_deaths = dbc.Card(dcc.Graph(
                                id='wordBar_deaths',
                                figure = plot_pct(df,'deaths')),
                                body=True)

#----------------------------------------------------------------------------------------------------------
#---------------------------------------- Card to Hold Tables ---------------------------------------------

cntnt_total = dbc.Card(dt_total)
cntnt_24 = dbc.Card(dt_24)
cntnt_7 = dbc.Card(dt_7)
cntnt_14 = dbc.Card(dt_14)

#----------------------------------------------------------------------------------------------------------
#------------------------------------Card to hold the tabs for tables--------------------------------------

Cardtabs = dbc.Card([
                    dbc.CardHeader(
                            dbc.Tabs(
                                    children=[
                                            dbc.Tab(label='Total',tab_id='totalTab',label_style={'fontWeight': 'bold'}),
                                            dbc.Tab(label='24 Hrs',tab_id='24Tab',label_style={'fontWeight': 'bold'}),
                                            dbc.Tab(label='7 Days',tab_id='7Tab',label_style={'fontWeight': 'bold'}),
                                            dbc.Tab(label='14 Days',tab_id='14Tab',label_style={'fontWeight': 'bold'}),
                                            ],
                                    id='tabTables',
                                    card=True,
                                    active_tab='totalTab'
                                )),
                    dbc.CardBody(html.Div(id="table-content")),
                    ],style={'padding':3})

#----------------------------------------------------------------------------------------------------------
####------------------------------- Initialising App ------------------------------------------------------

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

#----------------------------------------------------------------------------------------------------------
#this allows dash to understand that we are deploying this to a server
#server = app.server
#----------------------------------------------------------------------------------------------------------
######------------------------------------ App Layout------------------------------------------------------
app_layout =[
            dbc.Row(
                    dbc.Col(dcc.Markdown(title), width={'size': 6})
                    ),

            dbc.Row(
                dbc.Col(dbc.Tabs(
                    [
                        dbc.Tab(world_cases, label='Cases', label_style={'fontWeight': 'bold'},tab_id='world_cases'),
                        dbc.Tab(world_deaths, label='Deaths', label_style={'fontWeight': 'bold'},tab_id='world_deaths')
                    ],
                    active_tab='world_cases'
                ), align='center')
            ),

            dbc.Row(
                dbc.Col(dcc.Markdown(cas_dth), width={'size': 10, 'offset': 2})
                ),

            dbc.Row(
                [
                    dbc.Col(html.Div(cd_grph_cases), width={'size': 6, 'order': 1}),
                    dbc.Col(html.Div(cd_grph_deaths), width={'size': 6, 'order': 2})
                ],
                ),

            dbc.Row(
                dbc.Col(Cardtabs, width={'size': 12})
                ),

            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(id='country_dropdown', options=countries_option,
                                value=['India'], multi=True),
                    width={'size': 5}
                    )
                ),
            dbc.Row(dbc.Col(dcc.Graph(id='countryGraph'), width={'size': 12}))
        ]

#----------------------------------------------------------------------------------------------------------
######------------------------------------ Setting App Layout----------------------------------------------
app.layout = html.Div([dcc.Interval(
                        n_intervals=0,
                        interval=2*60*60*1000,   # Updates every 2hrs
                        id='interval_component'
                    ),
                html.Div(app_layout,
                         id='Lat=youtDiv')],
                              id='main_div')

#----------------------------------------------------------------------------------------------------------
####------------------------------------------ CallBacks--------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

#-----------------------------------------Callback to Live update app -----------------------------------------
@app.callback(Output('LayoutDiv','children'),
              [Input('interval_component','n_interval')])
def updateLayout(n):
    global df
    global link
    df = pd.read_csv(link)
    df = data_preProcess(df)
    layout = app_layout
    return layout

#---------------------------------------------------------------------------------------------------------
#call back to update table content on tab selection
@app.callback(Output("table-content", 'children'),
              [Input('tabTables', "active_tab")])
def render_content(tab):
    if tab == 'totalTab':
        return cntnt_total
    elif tab == '24Tab':
        return cntnt_24
    elif tab == '7Tab':
        return cntnt_7
    elif tab == '14Tab':
        return cntnt_14

#---------------------------------------------------------------------------------------------------------
#call back to get country data

@app.callback(Output('countryGraph','figure'),
              [Input('country_dropdown','value')])
def render_country(countries):
    global  df
    fig = go.Figure()
    for c in countries:
        dff = df.loc[df['country']==c]
        fig.add_trace(go.Scatter(x=dff['date'],y=dff['cases'],fill='tozeroy',name=c))
    fig.update_xaxes(rangeslider_visible=True)
    return fig

#----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server()
