# MapMate

## Required packages

- Numpy
- Plotly
- Cartopy (see conda install script, easiest install method)
  - Planned to migrate away from as can be barrier of entry for users
- netcdf4 (see conda install script)
  - Similar to cartopy, sometimes annoying to install 
  - NASA data depends on this unfortunately 
  - Processed data to Lat/Long can be used without
- Pandas
- PyCountry
- Probably others, but these packages should have them as dependencies 

Temperature Data can be fetched from 

```
https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data/version/2
``` 

NASA data for Veg indices can be gotten from

```
https://reason.gesdisc.eosdis.nasa.gov/data/Vegetation_Indices/MODVI.005/2015/
```
We used 2015 data, but any can be used (hopefully!)

Put these in the data folder or things won't quite work
