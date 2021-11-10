import base64
from PIL import Image, ImageColor
from os import path


def saveImage(base64Image, fileName):
    
    '''
    save the image to the static folder
    '''
    img = Image.open( base64.b64decode(base64Image))
    img.save(path.join('static', 'images', f"{fileName}.png"), 'PNG')
    

def getImage(fileName):
    '''
    grabs the image from the static folder and returns it as a base64 string
    '''
    try:
        with open(path.join('static', 'images', fileName), 'rb') as imageFile:
            return base64.b64encode(imageFile.read())
    except FileNotFoundError:
        print('given file not found')
        return base64.b64encode(Image.new("RGB", [100, 100], ImageColor.getcolor("red")))
    