# Mono face detection by deepface 

from deepface import DeepFace
import os

# Set the paths
train_dir = "/content/drive/MyDrive/Colab Notebooks/Image Dataset/Training Data"
test_dir = "/content/drive/MyDrive/Colab Notebooks/Image Dataset/Test Data/mono images"
# Verify the directory structure
print("Training images:")
print(os.listdir(train_dir))
print("Testing images:")
print(os.listdir(test_dir))

# DeepFace doesn't have a direct training function like other frameworks.
# Instead, it's more commonly used for pre-trained model inference and fine-tuning.

# Perform face recognition using DeepFace
models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib"]

# Example to find the best model
result = DeepFace.find(img_path="/content/drive/MyDrive/Colab Notebooks/Image Dataset/Training Data/ss1.jpeg", db_path=train_dir, model_name=models[0], enforce_detection=False)
print(result)
#df = pd.DataFrame(result)
#print(df.head())
print(result[0])
