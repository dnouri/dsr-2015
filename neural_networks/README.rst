Resources for DSR neural networks tutorial
==========================================

- `Online course on neural networks
  <http://info.usherbrooke.ca/hlarochelle/neural_networks/content.html>`_
  by Hugo Larochelle

- `Neural Networks and Deep Learning online book
  <http://neuralnetworksanddeeplearning.com/>`_ by Michael Nielsen

- `ConvNetJS: Deep Learning in your browser
  <http://cs.stanford.edu/people/karpathy/convnetjs/>`_ by Andrej
  Karpathy

- `Neural Networks, Manifolds, and Topology
  <http://colah.github.io/posts/2014-03-NN-Manifolds-Topology/>`_ by
  Christopher Olah

- Visual comparison of some optimization algorithms by Alec Radford:
  `1 <http://imgur.com/a/Hqolp>`_ `2 <http://imgur.com/s25RsOr>`_

- `Caffe network visualization notebook
  <http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/filter_visualization.ipynb>`_

- `Deep Learning Tutorials <http://www.deeplearning.net/tutorial/>`_
  by Theano Development Team

Software
========

We'll use Theano, nntools and nolearn.

To install::

    cd ~/src  # or wherever you keep your source

    git clone https://github.com/Theano/Theano.git
    cd Theano
    python setup.py develop
    cd ..

    git clone https://github.com/benanne/nntools.git
    cd nntools
    python setup.py develop
    cd ..

    git clone https://github.com/dnouri/nolearn.git
    cd nolearn
    python setup.py develop
    cd ..
