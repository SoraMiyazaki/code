import numpy as np
import pandas as pd

cal_path = "cal_area.csv"
split_path = "split.csv"

cal_area = pd.read_csv(cal_path).values
split_area = pd.read_csv(split_path).values
columns = np.array([["x", "y", "z"]])
comb_area = np.concatenate((columns, cal_area, split_area))

np.savetxt("combination.csv", comb_area, delimiter=",", fmt="%s")


