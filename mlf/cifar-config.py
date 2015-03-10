{
    'n_jobs': -1,
    'verbose': True,

    'csv_filename': '/home/daniel/data/cifar-10-kaggle/trainLabels.csv',
    'folder': '/home/daniel/data/cifar-10-kaggle/train/',

    'models': 'cifar.MODELS',
    'model_name': 'linearsvc-hog',

    'loader': 'cifar.load',
    'train_set': (0, 40000),
    'test_set': (40000, 50000),
    'img_size': (32, 32, 3),
}
