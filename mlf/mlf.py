#! /usr/bin/env python

import cPickle
from datetime import datetime
import importlib
from pprint import pprint
import sys
from StringIO import StringIO

import Image
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from matplotlib import pyplot as plt
import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from skimage.io import imread
from skimage.transform import resize


app = Flask(__name__)


def load(loader, test=False, **cfg):
    module, name = loader.rsplit('.', 1)
    loader = getattr(importlib.import_module(module), name)
    return loader(test=test, **cfg)


def get_model(models, model_name, **cfg):
    module, name = models.rsplit('.', 1)
    models = getattr(importlib.import_module(module), name)
    return models[model_name]


def plot_some(**cfg):
    dataset = load(**cfg)
    n_images = dataset['images'].shape[0]

    fig = plt.figure(figsize=(6, 6))
    fig.subplots_adjust(
        left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

    for i, j in enumerate(np.random.choice(n_images, 64)):
        ax = fig.add_subplot(8, 8, i + 1, xticks=[], yticks=[])
        ax.imshow(dataset['images'][j])
        ax.text(0, 7, str(dataset['target'][j]))
    plt.show()


def search(model_name, cv=3, n_jobs=1, verbose=4, **cfg):
    model, param_grid = get_model(model_name=model_name, **cfg)
    dataset = load(**cfg)
    gs = GridSearchCV(
        model, param_grid,
        cv=cv,
        n_jobs=n_jobs,
        verbose=verbose,
        )
    gs.fit(dataset['data'], dataset['target'])

    pprint(sorted(gs.grid_scores_, key=lambda x: -x.mean_validation_score))

    now_str = datetime.now().isoformat().replace(':', '-')
    fname_out = '{}-{}.pickle'.format(model_name, now_str)
    with open(fname_out, 'wb') as fout:
        cPickle.dump(gs, fout, -1)

    print "Saved model to {}".format(fname_out)


def evaluate(model_filename, **cfg):
    with open(model_filename, 'rb') as fin:
        model = cPickle.load(fin)

    dataset = load(test=True, **cfg)
    data = dataset['data']
    images = dataset.get('images')
    y_true = dataset['target']
    target_names = map(str, sorted(np.unique(y_true)))

    if images is not None:
        # Plot some predictions
        n_images = images.shape[0]
        fig = plt.figure(figsize=(6, 6))
        fig.subplots_adjust(
            left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

        for i, j in enumerate(np.random.choice(n_images, 64)):
            ax = fig.add_subplot(8, 8, i + 1, xticks=[], yticks=[])
            ax.imshow(images[j])
            predicted = model.predict(np.array([data[j]]))[0]
            if predicted == y_true[j]:
                color = 'black'
            else:
                color = 'red'

            ax.text(0, 7, predicted, color=color)

    y_pred = model.predict(dataset['data'])

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.matshow(cm)
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.xticks(range(len(target_names)), target_names, rotation='vertical')
    plt.yticks(range(len(target_names)), target_names)

    # Classification report
    print classification_report(y_true, y_pred, target_names=target_names)

    plt.show()


def classify(image_filename, model_filename, **cfg):
    """Given the path to a trained model `model_filename` and path to
    a JPG or PNG image `image_filename`, output the predicted class.

    This function will accept images of any size and scale them down
    to 32x32.
    """
    with open(model_filename, 'rb') as fin:
        model = cPickle.load(fin)

    # load and resize image
    image = imread(image_filename)
    image = resize(image, (32, 32))
    data = np.array([image.flatten()])

    pred = model.predict(data)[0]
    print pred


_LOADED_MODEL = None


@app.route('/', methods=['GET'])
def web_form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def web_post():
    pil_image = Image.open(StringIO(request.files['image'].read()))
    image = np.array(pil_image)
    data = resize(image, (32, 32, 3)).reshape(1, -1)
    predicted = _LOADED_MODEL.predict(data)[0]
    return jsonify(prediction=predicted)


def flask(model_filename, **cfg):
    global _LOADED_MODEL

    with open(model_filename, 'rb') as fin:
        _LOADED_MODEL = cPickle.load(fin)

    app.run(debug=True)


def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and traning learning curve.

    Taken from
    http://scikit-learn.org/stable/modules/learning_curve.html
    """
    from sklearn.learning_curve import learning_curve  # soft dependency

    plt.figure()
    if ylim is not None:
        plt.ylim(*ylim)
    plt.title(title)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, train_sizes=train_sizes,
        n_jobs=n_jobs, verbose=1,
        )
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


def learning_curve(model_name, n_jobs=1, **cfg):
    model = get_model(model_name=model_name, **cfg)[0]
    dataset = load(**cfg)

    plt = plot_learning_curve(
        model,
        title="Learning curve for {}".format(model_name),
        X=dataset['data'],
        y=dataset['target'],
        n_jobs=n_jobs,
        )
    plt.show()


def _usage_and_exit():
    print "Usage: {} function-name config-filename".format(sys.argv[0])
    sys.exit(0)


def _load_config(filename):
    return eval(open(filename).read())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        _usage_and_exit()

    func = globals().get(sys.argv[1])
    if func is None:
        _usage_and_exit()

    cfg = _load_config(sys.argv[2])
    func(*sys.argv[3:], **cfg)
