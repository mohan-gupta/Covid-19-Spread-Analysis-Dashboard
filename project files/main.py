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

#-- call back to update table content on tab selection
@app.callback(Output("tableContent", 'children'),
              [Input('tabTables', "active_tab")])
def render_content(tab):
    global initializer

    table = initializer.get_table_content()
    cntnt_total, cntnt_24, cntnt_7, cntnt_14 = table.get_table_tabs_body()
    if tab == 'totalTab':
        return cntnt_total
    elif tab == '24Tab':
        return cntnt_24
    elif tab == '7Tab':
        return cntnt_7
    elif tab == '14Tab':
        return cntnt_14

#-- call back to get country data
@app.callback(Output('countryGraph','figure'),
              [Input('country_dropdown','value')])
def render_country(countries):
    global initializer

    plot = initializer.get_plot()
    fig = plot.plot_area(countries)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)