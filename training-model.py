import cv2
import os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow

# Function to read images from a folder
def read_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            images.append((img, filename))  # Store image and filename as a tuple
    return images

# Function to display images
def display_images(images, cols=3):
    n_images = len(images)
    rows = n_images // cols + (n_images % cols > 0)
    fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
    axes = axes.flatten()
    for (img, filename), ax in zip(images, axes):
        ax.imshow(img)
        ax.set_title(filename)  # Display image filename as title
        ax.axis('off')
    for ax in axes[len(images):]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# Example usage
folder_path = '/content/drive/MyDrive/Colab Notebooks/Image Dataset/Training Data'
images = read_images_from_folder(folder_path)

# Display images with filenames
display_images(images)
