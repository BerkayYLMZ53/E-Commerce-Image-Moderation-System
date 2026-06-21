# 🛡️ Akıllı E-Ticaret Yorum Moderasyon Sistemi
### 🤖 Kendi Kendini Besleyen (Self-Feeding) Çoklu Referans & Nesne Algılama Motoru

Bu proje, e-ticaret platformlarındaki (Trendyol, Hepsiburada vb.) kullanıcı ürün yorum görsellerini otomatize edilmiş bir süzgeçten geçirerek manipülatif, hatalı, alakasız içerikleri veya kargo kutularını engellemek amacıyla geliştirilmiş **veri merkezli (Data-Centric) bir yapay zeka** moderasyon sistemidir. 

Sistem, geleneksel statik sınıflandırma modellerinin aksine, yaşayan ve kendi kararlarından beslenen dinamik bir mimariye sahiptir.

---

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

🚀 **Key Core Features**

*   **Two-Stage Hybrid Filter:** Uploaded images are first scanned with the YOLOv8 object detection model to detect and immediately eliminate elements that obscure the product, such as shipping boxes, packages, or bags. In the second stage, OpenAI's CLIP (Vision Transformer) model is used to measure the semantic similarity between the image and the product.
*   **Self-Feeding Architecture:** The system automatically integrates verified, clean real-user home environment photos that pass the specified safety threshold (65%+) into an isolated reference pool.
*   **Multi-View Matching:** Leveraging the real-user images accumulated in the pool, the system overcomes variations and inconsistencies—such as lens flares, harsh angles, and differing home textures—by evaluating based on the maximum similarity score (*max_similarity*). Consequently, the system's false negative rate approaches zero over time.
*   **Dynamic Counter & Time Optimization:** Thanks to a live progress bar and a dynamic countdown timer calculated based on average processing speed, the remaining time during batch analyses can be monitored in real time.
*   **Data Poisoning Protection:** Utilizing an isolated folder structure, unique timestamped logging, and mathematical early stopping optimizations, irrelevant products (for example, a coffee maker uploaded when an adapter is selected) are detected within seconds without causing deadlocks in the pool, preventing the degradation of the system's intelligence.
