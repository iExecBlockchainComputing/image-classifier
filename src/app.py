import os
import json
import numpy as np
import tensorflow as tf
from os.path import join
from zipfile import ZipFile
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import imagenet_utils


def unizp_input_images():
    with ZipFile(join(input_directory, input_images_filename), 'r') as zipObj:
        print("unzipping files")
        zipObj.extractall(path=join(input_directory, input_images_folder), pwd=bytes(
            requester_secret, encoding='utf8'))


def load_classes():
    with open(join(input_directory, classes_filename), "r") as j:
        global prediction_classes
        prediction_classes = json.loads(j.read())


def load_model():
    global prediction_model
    prediction_model = tf.keras.models.load_model(
        join(input_directory, dataset_filename))


def classify_images():

    def prepare_image(img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array_expanded_dims = np.expand_dims(img_array, axis=0)
        return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

    def predict_image(img_path):
        preprocessed_image = prepare_image(img_path)
        predictions = prediction_model.predict(preprocessed_image)
        return(predictions)

    def classify_predictions(predictions):
        top = 5
        for pred in predictions:
            top_indices = pred.argsort()[-top:][::-1]
            decoded_prediction = [tuple(prediction_classes[str(i)]) + (pred[i],)
                                  for i in top_indices]
            decoded_prediction.sort(key=lambda x: x[2], reverse=True)
        return decoded_prediction

    def get_predictions_dict(predictions):
        result = {}
        for idx, prediction in enumerate(predictions):
            result.update({
                idx: {
                    "class": prediction[0],
                    "description": prediction[1],
                    "score": float(prediction[2])
                }
            })
        return result

    global prediction_results
    prediction_results = {}
    for idx, filename in enumerate(os.listdir(join(input_directory, input_images_folder))):
        if filename.endswith((".jpg", ".JPG")):
            image_path = join(input_directory, input_images_folder, filename)
            predictions = predict_image(image_path)
            predictions = classify_predictions(predictions)
            prediction_results[idx] = {
                "filename": filename,
                "predictions": get_predictions_dict(predictions)
            }


def save_results():
    print(json.dumps(prediction_results))
    with open(join(output_directory, "prediction_results.json"), "w+") as f:
        f.write(json.dumps(prediction_results))
    with open(join(output_directory, "computed.json"), "w+") as f:
        json.dump(
            {"deterministic-output-path": join(output_directory, "prediction_results.json")}, f)


if __name__ == '__main__':
    input_directory = os.environ["IEXEC_IN"]
    output_directory = os.environ["IEXEC_OUT"]
    dataset_filename = os.environ["IEXEC_DATASET_FILENAME"]
    requester_secret = os.environ["IEXEC_REQUESTER_SECRET_1"]
    classes_filename = "imagenet_class_index.json"
    input_images_filename = "input_images.zip"
    input_images_folder = "input_images"
    unizp_input_images()
    load_model()
    load_classes()
    classify_images()
    save_results()
