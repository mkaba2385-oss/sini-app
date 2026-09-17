import torch
import torch.nn as nn
from fastapi import FastAPI
from torchvision.models import resnet50
from PIL import Image
from torchvision import transforms
from fastapi import FastAPI, File, UploadFile
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models" / "resnet50_plantvillage_epoch3.pth"

CLASS_NAMES = [
    "Corn___Cercospora_leaf_spot_Gray_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites_Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]


def load_model():
    model = resnet50(weights=None)
    model.fc = nn.Linear(model.fc.in_features, len(CLASS_NAMES))

    state_dict = torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True,
    )

    model.load_state_dict(state_dict)
    model.eval()

    return model


model = load_model()



app = FastAPI(title="Sini ML Service")


@app.get("/")
def root():
    return {"message": "Sini ML Service is running"}

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_idx = probabilities.argmax(dim=1).item()
        confidence = probabilities[0, predicted_idx].item()

    return {
        "classe": CLASS_NAMES[predicted_idx],
        "confiance": confidence,
    }