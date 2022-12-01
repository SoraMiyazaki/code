# --- GUIライブラリ
import PySimpleGUI as sg
from queue import Queue

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


# --- 作業のキューの設定
que_ui = Queue()
que_data = Queue()


# --- Fortran ライブラリの取得
lib = np.ctypeslib.load_library(libname="mod_fort.dll", loader_path="./dll/")


# --- 出力動画のサイズ
mov_size = (1920, 1080)


def main(): 
    # --- GUIの作成
    window = sg.Window("動画作成ツール", set_layout())

    # --- GUIイベント
    while True:
        event, values = window.read(timeout=100, timeout_key="-timeout-")

        if event in (None, "Cancel"):
            # 終了処理
            break

        elif event in "-RUN-":
            # ログファイルの保存
            print(type(values))
            with open(r"bin/log.bin", "wb") as p:
                pickle.dump(values, p)

            # 実行
            que_data.put(values)
            run(que_data, que_ui)
        


def set_layout():
    """ GUIレイアウトの設定

    """
    if os.path.isfile(r"bin/log.bin"):
        with open(r"bin/log.bin", "rb") as p:
            default_val = pickle.load(p)

    else:
        default_val = {
            "-RESULT_DIR-": "",
            "-BKG_IMG-": "",
            "-MIN_VAL-": "0.0",
            "-MAX_VAL-": "10.0",
            "-DIV_VAL-": "1",
            "-FPS-": "1",
            "-MIN_X-": "0.0",
            "-MIN_Y-": "0.0",
            "-MAX_X-": "0.0",
            "-MAX_Y-": "0.0",
        }

    layout = [
        # 計算結果フォルダの指定
        [
            sg.Text("計算結果フォルダ"), sg.InputText(key="-RESULT_DIR-", default_text=default_val["-RESULT_DIR-"]),
            sg.FolderBrowse(key="-FOL_RESULT_DIR-", target="-RESULT_DIR-", button_text="..."),
        ],
        # 背景画像の設定
        [
            sg.Text("背景画像ファイル"), sg.InputText(key="-BKG_IMG-", default_text=default_val["-BKG_IMG-"]),
            sg.FileBrowse(key="-FIL_BKG_IMG-", target="-BKG_IMG-", button_text="...",
            file_types=(('画像ファイル', '*.png; *.jpg;'),))
        ],
        # 描画に関する変数
        [
            sg.Text("最小値:"), sg.InputText(key="-MIN_VAL-", size=(7, 1), default_text = default_val["-MIN_VAL-"]),
            sg.Text("最大値:"), sg.InputText(key="-MAX_VAL-", size=(7, 1), default_text = default_val["-MAX_VAL-"]),
            sg.Text("ラベル:"), sg.InputText(key="-DIV_VAL-", size=(7, 1), default_text = default_val["-DIV_VAL-"]),
            sg.Text("FPS:"), sg.InputText(key="-FPS-", size=(7, 1), default_text = default_val["-FPS-"]),
        ],
        # 描画範囲の設定
        [
            sg.Text("左下座標(X, Y):"),
            sg.InputText(key="-MIN_X-", size=(10, 1), default_text=default_val["-MIN_X-"]),
            sg.InputText(key="-MIN_Y-", size=(10, 1), default_text=default_val["-MIN_Y-"]),
        ],
        [
            sg.Text("右上座標(X, Y):"),
            sg.InputText(key="-MAX_X-", size=(10, 1), default_text=default_val["-MAX_X-"]),
            sg.InputText(key="-MAX_Y-", size=(10, 1), default_text=default_val["-MAX_Y-"]),
        ],
        # ステータスモニタ
        [sg.Output(size=(65, 7))],
        # 実行ボタン
        [
            sg.Push(), sg.Submit(button_text="実行", key="-RUN-", size=(12, 1))
        ],
    ]
    return layout



