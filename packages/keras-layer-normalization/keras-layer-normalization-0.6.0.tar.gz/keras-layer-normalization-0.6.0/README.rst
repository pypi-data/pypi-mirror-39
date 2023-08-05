
Keras Layer Normalization
=========================


.. image:: https://travis-ci.org/CyberZHG/keras-layer-normalization.svg
   :target: https://travis-ci.org/CyberZHG/keras-layer-normalization
   :alt: Travis


.. image:: https://coveralls.io/repos/github/CyberZHG/keras-layer-normalization/badge.svg?branch=master
   :target: https://coveralls.io/github/CyberZHG/keras-layer-normalization
   :alt: Coverage


Implementation of the paper: `Layer Normalization <https://arxiv.org/pdf/1607.06450.pdf>`_

Install
-------

.. code-block:: bash

   pip install keras-layer-normalization

Usage
-----

.. code-block:: python

   import keras
   from keras_layer_normalization import LayerNormalization


   input_layer = keras.layers.Input(shape=(2, 3))
   norm_layer = LayerNormalization()(input_layer)
   model = keras.models.Model(inputs=input_layer, outputs=norm_layer)
   model.compile(optimizer='adam', loss='mse', metrics={},)
   model.summary()
