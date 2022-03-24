import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from app_init import App


#loading all the contents of the WebApp
initializer = App()

#initializing the app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

#this tells the dash that we are running our app on a server
server = app.server

# Setting App Layout
app.layout =initializer.get_app_layout()


#Callbacks
@app.callback(Output('LayoutDiv','children'),
              [Input('interval_component','n_intervals')])
def updateLayout(n):
    #reload dataset
    global initializer
    initializer = App()
    layout = initializer.get_app_layout()
    return layout

#-- call back to get daily cases
@app.callback(Output('country_cases_Graph','figure'),
              [Input('country_dropdown','value')])
def render_country(countries):
    global initializer

    plot = initializer.get_plot()
    fig = plot.plot_area(countries, 'cases')
    return fig

#-- call back to get daily deaths
@app.callback(Output('country_deaths_Graph','figure'),
              [Input('country_dropdown','value')])
def render_country(countries):
    global initializer

    plot = initializer.get_plot()
    fig = plot.plot_area(countries, 'deaths')
    return fig

if __name__ == '__main__':
    app.run_server()