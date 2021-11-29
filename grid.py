import os
import numpy as np
import re
from PIL import Image
from utility import *
import imageio as io

def main():
    masked_train_path = "train/masked_train/"
    masked_test_path = "test/masked_test/"
    mask_path = "train/mask/"
    patch_size = 32
    saved_path = "train/patched_images/"
    input_train_images = [item for item in os.listdir(masked_train_path) if re.search("_training", item)]
    #input_test_images = [item for item in os.listdir(masked_test_path) if re.search("_test", item)]
    mask_train_images = [item for item in os.listdir(mask_path) if re.search("_training_mask", item)]
    for i, j in enumerate(input_train_images):
        image = io.imread(masked_train_path + j)
        mask_image = io.imread(mask_path + mask_train_images[i])
        mask_mat = np.array(mask_image)
        prob_mat = np.zeros(np.array(image).shape, dtype=np.float32)
        x_dim, y_dim, z_dim = prob_mat.shape
        #getting the two dimension where there is still eye
        x, y = np.where(mask_mat)
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        #calculate the number of patches in x and y direction
        num_of_x_patches = np.int(np.ceil((x_max - x_min)/patch_size))
        num_of_y_patches = np.int(np.ceil((y_max - y_min)/patch_size))
        for m in range(num_of_x_patches):
            for n in range(num_of_y_patches):
                patch_start_x = x_min + patch_size * m
                patch_end_x = x_min + patch_size * (m + 1)
                patch_start_y = y_min + patch_size * n
                patch_end_y = y_min + patch_size * (n + 1)
                if patch_end_x > x_dim:
                    patch_end_x = x_max
                    patch_start_x = x_max - patch_size
                if patch_end_y > y_dim:
                    patch_end_y = y_max
                    patch_start_y = y_max - patch_size
                prob_mat[patch_start_x: patch_end_x, patch_start_y] = 1
                prob_mat[patch_start_x: patch_end_x, patch_end_y] = 1
                prob_mat[patch_start_x, patch_start_y: patch_end_y] = 1
                prob_mat[patch_end_x, patch_start_y: patch_end_y] = 1

        createAndSaveImage(prob_mat, saved_path + j)
        print("Patched generated")


if __name__ == "__main__":
    main()