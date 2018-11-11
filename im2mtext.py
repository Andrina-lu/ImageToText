from matplotlib import image as mpimg, pyplot as plt
import numpy as np
import cv2
from pathlib import Path
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='file name of the input image')
parser.add_argument('-C', '--charlist', default='@W#$OEXC[(/?=^~_.` ',
                    help='character list used to print the output "image"')
parser.add_argument('-H', '--height', type=int, default=100,
                    help='number of text lines in the output (default=100)')
parser.add_argument('-E', '--equalize', action='store_true',
                    help='equalize the histogram')


def imshow(im):
    plt.imshow(255 - im, cmap='Greys')
    plt.show()


def im2char(im, charlist, dsize):
    im = cv2.resize(im, dsize=dsize, interpolation=cv2.INTER_AREA)
    length = len(charlist) - 1
    im = np.int32(np.round(im / 255 * length))
    output = []
    for y in range(dsize[1]):
        s = ""
        for x in range(dsize[0]):
            s += charlist[im[y][x]]
        # print(s)
        output.append(s)
    # print(output)
    return '\r\n'.join(output)


def main():
    args = parser.parse_args(['ywy.jpg', '-E'])
    charlist = args.charlist

    path = Path(args.filename)
    im = cv2.imread(str(path))
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    if args.equalize:
        im = cv2.equalizeHist(im)
    
    height, width, *_ = im.shape
    output_height = args.height
    output_width = round(width * 1.865 * output_height / height)
    # output_height = round(height / 1.865 * output_width / width)
    output = im2char(im, charlist, (output_width, output_height))
    if args.equalize:
        path = path.with_name(path.stem + '_eq.txt')
    else:
        path = path.with_suffix('.txt')
    with path.open('w') as f:
        f.write(output)
        print(f'Output: {path.name}')
    # print(f'Output size: {output_width}x{output_height}')


if __name__ == '__main__':
    main()
