from app import app
import requests
from flask import render_template
from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale
import io
import matplotlib.pyplot as plt
import random
import base64
import numpy as np

def image_tint(tint='#ffffff'):
    r = requests.get("https://picsum.photos/200/300?grayscale")
    img_byte_array = io.BytesIO(r.content)              # create file-like object in memory to save image without using disk
    # plt.savefig(img, format='png')  # save image in file-like object
    #convert from Byte array to Image file
    im_Image = Image.open(img_byte_array)
    im_Image = im_Image.convert('RGBA') # ensure image has 3 channels
    src = im_Image
    tr, tg, tb = getrgb(tint)
    tl = getcolor(tint, "L")  # tint color's overall luminosity
    if not tl: tl = 1  # avoid division by zero
    tl = float(tl)  # compute luminosity preserving tint factors
    sr, sg, sb = map(lambda tv: tv/tl, (tr, tg, tb))  # per component
                                                      # adjustments
    # create look-up tables to map luminosity to adjusted tint
    # (using floating-point math only to compute table)
    luts = (tuple(map(lambda lr: int(lr*sr + 0.5), range(256))) +
            tuple(map(lambda lg: int(lg*sg + 0.5), range(256))) +
            tuple(map(lambda lb: int(lb*sb + 0.5), range(256))))
    l = grayscale(src)  # 8-bit luminosity version of whole image
    if Image.getmodebands(src.mode) < 4:
        merge_args = (src.mode, (l, l, l))  # for RGB verion of grayscale
    else:  # include copy of src image's alpha layer
        a = Image.new("L", src.size)
        a.putdata(src.getdata(3))
        merge_args = (src.mode, (l, l, l, a))  # for RGBA verion of grayscale
        luts += tuple(range(256))  # for 1:1 mapping of copied alpha values

    return Image.merge(*merge_args).point(luts)

def generate_image():

    # y = [random.randint(-10, 10) for _ in range(10)]
    # x = list(range(10))
    # plt.plot(x, y)

    

    # #process Image file
    # data = np.array(im_Image)   # "data" is a height x width x 4 numpy array
    # red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # # Replace white with red... (leaves alpha values alone...)
    # white_areas = (red == 255) & (blue == 255) & (green == 255)
    # data[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed

    # im2 = Image.fromarray(data)

    result = image_tint('#030FFC')

    #convert Image to Byte array
    img_byte_array = io.BytesIO()
    result.save(img_byte_array, format='PNG')
    # img_byte_array = img_byte_array.getvalue()
    
    # img_byte_array.seek(0)

    return img_byte_array

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