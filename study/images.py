from PIL import Image
import urllib3
import io
import urllib.request
from io import StringIO
import requests

link = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Declaration_of_Independence_%281819%29%2C_by_John_Trumbull.jpg/1280px-Declaration_of_Independence_%281819%29%2C_by_John_Trumbull.jpg"


print(Image.open(requests.get(link, stream=True).raw).width)