import os
import numpy as np
import re
from PIL import Image
from utility import *
import imageio as io
from pathlib import Path

def main():
    masked_train_path = "CHASE_DB1/masked_images/"
    mask_path = "CHASE_DB1/mask/"
    label_path = "CHASE_DB1/labels/"
    patch_size = 32
    saved_path = "CHASE_DB1/patched_images/"
    grid_path = "CHASE_DB1/images_with_grid/"
    input_train_images = [item for item in os.listdir(masked_train_path)]

    # Create folders if they don't exist already
    Path('CHASE_DB1/patched_images/').mkdir(parents=True, exist_ok=True)
    Path('CHASE_DB1/images_with_grid/').mkdir(parents=True, exist_ok=True)

    mask_train_images = [item for item in os.listdir(mask_path)]
    label_train_images = [item for item in os.listdir(label_path)]

    for i, j in enumerate(input_train_images):
        image = io.imread(masked_train_path + j)
        mask_image = io.imread(mask_path + mask_train_images[i])
        label_image = io.imread(label_path + label_train_images[i])
        mask_mat = np.array(mask_image)
        label_mat = np.array(label_image)
        # prob_mat = np.zeros(np.array(image).shape, dtype=np.float32)
        prob_mat = np.array(image)
        image_mat = np.array(image)
        x_dim, y_dim, z_dim = prob_mat.shape
        # getting the two dimension where there is still eye
        x, y = np.where(np.sum(mask_mat,axis=2))
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        # calculate the number of patches in x and y direction
        num_of_x_patches = np.int(np.ceil((x_max - x_min) / patch_size))
        num_of_y_patches = np.int(np.ceil((y_max - y_min) / patch_size))
        for m in range(num_of_x_patches):
            for n in range(num_of_y_patches):
                end_x = False
                end_y = False
                patch_start_x = x_min + patch_size * m
                patch_end_x = x_min + patch_size * (m + 1)
                patch_start_y = y_min + patch_size * n
                patch_end_y = y_min + patch_size * (n + 1)
                # Modify the last patch in the row if it is out of bounds
                if patch_end_x >= x_dim:
                    patch_end_x = x_max
                    patch_start_x = x_max - patch_size
                    end_x = True
                if patch_end_y >= y_dim:
                    patch_end_y = y_max
                    patch_start_y = y_max - patch_size
                    end_y = True

                to_overlap = int(patch_size / 2)
                if patch_end_y + to_overlap >= y_dim:
                    end_y = True
                if patch_end_x + to_overlap >= x_dim:
                    end_x = True

                def saveOverlap(toSave, gridToSave, overlap):

                    # If you want to have the different patches (with and without vessels in different paths)
                    if 255 in gridToSave:
                        label = "vessel"
                        path_to_save = saved_path + "class_1/"
                    else:
                        label = "no_vessel"
                        path_to_save = saved_path + "class_0/"

                    # If you want to remove all the images which are almost totally black
                    tot_patch_size = patch_size ** 2
                    threshold = 5
                    if np.sum(np.mean(toSave, axis=2) > threshold) >= tot_patch_size / 10:
                        createAndSaveImage(toSave, saved_path + f"{label}_{m}_{n}_{j[:-3]}jpg")

                if end_x == False and end_y == False:
                    overlapping_patch = image_mat[patch_start_x + to_overlap: patch_end_x + to_overlap,
                                        patch_start_y + to_overlap: patch_end_y + to_overlap]
                    gridToSave = label_mat[patch_start_x + to_overlap: patch_end_x + to_overlap,
                                 patch_start_y + to_overlap: patch_end_y + to_overlap]
                    if overlapping_patch.shape != (32, 32, 3) or gridToSave.shape != (32, 32):
                        print("Wut")
                    saveOverlap(overlapping_patch, gridToSave, "x_y_")
                if end_x == False:
                    overlapping_patch = image_mat[patch_start_x + to_overlap: patch_end_x + to_overlap,
                                        patch_start_y: patch_end_y]

                    gridToSave = label_mat[patch_start_x + to_overlap: patch_end_x + to_overlap,
                                 patch_start_y: patch_end_y]
                    if overlapping_patch.shape != (32, 32, 3) or gridToSave.shape != (32, 32):
                        print("Wut")
                    saveOverlap(overlapping_patch, gridToSave, "x_")
                if end_y == False:
                    overlapping_patch = image_mat[patch_start_x: patch_end_x,
                                        patch_start_y + to_overlap: patch_end_y + to_overlap]

                    gridToSave = label_mat[patch_start_x: patch_end_x,
                                 patch_start_y + to_overlap: patch_end_y + to_overlap]
                    if overlapping_patch.shape != (32, 32, 3) or gridToSave.shape != (32, 32):
                        print("Wut")

                    saveOverlap(overlapping_patch, gridToSave, "y_")
                prob_mat[patch_start_x: patch_end_x, patch_start_y] = 1
                prob_mat[patch_start_x: patch_end_x, patch_end_y] = 1
                prob_mat[patch_start_x, patch_start_y: patch_end_y] = 1
                prob_mat[patch_end_x, patch_start_y: patch_end_y] = 1
                toSave = image_mat[patch_start_x: patch_end_x, patch_start_y:patch_end_y]
                # I generate the labels to automatize the work of the oracle
                gridToSave = label_mat[patch_start_x: patch_end_x, patch_start_y:patch_end_y]
                if toSave.shape != (32, 32, 3) or gridToSave.shape != (32, 32):
                    print("bdbdbdb")
                saveOverlap(toSave, gridToSave, "")

            createAndSaveImage(prob_mat, grid_path + j)
            print("Patches generated")

if __name__ == "__main__":
    main()