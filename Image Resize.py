import PIL
from PIL import Image, ImageTk

width=4250
height=5500

img= Image.open(f".\images\Output_0.png")

resized = img.resize((552,715), Image.ANTIALIAS)

resized.save(f".\images\Resized_2.png")
