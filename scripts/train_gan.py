#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%
import numpy as np
from numpy import expand_dims
from numpy import zeros
from numpy import ones
from numpy import vstack
from numpy.random import randn
from numpy.random import randint
from keras.datasets.mnist import load_data
from tensorflow.keras.optimizers import Adam
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Reshape
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import Conv2DTranspose
from keras.layers import LeakyReLU
from keras.layers import Dropout
from matplotlib import pyplot
from constants import WIDTH, HEIGHT
from data_preprocessing import preprocess_data
import os

#%%
def define_discriminator(in_shape=(WIDTH,HEIGHT,1)):
	model = Sequential()
	model.add(Conv2D(64, (3,3), strides=(2, 2), padding='same', input_shape=in_shape))
	model.add(LeakyReLU(alpha=0.2))
	model.add(Dropout(0.4))
	model.add(Conv2D(64, (3,3), strides=(2, 2), padding='same'))
	model.add(LeakyReLU(alpha=0.2))
	model.add(Dropout(0.4))
	model.add(Flatten())
	model.add(Dense(1, activation='sigmoid'))
	opt = Adam(lr=0.0002, beta_1=0.5)
	model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
	return model
#%%
def define_generator(latent_dim):
	model = Sequential()
	n_nodes = 128 * 8 * 8
	
	model.add(Dense(n_nodes, input_dim=latent_dim))
	model.add(LeakyReLU(alpha=0.2))
	model.add(Reshape((8, 8, 128)))
	for i in range(3):
		# upsample
		model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'))
		model.add(LeakyReLU(alpha=0.2))


	model.add(Conv2D(1, (8,8), activation='sigmoid', padding='same'))
	return model

def define_gan(g_model, d_model):
	d_model.trainable = False
	model = Sequential()
	model.add(g_model)
	model.add(d_model)
	opt = Adam(lr=0.0002, beta_1=0.5)
	model.compile(loss='binary_crossentropy', optimizer=opt)
	return model
# %%
def load_real_samples():
	num_samples = 0
	for dir in os.listdir('../data/Invisalign'):
		num_samples += sum(['front' in i for i in os.listdir('../data/Invisalign/' + dir)])
	
	X = np.empty((num_samples, WIDTH, HEIGHT, 1))
	i = 0
	for dir in os.listdir('../data/Invisalign'):
		for sample in os.listdir('../data/Invisalign/' + dir):
			if 'front' in sample:
				X[i,:,:,0] = preprocess_data(os.path.join('../data/Invisalign', dir, sample))
				i += 1

	X = X.astype('float32')
	X = X / 255.0
	return X
# %%
def generate_real_samples(dataset, n_samples):
	ix = randint(0, dataset.shape[0], n_samples)
	X = dataset[ix]
	y = ones((n_samples, 1))
	return X, y

def generate_latent_points(latent_dim, n_samples):
	x_input = randn(latent_dim * n_samples)
	x_input = x_input.reshape(n_samples, latent_dim)
	return x_input

def generate_fake_samples(g_model, latent_dim, n_samples):
	x_input = generate_latent_points(latent_dim, n_samples)
	X = g_model.predict(x_input)
	y = zeros((n_samples, 1))
	return X, y

def save_plot(examples, epoch, n=10):
	for i in range(n * n):
		pyplot.subplot(n, n, 1 + i)
		pyplot.axis('off')
		pyplot.imshow(examples[i, :, :, 0], cmap='gray_r')
	filename = 'generated_plot_e%03d.png' % (epoch+1)
	pyplot.savefig(filename)
	pyplot.close()

def summarize_performance(epoch, g_model, d_model, dataset, latent_dim, n_samples=100):
	X_real, y_real = generate_real_samples(dataset, n_samples)
	_, acc_real = d_model.evaluate(X_real, y_real, verbose=0)
	x_fake, y_fake = generate_fake_samples(g_model, latent_dim, n_samples)
	_, acc_fake = d_model.evaluate(x_fake, y_fake, verbose=0)
	print('>Accuracy real: %.0f%%, fake: %.0f%%' % (acc_real*100, acc_fake*100))

def train(g_model, d_model, gan_model, dataset, latent_dim, n_epochs=20, batch_size=32):
	n_batch = int(dataset.shape[0] / batch_size)
	half_batch = int(n_batch / 2)
	for i in range(n_epochs):
		for j in range(batch_size):
			X_real, y_real = generate_real_samples(dataset, half_batch)
			X_fake, y_fake = generate_fake_samples(g_model, latent_dim, half_batch)
			X, y = vstack((X_real, X_fake)), vstack((y_real, y_fake))
			d_loss, _ = d_model.train_on_batch(X, y)
			X_gan = generate_latent_points(latent_dim, n_batch)
			y_gan = ones((n_batch, 1))
			g_loss = gan_model.train_on_batch(X_gan, y_gan)
			print('>%d, %d/%d, d=%.3f, g=%.3f' % (i+1, j+1, batch_size, d_loss, g_loss))
		if (i+1) % 10 == 0:
			summarize_performance(i, g_model, d_model, dataset, latent_dim)

# %% size of the latent space
latent_dim = 100
d_model = define_discriminator()
g_model = define_generator(latent_dim)
gan_model = define_gan(g_model, d_model)
# %% load image data
dataset = load_real_samples()

# %% train model
train(g_model, d_model, gan_model, dataset, latent_dim)

g_model.save("../models/generator")

model = load_model("../models/generator")
X, y = generate_fake_samples(model, 100, 1)
pyplot.imshow(X[0,:,:,0], cmap='gray')
pyplot.savefig("../plots/fake_sample1.png")

# %%