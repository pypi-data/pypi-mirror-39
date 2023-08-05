# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import


def plot_importance(
    feature_importances=[],
    max_num_features=100,
    title='Feature Importances',
    feature_names=None,
):
    try:
        if feature_names is None:
            feature_names=['f'+str(i) for i in range(len(feature_importances))]

        import pandas as pd
        import matplotlib.pyplot as plt
        import matplotlib

        matplotlib.rc('font', **{'family': 'SimHei'})

        (pd.Series(feature_importances, index=feature_names)
            .nlargest(max_num_features).sort_values()
            .plot(kind='barh'))

        plt.title(title)
        plt.show()
    except:
        pass


if __name__ == '__main__':
    pass
