import io
from base64 import b64encode
import os, sys
sys.path.append('../')
from data_functions import degree2radians, mapping_map_to_sphere, process_df, get_XYZV, create_spherical_heatmap_vals, get_lines
import dash
import dash_core_components as dcc
import dash_html_components as html
import cartopy.feature as cf
import plotly.graph_objects as go
from dash.dependencies import Input, Output

buffer = io.StringIO()
import numpy as np
import pandas as pd

print('making data...')
df = pd.read_csv("../data/GlobalLandTemperaturesByCity.csv")
df = df[df['AverageTemperature'].notna()]
df['Year'] = [dt.split('-')[0] for dt in df['dt']]
tdf = process_df(df, ['City'], 'Latitude', 'Longitude', date=df['Year'].max(), date_var='Year'  )
xyzv = get_XYZV(tdf, 'AverageTemperature')
XX, YY, ZZ, WW = create_spherical_heatmap_vals(xyzv)
fig = go.Figure(data=[go.Surface(x=XX, y=YY, z=ZZ, surfacecolor=WW, opacity=1)] )
for x,y,z in [get_lines(g) for g in [cf.COASTLINE.geometries, cf.BORDERS.geometries] ]:
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, showlegend=False, hoverinfo='skip', mode='lines', line = dict(color='black', width=4)))
#fig.add_trace(go.Scatter3d(x=xyzv[:,0], y=xyzv[:,1],z=xyzv[:,2], mode='markers'))

width = 1000
height = 1000
fig.update_layout(width=int(width), height=int(height))
fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig),
    html.A(
        html.Button("Download HTML"), 
        id="download",
        href="data:text/html;base64," + encoded,
        download="plotly_graph.html"
    )
])
print('Server now running!')
app.run_server()