def run(que_data, que_ui):
    """ アニメーション作成
    """
    # --- メインのデータをque_data経由で取得
    values = que_data.get()


    # --- 計算結果のファイルリストを取得
    print(">>> ファイルリストの取得")
    calc_file_list = glob(os.path.join(values["-RESULT_DIR-"], "res_*0.bin"))
    print(f"   - ファイル数: {len(calc_file_list)}")


    # --- 背景画像ファイルの読み込み
    print(">>> 背景図の取得")
    p = pathlib.Path(os.getcwd()).parent
    file = os.path.join("../", pathlib.Path(values["-BKG_IMG-"]).relative_to(p))  # 相対パスに変更（日本語不可）
    img_background = cv2.imread(str(file))
    img_background = cv2.cvtColor(img_background, cv2.COLOR_BGR2BGRA)
    print(f"   - イメージサイズ: ({img_background.shape[1]:}, {img_background.shape[0]:})")


    # --- カラーバーの設定
    cb_div = np.uint8(values["-DIV_VAL-"]) + 1
    cb_max = np.float32(values["-MAX_VAL-"])
    cb_min = np.float32(values["-MIN_VAL-"])
    cb_ticks = [(n / (cb_div - 1)) for n in range(cb_div)]
    cb_label = [cb_min + v * (cb_max - cb_min) for v in cb_ticks]
    cb_label = [f"{v:5.1f}" for v in cb_label]


    # --- 計算結果の図化
    img_list = []
    print(">>> 計算結果の図化")
    for calc_file in calc_file_list:
        # --- 時刻の取得
        print_time = os.path.basename(calc_file).replace("res_", "").replace(".bin", "")
        print_time = datetime.strptime(print_time, "%Y%m%d%H%M%S")
        print(f"   - Time: {print_time}")

        # --- 計算結果を画像ファイルに変換
        img_depth = generate_depth_image(calc_file, values)

        # --- 画像を合成
        decorete_image(img_depth, img_background, print_time, cb_ticks, cb_label)

        # --- 画像を指定のフォルダに格納
        path = f"output/png/"
        os.makedirs(path, exist_ok=True)
        shutil.move(r"bin/temp.png", os.path.join(path, f"dep_{print_time.strftime('%Y%m%d%H%M%S')}.png"))
        img_list.append(os.path.join(path, f"dep_{print_time.strftime('%Y%m%d%H%M%S')}.png"))

    # --- アニメーションへ変換
    print(">>> アニメーション作成")
    generate_video(values)

    # --- 終了後パラメータを返す（スレッド終了の判定）
    que_ui.put(values)
    
    print(">>> 動画作成完了 !")



def generate_depth_image(calc_file, values):
    """ ラスタファイルを画像ファイルへ変換

    """
    # --- ファイルを相対パスへ変換
    p = pathlib.Path(os.getcwd()).parent
    file = os.path.join("../", str(pathlib.Path(calc_file).relative_to(p)))

    # --- 計算結果をアスキー形式へ変換
    read_depth(file, values["-MIN_X-"], values["-MIN_Y-"], values["-MAX_X-"], values["-MAX_Y-"])

    # --- アスキーデータの読み込み
    raster = gdal.Open(r"bin/temp.asc", gdal.GA_ReadOnly)
    array_dep = raster.GetRasterBand(1).ReadAsArray()

    # --- データを0 - 1の範囲の値に変換
    dep_max = np.float32(values["-MAX_VAL-"])
    dep_min = np.float32(values["-MIN_VAL-"])
    img_depth = np.where(array_dep == -9999.0, np.nan, (array_dep - dep_min) / (dep_max - dep_min))

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

    # --- 一時ファイルの削除
    del raster
    os.remove(r"bin/temp.asc")
    os.remove(r"bin/temp.png")

    return img_depth



