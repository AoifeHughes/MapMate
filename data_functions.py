from numpy import pi, sin, cos
import numpy as np
import pandas as pd
import warnings
import cartopy.feature as cf
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def degree2radians(degree):
    #convert degrees to radians
    return degree*pi/180

def mapping_map_to_sphere(lon, lat, radius=1):
    lon=np.array(lon, dtype=np.float64)
    lat=np.array(lat, dtype=np.float64)
    lon=degree2radians(lon)
    lat=degree2radians(lat)
    xs=radius*cos(lon)*cos(lat)
    ys=radius*sin(lon)*cos(lat)
    zs=radius*sin(lat)
    return xs, ys, zs

from pandas.api.types import is_numeric_dtype
def process_df(df, groupbyLst, lat, long, date=None, date_var = None):

    # crop to date region if required
    if date is not None:
        df = df[df[date_var] == date]
    #check if directions in data

    if not is_numeric_dtype(df[long]):
        df[long] = [float(v[:-1])*(1 if v[-1] in ['N', 'E'] else -1) for v in df[long]]
    if not is_numeric_dtype(df[lat]):
        df[lat] = [float(v[:-1])*(1 if v[-1] in ['N', 'E'] else -1) for v in df[lat]]

    xs, ys, zs = mapping_map_to_sphere(df[long], df[lat])
    df['X'] = xs
    df['Y'] = ys
    df['Z'] = zs
    if groupbyLst is not None:
        tdf = df.groupby([lat, long, *groupbyLst, 'X','Y','Z']).mean().reset_index()
        return tdf
    return df

def get_XYZV(df, var):
    return df[['X','Y','Z', var]].values


def find_nearest(array, value):
    idx = (np.linalg.norm(array - value, axis=1)).argmin()
    return idx

def create_spherical_heatmap_vals(xyzv, num_samples=200):

    u = np.linspace( 0, 2 * np.pi, num_samples)
    v = np.linspace( 0, np.pi, num_samples)
    # create the sphere surface
    XX =  np.outer( np.cos( u ), np.sin( v ) )
    YY =  np.outer( np.sin( u ), np.sin( v ) )
    ZZ =  np.outer( np.ones( np.size( u ) ), np.cos( v ) )

    WW = XX.copy()
    for i in range( len( XX ) ):
        for j in range( len( XX[0] ) ):
            x = XX[ i, j ]
            y = YY[ i, j ]
            z = ZZ[ i, j ]
            WW[ i, j ] =  xyzv[find_nearest(xyzv[:, :-1], np.array([x,y,z])), -1]  

    return XX,YY,ZZ,WW



def get_lines(geoms):
    # create the list of coordinates separated by nan to avoid connecting the lines
    x_coords = []
    y_coords = []
    for coord_seq in geoms(): #e.g. cf.BORDERS.geometries()
        x_coords.extend([k[0] for k in coord_seq.coords] + [np.nan])
        y_coords.extend([k[1] for k in coord_seq.coords] + [np.nan])
    x2, y2, z2 = mapping_map_to_sphere(x_coords, y_coords, 1.001)
    return x2, y2, z2