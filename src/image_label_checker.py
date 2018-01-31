# Given image and label directories and a list containing image number of 
# interest, plots the image and label side-by-side for a quick visual check
# of whether they are consistent.

import numpy as np
import scipy.io
import skimage.io
import matplotlib.pyplot as plt

if __name__ == '__main__':
    imgs_city = '/home/frank/Pictures/image_segmentation/field_and_city/720p/images_city/'
    lbls_city = '/home/frank/Pictures/image_segmentation/field_and_city/720p/labels_city/' 
    imgs_field = '/home/frank/Pictures/image_segmentation/field_and_city/720p/images_field/'
    lbls_field = '/home/frank/Pictures/image_segmentation/field_and_city/720p/labels_field/'

    img_nums = ['0001.png', '0128.png', '1089.png', '2639.png', '3017.png', 
                '3221.png', '3310.png', '3501.png', '3879.png', '4117.png']

    path_img = imgs_city
    path_lbl = lbls_city

    check_directory = 'check/'
    
    for num in img_nums:
        fname_img =  path_img + num
        fname_lbl = path_lbl + num
        img = skimage.io.imread(fname_img)
        lbl = skimage.io.imread(fname_lbl)
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
        axes[0].imshow(img)
        axes[1].imshow(lbl)
        fname = check_directory + num
        plt.savefig(fname)
        plt.close()


