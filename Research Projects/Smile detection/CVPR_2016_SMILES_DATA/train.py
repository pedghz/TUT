import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten, Reshape
from keras.layers.convolutional import Conv2D, MaxPooling2D, Conv3D, MaxPooling3D
# from skimage.measure import block_reduce
from keras.utils import np_utils
import os
from skimage import io
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score

src_path = 'datasets_None_73216c98-d83d-48b9-b4f6-e2ec9207d399_smiles_trset/smiles_trset/'
paths = [src_path + '0/', src_path + '1/']
X = []
y = []
for label, path in enumerate(paths):
    for filename in os.listdir(path):
        img = io.imread(path + filename)
        if img.shape == (224, 224, 3):
            # gray = np.average(img, axis=-1)
            X.append(img)
            y.append(label)

X = np.asarray(X)
y = np.asarray(y)
X = X.astype(np.float32) / 255.
y = y.astype(np.int32)

# convert classes to vector
nb_classes = 2
y = np_utils.to_categorical(y, nb_classes).astype(np.float32)

# shuffle all the data
indices = np.arange(len(X))
np.random.shuffle(indices)
X = X[indices]
y = y[indices]

# prepare weighting for classes since they're unbalanced
class_totals = y.sum(axis=0)
class_weight = class_totals.max() / class_totals

print(X.dtype, X.min(), X.max(), X.shape)
print(y.dtype, y.min(), y.max(), y.shape)

img_rows, img_cols, img_dim = X.shape[1:]
nb_filters = 32
nb_pool = 2
nb_conv = 3

# X = X.reshape(X.shape[0], img_cols, img_rows, 1)

model = Sequential()
# model.add(Reshape((1, img_rows, img_cols), input_shape=(img_rows, img_cols)))
model.add(Conv2D(nb_filters, (nb_conv, nb_conv), input_shape=(img_cols, img_rows, img_dim), activation='relu'))
model.add(Conv2D(nb_filters, (nb_conv, nb_conv), input_shape=(img_cols, img_rows, img_dim), activation='relu'))
model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

validation_split = 0.10
model.fit(X, y, batch_size=128, class_weight=class_weight, epochs=5, verbose=1, validation_split=validation_split)

open('model.json', 'w').write(model.to_json())
model.save_weights('weights.h5')

plt.plot(model.model.history.history['loss'])
plt.plot(model.model.history.history['acc'])
plt.plot(model.model.history.history['val_loss'])
plt.plot(model.model.history.history['val_acc'])
plt.show()

n_validation = int(len(X) * validation_split)
y_predicted = model.predict(X[-n_validation:])
print(roc_auc_score(y[-n_validation:], y_predicted))
