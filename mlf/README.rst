mlf - my little framework
=========================

A small scikit-learn framework for definition, training, and
evaluation of machine learning algorithms.

This software is currently an alpha version.  Beware of API changes.

Developed for educational purposes, mlf is mostly a re-wrapping of
pieces of code that are found in scikit-learn's docs.

Usage::

  python mlf.py <command> <config-file> [args...]

An example for CIFAR-10 is provided.  It uses the version of CIFAR-10
that's available in the `Kaggle competition
<https://www.kaggle.com/c/cifar-10/data>`_.  To train one of the
example models on CIFAR-10, run::

  python mlf.py search cifar-config.py

The complete list of commands is:

- *search* runs a grid search using the training data and model
  defined in the configuration file.  The model with the best score is
  then pickled to disk.

- *evaluate* allows to evaluate a trained model (created by running
  *search*) on the held-out test set defined in the configuration file.
  It will plot a confusion matrix and print a classification report.
  If working with image data, evaluate will also plot some of the
  images along with their predicted class.

- *learning_curve* uses the training data and model defined in the
  configuration file to train and plot a learning curve.

- *plot_some*: plot some of the images in the dataset along with their
  label.  Only useful for image classification problems.

- *flask*: Run an example small flask server that classifies uploaded
  images.
