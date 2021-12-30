import plotly.graph_objects as go


def make_choro(tdf, data_col, cname, ccodes, cbar_name, cbar_suffix=''):
    return go.Choropleth(
            visible=False,
            locations = tdf[ccodes],
            z = tdf[data_col],
            text = tdf[cname],
            colorscale = 'RdBu',
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_ticksuffix = cbar_suffix,
            colorbar_title = cbar_name,
            zmin=tdf[data_col].min(), zmax=tdf[data_col].max(), zmid=0
        )

def create_plot(tdf, data_col, cname, ccodes, cbar_name, cbar_suffix='', projection='equirectangular'):
    plot = make_choro(tdf, data_col, cname, ccodes, cbar_name, cbar_suffix)
    fig = go.Figure(data=[plot])

    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type=projection
    )

    fig.update_layout(
        geo=geo
    )

    return fig

def create_slider_plot(tdf, slider_col, data_col, cname, ccodes, cbar_name, cbar_suffix='', slide_title_prefix='', projection='equirectangular'): 
    slides = tdf[slider_col].unique()
    slides.sort()
    slides_sliders = []

    for year in slides:
        ttdf = tdf[tdf[slider_col] == year]

        slides_sliders.append(make_choro(ttdf, data_col, cname, ccodes, cbar_name, cbar_suffix))

    fig = go.Figure(data=slides_sliders)

    steps = []
    for i in range(len(slides)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                {"title": slide_title_prefix + str(slides[i])}],
                label=str(slides[i])  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=len(slides),
        currentvalue={"prefix": slide_title_prefix},
        pad={"t": 50},
        steps=steps,
    )]

    geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type=projection
        )
    fig.update_layout(
        sliders=sliders,
        geo=geo
    )
    fig.data[0].visible = True
    return fig




    