from dash import html, dcc
from save_load_data import ProcessData
from app_layout_grid import CreateLayout
from layout_content import PrepareLayoutContent
from get_plots import Plots

class App:
    def __init__(self):
        self.process_data = ProcessData()
        self.process_data.save_data()

        self.df = self.process_data.load_data()

        self.layout = CreateLayout(self.df,)

        self.app_grid = self.layout.get_home_grid()

        self.table_content = PrepareLayoutContent(self.df)

        self.plots = Plots(self.df)

    def get_app_layout(self):
        app_grid = html.Div(
            [
                dcc.Interval(
                    n_intervals=0,
                    interval=6 * 60 * 60 * 1000,  # Updates every 6hrs
                    id='interval_component'
                ),
                dcc.Location(id='url', refresh=False),
                html.Div(
                    children=self.app_grid,
                    id='LayoutDiv'
                )
            ],
            id='main_div')
        return app_grid

    def get_plot(self):
        return self.plots