# Import the necessary Libraries
import numpy as np
import pandas as pd
import matplotlib
import sklearn
import sklearn.metrics as metrics
import matplotlib.pyplot as ply
import tensorflow as tf

from tensorflow.keras.callbacks import ModelCheckpoint,CSVLogger
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.utils import plot_model
from tensorflow.keras.datasets import cifar10
from tensorflow.keras import optimizers

print("Versions of key libraries")
print("---")
print("tensorflow: ", tf.__version__)
print("numpy:      ", np.__version__)
print("matplotlib: ", matplotlib.__version__)
print("sklearn:    ", sklearn.__version__)


# File Path
TRAINFEATURES_FILE = "./data/train_values.csv"
TRAINLABELS_FILE = "./data/train_labels.csv"
TESTFEATURES_FILE = "./data/test_values.csv"


# Load the Data
X_full = pd.read_csv(TRAINFEATURES_FILE)
y_full = pd.read_csv(TRAINLABELS_FILE)


# EDA
print("The shape of training data, X is ", X_full.shape)
print("The shape of training label, y is ", y_full.shape)
print("")
print("Additional Information")
print("Features")
print(X_full.info())
print(X_full.describe())
print("Labels")
print(y_full.info())
print(y_full.describe())
X_full.set_index(["building_id"], inplace=True)
y_full.set_index(["building_id"], inplace=True)
print("")
print(X_full.head())
print(y_full.head())