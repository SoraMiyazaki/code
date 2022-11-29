from PIL import Image
import matplotlib.pyplot as plt

img = Image.open("test.png")
img_resized = img.resize((1280, 960))
img_resized.show()


