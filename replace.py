import pandas as pd

comb_path = "combination.csv"
out_path = "comb_replace.csv"

comb = pd.read_csv(comb_path)
height = comb["z"].tolist()

new_h = []
for num in height:
    if num <= 0:
        num = -99.0
    new_h.append(num)

op_df = pd.DataFrame({
        "x" : comb["x"],
        "y" : comb["y"],
        "z" : new_h
    })

op_df.to_csv(out_path, index=False)
    