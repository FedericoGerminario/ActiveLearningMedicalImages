import numpy as np
import tensorflow as tf
from utility import *
import train

def main():
    train_images_path = "train/images"
    train_input_path = "train/patched_images/"
    train_CHASE_DB1_path = "CHASE_DB1/patched_images"
    test_path = "train/patched_images_test"

    # get the labels for segmentation through kmeans/canny and eventually an additional dataset
    # labels = train.train_whole_dataset(train_input_path, train_CHASE_DB1_path, test_path,
    #                                    use_second_dataset=False, method="canny")
    labels = train.train_active_learning(train_input_path, num_iterations=1,
                                         metrics="least_confidence", method="canny")
    train.segnet(train_images_path, labels)

    print("End")

if __name__ == "__main__":
    main()