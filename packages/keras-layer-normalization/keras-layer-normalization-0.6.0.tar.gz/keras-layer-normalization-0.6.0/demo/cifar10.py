import keras
import numpy as np
from keras.datasets import imdb
from keras_layer_normalization import LayerNormalization


BATCH_SIZE = 32
NUM_WORDS = 60000


(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=NUM_WORDS)

train_num = round(x_train.shape[0] * 0.9)
x_train, x_valid = x_train[:train_num, ...], x_train[train_num:, ...]
y_train, y_valid = y_train[:train_num, ...], y_train[train_num:, ...]


class Generator(keras.utils.Sequence):

    def __init__(self, x, y, batch_size=32):
        self.x = x
        self.y = y
        self.batch_size = batch_size

    def __len__(self):
        return (len(self.x) + self.batch_size - 1) // self.batch_size

    def __getitem__(self, i):
        begin = self.batch_size * i
        end = begin + self.batch_size
        bx = self.x[begin:end]
        max_len = max(map(len, bx))
        bx = [x + [0] * (max_len - len(x)) for x in bx]
        return np.array(bx), np.array(self.y[begin:end])


def get_bn_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Embedding(input_dim=NUM_WORDS, output_dim=100))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Bidirectional(keras.layers.GRU(units=50, return_sequences=True)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Bidirectional(keras.layers.GRU(units=50, return_sequences=False)))
    model.add(keras.layers.Dense(units=100, activation='tanh'))
    model.add(keras.layers.Dense(units=2, activation='softmax'))
    model.build(input_shape=(None, None))
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )
    return model


bn_model = get_bn_model()
bn_model.summary()
bn_model.fit_generator(
    generator=Generator(x_train, y_train, batch_size=BATCH_SIZE),
    validation_data=Generator(x_valid, y_valid, batch_size=BATCH_SIZE),
    epochs=10,
    callbacks=[
        keras.callbacks.ReduceLROnPlateau(monitor='val_acc', patience=1),
        keras.callbacks.EarlyStopping(monitor='val_acc', patience=2),
    ],
)
bn_score = bn_model.evaluate_generator(Generator(x_test, y_test, batch_size=BATCH_SIZE))
print('Score of BN model:\t%.4f' % bn_score[1])


def get_ln_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Embedding(input_dim=NUM_WORDS, output_dim=100))
    model.add(LayerNormalization())
    model.add(keras.layers.Bidirectional(keras.layers.GRU(units=50, return_sequences=True)))
    model.add(LayerNormalization())
    model.add(keras.layers.Bidirectional(keras.layers.GRU(units=50, return_sequences=False)))
    model.add(keras.layers.Dense(units=100, activation='tanh'))
    model.add(keras.layers.Dense(units=2, activation='softmax'))
    model.build(input_shape=(None, None))
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )
    return model


ln_model = get_ln_model()
ln_model.summary()
ln_model.fit(
    generator=Generator(x_train, y_train, batch_size=BATCH_SIZE),
    validation_data=Generator(x_valid, y_valid, batch_size=BATCH_SIZE),
    epochs=10,
    callbacks=[
        keras.callbacks.ReduceLROnPlateau(monitor='val_acc', patience=1),
        keras.callbacks.EarlyStopping(monitor='val_acc', patience=2),
    ],
)
ln_score = ln_model.evaluate_generator(Generator(x_test, y_test, batch_size=BATCH_SIZE))
print('Score of BN model:\t%.4f' % bn_score[1])
print('Score of LN model:\t%.4f' % ln_score[1])
