import numpy as np

meshsize = 2.5
meshsize_half = meshsize / 2
NW = [101700, 113300]
NE = [104700, 113300]
SW = [101700, 109300]
extent = [int(((NE[0]-NW[0])/meshsize)), int(((NW[1]-SW[1])/meshsize))]
mesh_c_x = NW[0] + meshsize_half
mesh_c_y = NW[1] - meshsize_half
x = [mesh_c_x]
y = [mesh_c_y]
mesh_x = []
mesh_y = []
columns = np.array([["x", "y"]])
out_path = "mesh.csv"

for _ in range(extent[0]-1):
    mesh_c_x += meshsize
    x.append(mesh_c_x)
    
for _ in range(extent[1]-1):
    mesh_c_y -= meshsize
    y.append(mesh_c_y)
    
for _ in range(extent[1]):
    for i in x:
        mesh_x.append(i)
        
for i in y:
    for _ in range(extent[0]):
        mesh_y.append(i)      

xy = np.concatenate((np.array([mesh_x]).T, np.array([mesh_y]).T), axis=1)
mesh = np.concatenate((columns, xy))

np.savetxt(out_path, mesh, delimiter=",", fmt="%s")
