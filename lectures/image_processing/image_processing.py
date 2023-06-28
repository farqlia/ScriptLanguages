from PIL import ImageColor
from PIL import Image

print(ImageColor.getcolor('red', 'RGB'))
print(ImageColor.getcolor('hsv(22,100%,80%)', 'RGBA'))

cat = Image.open('cat_image.jpg')
cat.save('kot.webp')
rgb_cat = cat.convert('RGB')
rgb_cat.save('kot.jpg')