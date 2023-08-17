from keras.utils import to_categorical
from keras.datasets import cifar10

def bazaPodatkov():
    """ Nalaganje baze podatkov slik """
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()

    # Obdelava in normiranje slik
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train = X_train / 255.0
    X_test = X_test / 255.0

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    class_num = y_test.shape[1]
    return (X_train, y_train), (X_test, y_test), class_num