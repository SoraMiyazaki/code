import re
import glob
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]    
  
drift_kobe = sorted(glob.glob("../インターン生課題/temp/津波漂流物計算結果/kobe/out/drift/*.csv"), key=natural_keys)
drift_fukushima = sorted(glob.glob("../インターン生課題/temp/津波漂流物計算結果/fukushima/drift/*.csv"), key=natural_keys)
img = Image.open("test.png")
img_resized = img.resize((1280, 960))
figsize = (12.8, 9.6)
fontsize = 30
col = 1000
extent = [102000,107000, 172000,176000]


for i in tqdm(range(len(drift_fukushima))):
    plt.figure(figsize=figsize)
    if i+1 == 361:
        break
    df_before = pd.read_csv(drift_fukushima[i], header=None).values
    df_before = df_before[1:1001, 1:3].astype(float)
    df_after = pd.read_csv(drift_fukushima[i+1], header=None).values
    df_after = df_after[1:1001, 1:3].astype(float)
    plt.title(f"Time={i}~{(i+1)}[min]", fontsize=fontsize)
    plt.xlim(102000, 107000)
    plt.ylim(172000, 176000)
    plt.scatter(df_before[:, 0], df_before[:, 1], s=20, c="r", alpha=0.5)
    plt.scatter(df_after[:, 0], df_after[:, 1], s=20, c="b", alpha=0.5)
    for j in range(col):
        dx = df_after[j, 0] - df_before[j, 0]
        dy = df_after[j, 1] - df_before[j, 1]
        plt.arrow(df_before[j, 0],df_before[j, 1], dx,dy, head_width=2, head_length=2)
    plt.imshow(img_resized, extent=extent)
    plt.xticks(color="None")
    plt.yticks(color="None")
    plt.tick_params(length=0)
    plt.savefig(f"img_fukushima_arrow/fukushima_arrow{i+1}.jpg")
    plt.cla()
    plt.clf()
    plt.close()
