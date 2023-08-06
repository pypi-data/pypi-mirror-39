# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import
import numpy
import warnings


def plot_image(data, title=None):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            arr = numpy.array(data, numpy.float64)

            shape = arr.shape
            if len(shape) > 1:
                import matplotlib.pyplot as plt

                img = (arr - arr.min()) / (arr.max() - arr.min())

                if len(shape) == 2:
                    plt.imshow(img, cmap='gray')
                elif len(shape) == 3:
                    if shape[0] < shape[2]:
                        img = img.transpose(1, 2, 0)
                    plt.imshow(img)

                if title is not None:
                    plt.title(title)
                plt.grid(False)
                plt.show()
        except:
            warnings.warn("plot_image error")


def plot_importance(
    feature_importances,
    max_num_features=100,
    title='Feature Importances',
    feature_names=None,
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            import pandas
            import matplotlib.pyplot as plt
            import matplotlib

            arr = numpy.array(feature_importances, numpy.float64).reshape(-1)

            if feature_names is None:
                feature_names = ['f'+str(i) for i in range(len(arr))]

            matplotlib.rc('font', **{'family': 'SimHei'})

            (pandas.Series(arr, index=feature_names)
                .nlargest(max_num_features).sort_values()
                .plot(kind='barh'))

            if title is not None:
                plt.title(title)
            plt.show()
        except:
            warnings.warn("plot_importance error")


if __name__ == '__main__':
    plot_image([[1, 2], [3, 4]])
    plot_importance([[1, 2], [3, 4]])
