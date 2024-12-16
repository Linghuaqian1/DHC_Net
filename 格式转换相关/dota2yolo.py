import dota_util as util
import os
import numpy as np
from PIL import Image

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


## trans dota format to format YOLO(darknet) required
def dota2darknet(imgpath, txtpath, dstpath, extractclassname):
    """
    :param imgpath: the path of images
    :param txtpath: the path of txt in dota format
    :param dstpath: the path of txt in YOLO format
    :param extractclassname: the category you selected
    :return:
    """
    filelist = util.GetFileFromThisRootDir(txtpath)
    for fullname in filelist:
        objects = util.parse_dota_poly(fullname)
        name = os.path.splitext(os.path.basename(fullname))[0]
        img_fullname = os.path.join(imgpath, name + '.jpg')
        img = Image.open(img_fullname)
        img_w, img_h = img.size
        # print img_w,img_h
        with open(os.path.join(dstpath, name + '.txt'), 'w') as f_out:
            for obj in objects:
                poly = obj['poly']
                bbox = np.array(util.dots4ToRecC(poly, img_w, img_h))
                if (sum(bbox <= 0) + sum(bbox >= 1)) >= 1:
                    continue
                if (obj['name'] in extractclassname):
                    id = extractclassname.index(obj['name'])
                else:
                    continue
                outline = str(id) + ' ' + ' '.join(list(map(str, bbox)))
                f_out.write(outline + '\n')


if __name__ == '__main__':
    dota2darknet(r'E:\dota_test\images',
                 r'E:\dota_test\old',
                 r'E:\dota_test\new',
                 util.wordname_18)

    # dota2darknet('C:/Users/xy/Desktop/Work/upload/DOTA/val/images',
    #              'C:/Users/xy/Desktop/Work/upload/DOTA/val/labels1',
    #              'C:/Users/xy/Desktop/Work/upload/DOTA/val/labels',
    #              util.wordname_18)
