from threading import Thread
from time import sleep

import cv2
import numpy as np
from classifier import is_bad_posture
from loader import event
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model_2.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
cam = cv2.VideoCapture(0)


def get_score(filename = "image.png"):

    image_to_process = Image.open("image.png").convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image_to_process = ImageOps.fit(image_to_process, size, Image.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image_to_process)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]


    return (class_name, confidence_score)


def posture_checker():
    filename = "image.png"
    while True:
        try:
            result, image = cam.read()

            cv2.imshow("image", image)

            cv2.imwrite(filename, image)

            class_name, confidence_score = get_score(filename)

            print("Class:", class_name[2:], end="")
            print("Confidence Score:", confidence_score)

            if event.isSet():
                break

        except KeyboardInterrupt:
            cam.release()
            cv2.destroyAllWindows()



if __name__=='__main__':
    posture_checker()

# closing the windows that are opened
cv2.destroyAllWindows()

