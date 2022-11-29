from PIL import Image
import re
import glob
from tqdm import tqdm

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]    
  
drift_fukushima = sorted(glob.glob("img_fukushima_improvement/*.jpg"), key=natural_keys)
pictures = []

for name in drift_fukushima:
    img = Image.open(name)
    pictures.append(img)
    
pictures[0].save('anime.gif',save_all=True, append_images=pictures[1:],
optimize=True, duration=250, loop=1)