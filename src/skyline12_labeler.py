# Parses the skyline12 dataset images for analysis by NVIDIA's
# TensorRT framework.  Desired image dimension is 1280x720 RGB
# with labels ...
# The Skyline12 dataset is available from the Toyota Technical Institute at 
# Chicago: 
# http://ttic.uchicago.edu/%7Esmaji/projects/skylineParsing/skyline12.tar.gz

import numpy as np
import scipy.io
import skimage.io
import matplotlib.pyplot as plt
import cProfile
import pstats
import StringIO
import math

def make_img_paths(root, folder, city_dict, imgs_per_folder, pref, ext):
    """ Returns a numpy array containing paths to all the images in the dataset """
    img_paths = [] 
    for city in sorted(city_dict):
        for img_num in range(1,imgs_per_folder+1):
            img_path = "".join([root, folder, city, '/', pref, city_dict[city], 
                                '_',str(img_num),ext])
            img_paths.append(img_path)     
    return np.array(img_paths)

def check_rows_and_cols(img, rows_min, cols_min):
    """ For each image in the numpy array, find its number of rows and columns
        and check it against rows_min and cols_min.  If image_rows >= rows_min
        and image_cols >= cols_min return True.
    """
    if img.shape[0] >= rows_min and img.shape[1] >= cols_min:
        return True
    else:
        return False

def flag_images_to_use(img_paths, rows_min, cols_min):
    """ Returns a numpy array of boolean values the length of the imgs paths
        numpy array, where True indicates that the image corresponding to that
        row has greater than or equal to rows_min and cols_min.
    """
    imgs = np.array([skimage.io.imread(fname) for fname in img_paths])
    vect_check_rows_cols = np.vectorize(check_rows_and_cols)
    use = vect_check_rows_cols(imgs, rows_min, cols_min)
    return use

def print_profiler_output(pr):
    """ Prints profiler output """
    #pr = cProfile.Profile()
    #pr.enable() 
    #pr.disable() 
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())


def read_images(img_paths, use):
    """ Read in the images that are large enough """
    paths_to_use = img_paths[use]
    imgs = np.array([skimage.io.imread(path) for path in paths_to_use])
    return paths_to_use, imgs

def read_labels(label_paths, use):
    """ Reads in labels.  Labels are in Matlab .mat format """
    paths_to_use = label_paths[use]
    lbls_raw = [scipy.io.loadmat(path)['labels'] for path in paths_to_use]
    lbls = []
    for lbl_raw in lbls_raw:
        lbl = np.zeros((lbl_raw.shape[0], lbl_raw.shape[1], 3), dtype=np.uint8)
        bmask = lbl_raw == 1 
        gmask = ~bmask
        lbl[:,:,1] = gmask * 255
        lbl[:,:,2] = bmask * 255
        lbls.append(np.copy(lbl))
    return np.array(lbls)

def plot_image_and_label(imgs, lbls):
    """ Plots images and labels together as a visual check """ 
    for i, (img, lbl) in enumerate(zip(imgs, lbls)):
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
        image = axes[0].imshow(img)
        mask = axes[1].imshow(lbl)
        fname = 'temp/' + str(i) + '_.png'
        plt.savefig(fname)
        plt.close()

def partition_images(imgs, desired_image_size, num_horz, num_vert, flip=True):
    """ Splits a larger image into num_horz * num_vert images, each of size
        desired_image_size, which is a tuple of (pix_vert, pix_vert).  
        If flip is true it also flips each image left-right, doubling the 
        number of images.
    """
    partitioned_images = [] 
    pix_vert = desired_image_size[0]
    pix_horz = desired_image_size[1]
    for img in imgs:
        del_rows = img.shape[0] - pix_vert 
        del_cols = img.shape[1] - pix_horz 
        row_shift  = int(math.floor(del_rows / (num_vert - 1))) 
        col_shift  = int(math.floor(del_cols / (num_horz - 1)))
        for i_vert in range(num_vert):
            rs = i_vert * row_shift
            re = rs + pix_vert
            for i_horz in range(num_horz):
                cs = i_horz * col_shift
                ce = cs + pix_horz
                part_img = img[rs:re, cs:ce,:]
                partitioned_images.append(part_img)
                if flip:
                    partitioned_images.append(np.fliplr(part_img))
    return np.array(partitioned_images)
            
def save_images(imgs, path):
    """ Saves the images to the desired path as .png files """
    for i, img in enumerate(imgs): 
        if i < 10:
            fname = "000" + str(i) + ".png"
        elif i < 100:
            fname = "00" + str(i) + ".png"
        elif i < 1000:
            fname = "0" + str(i) + ".png"
        else:
            fname = str(i) + ".png"
        path_with_name =  path + fname
        skimage.io.imsave(path_with_name,img)


if __name__ == '__main__':
    # inputs 
    desired_img_size = (720, 1280)
    min_rows_img = 800
    min_cols_img = 1600
    num_horz = 5 # number of slices of image to take horizontally
    num_vert = 5 # number of slices of image to take vertically
    root = '/home/frank/Pictures/skyline12/data/'
    img_folder = 'images/'
    lbl_folder = 'labels/'
    city_dict = {'Chicago': '1', 'Dallas': '2', 'Frankfurt': '3', 
                 'HongKong': '4', 'Miami': '5', 'NewYork': '6',
                 'Philadelphia': '7', 'Seattle': '8', 'Shanghai': '9',
                 'Singapore': '10', 'Tokyo': '11', 'Toronto': '12'}
    images_out = '/home/frank/Pictures/image_segmentation/field_and_city/720p/images_city/'
    labels_out = '/home/frank/Pictures/image_segmentation/field_and_city/720p/labels_city/' 

    # calculations and saved images 
    img_paths = make_img_paths(root, img_folder, city_dict, 10,'', '.jpg')
    label_paths = make_img_paths(root, lbl_folder, city_dict, 10, 'label_', '.mat')
    use = flag_images_to_use(img_paths, min_rows_img, min_cols_img)
    img_paths_to_use, imgs = read_images(img_paths, use)
    lbls = read_labels(label_paths, use)
    part_imgs = partition_images(imgs, desired_img_size, num_horz, num_vert)
    save_images(part_imgs, images_out)
    part_lbls = partition_images(lbls, desired_img_size, num_horz, num_vert)
    save_images(part_lbls, labels_out)
     
