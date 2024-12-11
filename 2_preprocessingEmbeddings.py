import os
import pickle
import numpy as np
import cv2
import imutils
from imutils import paths

dataset = "dataset"
embeddingFile = "output/embeddings.pickle"
embeddingModel = "model/openface_nn4.small2.v1.t7"
prototxt = "model/deploy.prototxt"
model = "model/res10_300x300_ssd_iter_140000.caffemodel"

# Verify model files and create directories if necessary
if not os.path.isdir("model"):
    os.makedirs("model")

if not os.path.isfile(prototxt):
    print(f"Prototxt file not found at: {prototxt}")
    raise FileNotFoundError("Prototxt file not found!")

if not os.path.isfile(model):
    print(f"Model file not found at: {model}")
    raise FileNotFoundError("Model file not found!")

# Load the face detection model
detector = cv2.dnn.readNetFromCaffe(prototxt, model)

# Load the facial embeddings model
if not os.path.isfile(embeddingModel):
    print(f"Embedding model file not found at: {embeddingModel}")
    raise FileNotFoundError("Embedding model file not found!")
else:
    embedder = cv2.dnn.readNetFromTorch(embeddingModel)

# Ensure output directory exists
output_dir = os.path.dirname(embeddingFile)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get image paths
imagePaths = list(paths.list_images(dataset))

# Initialize lists for known embeddings and names
knownEmbeddings = []
knownNames = []
total = 0
conf = 0.5

# Process each image
for (i, imagePath) in enumerate(imagePaths):
    print("Processing image {}/{}".format(i + 1, len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=600)
    (h, w) = image.shape[:2]

    # Convert image to blob for DNN face detection
    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # Print blob shape for debugging
    print("ImageBlob shape:", imageBlob.shape)

    # Set input blob image
    detector.setInput(imageBlob)
    detections = detector.forward()

    if len(detections) > 0:
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        if confidence > conf:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            knownNames.append(name)
            knownEmbeddings.append(vec.flatten())
            total += 1

print("Embeddings: {0}".format(total))
data = {"embeddings": knownEmbeddings, "names": knownNames}

# Ensure the output directory exists and save the embeddings
if not os.path.exists(os.path.dirname(embeddingFile)):
    os.makedirs(os.path.dirname(embeddingFile))

with open(embeddingFile, "wb") as f:
    f.write(pickle.dumps(data))

print("Process Completed")
