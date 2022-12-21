''''
Utlity script to prepare RTCC datset for use in GSTN.
The Results of these computations are already used in the csv file.  
'''


import math 
import json
import pandas as pd
from pyproj import Proj, transform
from pyproj import Transformer


def main():
    geodf = get_rtcc_geometry_df()
    lonlatdf = get_lonlat(geodf)
    print('\n','epsg:3452','\n', geodf)
    print('\n', 'epsg:4326','\n', lonlatdf)


'''
RTCC Camera geodata is available as json from rest api:


The geodata geometry is encoded as x,y values using a wkid
    --> The Well-Known ID (WKID) is a unique number assigned to a coordinate system
'''
def get_rtcc_geometry_df():
    #opens json file and reads data into memory
    with open('RTCC_Cameras.json') as json_data:
        data = json.load(json_data)
    #convert the rows of nested geometry dicts into a dataframe 
    geometry_df = pd.json_normalize(data['features'])
    #rename the columsn from geometery.x, geometry.y into x, y 
    geometry_df = geometry_df.rename(index=str, columns={'geometry.x': 'x', 'geometry.y': 'y'})
    return geometry_df

'''
Using Proj4 to transform from wkid coord space into lonlat coord space
'''
def get_lonlat(geodf):
    transformer = Transformer.from_crs("epsg:3452", "epsg:4326")
    lats, lons = transformer.transform(geodf.x,geodf.y)
    return pd.DataFrame({'lat':lats, 'lon':lons})


'''
#works but deprecated! 
def xy_to_lonlat(x,y):
    inProj = Proj('epsg:3452')
    outProj = Proj('epsg:4326')
    dx,dy = transform(inProj,outProj,x,y)
    return {'lat': dx, 'lon': dy}

def get_lonlats(geodf):
    lonlats = geodf.apply(lambda row: xy_to_lonlat(row['x'], row['y']), axis=1)
    return pd.json_normalize(lonlats)
'''

if __name__ == "__main__":
    main()
