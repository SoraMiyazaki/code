import re
import glob
import pandas as pd
import os
from datetime import datetime, timedelta
from pprint import pprint

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]   

drift_fukushima = glob.glob("../インターン生課題/temp/津波漂流物計算結果/fukushima/drift/*.csv")

for k,file in enumerate(drift_fukushima[0:1]):
    df = pd.read_csv(file)
    x = df.loc[:, "x"].to_numpy()
    y = df.loc[:, "y"].to_numpy()
    s_time = os.path.basename(file).replace("drift_", "").replace(".csv", "")
    s_time = datetime.strptime(s_time, "%Y%m%d%H%M%S")
    print(s_time.strftime("%Y/%m/%d %H:%M:%S")) 

filelist = [[f1, f2] for f1, f2 in zip(drift_fukushima[:-1], drift_fukushima[1:])]
# for f1, f2 in zip(drift_fukushima[:-1], drift_fukushima[1:]):
#     print(f1, f2)   
pprint(filelist)

# pram = {
#     "x":[1, 2, 3, 4], 
#     "y":[5, 6, 7, 8]
# }
# pram = pd.DataFrame({
#     "x":[1, 2, 3, 4], 
#     "y":[5, 6, 7, 8]
# })
# print(pram)