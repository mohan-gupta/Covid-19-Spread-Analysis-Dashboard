from dash import html, dcc
import dash_bootstrap_components as dbc
from get_plots import Plots
from prep_data_frames import CreateDataFrames

class PrepareLayoutContent:
    def __init__(self, df):
        self.df = df
        self.plots = Plots(self.df)
        self.tables = CreateDataFrames(self.df)
        self.app_layout = None
        self.total, self.day1, self.day7, self.day14 = self.tables.get_data_frames()

    def get_case_card(self):
        fmt_case = format(self.df['cases'].sum(), ',')
        fmt_death = format(self.df['deaths'].sum(), ',')

        case_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Total Cases", className="card-title"),
                    html.H6(f"{fmt_case}", className="card-subtitle"),
                ]
            ),
            style={'width':'12rem', 'background-color': 'rgb(26, 24, 24)', 'border-width': 'medium'}, inverse=True,
        )

        death_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Total Deaths", className="card-title"),
                    html.H6(f"{fmt_death}", className="card-subtitle"),
                ],
            ),
            style={'width':'12rem', 'background-color': 'rgb(26, 24, 24)', 'border-width': 'medium'}, inverse=True,
        )

        return case_card, death_card

    def create_navbar(self):
        title = """### Covid-19 Spread Analysis"""

        cs_card, dth_card = self.get_case_card()

        word_link = html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand(
                        dcc.Markdown(title, style={'color': 'rgb(38, 221, 237)'}),
                        className="ml-2"),
                    xs = 10, sm = 10, md = 12, lg = 6, xl = 6)
                ],
                align="left",
            ),
            id="world_layout",
            href="/",
        )

        navbar = dbc.Navbar(
            [
                word_link,
                dbc.Row([
                    dbc.Col(xs = 0, sm = 0, md = 0, lg = 3, xl = 3, align="left"),
                    dbc.Col(cs_card, xs = 10, sm = 10, md = 10, lg = 3, xl = 3, align="left"),
                    dbc.Col(xs=0, sm=0, md=0, lg=3, xl=3, align="left"),
                    dbc.Col(dth_card, xs = 10, sm = 10, md = 10, lg = 3, xl = 3, align='right')
                    ],
                    align="right"
                ),
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
                figure= self.plots.map_cases_deaths('cases'),
                responsive = True
            )
        )
        world_deaths_map = dbc.Card(
            dcc.Graph(
                id='wordMap_deaths',
                figure= self.plots.map_cases_deaths('deaths'),
                responsive=True
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

    def get_bar_plots_cards(self):
        cases_total = dbc.Card(dcc.Graph(
            id='total_cases_bar',
            figure=self.plots.plot_bar(self.total,'Total')),
            style={'overflowY': 'scroll', 'height': 400}
        )

        cases_24 = dbc.Card(dcc.Graph(
            id='24_cases_bar',
            figure=self.plots.plot_bar(self.day1, '24H')),
            style={'overflowY': 'scroll', 'height': 400}
        )

        cases_7 = dbc.Card(dcc.Graph(
            id='7_cases_bar',
            figure=self.plots.plot_bar(self.day7, '7 Days')),
            style={'overflowY': 'scroll', 'height': 400}
        )

        cases_14 = dbc.Card(dcc.Graph(
            id='14_cases_bar',
            figure=self.plots.plot_bar(self.day14, '14 Days')),
            style={'overflowY': 'scroll', 'height': 400}
        )


        bar_tabs = dbc.Tabs(
            [
                dbc.Tab(cases_total, label='Total', label_style={'fontWeight': 'bold'},
                        tab_id='total'),
                dbc.Tab(cases_24, label='24H', label_style={'fontWeight': 'bold'},
                        tab_id='24h'),
                dbc.Tab(cases_7, label='7 Days', label_style={'fontWeight': 'bold'},
                        tab_id='7days'),
                dbc.Tab(cases_14, label='14 Days', label_style={'fontWeight': 'bold'},
                        tab_id='14days')
            ],
            active_tab='total'
        )
        return bar_tabs

    def create_pie_chart(self):
        # - Card For Cases (Barplot)

        cases_pie = dbc.Card(dcc.Graph(
            id='wordBar_cases',
            figure = self.plots.plot_pct('cases'),
            responsive = True)
        )

        # - Card For Deaths (Barplot)

        deaths_pie = dbc.Card(dcc.Graph(
            id='wordBar_deaths',
            figure = self.plots.plot_pct('deaths'),
            responsive = True)
            )

        case_death_tabs = dbc.Tabs(
            [
                dbc.Tab(cases_pie, label='Cases', label_style={'fontWeight': 'bold'},
                        tab_id='pct_cases'),
                dbc.Tab(deaths_pie, label='Deaths', label_style={'fontWeight': 'bold'},
                        tab_id='pct_deaths')
            ],
            active_tab='pct_cases'
        )

        return case_death_tabs


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
