from app import app
import requests
from flask import render_template
from PIL import Image
import io
import matplotlib.pyplot as plt
import random
import base64
#from transforms import RGBTransform

def generate_image():

    # y = [random.randint(-10, 10) for _ in range(10)]
    # x = list(range(10))
    # plt.plot(x, y)

    r = requests.get("https://picsum.photos/200/300?grayscale")
    img = io.BytesIO(r.content)              # create file-like object in memory to save image without using disk
    # plt.savefig(img, format='png')  # save image in file-like object
    img.seek(0)

    return img

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    #image = Image.open("https://picsum.photos/200/300?grayscale")
    #image = image.convert("RGB")


    # in_memory_file = io.BytesIO(r.content)
    # im = Image.open(in_memory_file)
    # output = io.StringIO()
    # im.save(output, "PNG")
    # contents = output.getvalue().encode("base64")
    # output.close()
    # contents = contents.split('\n')[0]
    #im = im.convert("RGB")
    img = generate_image()

    data = img.getvalue()         # get data from file (BytesIO)

    data = base64.b64encode(data) # convert to base64 as bytes
    data = data.decode()  
    return render_template('index.html', title='Home', user=user, posts=posts, data=data)