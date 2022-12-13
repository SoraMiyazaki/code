import numpy as np

NW = [101700, 113300]
NE = [104700, 113300]
SW = [101700, 109300]
meshsize = 2.5
extent = [int((NE[0]-NW[0])/meshsize), int((NW[1]-SW[1])/meshsize)]

x = []
for i in range(extent[0]):
    x.append(i+1)
    
x_coord = []
for i in x:
    for _ in range(extent[1]):
        x_coord.append(i)

y = []
for i in range(extent[1]):
    y.append(i+1)
    
y_coord = []
for _ in range(extent[0]):
    for i in y:
        y_coord.append(i)
        
xy = np.concatenate((np.array([x_coord]).T, np.array([y_coord]).T), axis=1)
columns = np.array([["x", "y"]])
mesh = np.concatenate((columns, xy))

np.savetxt("meshx_y.csv", mesh, delimiter=",", fmt="%s")