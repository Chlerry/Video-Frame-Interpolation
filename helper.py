import cv2
import numpy as np
import os.path
import math
from os import path
from sklearn.metrics import mean_squared_error 
from skimage.metrics import peak_signal_noise_ratio 
from skimage.metrics import structural_similarity 

class Helper(object):
    def __init__(self):
        pass

    def load_imgs(self, dir_path="./dataset/BlowingBubbles_416x240_50/", start=0, end=0, mode=1, file_format="png"):
        """
        Group the images of the training set
        :param dir_path:  the directory path where the image set locates
        :param start:  the start index of the training set image
        :param end:  the ending index of the training set image
        :param mode:  grouping mode
                      1: group every 3 images with consecutive index
                      2: extract images with the index interval of 2 into one group
        :param file_format:  image file format
        :return: a numpy array of grouped images
        """
        subset_size = 3
        increment = 1
        if mode == 2:
            increment = 2

        train_set = []
        train_subset = []
        for n in range(start, end, increment):
            f_path = dir_path + str(n) + "." + file_format
            if not (path.exists(f_path)):
                print("ERROR: FILE CAN NOT BE FOUND -- ", f_path)
                exit(0)

            img = cv2.imread(f_path, 1)
            if img is not None:
                if mode == 1:
                    train_subset.append(img)
                else:
                    train_set.append(img)
            else:
                print("WARNING: READ NULL IMAGE FROM FILE -- ", f_path)

            # For mode 2, the len(train_subset) == 0 since it is always be empty!
            if len(train_subset) == subset_size:
                train_set.append(np.array(train_subset))
                train_subset.pop(0)

        return np.array(train_set)

    def load_image(self, ph="./dataset/vimeo_triplet/", start=1, end=1):
        # expect path: "./dataset/vimeo_triplet/"
        if not(path.isdir(ph)):
            print("ERROR: PATH COULD NOT FOUND!")
            exit(0)
        ph += "sequences/00001/{:0>4d}/im{}.png"
        imgs = []
        for set_num in range(start, end):
            img_set = []
            for image_num in range(1, 4):
                if not(path.isfile(ph.format(set_num, image_num))):
                    print("ERROR: FILE COULD NOT FOUND! " + ph.format(set_num, image_num))
                    exit(0)
                img = cv2.imread(ph.format(set_num, image_num))
                img_set.append(img)
            imgs.append(img_set)
        cv2.destroyAllWindows()
        return np.asarray(imgs)

    def save_image(self, ph="./output/", index_start=1, images=[]):
        # expect image shape: (1,1,256,448,3)
        if not(path.isdir(ph)):
            os.mkdir(ph)
            print("Creating save image path:" + ph)
        filename = index_start
        ph += "{}.png"
        for img_set in images:
            cv2.imwrite(ph.format(filename), img_set[0])
            filename += 1
        cv2.destroyAllWindows()

    def plot_image(self, image):
        cv2.imshow('', image)
        cv2.destroyAllWindows()

    def performance_evaluation(self, image, pred, mode=1):
        img = np.array(image.reshape(-1, 3))
        res = pred.reshape(-1, 3)
        
        mse = mean_squared_error(img, res)
        psnr = peak_signal_noise_ratio(img, res)
        ssim = structural_similarity(img, res, multichannel=True)

        avg_mse = np.mean(mse)
        avg_psnr = np.mean(psnr)
        avg_ssim = np.mean(ssim)
        return avg_mse, avg_psnr, avg_ssim