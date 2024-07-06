import cv2
import numpy as np
# from tensorflow.keras.models import load_model

# Load the pre-trained model
model = ('fire_detection_model.h5')

def predict_fire(image_path):
    """
    Predict whether the image contains fire or not.

    Parameters:
    image_path (str): The path to the input image.

    Returns:
    str: 'Fire' if fire is detected, 'No Fire' otherwise.
    """
    # Load and preprocess the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))
    img = img.reshape((1, 256, 256, 3))

    # Make a prediction
    prediction = model.predict(img)

    # Determine the result
    result = 1 if prediction[0][0] > 0.5 else 0

    return result

