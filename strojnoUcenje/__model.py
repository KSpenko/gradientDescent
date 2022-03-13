import numpy
from tensorflow import keras
from keras.constraints import maxnorm

seed = 21

from __bazaPodatkov import bazaPodatkov

# Nalaganje baze podatkov slik
(X_train, y_train), (X_test, y_test), class_num = bazaPodatkov()

# Sestavljanje modela
# POKUSI spremenite plasti nevronske mreže, tako da dodaš, odvzameš plast ali pa spremeniš njene parametre!
# Več o posameznih tipih lasti: https://keras.io/api/layers/
model = keras.Sequential()
model.add(keras.layers.Conv2D(32, (3, 3), input_shape=X_train.shape[1:], padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.Conv2D(32, 3, input_shape=(32, 32, 3), activation='relu', padding='same'))
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.BatchNormalization())

model.add(keras.layers.Conv2D(64, 3, activation='relu', padding='same'))
model.add(keras.layers.MaxPooling2D(2))
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.BatchNormalization())

model.add(keras.layers.Conv2D(64, 3, activation='relu', padding='same'))
model.add(keras.layers.MaxPooling2D(2))
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.BatchNormalization())
    
model.add(keras.layers.Conv2D(128, 3, activation='relu', padding='same'))
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.BatchNormalization())

model.add(keras.layers.Flatten())
model.add(keras.layers.Dropout(0.2))

model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dropout(0.3))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dense(class_num, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary()) # Izpisek sestavljenega modela

# Učenje modela: POZOR program je zelo počasen 2h+
numpy.random.seed(seed)
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=25, batch_size=64)
# Shranimo model
model.save("cifar-cnn")

import pandas as pd
import matplotlib.pyplot as plt

# Prikaz zgodovine učenja oz. treninga!
pd.DataFrame(history.history).plot()
plt.show()