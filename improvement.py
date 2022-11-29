import re
import glob
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
from datetime import datetime

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]    
  
drift_fukushima = sorted(glob.glob("../インターン生課題/temp/津波漂流物計算結果/fukushima/drift/*.csv"), key=natural_keys)

img = Image.open("test.png")
img_resized = img.resize((1280, 960))
figsize = (12.8, 9.6)
fontsize = 30
col = 1000
extent = [102000, 107000, 172000, 176000]

for k,file in tqdm(enumerate(drift_fukushima)):
    df = pd.read_csv(file)
    x = df.loc[:, "x"].to_numpy()
    y = df.loc[:, "y"].to_numpy()
    s_time = os.path.basename(file).replace("drift_", "").replace(".csv", "")
    strptime = datetime.strptime(s_time, "%Y%m%d%H%M%S")
    plt.figure(figsize=figsize)
    plt.title(strptime, fontsize=fontsize)
    plt.xlim(extent[0], extent[1])
    plt.ylim(extent[2], extent[3])
    plt.scatter(x, y, s=20, c= "r")
    plt.imshow(img_resized, extent=extent)
    plt.xticks(color="None")
    plt.yticks(color="None")
    plt.tick_params(length=0)
    plt.savefig(f"img_fukushima_improvement/{s_time}.jpg")
    plt.cla()
    plt.clf()
    plt.close()
    