import numpy as np
import os
from keras.models import load_model
import cv2
from PIL import Image
from flask import Flask, jsonify, request, render_template
from keras.applications.resnet_v2 import preprocess_input  
import requests

# URL for RASA chatbot API
RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

app = Flask(__name__)
# automatically reloads templates when they are changed
app.config['TEMPLATES_AUTO_RELOAD'] = True

# load pretrained models
try:
    classification_model = load_model("identification_models\ResNet152V2.h5", compile=False)
    identification_model = load_model("identification_models\SnakeDetectionModel_ResNet50.h5", compile=False)
except Exception as e:
    raise Exception("Error loading model : ", e)

@app.route("/")
def index():
    return render_template("index.html")

# snake identification process
def identification_image_preprocess(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    return img

# snake species classification process
def classification_image_preprocess(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    x = np.array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

# route for image prediction
@app.route("/predict", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files["image"]
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, "uploads", f.filename)
        f.save(filepath)

        # Checks if uploaded file is an image
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if '.' not in f.filename or f.filename.split('.')[-1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file format. Please upload a PNG or JPEG image.'}), 400

        # Identification model prediction
        try:
            identification_model_preprocess = identification_image_preprocess(filepath)
            prediction = identification_model.predict(identification_model_preprocess)
            predicted_class = np.argmax(prediction)
        except Exception as e:
            return jsonify({'error': 'Error predicting using identification model.'}), 500

        # Classification model prediction
        if predicted_class == 1:
            try:
                classification_model_preprocess = classification_image_preprocess(filepath)
                y = classification_model.predict(classification_model_preprocess)
                preds = np.argmax(y)
                index = ["Common Rat Snake", "Russel's Viper", "Forsten's Cat Snake", "Green Pit Viper"]
                text = str(index[preds])
                return render_template('predict-index.html', pred_text=text)
            except Exception as e:
                return jsonify({'error': 'Error predicting using classification model.'}), 500
        else:
            return render_template('invalid-image-index.html', pred_text="Not a snake.")
    return render_template('predict-index.html')

# route for receiving messages from the chatbot
@app.route('/webhook', methods=['POST'])
def webshook():
    user_message = request.json['message']
    print("User message", user_message)

    # send user message to RASA chatbot
    rasa_response = requests.post(RASA_API_URL, json={'message': user_message})

    # check if the response from RASA API is not successful (status code 200).
    if rasa_response.status_code != 200:
        return jsonify({'error': 'Error communicating with RASA API.'}), rasa_response.status_code

    # parse the JSON response from the RASA API
    rasa_response_json = rasa_response.json()
    print("Rasa response: ", rasa_response_json)

    # extract the text field from the first response message if available
    bot_response = rasa_response_json[0]['text'] if rasa_response_json else 'Sorry, I didn\'t get that'

    # return response in JSON format.
    return jsonify({'response': bot_response})

# run the flask app
if __name__ == "__main__":
    app.run(debug=True, threaded=False)