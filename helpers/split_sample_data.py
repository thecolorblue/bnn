from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--width', type=int, default=512, help='input image width')
parser.add_argument('--height', type=int, default=512, help='input image height')
parser.add_argument('--img-folder', type=str, default='sample_data/raw', help='folder with images to cut up')
parser.add_argument('--img-dest', type=str, default='sample_data/unlabeled', help='destination folder')
opts = parser.parse_args()

sample_images = [f for f in listdir(opts.img_folder) if isfile(join(opts.img_folder, f))]

# source: https://stackoverflow.com/questions/5953373/how-to-split-image-into-multiple-pieces-in-python
def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

if __name__=='__main__':
    start_num = 0

    for image in sample_images:
        for k, piece in enumerate(crop(os.path.join(opts.img_folder, image), opts.height, opts.width),start_num):
            img=Image.new('RGB', (opts.width, opts.height), 255)
            img.paste(piece)
            path=os.path.join(opts.img_dest, "%s-%s" % (k, image))
            img.save(path)