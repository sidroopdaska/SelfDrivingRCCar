"""mlp_training.py: Neural Network training using Back-propagation"""

import cv2
import glob
import numpy as np
from sklearn.model_selection import train_test_split
import sys
import time

# todo: look at k-fold cross validation, understgand the use of tr/va/te, see how to employ these to ensure
# good generalisation


def retrieve_data_set():
    """Retrieve data from all the .npz files and aggregate it into a
    data set for mlp training"""

    start_time = cv2.getTickCount()

    print("Loading data set...")

    image_array = np.zeros((1, 38400), 'float')
    label_array = np.zeros((1, 4), 'float')

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

    X = np.float32(image_array[1:, :])
    Y = np.float32(label_array[1:, :])
    print("Image array shape: {0}".format(X.shape))
    print("Label array shape: {0}".format(Y.shape))

    end_time = cv2.getTickCount()
    print("Data set load duration: {0}"
          .format((end_time - start_time) // cv2.getTickFrequency()))

    return X, Y


if __name__ == '__main__':
    X, Y = retrieve_data_set()

    # Split the data set with 7:3 ratio into training set and test set
    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2)

    # Create MLP model and train
    start_time = cv2.getTickCount()

    layer_sizes = np.int32([38400, 64, 4])
    model = cv2.ml.ANN_MLP_create()
    model.setLayerSizes(layer_sizes)
    model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
    model.setBackpropMomentumScale(0.0)
    model.setBackpropWeightScale(0.001)
    model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001))
    model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)

    print("Training MLP...")
    model.train(train_X, cv2.ml.ROW_SAMPLE, train_Y)

    end_time = cv2.getTickCount()
    duration = (end_time - start_time) // cv2.getTickFrequency()
    print("Training duration: {0}".format(duration))

    # Get the training accuracy
    ret_train, resp_train = model.predict(train_X)
    train_mean_sq_error = ((resp_train - train_Y) * (resp_train - train_Y)).mean()
    print("Train set error: {0:.2f}".format(train_mean_sq_error * 100))

    # Get the test accuracy
    ret_test, resp_test = model.predict(test_X)
    test_mean_sq_error = ((resp_test - test_Y) * (resp_test - test_Y)).mean()
    print("Test set error: {0:.2f}".format(test_mean_sq_error * 100))

    # Save model
    model.save("mlp_xml/mlp_{0}.xml".format(str(int(time.time()))))

