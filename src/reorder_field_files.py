import skimage.io
import matplotlib.pyplot as plt
import os.path


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
    max_img_num = 4582 
    images_in = '/home/frank/Videos/NVIDIA-Aerial-Drone-Dataset/FPV/SFWA/720p/images/'
    labels_in = '/home/frank/Videos/NVIDIA-Aerial-Drone-Dataset/FPV/SFWA/720p/labels/'
    images_out = '/home/frank/Pictures/image_segmentation/field_and_city/720p/images_field/'
    labels_out = '/home/frank/Pictures/image_segmentation/field_and_city/720p/labels_field/' 
   
    img_num = 0
    for i in range(max_img_num):
        img_in = change_integer_into_fname(i, images_in)
        lbl_in = change_integer_into_fname(i, labels_in)
        if os.path.isfile(img_in):
            img = skimage.io.imread(img_in)
            lbl = skimage.io.imread(lbl_in)
            img_out = change_integer_into_fname(img_num, images_out)
            lbl_out = change_integer_into_fname(img_num, labels_out)
            skimage.io.imsave(img_out, img)
            skimage.io.imsave(lbl_out, lbl)
            img_num += 1


