from MapMate.mm_data import prepare_data


def test_plot():
    import numpy as np
    import pandas as pd
    import pycountry
    import plotly.graph_objects as go

    loc = "./data/GlobalLandTemperaturesByCity.csv"
    def fs(df): df['Year'] = np.around([int(dt.split('-')[0]) for dt in df['dt']], -1)
    cname_cols=['Country', 'Year']
    data_col='AverageTemperature'
    tdf = prepare_data(loc, data_col, cname_cols,  nrows=10000, col_mods=[fs])



    # Below be working
    years = tdf['Year'].unique()
    years.sort()
    years_sliders = []

    for year in years:
        ttdf = tdf[tdf['Year'] == year]

        years_sliders.append(go.Choropleth(
            visible=False,
            locations = ttdf['codes'],
            z = ttdf[data_col],
            text = ttdf['Country'],
            colorscale = 'RdBu',
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_ticksuffix = '°C',
            colorbar_title = 'Temperature',
            zmin=tdf[data_col].min(), zmax=tdf[data_col].max(), zmid=0
        ))

    fig = go.Figure(data=years_sliders)

    steps = []
    for i in range(len(years)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                {"title": "Year: " + str(years[i])}],
                label=str(years[i])  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=len(years),
        currentvalue={"prefix": "Steps: "},
        pad={"t": 50},
        steps=steps,
    )]

    geo=dict(
            showframe=False,
            showcoastlines=False,
            #projection_type='orthographic'
        )
    fig.update_layout(
        sliders=sliders,
        geo=geo
    )
    fig.data[0].visible = True
    fig.write_html('./plots/complex_globe_flat.html')


def test_temporal():
    pass

def test_3D():
    pass