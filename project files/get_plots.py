import plotly.express as px
import plotly.graph_objects as go
from prep_data_frames import CreateDataFrames

class Plots:
    def __init__(self,df):
        self.df = df
        self.get_data = CreateDataFrames(self.df)

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
                                       'yanchor': 'top'},
                          autosize=False,width=685, height=500,)
        return fig

    def plot_pct(self, feature):
        feature_each = self.df.groupby('country', as_index=False)[feature].sum()
        feature_each[feature] = round(100 * feature_each[feature] / feature_each[feature].sum(), 2)

        if feature == 'cases':
            color_scale = px.colors.sequential.Tealgrn
        else:
            color_scale = px.colors.sequential.Magenta

        feature_each = feature_each.sort_values(by=feature, ascending=False)
        data = feature_each.iloc[:, :]

        fig = px.pie(data, names='country', values=feature,
                     labels=data["country"], hole=0.3,
                     color=feature, title='{}'.format(feature.title()),
                     color_discrete_sequence=color_scale)

        fig.update_traces(textposition='inside', textinfo='percent+label')

        fig.update_layout(title='{}'.format(feature.title()),
                          xaxis_title='Countries',
                          yaxis_title='Percent {} (%)'.format(feature),
                          template="plotly_dark", showlegend=False,
                          autosize=False, width=680, height=500,
                          annotations=[dict(text=f"{format(self.df[feature].sum(), ',')}", x=0.5, y=0.5,
                                            font_size=11, showarrow=False)]
                          )
        return fig

    def standard_format(self,num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'),
                             ['', 'K', 'M', 'B', 'T'][magnitude])

    def plot_bar(self, df, label):
        """
        df: Data Frame
        feature: ['Cases', 'Deaths']
        label: ['Total', '24H', '7 Days', '14 Days']
        """
        agg_df_cases = df.sort_values(by=['cases'])
        agg_df_cases["text_data_cases"] = agg_df_cases.apply(lambda r: f"{self.standard_format(r['cases'])}",
                                                             axis=1)

        agg_df_deaths = df.sort_values(by=['deaths'])
        agg_df_deaths["text_data_deaths"] = agg_df_deaths.apply(lambda r: f"{self.standard_format(r['deaths'])}",
                                                                axis=1)

        fig = go.Figure()

        fig.add_trace(go.Bar(name='Cases', x=agg_df_cases['cases'], y=agg_df_cases['country'],
                             marker_color='Teal', text=agg_df_cases['text_data_cases'],
                             texttemplate='%{text}', textposition='outside', orientation='h')
                      )
        fig.add_trace(go.Bar(name='Deaths', x=agg_df_deaths['deaths'], y=agg_df_deaths['country'],
                             marker_color='rgb(177, 77, 142)', text=agg_df_deaths['text_data_deaths'],
                             texttemplate='%{text}', textposition='outside', orientation='h')
                      )
        fig.update_layout(barmode='group')

        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    bgcolor='rgb(69,69,69)',
                    active=2,
                    font=dict(color='rgb(25,25,25)'),
                    buttons=list([
                        dict(
                            label="Cases",
                            method="update",
                            args=[{"visible": [True, False]}, {'title': f"{label} Cases"}]
                        ),
                        dict(
                            label="Deaths",
                            method="update",
                            args=[{"visible": [False, True]}, {'title': f"{label} Deaths"}]
                        )]
                    ),
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.025,
                    yanchor="top"
                )
            ])

        fig.update_coloraxes(showscale=False)
        fig.update_layout(
            title=label,
            height=3900, width=1380, autosize=False,
            template="plotly_dark",
            yaxis_title="Country",
        )

        return fig

    def plot_area(self,countries,feature):
        fig = go.Figure()
        for c in countries:
            dff = self.df.loc[self.df['country'] == c]
            fig.add_trace(go.Scatter(x=dff['date'], y=dff[feature], fill='tozeroy', name=c))
        fig.update_layout(title=f'Covid {feature.title()} since the begining'.title(), template="plotly_dark")
        fig.update_xaxes(rangeslider_visible=True)
        return fig
