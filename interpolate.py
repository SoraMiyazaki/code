import pandas as pd
import scipy.interpolate

comb_path = "comb_replace.csv"
mesh_path = "mesh.csv"
out_path = "interpolate.csv"

mesh = pd.read_csv(mesh_path)
comb = pd.read_csv(comb_path)

op_x_list = mesh["x"].tolist()
op_y_list = mesh["y"].tolist()
tin_x = comb["x"].values
tin_y = comb["y"].values
tin_h = comb["z"].values

interpolate_h = scipy.interpolate.LinearNDInterpolator(list(zip(tin_x, tin_y)), tin_h, fill_value=0)
h_mesh = interpolate_h(op_x_list, op_y_list)

op_df = pd.DataFrame({
        "deform" : h_mesh,
        "x" : op_x_list,
        "y" : op_y_list
    })

op_df.to_csv(out_path, index=False)
