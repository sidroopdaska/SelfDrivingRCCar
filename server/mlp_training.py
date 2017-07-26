"""mlp_training.py: Neural Network training"""

import cv2
import sys
import numpy as np
import glob
from sklearn.model_selection import train_test_split

def retrieve_data_set():
    """Retrieve data from all the .npz files and aggregate it into a
    data set for mlp training"""
    start_time = cv2.getTickCount()

    print("Loading data set...")

    image_array = np.zeros((1, 38400))
    label_array = np.zeros((1, 4))

    # Retrieve a list of pathname that matches the below expr
    data_set = glob.glob("data_set/*.npz")

    if not data_set:
        print("No data set in directory, exiting!")
        sys.exit()

    for single_npz in data_set:
        with np.load(single_npz) as data:
            temp_images = data["images"]
            temp_labels = data["labels"]

        image_array = np.vstack((image_array, temp_images))
        label_array = np.vstack((label_array, temp_labels))

    X = image_array[1:, :]
    Y = label_array[1:, :]
    print("Image array shape: {0}".format(X.shape))
    print("Label array shape: {0}".format(Y.shape))

    end_time = cv2.getTickCount()
    print("Data set load duration: {0}"
          .format((end_time - start_time) // cv2.getTickFrequency()))

    return X, Y


if __name__ == '__main__':
    X, Y = retrieve_data_set()

    # Split the data set with 7:3 ratio into training set and test set
    train_X, train_Y, test_X, test_Y = train_test_split(X, Y, test_size=0.3)

    # Create MLP
