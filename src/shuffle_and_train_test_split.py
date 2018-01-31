# Given image and label directories and a list containing image number of 
# interest, plots the image and label side-by-side for a quick visual check
# of whether they are consistent.

import random
import skimage.io

def change_integer_into_fname(i, path):
    """ Change integer into four character string with .png extension """
    if i < 10:
        fname = "000" + str(i) + ".png"
    elif i < 100:
        fname = "00" + str(i) + ".png"
    elif i < 1000:
        fname = "0" + str(i) + ".png"
    else:
        fname = str(i) + ".png"
    return path + fname

if __name__ == '__main__':
    num_rows_city = 4400 
    num_rows_field = 4582
    num_rows_holdout_from_each = 440
    
    imgs_city = '/home/frank/Pictures/image_segmentation/field_and_city/720p/images_city/'
    lbls_city = '/home/frank/Pictures/image_segmentation/field_and_city/720p/labels_city/' 
    imgs_field = '/home/frank/Pictures/image_segmentation/field_and_city/720p/images_field/'
    lbls_field = '/home/frank/Pictures/image_segmentation/field_and_city/720p/labels_field/'
    imgs = '/home/frank/Pictures/image_segmentation/field_and_city/720p/images/'
    lbls = '/home/frank/Pictures/image_segmentation/field_and_city/720p/labels/'
    imgs_ho = '/home/frank/Pictures/image_segmentation/field_and_city/720p/holdout/images/'
    lbls_ho = '/home/frank/Pictures/image_segmentation/field_and_city/720p/holdout/labels/'

    
    nums_city = list(range(4400))
    nums_field = list(range(4565))

    random.shuffle(nums_city)
    random.shuffle(nums_field)

    alternate = list(zip(nums_city, nums_field))
    alternate_ho = alternate[:num_rows_holdout_from_each]
    alternate_train = alternate[num_rows_holdout_from_each:]

    i = 0 
    for num_city, num_field in alternate_ho:
        img = skimage.io.imread(change_integer_into_fname(num_city, imgs_city))
        lbl = skimage.io.imread(change_integer_into_fname(num_city, lbls_city))
        skimage.io.imsave(change_integer_into_fname(i, imgs_ho), img)
        skimage.io.imsave(change_integer_into_fname(i, lbls_ho), lbl)
        i += 1
        img = skimage.io.imread(change_integer_into_fname(num_field, imgs_field))
        lbl = skimage.io.imread(change_integer_into_fname(num_field, lbls_field))
        skimage.io.imsave(change_integer_into_fname(i, imgs_ho), img)
        skimage.io.imsave(change_integer_into_fname(i, lbls_ho), lbl)
        i += 1

    i = 0 
    for num_city, num_field in alternate_train:
        img = skimage.io.imread(change_integer_into_fname(num_city, imgs_city))
        lbl = skimage.io.imread(change_integer_into_fname(num_city, lbls_city))
        skimage.io.imsave(change_integer_into_fname(i, imgs), img)
        skimage.io.imsave(change_integer_into_fname(i, lbls), lbl)
        i += 1
        img = skimage.io.imread(change_integer_into_fname(num_field, imgs_field))
        lbl = skimage.io.imread(change_integer_into_fname(num_field, lbls_field))
        skimage.io.imsave(change_integer_into_fname(i, imgs), img)
        skimage.io.imsave(change_integer_into_fname(i, lbls), lbl)
        i += 1


