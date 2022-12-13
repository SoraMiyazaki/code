import pandas as pd
import numpy as np
import math
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os

mesh_file = "meshx_y.csv"
coord_file = "interpolate.csv"
ij_base = pd.read_csv(mesh_file, encoding='utf-8')
xy_base = pd.read_csv(coord_file, encoding="utf-8")

i_mesh = np.array(ij_base["x"],dtype=np.int64)
j_mesh = np.array(ij_base["y"],dtype=np.int64)
x_mesh = np.array(xy_base["x"],dtype=np.float64)
y_mesh = np.array(xy_base["y"],dtype=np.float64)

imax = i_mesh.max()
jmax = j_mesh.max()

i_mesh_2D = i_mesh.reshape(imax,jmax)
j_mesh_2D = j_mesh.reshape(imax,jmax)
x_mesh_2D = x_mesh.reshape(imax,jmax)
y_mesh_2D = y_mesh.reshape(imax,jmax)

i_mesh_1D = []
j_mesh_1D = []
x_mesh_1D = []
y_mesh_1D = []
vtx = []
for j in range(jmax-1):
    for i in range(imax-1):
        x1 = x_mesh_2D[i,j]
        y1 = y_mesh_2D[i,j]
        x2 = x_mesh_2D[i+1,j]
        y2 = y_mesh_2D[i+1,j]
        x3 = x_mesh_2D[i+1,j+1]
        y3 = y_mesh_2D[i+1,j+1]
        x4 = x_mesh_2D[i,j+1]
        y4 = y_mesh_2D[i,j+1]

        i_mesh_1D.append(i_mesh_2D[i,j])
        j_mesh_1D.append(j_mesh_2D[i,j])
        x_mesh_1D.append((x1+x2+x3+x4)/4)
        y_mesh_1D.append((y1+y2+y3+y4)/4)
        vtx.append(Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]))



gdf = gpd.GeoDataFrame(crs='EPSG:2446', geometry=vtx)
gdf['i'] = pd.Series(i_mesh_1D, dtype=np.int32)
gdf['j'] = pd.Series(j_mesh_1D, dtype=np.int32)
gdf['x'] = pd.Series(x_mesh_1D, dtype=np.float64)
gdf['y'] = pd.Series(y_mesh_1D, dtype=np.float64)

gdf.to_file('mesh/mesh.shp', driver='ESRI Shapefile', encoding="utf-8")