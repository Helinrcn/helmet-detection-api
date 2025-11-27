#!/usr/bin/env python3
"""
Helmet Detection API Test Script
"""

import requests
import json
from pathlib import Path

# API URL
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
        
        # Özet bilgi
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
    
    try:
        # Test 1: Ana sayfa
        test_root()
        
        # Test 2: Sağlık kontrolü
        test_health()
        
        # Test 3: Görüntü tespiti (opsiyonel)
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
    
    # Komut satırından görüntü yolu al
    if len(sys.argv) > 2 and sys.argv[1] == "--image":
        image_path = sys.argv[2]
        test_predict(image_path)
    else:
        main()
```

5. **"Commit new file"** tıkla

---

### ADIM 3: .gitignore Ekle

1. Ana sayfaya dön
2. **"Add file"** → **"Create new file"**
3. **Dosya adı:** `.gitignore` (noktayı unutma!)
4. **İçeriği yapıştır:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# PyTorch model files
*.pth
*.pt
*.ckpt

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Test images
test_images/
*.jpg
*.jpeg
*.png

# Logs
*.log

# Environment
.env
