import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout_content import PrepareLayoutContent

class CreateLayout:
    def __init__(self,df):
        self.content = PrepareLayoutContent(df)
        self.app_layout = None
        self.navbar = None

    def generate_layout(self):
        case_death_tabs = self.content.create_world_cards()
        case_death_md = self.content.get_case_markdown()
        cases_bar_div, deaths_bar_div = self.content.create_bar_plots()
        table = self.content.create_table()
        dropdown = self.content.create_drpdown()

        self.navbar = self.content.create_navbar()

        self.app_layout =[
                    self.navbar,
                    dbc.Row(
                        dbc.Col(case_death_tabs, align='center')
                    ),

                    dbc.Row(
                        dbc.Col(case_death_md, width = {'size': 10, 'offset': 2})
                        ),

                    dbc.Row(
                        [
                            dbc.Col(cases_bar_div, width = {'size': 6, 'order': 1}),
                            dbc.Col(deaths_bar_div, width={'size': 6, 'order': 2})
                        ],
                        ),

                    dbc.Row(
                        dbc.Col(table, width={'size': 12})
                        ),

                    dbc.Row(
                        dbc.Col(dropdown, width={'size': 5}),

                            ),
                    dbc.Row(
                        dbc.Col(dcc.Graph(id='countryGraph'), width={'size': 12})
                    )
                ]

    def get_home_grid(self):
        if self.app_layout ==None:
            self.generate_layout()
        return self.app_layout