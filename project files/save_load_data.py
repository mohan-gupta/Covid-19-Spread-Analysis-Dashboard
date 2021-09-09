import numpy as np
import pandas as pd

class ProcessData:
    def __init__(self):
        self.link = r'https://covid.ourworldindata.org/data/owid-covid-data.csv'
        self.local = 'data/covid_data.csv'
        self.df = None

    def read_data(self):
        """Reads the data from the link and saves it as csv file"""
        self.df = pd.read_csv(self.link)
        print("Data-Set Extracted")

    def pre_process_data(self):
        """Cleaning and formatting the data set"""

        # extracting useful columns
        cols = ['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases',
                'total_deaths', 'new_deaths', 'population']

        df = self.df[cols]

        # Extracting records where continent is not missing
        df2 = df[~df['continent'].isnull()]

        # filling null data with 0
        df3 = df2.fillna(0)

        # renaming colums
        df3.rename(columns={'location': 'country',
                            'new_cases': 'cases', 'new_deaths': 'deaths'}, inplace=True)

        df3['cases'] = np.absolute(df3['cases'])
        df3['deaths'] = np.absolute(df3['deaths'])

        # converting date to datetime
        df3['date'] = pd.to_datetime(df3['date'])

        return df3

    def save_data(self):
        #first pre process the data
        if self.df==None:
            self.read_data()
        self.df = self.pre_process_data()

        # Saving the data
        self.df.to_csv(self.local, index=False)

    def load_data(self):
        df = pd.read_csv(self.local)
        return df
