import numpy as np

df = [["i", "j", "deform"]]
raw_s = 791
raw_e = 811
column_s = 1
column_e = 1150
deform = 20
path = "cal/input/deform/deform_test.csv"

for raw in range(raw_s, raw_e):
    for col in range(column_s, column_e):
        df.append([raw, col, deform])

np.savetxt(path, df, fmt="%s", delimiter=',')