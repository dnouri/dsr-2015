import csv
import os

import numpy as np
from skimage.io import imread

from sklearn.base import BaseEstimator
from sklearn.decomposition import RandomizedPCA
from skimage.color import rgb2gray
from skimage.feature import hog
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


class HOGFeatures(BaseEstimator):
    def __init__(self, orientations=8, pixels_per_cell=(16, 16),
                 cells_per_block=(1, 1), image_shape=(32, 32, 3)):
        super(HOGFeatures, self).__init__()
        self.orientations = orientations
        self.pixels_per_cell = pixels_per_cell
        self.cells_per_block = cells_per_block
        self.image_shape = image_shape

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.reshape((X.shape[0],) + self.image_shape)
        result = []
        for image in X:
            if len(image.shape) == 3:
                image = rgb2gray(image)
            features = hog(
                image,
                orientations=self.orientations,
                pixels_per_cell=self.pixels_per_cell,
                cells_per_block=self.cells_per_block,
                )
            result.append(features)
        return np.array(result)


MODELS = {
    'linearsvc': (
        LinearSVC(),
        {'C': [0.01, 0.1, 1.0]},
        ),

    'linearsvc-pca': (
        Pipeline([
            ('pca', RandomizedPCA(n_components=100, whiten=True)),
            ('clf', LinearSVC(C=1.0)),
            ]),
        {'pca__n_components': [10, 30, 100], 'clf__C': [0.01, 0.1, 1.0]},
        ),

    'linearsvc-hog': (
        Pipeline([
            ('hog', HOGFeatures(
                orientations=8,
                pixels_per_cell=(4, 4),
                cells_per_block=(3, 3),
                )),
            ('clf', LinearSVC(C=1.0)),
            ]),
        {
            'hog__orientations': [8, 16],
            'hog__pixels_per_cell': [(4, 4), (6, 6)],
            'hog__cells_per_block': [(2, 2), (3, 3)],
            'clf__C': [0.1, 1.0],
            },
        ),
    }


def load(config, test=False):
    """Given the CSV file name and the folder for the Kaggle CIFAR
    dataset, return a dictionary with the following contents:

      - images:  n x 32 x 32 x 3  array
      - data:    n x 3072  array
      - target:  n  array
    """
    with open(config['csv_filename']) as csv_file:
        labels = list(csv.reader(csv_file))[1:]

    if test:
        idx_start, idx_end = config['test_set']
    else:
        idx_start, idx_end = config['train_set']

    labels = labels[idx_start:idx_end]

    filenames = [
        os.path.join(config['folder'], "{}.png".format(id))
        for id, label in labels
        ]
    target = [label for id, label in labels]

    n_images = len(filenames)
    images = np.zeros((n_images,) + config['img_size'], dtype=np.uint8)

    for index, filename in enumerate(filenames):
        image = imread(filename)
        images[index, :, :] = image

    if config['verbose']:
        print "Loaded {} images.".format(n_images)

    return {
        'images': images,
        'data': images.reshape((images.shape[0], -1)) / 255.0,
        'target': np.array(target),
        }
