from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import json

class Identifier:
    def __init__(self, model_path="./models/model_v3_b20_trainable_conv.model", classes_path="classes.json", image_dims=(256,256)):
        self.classes_map = json.load(open(classes_path, "r"))
        self.classes_list = list(self.classes_map.keys())
        self.model = keras.models.load_model(model_path)
        self.IMAGE_DIMS = image_dims

    def predict_image(self, IMAGE_PATH):
        img = image.load_img(IMAGE_PATH, target_size=(self.IMAGE_DIMS), color_mode='rgb')
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)/255
        images = np.vstack([x])
        test = self.model(images)
        p_class = np.argmax(test.numpy()[0])
        probabilty = test[0][p_class].numpy()
        # return self.classes_map[self.classes_list[p_class]], round(probabilty*100, 2)
        return self.classes_list[p_class], round(probabilty*100, 2)