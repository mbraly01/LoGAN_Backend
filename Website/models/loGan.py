
#credit to Anish Shrestha . https://towardsdatascience.com/generating-modern-arts-using-generative-adversarial-network-gan-on-spell-39f67f83c7b4
import os
import numpy as np
from PIL import Image
from keras.layers import Input, Reshape, Dropout, Dense, Flatten
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential, Model, load_model
from keras.optimizers import Adam
from keras import backend as K
import tensorflow as tf

PREVIEW_ROWS = 1
PREVIEW_COLS = 1
PREVIEW_MARGIN = 1
EPOCHS = 9
SAVE_FREQ = EPOCHS // 9 #13
# Size vector to generate images from
NOISE_SIZE = 100
# Configuration
 # number of iterations #120
BATCH_SIZE = 10
GENERATE_RES = 3

#Used
IFP = "/home/mbraly/python-for-byte-academy/Final_Project/Website/ifp/ifp.npy"
IMAGE_SHAPE = (192,192, 3)

class Discriminator():

    def __init__(self):
        model = Sequential()
        model.add(Conv2D(50, kernel_size=3, strides=2,
        input_shape=IMAGE_SHAPE, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(100, kernel_size=3, strides=2, padding="same"))
        model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(200, kernel_size=3, strides=2, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(400, kernel_size=3, strides=1, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(800, kernel_size=3, strides=1, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        optimizer = Adam(1.5e-4, 0.5)
        input_image = Input(shape=IMAGE_SHAPE)
        validity = model(input_image)
        model = Model(input_image, validity)
        model.compile(loss="binary_crossentropy", optimizer=optimizer,
                     metrics = ["accuracy"])
        model.trainable = False
        self.model = model

class Generator():
    def __init__(self):
        model = Sequential()
        model.add(Dense(6 * 6 * 400, activation="relu", input_dim=NOISE_SIZE))
        model.add(Reshape((6, 6, 400)))
        model.add(UpSampling2D())
        model.add(Conv2D(400, kernel_size=3, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))
        model.add(UpSampling2D())
        model.add(Conv2D(400, kernel_size=3, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))
        for i in range(GENERATE_RES):
            model.add(UpSampling2D())
            model.add(Conv2D(400, kernel_size=3, padding="same"))
            model.add(BatchNormalization(momentum=0.8))
            model.add(Activation("relu"))
        model.summary()
        model.add(Conv2D(IMAGE_SHAPE[2], kernel_size=3, padding="same"))
        model.add(Activation("tanh"))
        input = Input(shape=(NOISE_SIZE,))
        generated_image = model(input)
        self.model = Model(input, generated_image)

def save_images(cnt, gen_image):
    image_array = np.full((IMAGE_SHAPE[0] + PREVIEW_MARGIN,
                                IMAGE_SHAPE[1] + PREVIEW_MARGIN,
                                IMAGE_SHAPE[2]), 255, dtype=np.uint8)
    image_count = 0
    for row in range(1):
        for col in range(1):
            image_array[0: IMAGE_SHAPE[0], 0: IMAGE_SHAPE[1]] = gen_image[image_count] * 255
            image_count += 1
            break
        break

    filename = "/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/src/output/img{}.jpg".format(cnt)
    im = Image.fromarray(image_array)
    im.save(filename)

def run():
    training_data = np.load(IFP)
    try:
        counter = 1
        while (counter*SAVE_FREQ) <= EPOCHS:
            os.remove("img{}.jpg".format(counter))
            counter += 1
    except:
        pass
    disc = Discriminator()
    gen = Generator()
    optimizer = Adam(1.5e-4, 0.5)
    random_input = Input(shape=(NOISE_SIZE,))
    generated_image = gen.model(random_input)
    validity = disc.model(generated_image)
    combined = Model(random_input, validity)
    combined.compile(loss="binary_crossentropy", optimizer=optimizer,
                    metrics=["accuracy"])
    # gen.model.compile(loss="binary_crossentropy", optimizer=optimizer,
    #                 metrics=["accuracy"])
    # disc.model.compile(loss="binary_crossentropy", optimizer=optimizer,
    #                 metrics=["accuracy"])
    y_real = np.ones((BATCH_SIZE, 1))
    y_fake = np.zeros((BATCH_SIZE, 1))
    fixed_noise = np.random.normal(0, 1, (1, NOISE_SIZE))
    cnt = 1
    for epoch in range(EPOCHS):
        idx = np.random.randint(0, training_data.shape[0], BATCH_SIZE)
        x_real = training_data[idx]
        noise=np.random.normal(0,1, (BATCH_SIZE, NOISE_SIZE))
        x_fake = gen.model.predict(noise)
        disc_metric_real = disc.model.train_on_batch(x_real, y_real)
        disc_metric_gen = disc.model.train_on_batch(x_fake, y_fake)
        disc_metric = 0.5 * np.add(disc_metric_real, disc_metric_gen)
        gen_metric = combined.train_on_batch(noise, y_real)
        if epoch % SAVE_FREQ == 0:
            save_images(cnt, x_fake)
            cnt += 1
        print("{} epoch, Discriminator accuracy: {}, Generator accuracy: {}".format(epoch, (100*  disc_metric[1]), (100 * gen_metric[1])))
            # Preview image Frame
for i in range(9):
    try:
        os.remove("img{}.jpg".format(i))
    except:
        pass


