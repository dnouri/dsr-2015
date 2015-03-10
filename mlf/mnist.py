import matplotlib.pyplot as plt
from lasagne import layers
from nolearn.nntools import NeuralNet
from lasagne.nonlinearities import softmax
import numpy as np
from sklearn.datasets import fetch_mldata
from sklearn.utils import shuffle


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class PlotLoss(object):
    def __init__(self, title=None, update_every=2):
        self.title = title
        self.update_every = update_every
        plt.ion()

    def __call__(self, nn, train_history):
        train_loss = [info['train_loss'] for info in train_history]
        valid_loss = [info['valid_loss'] for info in train_history]

        n_epochs = len(train_loss)
        if n_epochs % self.update_every != 0:
            return

        plt.clf()
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.grid()
        if self.title:
            plt.title(self.title)

        # Plot train and validation loss curves
        x = range(1, n_epochs + 1)
        plt.plot(x, train_loss, color='b', label='train')
        plt.plot(x, valid_loss, color='r', label='valid')
        plt.legend()

        # Place a marker whenever there was a new best valid loss:
        for i in range(n_epochs):
            if i == 0:
                continue
            if valid_loss[i] < min(valid_loss[:i]):
                plt.scatter([i + 1], [valid_loss[i]],
                            c='k', s=80, marker='+')

        plt.pause(0.0001)


class PlotWeights(object):
    def __init__(self, update_every=1):
        self.update_every = update_every
        plt.ion()
        fig = plt.figure(figsize=(12, 6))
        fig.subplots_adjust(
            left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

    def __call__(self, nn, train_history):
        if len(train_history) % self.update_every != 0:
            return

        # YOUR CODE HERE

        # Visualize the weights of the first 128 neurons of the first
        # hidden layer.

        # Use nn.get_all_params() to get a list of all the parameters
        # of your network, with one entry per layer.  Note that these
        # parameters are Theano shared variables and that you can
        # retrieve their actual value as numpy arrays using their
        # get_value() method.

        # Observe how the parameters of the first hidden layer is a
        # matrix of 784 by 128 numbers.  How would you index into the
        # matrix to get all the weights of connections going into the
        # first neuron of that layer?  And how would you best
        # visualize those weights?

        # Assign to weights_first_layer the numpy array that
        # represents all the weights of the first hidden layer:

        # weights_first_layer = ?

        fig = plt.gcf()
        fig.clf()

        # You may want to use the Python debugger to stop at this
        # point at play around with the variables:
        # import pdb; pdb.set_trace()

        for i in range(128):
            ax = fig.add_subplot(8, 16, i + 1, xticks=[], yticks=[])

            # Plot the weights of the i-th layer:

            # ax.imshow( ? )

        plt.pause(0.0001)


MODELS = {
    'nn': (
        NeuralNet(
            layers=[
                ('input', layers.InputLayer),
                ('hidden1', layers.DenseLayer),
                ('hidden2', layers.DenseLayer),
                ('output', layers.DenseLayer),
                ],
            update_learning_rate=0.01,
            update_momentum=0.9,

            input_shape=(None, 784),
            hidden1_num_units=128,
            hidden2_num_units=128,
            output_num_units=10,
            output_nonlinearity=softmax,

            max_epochs=100,
            verbose=4,

            on_epoch_finished=PlotLoss(title="nn"),
            #on_epoch_finished=PlotWeights(),
            ),

        # YOUR CODE HERE

        # Try out the 'nn' neural net and observe if it's overfitting
        # or underfitting.

        # Then decide if it's a good idea to increase the number of
        # neurons in the two hidden layers.  Or maybe it's a better
        # idea to increase the number of training examples?  (See
        # mnist-config.py.)
        {},
        ),
}


def load(train_set, test_set, test=False, **cfg):
    """Load MNIST dataset using scikit-learn.  Returns a dict with the
    following entries:

      - images:  n x 28 x 28 array
      - data:    n x 784  array
      - target:  n  array
    """
    dataset = fetch_mldata('mnist-original')
    X, y = dataset.data, dataset.target
    X = X.astype(np.float32) / 255.0
    y = y.astype(np.int32)

    if test:
        idx_start, idx_end = test_set
    else:
        idx_start, idx_end = train_set

    X, y = shuffle(X, y, random_state=42)
    X = X[idx_start:idx_end]
    y = y[idx_start:idx_end]

    return {
        'images': X.reshape(-1, 28, 28),
        'data': X,
        'target': y,
        }
