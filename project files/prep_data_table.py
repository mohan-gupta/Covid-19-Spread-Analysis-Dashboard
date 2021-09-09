import pandas as pd
import dash_table as dt
import datetime

class CreateDataTable:
    def __init__(self,df):
        self.df = df

    def get_data(self,period):
        '''period can be 0,1,7,14
                    0: for Total,
                    1: for 24 hrs,
                    7: for last 7 days,
                    14: for last 14 days'''
        self.df['date'] = pd.to_datetime(self.df['date'])
        last_rcrd_date = pd.to_datetime(self.df['date'].max())
        if period == 0:
            df_date = self.df
        elif period == 1:
            last_24hrs = pd.to_datetime(last_rcrd_date - datetime.timedelta(1))
            df_date = self.df[self.df['date'] == last_24hrs]

        else:
            dates = pd.date_range(end=last_rcrd_date, periods=period, freq='1D')
            df_date = self.df[self.df['date'].isin(dates)]

        new_df = df_date.groupby('country', as_index=False).agg({'cases': 'sum', 'deaths': 'sum'})
        new_df = new_df.sort_values(by='cases', ascending=False)

        master_df = pd.merge(new_df, df_date.loc[:, ['iso_code', 'country', 'continent', 'population']], on='country',
                             how='inner')
        master_df = master_df.drop_duplicates()
        master_df = master_df.reset_index(drop=True)

        master_df = master_df.sort_values(by='cases', ascending=False, ignore_index=True)
        master_df.insert(loc=0, column='#', value=master_df.index + 1)

        return master_df

    def to_dataTable(self,period_df, idt):
        data_table = dt.DataTable(
                                id=idt,
                                style_cell={
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'textAlign': 'center',
                                            'minwidth':95,
                                            'maxwidth':95,
                                            'width':95,
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'color': 'white'
                                        },
                                fixed_rows={'headers': True},
                                style_table={'height': '333px'},
                                style_header={
                                    'backgroundColor': 'rgb(0, 0, 0)',
                                    'fontWeight': 'bold',
                                    'height':40,
                                    'fontSize':20
                                },
                                data = period_df.to_dict('records'),
                                columns=[{"name": i.title(), "id": i} for i in period_df.columns],
                                sort_action="native",
                                page_action='none'
                            )
        return data_table

    #funnction to return the datatables
    def get_data_tables(self):
        self.total = self.get_data(0)
        self.hour_24 = self.get_data(1)
        self.day_7 = self.get_data(7)
        self.day_14 = self.get_data(14)

        dt_total = self.to_dataTable(self.total,'0')
        dt_24 = self.to_dataTable(self.hour_24,'1')
        dt_7 = self.to_dataTable(self.day_7, '7')
        dt_14 = self.to_dataTable(self.day_14, '14')

        return dt_total, dt_24, dt_7, dt_14