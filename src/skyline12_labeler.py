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
import time
import cProfile
import pstats
import StringIO

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
    i = 0    
    for img, lbl in zip(imgs, lbls):
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
        image = axes[0].imshow(img)
        mask = axes[1].imshow(lbl)
        fname = 'temp/' + str(i) + '_.png'
        plt.savefig(fname)
        plt.close()
        i += 1

    

if __name__ == '__main__':
    # read in the skyline 12 dataset 
    root = '/home/frank/Pictures/skyline12/data/'
    img_folder = 'images/'
    lbl_folder = 'labels/'
    city_dict = {'Chicago': '1', 'Dallas': '2', 'Frankfurt': '3', 
                 'HongKong': '4', 'Miami': '5', 'NewYork': '6',
                 'Philadelphia': '7', 'Seattle': '8', 'Shanghai': '9',
                 'Singapore': '10', 'Tokyo': '11', 'Toronto': '12'}
    
    img_paths = make_img_paths(root, img_folder, city_dict, 10,'', '.jpg')
    label_paths = make_img_paths(root, lbl_folder, city_dict, 10, 'label_', '.mat')
    use = flag_images_to_use(img_paths, 800, 1600)
    img_paths_to_use, imgs = read_images(img_paths, use)
    lbls = read_labels(label_paths, use)
    plot_image_and_label(imgs, lbls)
#img_num = 2 
    #img_path = img_paths[img_num]
    #label_path = label_paths[img_num]
    #img = skimage.io.imread(img_path)
    #lbl_mat = scipy.io.loadmat(label_path)
    #lbl_raw = lbl_mat['labels']
    #lbl = np.zeros((lbl_raw.shape[0], lbl_raw.shape[1], 3), dtype=np.uint8)
    #bmask = lbl_raw == 1 
    #gmask = ~bmask
    #lbl[:,:,1] = gmask * 255
    #lbl[:,:,2] = bmask * 255
    #path_sample_lbl = '/home/frank/Pictures/skyline12/data/labels/sample_label.png'
    #ex_lbl = skimage.io.imread(path_sample_lbl)
    #fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
    #image = axes[0].imshow(img)
    #mask = axes[1].imshow(lbl)
    #plt.show()



#for i, img in enumerate(imgs):
    #    print i 
    #    plt.imshow(img)
    #    plt.show()
    
    #pr.disable()
    #print_profiler_output(pr) 
    #imgs, rows, cols, chans, aspect = find_raw_img_dimensions(img_paths)
    #city = 'Chicago'
    #ci = city_index[city]
    #img_lst = [str(val) for val in range(1,11)]
    #img_path = "".join([root, img_folder,city,'/',ci, '_',img_lst[0],'.jpg'])
    #print(img_path)
    #img = skimage.io.imread(img_path)
    #skimage.io.imshow(img)

