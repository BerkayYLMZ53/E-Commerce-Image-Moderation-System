<img width="1644" height="957" alt="Banner" src="https://github.com/user-attachments/assets/c0d05e4d-ffc9-48a1-8a8b-9c0a4f00ffbe" />
<br>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/YOLOv8-00FFA6?style=for-the-badge&logo=ultralytics&logoColor=black" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
</p>

<br>
# 🛡️ Akıllı E-Ticaret Yorum Moderasyon Sistemi
### 🤖 Kendi Kendini Besleyen (Self-Feeding) Çoklu Referans & Nesne Algılama Motoru

Bu proje, e-ticaret platformlarındaki (Trendyol, Hepsiburada vb.) kullanıcı ürün yorum görsellerini otomatize edilmiş bir süzgeçten geçirerek manipülatif, hatalı, alakasız içerikleri veya kargo kutularını engellemek amacıyla geliştirilmiş **veri merkezli (Data-Centric) bir yapay zeka** moderasyon sistemidir. 

Sistem, geleneksel statik sınıflandırma modellerinin aksine, yaşayan ve kendi kararlarından beslenen dinamik bir mimariye sahiptir.

---
🚀 **Key Core Features**

*   **Two-Stage Hybrid Filter:** Uploaded images are first scanned with the YOLOv8 object detection model to detect and immediately eliminate elements that obscure the product, such as shipping boxes, packages, or bags. In the second stage, OpenAI's CLIP (Vision Transformer) model is used to measure the semantic similarity between the image and the product.
*   **Self-Feeding Architecture:** The system automatically integrates verified, clean real-user home environment photos that pass the specified safety threshold (65%+) into an isolated reference pool.
*   **Multi-View Matching:** Leveraging the real-user images accumulated in the pool, the system overcomes variations and inconsistencies—such as lens flares, harsh angles, and differing home textures—by evaluating based on the maximum similarity score (*max_similarity*). Consequently, the system's false negative rate approaches zero over time.
*   **Dynamic Counter & Time Optimization:** Thanks to a live progress bar and a dynamic countdown timer calculated based on average processing speed, the remaining time during batch analyses can be monitored in real time.
*   **Data Poisoning Protection:** Utilizing an isolated folder structure, unique timestamped logging, and mathematical early stopping optimizations, irrelevant products (for example, a coffee maker uploaded when an adapter is selected) are detected within seconds without causing deadlocks in the pool, preventing the degradation of the system's intelligence.

🛠️ **Installation and Setup**

You can follow the steps below to run the project on your local machine:

**1. Clone the Repository:**
```bash
git clone https://github.com/BerkayYLMZ53/E-Commerce-Image-Moderation-System.git
cd E-Commerce-Image-Moderation-System
```

**2. Install the Required Libraries:**
```bash
pip install streamlit torch transformers ultralytics pillow
```

**3. Start the Application:**
```bash
streamlit run app.py
```
📦 **Technologies Used**

*   **Python 3.10+**
*   **Streamlit** (Web Interface and Live Time Management)
*   **Ultralytics YOLOv8** (Object Detection)
*   **Hugging Face Transformers - OpenAI CLIP** (Semantic Similarity Vectorization)
*   **PyTorch** (Deep Learning Infrastructure)
*   **Pillow** (Image Processing and Dynamic Format Management)

## 📝 Project Origin and Motivation

This project was developed entirely out of an **original idea and R&D motivation**, without any academic obligations or course requirements. 

It emerged from the pursuit of a dynamic solution to improve user experience and data quality on e-commerce platforms, and was designed end-to-end through the lens of Management Information Systems (MIS) and data science. The project is open-source and remains open to further development and scaling by the community.

## 📊 Sistem Akış Mimarisi (Workflow)

```mermaid
graph TD
    A[Kullanıcı Yorum Resmi Yüklenir] --> B{YOLOv8 Süzgeci}
    B -- Kargo Kutusu/Poşet Tespit Edildi --> C[❌ REDDEDİLDİ: Kargo Kutusu]
    B -- Temiz Görsel --> D[CLIP Vision Transformer]
    
    D --> E{Çoklu Referans Kıyaslaması <br> max_similarity}
    E -- Skor < %65 Benzerlik Yetersiz --> F[❌ REDDEDİLDİ: Alakasız Resim]
    E -- Skor >= %65 Başarılı --> G[✅ ONAYLANDI]
    
    G --> H[Benzersiz Zaman Damgası ile İsimlendirme]
    H --> I[💾 referanslar/ Klasörüne Dinamik Kayıt]
    I --> J[🧠 Aktif Hafıza Havuzunun Büyümesi]
    J -->|Bir sonraki denetimde referans olarak kullanılır| E



