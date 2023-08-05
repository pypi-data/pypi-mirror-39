# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import

def plot_importance(
    feature_importances,
    max_num_features=100,
    title='Feature Importances',
    feature_names=None,
):
    try:
        shape = feature_importances.shape
        if len(shape) > 1:
            import matplotlib.pyplot as plt

            feature_image = (feature_importances - feature_importances.min()) / (feature_importances.max() - feature_importances.min()) 

            if len(shape) == 2:
                plt.imshow(feature_image, cmap='gray')
            elif len(shape) == 3:
                if shape[0] < shape[2]:
                    feature_image = feature_image.transpose(1, 2, 0)   
                plt.imshow(feature_image)

            plt.title(title)
            plt.show()
            return
    except:
        pass

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
        return
    except:
        pass


if __name__ == '__main__':
    pass
