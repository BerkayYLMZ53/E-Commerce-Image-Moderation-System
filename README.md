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
