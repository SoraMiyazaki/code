import numpy as np
import pandas as pd

NW = [93300, 116400]
SW = [93300, 99300]
NE = [113700, 116400]

x_coodinates = []
for row in range(NW[0]+5, NE[0]+5, 10):
    x_coodinates.append(row)

x = []
for _ in range(1710):
    for j in x_coodinates:
        x.append(j)

y_coodinates = []
for col in range(SW[1]+5, NW[1]+5, 10):
    y_coodinates.append(col)

new_y = []   
for i in reversed(y_coodinates):
    new_y.append(i)  
    
y = []
for i in new_y:
    for _ in range(2040):
        y.append(i)
 
df = np.loadtxt(r"../インターン生課題/temp/地形データ作成/内閣府地形データ/地形データ_第04系/depth_0010-30.dat")

z= []
for i in range(len(df)):
    for j in range(len(df[1])):
        z.append(df[i, j])
        
x = np.array([x]).T
y = np.array([y]).T
z = np.array([z]).T

xyz = np.hstack((x, y, z))

np.savetxt("coodinates.csv", xyz, delimiter=",")
        



