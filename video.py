import glob
import cv2
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]    

print("解像度を下げる場合は〇分の1に出力するか入力してください\n解像度をそのまま出力する場合は1を入力してください")

img_arr = []
out_file = 'project.mp4'
img_file = "img_cal/*.jpg"
imgs = sorted(glob.glob(img_file), key=natural_keys)
denominator = int(input("数字を入力してください："))
fps = int(input("FPS : "))

def draw(input_file):
    img = cv2.imread(input_file)
    height, width, layers = img.shape
    img_resize = cv2.resize(img, (int(width/denominator), int(height/denominator)))
    height, width, layers = img_resize.shape
    size = (width, height)
    img_arr.append(img_resize)
    
    return size

for im in imgs:
    size = draw(im)
    
out = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc(*'MP4V'), fps, size)

for i in img_arr:
    out.write(i)
out.release()

print("finish")