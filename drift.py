import re
import glob
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
from datetime import datetime

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
extent = [102000,107000, 172000,176000]
pictures = []

for i in tqdm(range(len(drift_fukushima))):
    plt.figure(figsize=figsize)
    df = pd.read_csv(drift_fukushima[i], header=None).values
    df = df[1:1001, 1:3].astype(float)
    plt.title(f"Time={i*10}~{(i+1)*10}[min]", fontsize=fontsize)
    plt.xlim(102000, 107000)
    plt.ylim(172000, 176000)
    plt.scatter(df[:, 0], df[:, 1], s=20, c= "r")
    plt.imshow(img_resized, extent=extent)
    plt.xticks(color="None")
    plt.yticks(color="None")
    plt.tick_params(length=0)
    plt.savefig(f"img_fukushima/fukushima{i+1}.jpg")
    plt.close()
    