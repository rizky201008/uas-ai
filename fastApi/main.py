from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import joblib
import numpy as np
from keras.applications.vgg19 import VGG19, preprocess_input
from keras.models import Model
from io import BytesIO
import uvicorn
import pandas as pd

app = FastAPI()

categories = {
    0: "African Elephant",
    1: "Alpaca",
    2: "American Bison",
    3: "Anteater",
    4: "Arctic Fox",
    5: "Armadillo",
    6: "Baboon",
    7: "Badger",
    8: "Blue Whale",
    9: "Brown Bear",
    10: "Camel",
    11: "Dolphin",
    12: "Giraffe",
    13: "Groundhog",
    14: "Highland Cattle",
    15: "Horse",
    16: "Jackal",
    17: "Kangaroo",
    18: "Koala",
    19: "Manatee",
    20: "Mongoose",
    21: "Mountain Goat",
    22: "Opossum",
    23: "Orangutan",
    24: "Otter",
    25: "Polar Bear",
    26: "Porcupine",
    27: "Red Panda",
    28: "Black Rhinoceros",
    29: "Sea Lion",
    30: "Seal",
    31: "Snow Leopard",
    32: "Squirrel",
    33: "Sugar Glider",
    34: "Tapir",
    35: "Vampire Bat",
    36: "Vicuna",
    37: "Walrus",
    38: "Warthog",
    39: "Water Buffalo",
    40: "Weasel",
    41: "Wildebeest",
    42: "Wombat",
    43: "Yak",
    44: "Zebra",
}

# Load the trained model and label encoder
model_path = 'model/mlp_model.h5'
label_encoder_path = 'model/label_encoder.pkl'
model = joblib.load(model_path)
label_encoder = joblib.load(label_encoder_path)

# Load VGG19 model
base_model = VGG19(weights='imagenet', include_top=False)
feature_extractor = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)

# Load animal information dataset
animal_info_df = pd.read_csv('Animal Dataset.csv')
animal_info_dict = animal_info_df.set_index('Animal').T.to_dict()

def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    return image

def extract_features(image_array):
    features = feature_extractor.predict(image_array)
    features = features.flatten()
    return features

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the image file
        image = Image.open(BytesIO(await file.read()))
        # Preprocess the image
        preprocessed_image = preprocess_image(image)
        # Extract features
        features = extract_features(preprocessed_image)
        # Predict the class
        prediction = model.predict([features])
        predicted_class_idx = int(prediction[0])
        # Get the animal name
        predicted_class_label = categories.get(predicted_class_idx, "Unknown")
        # Get animal details
        animal_details = animal_info_dict.get(predicted_class_label, "No details available")
        return JSONResponse(content={"predicted_class": predicted_class_label, "details": animal_details})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
