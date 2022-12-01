# --- データ処理ライブラリ
import ctypes
import numpy as np
import os
import shutil
import pathlib
from glob import glob
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime
from osgeo import gdal
import pickle
import re
import glob
from tqdm import tqdm

extent = [102000, 107000, 172000, 176000]
c_range = [-5, 5]

def generate_depth_image(calc_file, extent, c_range, out):
    """ ラスタファイルを画像ファイルへ変換

    """
    
    # --- アスキーデータの読み込み
    raster = gdal.Open(calc_file, gdal.GA_ReadOnly)
    array_dep = raster.GetRasterBand(1).ReadAsArray() #ndarray
    x_origin, dl, _, y_top, _, _ = raster.GetGeoTransform()
    
    # --- 対象範囲の絞り込み
    # hight, width = np.array(array_dep.shape) * dl
    # y_origin = y_top - hight
    new_xo = int(((extent[0] - x_origin) / dl) + 1)
    new_yo = int(((y_top - extent[3]) / dl) + 1)
    new_w = int((extent[1] - extent[0]) / dl)
    new_h = int((extent[3] - extent[2]) / dl)
    area = array_dep[new_yo:new_yo+new_h, new_xo:new_xo+new_w]

    # --- データを0 - 1の範囲の値に変換
    dep_max = np.float32(c_range[1])
    dep_min = np.float32(c_range[0])
    img_depth = np.where(area == -9999.0, np.nan, (area - dep_min) / (dep_max - dep_min))

    # --- カラーマップへ変換
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(img_depth, cmap="jet", vmin=0, vmax=1)
    ax.axis("off")
    plt.savefig(r"bin/temp.png", bbox_inches='tight', pad_inches=0, dpi=1200)
    plt.clf()
    plt.close()

    # --- 陸域の透過処理
    img_depth = cv2.imread(r"bin/temp.png")
    mask = np.all(img_depth[:, :, :] ==  [255, 255, 255], axis=-1)
    img_depth = cv2.cvtColor(img_depth, cv2.COLOR_BGR2BGRA)
    img_depth[mask, 3] = 0
    cv2.imwrite(out, img_depth)

    return img_depth

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]  

asc_file = sorted(glob.glob(r"cal/to_raster/out/D06-0010/*.asc"), key=natural_keys)
for i, calc_file in tqdm(enumerate(asc_file)):
    print(i, calc_file)
    generate_depth_image(calc_file, extent, c_range, f"bin/temp{i+1}.jpg")
    