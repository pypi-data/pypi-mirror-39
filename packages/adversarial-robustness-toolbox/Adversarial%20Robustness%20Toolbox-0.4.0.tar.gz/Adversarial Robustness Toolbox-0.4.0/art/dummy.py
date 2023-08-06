"""
This is an example of how to use ART and Keras to perform adversarial training using data generators for CIFAR10
"""
import keras
from keras.datasets import cifar10
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils

from art.attacks import FastGradientMethod, DeepFool
from art.classifiers import KerasClassifier
from art.data_generators import KerasDataGenerator
from art.defences import AdversarialTrainer


# Example CIFAR classifier architecture with Keras & ART
def cnn_mnist_k(input_shape):
    # Create simple CNN
    model = Sequential()
    model.add(Conv2D(4, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(10, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(lr=0.01),
                  metrics=['accuracy'])

    cl = KerasClassifier((0, 1), model, use_logits=False)

    return cl

# Load data
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Regular preprocessing / normalization
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
y_train = np_utils.to_categorical(y_train, 10)  # FYI, there is a version of this function also in art.utils
y_test = np_utils.to_categorical(y_test, 10)
x_train /= 255
x_test /= 255

# Build a Keras data generator and wrap it in ART
datagen = ImageDataGenerator(horizontal_flip=True, width_shift_range=0.125, height_shift_range=0.125,
                             fill_mode='constant', cval=0.)
art_datagen = KerasDataGenerator(datagen, size=None, batch_size=128)

# Create classifier
classifier = cnn_mnist_k((32, 32, 3))

# Create attack for adversarial trainer; here, we use 2 attacks, both crafting adv examples on the target model
attack1 = FastGradientMethod(classifier)
attack2 = DeepFool(classifier)

# Create adversarial trainer and perform adversarial training
adv_trainer = AdversarialTrainer(classifier, attacks=[attack1, attack2])
adv_trainer.fit_generator(art_datagen, nb_epochs=5)
