FROM python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY app.py .
COPY helmet_model.pth .

EXPOSE 7001


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7001"]
```






version: '3.8'

services:
  helmet-api:
    build: .
    container_name: helmet-detection-api
    ports:
      - "7001:7001"
    volumes:
      - ./helmet_model.pth:/app/helmet_model.pth
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```




1. Ana repo sayfasına dön
2. **"Add file"** → **"Create new file"**

**Dosya adı** kutusuna yaz:
```
test_api.py





import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:7001"

def test_root():
    """Ana sayfayı test et"""
    print("🧪 Test 1: Ana sayfa...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Test 1 başarılı!\n")

def test_health():
    """Sağlık kontrolünü test et"""
    print("🧪 Test 2: Sağlık kontrolü...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Test 2 başarılı!\n")

def test_predict(image_path):
    """Görüntü tespitini test et"""
    print("🧪 Test 3: Görüntü tespiti...")
    
    if not Path(image_path).exists():
        print(f"❌ Görüntü bulunamadı: {image_path}")
        print("ℹ️  Test görüntüsü hazırlamak için bir .jpg veya .png dosya yolu belirtin")
        return
    
    with open(image_path, "rb") as f:
        files = {"file": (Path(image_path).name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/predict", files=files)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
     
        print("\n📊 Tespit Özeti:")
        print(f"  - Toplam tespit: {result['summary']['total_detections']}")
        print(f"  - Baret: {result['summary']['helmet_count']}")
        print(f"  - Kask olmayan baş: {result['summary']['head_without_helmet_count']}")
        print(f"  - Güvenlik durumu: {result['summary']['safety_status']}")
        
        print("✅ Test 3 başarılı!\n")
    else:
        print(f"❌ Hata: {response.text}")

def main():
    print("=" * 60)
    print("🚀 Helmet Detection API Test")
    print("=" * 60 + "\n")
    

        test_root()
    
        test_health()
        
   
        print("ℹ️  Test 3 için bir test görüntüsü belirtin:")
        print("    python test_api.py --image path/to/your/test_image.jpg")
        print()
        
    except requests.exceptions.ConnectionError:
        print("❌ API'ye bağlanılamadı!")
        print("ℹ️  Servisin çalıştığından emin olun: docker-compose up")
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2 and sys.argv[1] == "--image":
        image_path = sys.argv[2]
        test_predict(image_path)
    else:
        main()
```



*.pth
*.pt
*.ckpt

.ipynb_checkpoints
*.ipynb

.vscode/
.idea/
*.swp
*.swo
*~


.DS_Store
Thumbs.db


test_images/
*.jpg
*.jpeg
*.png
*.gif


*.log
logs/


.env
.env.local

