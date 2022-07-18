from dash import dcc
import dash_bootstrap_components as dbc
from layout_content import PrepareLayoutContent

class CreateLayout:
    def __init__(self,df):
        self.content = PrepareLayoutContent(df)
        self.app_layout = None
        self.navbar = None

    def generate_layout(self):
        case_death_tabs = self.content.create_world_cards()
        pie_case_death_tabs = self.content.create_pie_chart()
        bar_tabs = self.content.get_bar_plots_cards()
        dropdown = self.content.create_drpdown()

        self.navbar = self.content.create_navbar()

        self.app_layout =[
                    self.navbar,
                    dbc.Row([
                        dbc.Col(case_death_tabs, align='left',
                                xs=12, sm=12, md=12, lg=6, xl=6),
                        dbc.Col(dbc.Col(pie_case_death_tabs, align="right"),
                                xs=12, sm=12, md=12, lg=6, xl=6),
                    ]),
                    dbc.Row(
                        dbc.Col(bar_tabs, align="right",
                                xs=12, sm=12, md=12, lg = 14, xl = 12)
                    ),
                    dbc.Row(
                        dbc.Col(dropdown, width={'size': 12},
                                xs=10, sm=8, md=8, lg = 14, xl = 12)
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.Tabs(
                                [
                                    dbc.Tab(dcc.Graph(id='country_cases_Graph',responsive = True), label='Cases',
                                            label_style={'fontWeight': 'bold'},
                                            tab_id='daily_cases'),
                                    dbc.Tab(dcc.Graph(id='country_deaths_Graph',responsive = True), label='Deaths',
                                            label_style={'fontWeight': 'bold'},
                                            tab_id='daily_deaths')
                                ],
                                active_tab='daily_cases'
                        )
                            , width={'size': 12},
                            xs=12, sm=12, md=12, lg = 12, xl = 12
                        )
                    )
                ]

    def get_home_grid(self):
        if self.app_layout ==None:
            self.generate_layout()
        return self.app_layout