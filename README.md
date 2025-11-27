# 🪖 Helmet Detection FastAPI

Baret/Kask Tespit Sistemi - PyTorch + FastAPI + Docker

## 🎯 Proje Hakkında

Bu proje, PyTorch Faster R-CNN modeli kullanarak görüntülerde baret/kask tespiti yapan bir REST API servisidir.

**Özellikler:**
- ✅ Baret/kask takan kişileri tespit eder
- ⚠️ Kask takmayan kişileri belirler  
- 📊 Güvenlik durumu raporu oluşturur
- 🎯 Her tespitin konumunu ve güven skorunu verir

## 🚀 Hızlı Başlangıç

### 1. Repo'yu Klonla
```bash
git clone https://github.com/KULLANICI_ADIN/helmet-detection-api.git
cd helmet-detection-api
```

### 2. Model Dosyasını Ekle ⚠️

Google Drive'dan `helmet_model.pth` dosyanızı indirin ve proje dizinine yerleştirin:
```bash
cp ~/Downloads/helmet_model.pth ./helmet_model.pth
```

### 3. Docker ile Çalıştır
```bash
docker-compose up --build
```

### 4. Test Et

Tarayıcıda aç: http://localhost:7001/docs

## 📡 API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/` | Ana sayfa |
| GET | `/health` | Sağlık kontrolü |
| POST | `/predict` | Görüntü tespiti |
| GET | `/docs` | Swagger UI |

## 🧪 Test
```bash
# Ana sayfa
curl http://localhost:7001

# Sağlık kontrolü
curl http://localhost:7001/health

# Görüntü tespiti
curl -X POST "http://localhost:7001/predict" -F "file=@test_image.jpg"

# Python ile test
python test_api.py
```

## 🐳 Docker Komutları
```bash
docker-compose up --build  # İlk kez çalıştır
docker-compose up -d       # Arka planda çalıştır
docker-compose down        # Durdur
docker-compose logs -f     # Logları göster
```

## 📊 Model Bilgileri

- **Model**: Faster R-CNN (ResNet50 FPN)
- **Framework**: PyTorch
- **Sınıflar**: Helmet (baret), Head (kask olmayan baş)
- **Input**: RGB görüntü
- **Output**: Bounding boxes + confidence scores

## 🛠️ Teknolojiler

- FastAPI 0.104.1
- PyTorch 2.1.0
- Docker & Docker Compose
- Python 3.10

## 📧 İletişim

staj@diginova.com.tr
```

