import PIL
from PIL import Image

basewidth = 300
img = Image.open("/home/pi/Desktop/photobooth_pascal/test/2018-04-21-12:46:46.jpg")
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
img.save("resized_image.jpg")
