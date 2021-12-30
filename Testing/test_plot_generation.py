from MapMate.mm_data import prepare_data
from MapMate.mm_plot import create_slider_plot
from MapMate.mm_plot import create_plot

def test_data_reading():
    loc = "./data/GlobalLandTemperaturesByCity.csv"
    cname_cols=['Country']
    data_col='AverageTemperature'
    for nrows in [10, 100, 1000]:
        tdf = prepare_data(loc, data_col, cname_cols,  nrows=nrows)

def test_plot():
    loc = "./data/GlobalLandTemperaturesByCity.csv"
    cname_cols=['Country']
    data_col='AverageTemperature'
    tdf = prepare_data(loc, data_col, cname_cols)
    fig = create_plot(tdf, data_col, 'Country', 'codes', 'AverageTemperature' ,cbar_suffix='°C')
    fig.write_html('./plots/test_flat_temperature.html') 

def test_plot_3D():
    loc = "./data/GlobalLandTemperaturesByCity.csv"
    cname_cols=['Country']
    data_col='AverageTemperature'
    tdf = prepare_data(loc, data_col, cname_cols)
    fig = create_plot(tdf, data_col, 'Country', 'codes', 'AverageTemperature' ,cbar_suffix='°C',projection='orthographic')
    fig.write_html('./plots/test_3D_temperature.html') 

def test_temporal():
    import numpy as np
    loc = "./data/GlobalLandTemperaturesByCity.csv"
    def fs(df): df['Year'] = np.around([int(dt.split('-')[0]) for dt in df['dt']], -1)
    cname_cols=['Country', 'Year']
    data_col='AverageTemperature'
    tdf = prepare_data(loc, data_col, cname_cols, col_mods=[fs])
    fig = create_slider_plot(tdf, 'Year', data_col, 'Country', 'codes', 'Temperature' ,cbar_suffix='°C')
    fig.write_html('./plots/test_flat_temporal_temperature.html')

def test_temporal_3D():
    import numpy as np
    loc = "./data/GlobalLandTemperaturesByCity.csv"
    def fs(df): df['Year'] = np.around([int(dt.split('-')[0]) for dt in df['dt']], -1)
    cname_cols=['Country', 'Year']
    data_col='AverageTemperature'
    tdf = prepare_data(loc, data_col, cname_cols, col_mods=[fs])
    fig = create_slider_plot(tdf, 'Year', data_col, 'Country', 'codes', 'Temperature' ,cbar_suffix='°C', projection='orthographic')
    fig.write_html('./plots/test_3D_temporal_temperature.html')

