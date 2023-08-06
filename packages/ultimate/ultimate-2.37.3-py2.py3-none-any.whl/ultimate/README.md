# ultimate
A scikit-learn compatible neural network implementation

## Installation
pip install ultimate

## Why Ultimate?
+ Support feature importance
+ Support missing values
+ Support am2x/a2m2x activation functions
+ Support softmax/hardmax/mse/hardmse loss functions
+ Support fc/add/conv/star operations

## How To Use?
<pre>
# let's use a simple example to learn how to use
from ultimate.mlp import MLP
import numpy as np

# generate sample
X = np.linspace(-np.pi, np.pi, num=5000).reshape(-1, 1)
Y = np.sin(X)
print(X.shape, Y.shape)

# fit and predict
mlp = MLP(layer_size=[X.shape[1], 8, 8, 8, 1], rate_init=0.02, loss_type="mse", epoch_train=100, epoch_decay=10, verbose=1)

mlp.fit(X, Y)
pred = mlp.predict(X)

# show the result
import matplotlib.pyplot as plt  
plt.plot(X, pred)
plt.show()
</pre>

## Examples
+ [Feature Importance](https://www.kaggle.com/anycode/feature-importance-using-nn)
+ [Image Regression](https://www.kaggle.com/anycode/image-regression)
+ [Iris Classification](https://www.kaggle.com/anycode/iris-classification)
+ [MNIST Recognition](https://www.kaggle.com/anycode/mnist-recognition)