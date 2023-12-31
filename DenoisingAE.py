# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1azdeXSTYXWokLi8kirJX8wdkjkyXiPTI

**DENOISING AUTO-ENCODER FROM SCRATCH**
"""

import numpy as np
import cv2

# Define the architecture of the denoising autoencoder
class DenoisingAutoencoder:
    def __init__(self, input_shape=(28, 28, 1), latent_dim=64):
        self.input_shape = input_shape
        self.latent_dim = latent_dim
        
        self.encoder = self.build_encoder()
        self.decoder = self.build_decoder()
        
        self.model = self.build_model()
    
    def build_encoder(self):
        input_layer = Input(shape=self.input_shape)
        x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
        x = MaxPooling2D((2, 2), padding='same')(x)
        x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = MaxPooling2D((2, 2), padding='same')(x)
        x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = MaxPooling2D((2, 2), padding='same')(x)
        x = Flatten()(x)
        encoded = Dense(self.latent_dim)(x)
        
        encoder = Model(input_layer, encoded, name='encoder')
        return encoder
    
    def build_decoder(self):
        input_layer = Input(shape=(self.latent_dim,))
        x = Dense(128)(input_layer)
        x = Reshape((4, 4, 8))(x)
        x = Conv2DTranspose(128, (3, 3), strides=(2, 2), padding='same', activation='relu')(x)
        x = Conv2DTranspose(64, (3, 3), strides=(2, 2), padding='same', activation='relu')(x)
        x = Conv2DTranspose(32, (3, 3), strides=(2, 2), padding='same', activation='relu')(x)
        decoded = Conv2DTranspose(1, (3, 3), activation='sigmoid', padding='same')(x)
        
        decoder = Model(input_layer, decoded, name='decoder')
        return decoder
    
    def build_model(self):
        input_layer = Input(shape=self.input_shape)
        encoded = self.encoder(input_layer)
        decoded = self.decoder(encoded)
        model = Model(input_layer, decoded, name='autoencoder')
        return model
    
    def compile_model(self):
        self.model.compile(optimizer='adam', loss='mse')
        
    def train(self, x_train, y_train, epochs=10, batch_size=32, verbose=1):
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
    
    def predict(self, x_test):
        return self.model.predict(x_test)

# Load the noisy image
img = cv2.imread('/content/balloons_noisy.png', 0)

# Add some noise to the image
mean = 0
variance = 50
sigma = np.sqrt(variance)
gaussian = np.random.normal(mean, sigma, img.shape)
noisy_img = img + gaussian

# Rescale the image values between 0 and 1
noisy_img = noisy_img.astype('float32') / 255.

# Prepare the data for

# Resize the image to the desired input shape of the model
input_shape = (28, 28)
noisy_img_resized = cv2.resize(noisy_img, input_shape)

# Generate clean images by blurring the noisy images
kernel_size = (3, 3)
clean_img = cv2.GaussianBlur(noisy_img_resized, kernel_size, 0)

# Create a dataset of pairs of noisy and clean images
x_train = noisy_img_resized.reshape(1, *input_shape, 1)
y_train = clean_img.reshape(1, *input_shape, 1)

# Repeat the dataset multiple times to increase the training data
n_repeats = 1000
x_train = np.repeat(x_train, n_repeats, axis=0)
y_train = np.repeat(y_train, n_repeats, axis=0)

from google.colab.patches import cv2_imshow

# Generate denoised images using the trained model
denoised_img = model.predict(x_train)

# Rescale the denoised images between 0 and 1
denoised_img = denoised_img.astype('float32') / 255.

# Display the original noisy image, the clean image, and the denoised image
cv2_imshow(noisy_img_resized)
cv2_imshow(clean_img)
cv2_imshow(denoised_img[0,:,:,0])
cv2.waitKey(0)
cv2.destroyAllWindows()
