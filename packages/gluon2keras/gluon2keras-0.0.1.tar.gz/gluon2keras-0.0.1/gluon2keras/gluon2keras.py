import torch
import numpy as np
from gluon2pytorch import gluon2pytorch
from torch.autograd import Variable
from pytorch2keras.converter import pytorch_to_keras


def gluon2keras(model, input_shapes, verbose=False, names=False):
    """
    Deep neural network model converter from gluon to keras (via pytorch)
    :param model: gluon model to convert
    :param input_shapes: list of input shapes
    :param verbose: verbose output
    :param names: keras names (keep, short, random-suffix)
    :return: keras model
    """
    # Make sure it's hybrid and initialized
    model.hybridize()
    model.collect_params().initialize()

    # Convert gluon model to pytorch model
    pytorch_model = gluon2pytorch(model, input_shapes, dst_dir=None, pytorch_module_name='converted_model')
    pytorch_model.eval()

    # Fix shapes
    input_vars = []
    keras_shapes = []

    for shape in input_shapes:
        input_np = np.random.uniform(0, 1, shape)
        input_var = Variable(torch.FloatTensor(input_np))
        input_vars.append(input_var)
        keras_shapes.append(shape[1:])

    if len(input_vars) == 1:
        input_vars = tuple(input_vars)
    else:
        input_vars = tuple(*input_vars)

    # Convert pytorch model to keras
    k_model = pytorch_to_keras(pytorch_model, input_vars, keras_shapes, change_ordering=False, verbose=verbose, names=names)
    return k_model