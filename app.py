from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import torch
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from PIL import Image
import io
import numpy as np
from typing import List, Dict
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Helmet Detection API",
    description="Baret/Kask tespit eden FastAPI servisi",
    version="1.0.0"
)

model = None
device = None

def get_model(num_classes=3):
    """
    Faster R-CNN model oluşturur
    num_classes: background + helmet + head = 3
    """
    model = fasterrcnn_resnet50_fpn(weights=None)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

@app.on_event("startup")
async def load_model():
    """Uygulama başlarken model yüklenir"""
    global model, device
    
    try:
        logger.info("Model yükleniyor...")
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Device: {device}")
        
        model = get_model(num_classes=3)
        model.load_state_dict(torch.load('helmet_model.pth', map_location=device))
        model.to(device)
        model.eval()
        
        logger.info("✅ Model başarıyla yüklendi!")
        
    except Exception as e:
        logger.error(f"❌ Model yükleme hatası: {str(e)}")
        raise e

def process_image(image: Image.Image):
    """Görüntüyü model için hazırlar"""
    # RGB'ye çevir
    if image.mode != 'RGB':
        image = image.convert('RGB')
    

    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
    
    return transform(image)

@app.get("/")
async def root():
    """API ana sayfa"""
    return {
        "message": "Helmet Detection API",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Servis sağlık kontrolü"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device) if device else "not initialized"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Görüntüde baret/kask tespiti yapar
    
    Args:
        file: Yüklenecek görüntü dosyası (JPG, PNG)
    
    Returns:
        JSON formatında tespit sonuçları
    """
    try:
        # Model yüklü mü kontrol et
        if model is None:
            raise HTTPException(status_code=503, detail="Model yüklenmedi")
        
        # Dosya tipini kontrol et
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="Geçersiz dosya tipi. Lütfen bir görüntü dosyası yükleyin."
            )
        
     
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        logger.info(f"Görüntü yüklendi: {file.filename}, Boyut: {image.size}")
        
      
        img_tensor = process_image(image).to(device)
        
     
        with torch.no_grad():
            predictions = model([img_tensor])
        
  
        pred = predictions[0]
        boxes = pred['boxes'].cpu().numpy()
        labels = pred['labels'].cpu().numpy()
        scores = pred['scores'].cpu().numpy()
        

        threshold = 0.5
        
      
        class_names = {
            0: 'background',
            1: 'helmet',  # Baret
            2: 'head'     # Kask olmayan baş
        }
        
 
        detections = []
        for box, label, score in zip(boxes, labels, scores):
            if score >= threshold:
                detection = {
                    "class": class_names.get(int(label), "unknown"),
                    "confidence": float(score),
                    "bbox": {
                        "x_min": float(box[0]),
                        "y_min": float(box[1]),
                        "x_max": float(box[2]),
                        "y_max": float(box[3])
                    }
                }
                detections.append(detection)
        
        
        helmet_count = sum(1 for d in detections if d['class'] == 'helmet')
        head_count = sum(1 for d in detections if d['class'] == 'head')
        
        result = {
            "status": "success",
            "filename": file.filename,
            "image_size": {
                "width": image.size[0],
                "height": image.size[1]
            },
            "detections": detections,
            "summary": {
                "total_detections": len(detections),
                "helmet_count": helmet_count,
                "head_without_helmet_count": head_count,
                "safety_status": "SAFE" if head_count == 0 else "UNSAFE"
            }
        }
        
        logger.info(f"Tespit tamamlandı: {len(detections)} nesne bulundu")
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"İşlem hatası: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7001)
