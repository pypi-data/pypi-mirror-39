# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import
import numpy
import warnings
import sys
import matplotlib
import matplotlib.pyplot as plt

def plot_image(data, title=None, expand=False, show=True):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            arr = numpy.array(data, numpy.float64)

            shape = arr.shape
            if len(shape) > 1:
                
                img = (arr - arr.min()) / (arr.max() - arr.min())

                if len(shape) == 2:
                    plt.imshow(img, cmap='gray')
                elif len(shape) == 3:
                    if expand:
                        if shape[0] > shape[2]:
                            img = img.transpose(1, 2, 0)

                        img = img.reshape(1, -1, img.shape[2])
                        plt.imshow(img[0], cmap='gray')
                    else:
                        if shape[0] < shape[2]:
                            img = img.transpose(1, 2, 0)

                        if img.shape[2] <= 2:
                            plt.imshow(img[:, :, 0], cmap='gray')
                        else:
                            plt.imshow(img[:, :, :4])

                if title is not None:
                    plt.title(title)
                plt.grid(False)

                fig = plt.gcf()
                if show: plt.show()
                return fig
        except:
            print("plot_image error", file=sys.stderr)

    return plt


def plot_importance(
    feature_importances,
    max_num_features=100,
    title='Feature Importances',
    feature_names=None,
    show=True
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            import pandas
            
            arr = numpy.array(feature_importances, numpy.float64).reshape(-1)

            if feature_names is None:
                feature_names = ['f'+str(i) for i in range(len(arr))]

            matplotlib.rc('font', **{'family': 'SimHei'})

            (pandas.Series(arr, index=feature_names)
                .nlargest(max_num_features).sort_values()
                .plot(kind='barh'))

            if title is not None:
                plt.title(title)

            fig = plt.gcf()
            if show: plt.show()
            return fig
        except:
            print("plot_importance error", file=sys.stderr)

    return plt


if __name__ == '__main__':
    plot_image([[1, 2], [3, 4]])
    plot_importance([[1, 2], [3, 4]])

    # plot_importance([[1, 2], [3, 4]]).savefig("test.png")

    # fig = plot_image([[1, 2], [3, 4]], show=False)
    # fig.savefig("test.png")
