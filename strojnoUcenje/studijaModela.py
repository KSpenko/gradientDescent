import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from __bazaPodatkov import bazaPodatkov

# Nalaganje baze podatkov slik
(X_train, y_train), (X_test, y_test), class_num = bazaPodatkov()
clabel = ["letalo","avto","ptica","maček","jelen","pes","žaba","konj","ladja","tovornjak"] 

# Nalaganje že natreniranega modela
model = keras.models.load_model("cifar-cnn")
# Ocenitev natančnosti modela
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

# Poglejmo katere slike model prepozna ali ne
# CIFAR-10 baza: https://www.cs.toronto.edu/~kriz/cifar.html
predictions = model.predict(X_test)
for i in range(10):
    index = np.random.randint(0, len(predictions))
    plt.figure()
    plt.suptitle("Natančnost: %.2f%%" % (scores[1]*100) + "\n" + "Napoved: "+clabel[np.argmax(predictions[index])]+", Pravilno: "+clabel[np.argmax(y_test[index])])
    plt.imshow(X_test[index])
    plt.show()