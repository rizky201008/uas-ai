from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import joblib
import numpy as np
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input
from tensorflow.keras.models import Model
from sklearn.preprocessing import LabelEncoder
from io import BytesIO

app = FastAPI()

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
        predicted_class_idx = prediction[0]
        predicted_class_label = label_encoder.inverse_transform([predicted_class_idx])[0]
        # Convert predicted class to string
        predicted_class_label = str(predicted_class_label)
        return JSONResponse(content={"predicted_class": predicted_class_label})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
