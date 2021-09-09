import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from get_plots import Plots
from prep_data_table import CreateDataTable

class PrepareLayoutContent:
    def __init__(self, df):
        self.df = df
        self.plots = Plots(self.df)
        self.tables = CreateDataTable(self.df)
        self.app_layout = None
        self.cntnt_total = None
        self.cntnt_24 = None
        self.cntnt_7 = None
        self.cntnt_14 = None

    def create_navbar(self):
        title = """### Covid-19 Spread Analysis"""

        word_link = html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand(
                        dcc.Markdown(title, style={'color': 'rgb(38, 221, 237)'}),
                        className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            id="world_layout",
            href="/",
        )

        navbar = dbc.Navbar(
            [
                word_link,
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            ],
            id="navbar",
            color="dark",
            dark=True,
        )
        return navbar

    def create_world_cards(self):
        world_cases_map = dbc.Card(
            dcc.Graph(
                id='wordMap_cases',
                figure= self.plots.map_cases_deaths('cases')
            )
        )
        world_deaths_map = dbc.Card(
            dcc.Graph(
                id='wordMap_deaths',
                figure= self.plots.map_cases_deaths('deaths')
            )
        )

        case_death_tabs = dbc.Tabs(
            [
                dbc.Tab(world_cases_map, label='Cases', label_style={'fontWeight': 'bold'},
                        tab_id='world_cases'),
                dbc.Tab(world_deaths_map, label='Deaths', label_style={'fontWeight': 'bold'},
                        tab_id='world_deaths')
            ],
            active_tab='world_cases'
        )

        return case_death_tabs

    def get_case_markdown(self):

        fmt_case = format(self.df['cases'].sum(), ',')
        fmt_death = format(self.df['deaths'].sum(), ',')

        case_death = """#### Globally There have been ```{} confirmed Cases``` and ```{} confirmed Deaths``` """.format(
            fmt_case, fmt_death)

        case_death_md = dcc.Markdown(case_death)

        return case_death_md

    def create_bar_plots(self):
        # - Card For Cases (Barplot)

        cases_bar = dbc.Card(dcc.Graph(
            id='wordBar_cases',
            figure = self.plots.plot_pct('cases')),
            body=True)

        cases_bar_div = html.Div(cases_bar)

        # - Card For Deaths (Barplot)

        deaths_bar = dbc.Card(dcc.Graph(
            id='wordBar_deaths',
            figure = self.plots.plot_pct('deaths')),
            body=True)

        deaths_bar_div = html.Div(deaths_bar)

        return cases_bar_div, deaths_bar_div

    def create_table_tabs(self):
        card_header = dbc.CardHeader(
                dbc.Tabs(
                    children=[
                        dbc.Tab(label='Total', tab_id='totalTab', label_style={'fontWeight': 'bold'}),
                        dbc.Tab(label='24 Hrs', tab_id='24Tab', label_style={'fontWeight': 'bold'}),
                        dbc.Tab(label='7 Days', tab_id='7Tab', label_style={'fontWeight': 'bold'}),
                        dbc.Tab(label='14 Days', tab_id='14Tab', label_style={'fontWeight': 'bold'}),
                    ],
                    id='tabTables',
                    card=True,
                    active_tab='totalTab'
                )
            )
        return card_header

    def get_table_tabs_body(self):
        dt_total, dt_24, dt_7, dt_14 = self.tables.get_data_tables()

        self.cntnt_total = dbc.Card(dt_total)
        self.cntnt_24 = dbc.Card(dt_24)
        self.cntnt_7 = dbc.Card(dt_7)
        self.cntnt_14 = dbc.Card(dt_14)

        return self.cntnt_total, self.cntnt_24, self.cntnt_7, self.cntnt_14

    def create_table(self):
        table_header  = self.create_table_tabs()
        table_cntnt, _, _, _ = self.get_table_tabs_body()

        table = dbc.Card(
            [
                table_header,
                dbc.CardBody(html.Div(id="tableContent")),
            ],
            style={'padding': 3})

        return table

    def create_drpdown(self):
        # Reading unique countries and generating list of options for dropdown
        countries_option = [{'label': i, 'value': i} for i in self.df['country'].unique()]

        # drodown Menu
        dropdown = html.Div(dcc.Dropdown(id='country_dropdown',
                                         options=countries_option,
                                         value=['India'], multi=True,
                                         style={'background-color': 'rgb(30, 30, 30)'}
                                         )
                            )
        return dropdown
