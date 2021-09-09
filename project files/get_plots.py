import plotly.express as px
import plotly.graph_objects as go

class Plots:
    def __init__(self,df):
        self.df = df

    def map_cases_deaths(self,feature):
        country_wise = self.df.groupby(['iso_code',
                                    'country'],
                                   as_index=False)[feature].sum()
        if feature=='cases':
            color_scale = px.colors.sequential.Tealgrn
        else:
            color_scale = px.colors.sequential.Magenta

        fig = px.choropleth(country_wise,
                            locations="iso_code",
                            color=feature,
                            hover_name="country",
                            color_continuous_scale=color_scale, template="plotly_dark")

        fig.update_layout(title = {'text':'Total {}'.format(feature.title()),
                                       'y':0.95,
                                       'x':0.5,
                                       'xanchor': 'center',
                                       'yanchor': 'top'})
        return fig

    def plot_pct(self, feature):
        feature_each = self.df.groupby('country', as_index=False)[feature].sum()
        feature_each[feature] = round(100 * feature_each[feature] / feature_each[feature].sum(), 2)

        if feature == 'cases':
            color_scale = px.colors.sequential.Tealgrn
        else:
            color_scale = px.colors.sequential.Magenta

        feature_each = feature_each.sort_values(by=feature, ascending=False)
        fig = px.bar(feature_each.iloc[:10], x='country', y=feature,
                     color=feature, title='{}'.format(feature.title()),
                     color_continuous_scale=color_scale)

        fig.update_layout(xaxis_title='Countries',
                          yaxis_title='Percent {} (%)'.format(feature),
                          template="plotly_dark")
        return fig

    def plot_area(self,countries):
        fig = go.Figure()
        for c in countries:
            dff = self.df.loc[self.df['country'] == c]
            fig.add_trace(go.Scatter(x=dff['date'], y=dff['cases'], fill='tozeroy', name=c))
        fig.update_layout(title='Covid Cases since the begining'.title(), template="plotly_dark")
        fig.update_xaxes(rangeslider_visible=True)
        return fig
