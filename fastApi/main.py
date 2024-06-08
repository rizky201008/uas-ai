from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import joblib
import numpy as np
from keras.applications.vgg19 import VGG19, preprocess_input
from keras.models import Model
from io import BytesIO
import uvicorn

app = FastAPI()

categories = {
    0: "Gajah Afrika",
    1: "Alpaka",
    2: "Bison Amerika",
    3: "Pemakan Semut",
    4: "Rubah Arktik",
    5: "Armadilo",
    6: "Baboon",
    7: "Sigung",
    8: "Paus Biru",
    9: "Beruang Grizzly",
    10: "Onta",
    11: "Lumba-lumba",
    12: "Jerapah",
    13: "Marmot Tanah",
    14: "Sapi Skotlandia",
    15: "Kuda",
    16: "Serigala Emas",
    17: "Kangguru",
    18: "Koala",
    19: "Lembu laut",
    20: "Garangan",
    21: "Kambing Gunung",
    22: "Opossum",
    23: "Orangutan",
    24: "Berang-berang",
    25: "Beruang Kutub",
    26: "Landak",
    27: "Panda Merah",
    28: "Badak",
    29: "Singa Laut",
    30: "Anjing Laut",
    31: "Macan Tutul Salju",
    32: "Bajing",
    33: "Possum Layang",
    34: "Tapir",
    35: "Kelelawar Vampir",
    36: "Vikuna",
    37: "Walrus",
    38: "Babi Warthog",
    39: "Kerbau",
    40: "Cerpelai",
    41: "Gnu",
    42: "Wombat",
    43: "Yak",
    44: "Zebra",
    }

# Load the trained model
# Load the trained model and label encoder
model_path = 'model/mlp_model.h5'
label_encoder_path = 'model/label_encoder.pkl'
model = joblib.load(model_path)
label_encoder = joblib.load(label_encoder_path)

# Load VGG19 model
base_model = VGG19(weights='imagenet', include_top=False)
feature_extractor = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)

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
        predicted_class_idx = int(prediction[0])  # Pastikan ini integer
        # Get the animal name
        predicted_class_label = categories.get(predicted_class_idx, "Unknown")
        return JSONResponse(content={"predicted_class": predicted_class_label})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
