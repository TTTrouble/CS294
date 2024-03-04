import os
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision
from sklearn.datasets import make_swiss_roll

from deepul.models.vae import VAE

from .utils import (
    save_training_plot,
    save_scatter_2d,
    savefig,
    show_samples,
    get_data_dir,
)


def plot_training(losses, title, fname):
    plt.figure()
    n_itr = len(losses)


######################
##### Question 1 #####
######################


def q1_data(n=100000):
    x, _ = make_swiss_roll(n, noise=0.5)
    x = x[:, [0, 2]]
    return x.astype('float32')


def visualize_q1_dataset():
    data = q1_data()
    plt.figure()
    plt.scatter(data[:, 0], data[:, 1])
    plt.show()


def save_multi_scatter_2d(data: np.ndarray) -> None:
    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    for i in range(3):
        for j in range(3):
            axs[i, j].scatter(data[i * 3 + j, :, 0], data[i * 3 + j, :, 1])
    plt.title("Q1 Samples")
    savefig("results/q1_samples.png")


def q1_save_results(fn):
    train_data = q1_data(n=100000)
    test_data = q1_data(n=10000)
    train_losses, test_losses, samples = fn(train_data, test_data)

    print(f"Final Test Loss: {test_losses[-1]:.4f}")

    save_training_plot(
        train_losses,
        test_losses,
        f"Q1 Train Plot",
        f"results/q1_train_plot.png"
    )

    save_multi_scatter_2d(samples)
    

######################
##### Question 2 #####
######################

def load_q2_data():
    train_data = torchvision.datasets.CIFAR10("./data", transform=torchvision.transforms.ToTensor(),
                                              download=True, train=True)
    test_data = torchvision.datasets.CIFAR10("./data", transform=torchvision.transforms.ToTensor(),
                                              download=True, train=False)
    return train_data, test_data


def visualize_q2_data():
    train_data, _ = load_q2_data()
    imgs = train_data.data[:100]
    show_samples(imgs, title=f'CIFAR-10 Samples')


def q2_save_results(fn):
    train_data, test_data = load_q2_data()
    train_data = train_data.data / 255.0
    test_data = test_data.data / 255.0
    train_losses, test_losses, samples = fn(train_data, test_data)
    
    save_training_plot(
        train_losses,
        test_losses,
        "Q2(a) Train Plot",
        "results/q1_a_train_plot.png"
    ) 

    show_samples(samples * 255.0, fname="results/q2_a_samples.png", title=f"CIFAR-10 generated samples")


######################
##### Question 3 #####
######################

def load_q3_data():
    train_data = torchvision.datasets.CIFAR10("./data", transform=torchvision.transforms.ToTensor(),
                                              download=True, train=True)
    test_data = torchvision.datasets.CIFAR10("./data", transform=torchvision.transforms.ToTensor(),
                                              download=True, train=False)
    return train_data, test_data


def load_pretrain_vae():
    data_dir = get_data_dir(4)
    vae = VAE()
    vae.load_state_dict(torch.load(os.path.join(data_dir, f"vae_cifar10.pth")))
    vae.eval()
    return vae


def visualize_q3_data():
    train_data, _ = load_q3_data()
    imgs = train_data.data[:100]
    labels = train_data.targets[:100]
    show_samples(imgs, title=f'CIFAR-10 Samples')
    print('Labels:', labels)


def q3_save_results(fn):
    train_data, test_data = load_q3_data()
    train_images = train_data.data / 255.0
    train_labels = np.array(train_data.targets, dtype=np.int32)
    test_images = test_data.data / 255.0
    test_labels = np.array(test_data.targets, dtype=np.int32)
    vae = load_pretrain_vae()
    train_losses, test_losses, samples = fn(train_images, train_labels, test_images, test_labels, vae)
    
    save_training_plot(
        train_losses,
        test_losses,
        "Q3(a) Train Plot",
        "results/q1_a_train_plot.png"
    ) 

    show_samples(samples * 255.0, fname="results/q3_a_samples.png", title=f"CIFAR-10 generated samples")