def read_depth(file:str, xs, ys, xe, ye):
    """ 計算結果(binary)をラスタファイルへ変換

    """

    # --- 入力フォーマットの設定
    lib.read_depth.argtypes = (
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
    )

    # --- 出力フォーマットの設定
    lib.read_depth.restype = ctypes.c_void_p

    # --- データの取得
    file_len = len(file)
    lib.read_depth(
        file.encode("utf-8"),
        ctypes.byref(ctypes.c_int(file_len)),
        ctypes.byref(ctypes.c_double(np.float64(xs))),
        ctypes.byref(ctypes.c_double(np.float64(ys))),
        ctypes.byref(ctypes.c_double(np.float64(xe))),
        ctypes.byref(ctypes.c_double(np.float64(ye))),
    )



def decorete_image(img_depth, img_background, print_time, cb_ticks, cb_label):
    """ 図面の整形

    """

    # --- 背景画像の大きさに計算結果のデータを合わせる
    (j_size, i_size, _) = img_background.shape
    img_resize_dep = cv2.resize(img_depth, (i_size, j_size))

    # --- 背景図と結合
    # 透過率の設定
    mask = img_resize_dep[:, :, 3]
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask = mask / 255 * 0.6

    # アルファブレンド
    img_all = (1. - mask) * img_background[:, :, :3] + mask * img_resize_dep[:, :, :3]
    img_all = img_all.astype(np.uint8)

    # --- matplotlibで装飾
    # 本体の描画
    img_all = cv2.cvtColor(img_all, cv2.COLOR_BGR2RGB)
    fig, ax = plt.subplots(dpi=1200)
    im = ax.imshow(img_all, cmap="jet", vmin=0, vmax=1)

    # 軸ラベルと縦横比の設定
    ax.axis("off")
    ax.set_aspect("equal")

    # タイトル（時間）
    ax.set_title(f"Time : {print_time.strftime('%Y/%m/%d %H:%M:%S')}", fontsize=5, pad=0.1)

    # カラーバーの設定
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="1.5%", pad=0.1)
    cbar = fig.colorbar(im, cax=cax, orientation='horizontal', ticks=cb_ticks)
    cbar.ax.set_xticklabels(cb_label, fontsize=5)

    # ファイルへ保存
    plt.savefig(r"bin/temp.png", bbox_inches='tight', dpi=1200)
    plt.clf()
    plt.close()



def generate_video(values):
    """ 静止がから動画を作成

    """

    # --- 保存先フォルダの作成
    save_file = os.path.join(f"output/mov/", f"mov_dep.mp4")
    os.makedirs(f"output/mov/", exist_ok=True)

    # --- ビデオコーデックの初期化
    codec = cv2.VideoWriter_fourcc('m','p','4', 'v')
    video = cv2.VideoWriter(save_file, codec, np.uint8(values["-FPS-"]), mov_size)

    # --- 動画の作成
    for file in glob(os.path.join(f"output/png/", "dep_*.png")):
        # 背景の画像を作成
        img_base = np.full((mov_size[1], mov_size[0], 3), 255, np.uint8)

        # ファイルから画像を読み込む
        img = cv2.imread(file)
        (img_h, img_w, _) = img.shape

        # 縦横の比率の調整
        ratio_w = img_base.shape[1] / img.shape[1]
        ratio_h = img_base.shape[0] / img.shape[0]
        
        if ratio_w < ratio_h:
            resize = (int(img.shape[1] * ratio_w), int(img.shape[0] * ratio_w))
        else:
            resize = (int(img.shape[1] * ratio_h), int(img.shape[0] * ratio_h))
        img_resize = cv2.resize(img, dsize=resize)

        # 背景の画像に読み込んだ画像を結合して指定のサイズの画像に変換
        h_s = int(img_base.shape[1] / 2 - resize[0] / 2)
        h_e = int(img_base.shape[1] / 2 + resize[0] / 2)
        w_s = int(img_base.shape[0] / 2 - resize[1] / 2)
        w_e = int(img_base.shape[0] / 2 + resize[1] / 2)
        img_base[w_s:w_e, h_s:h_e, :] = img_resize
        video.write(img_base)

    video.release()



if __name__ == "__main__":
    main()