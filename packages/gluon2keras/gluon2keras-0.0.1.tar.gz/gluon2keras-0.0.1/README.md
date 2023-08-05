# gluon2keras
Gluon to Keras deep neural network model converter

[![Build Status](https://travis-ci.com/nerox8664/gluon2keras.svg?branch=master)](https://travis-ci.com/nerox8664/gluon2keras)
[![GitHub License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-2.7%2C3.6-lightgrey.svg)](https://github.com/nerox8664/gluon2keras)

## Installation

```
git clone https://github.com/nerox8664/gluon2keras
cd gluon2keras
pip install -e .
```

or you can use `pip`:

```
pip install gluon2keras
```

## Usage

```
# Get a model from gluon cv
from gluoncv2.model_provider import get_model as glcv2_get_model
net = glcv2_get_model("xception")

# Make sure it's hybrid and initialized
net.hybridize()
net.collect_params().initialize()

# Test input
input_np = np.random.uniform(0, 1, (1, 3, 299, 299))
gluon_output = net(mx.nd.array(input_np))

# Keras model
k_model = gluon2keras(net, [(1, 3, 299, 299)], verbose=True, names='short')
error = check_error(gluon_output, k_model, input_np)
```

## Code snippets
Look at the `tests` directory.

## License
This software is covered by MIT License.