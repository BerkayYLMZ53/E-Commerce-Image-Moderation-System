### 📊 Sistem Akış Mimarisi (System Workflow)

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
# 🛡️ Akıllı E-Ticaret Yorum Moderasyon Sistemi
### 🤖 Kendi Kendini Besleyen (Self-Feeding) Çoklu Referans & Nesne Algılama Motoru

Bu proje, e-ticaret platformlarındaki (Trendyol, Hepsiburada vb.) kullanıcı ürün yorum görsellerini otomatize edilmiş bir süzgeçten geçirerek manipülatif, hatalı veya alakasız içerikleri engellemek amacıyla geliştirilmiş **veri merkezli (Data-Centric) bir yapay zeka** moderasyon sistemidir. 

Proje, geleneksel statik sınıflandırma modellerinin aksine, yaşayan ve kendi kararlarından beslenen dinamik bir mimariye sahiptir.

### 🚀 Öne Çıkan Core Özellikler

* **Çift Aşamalı Hibrit Süzgeç:** Yüklenen görseller öncelikle **YOLOv8** nesne algılama modeliyle taranarak kargo kutusu, paket veya poşet gibi ürünü gölgeleyen unsurları tespit eder ve anında eler. İkinci aşamada ise **OpenAI'ın CLIP (Vision Transformer)** modeli kullanılarak görsel ile ürün arasındaki anlamsal (semantic) benzerlik ölçülür.
* **Kendi Kendini Besleyen (Self-Feeding) Mimari:** Sistem, belirlenen güvenli eşik değerini (%65+) geçen ve temiz çıkan gerçek kullanıcı ev ortamı fotoğraflarını otomatik olarak izole bir **`referanslar`** havuzuna dahil eder. 
* **Çoklu Referans Eşleştirme (Multi-View Matching):** Havuzda biriken gerçek kullanıcı resimleri sayesinde sistem; ışık patlamaları, ters açılar ve ev ortamı doku farklılıkları gibi kararsızlık senaryolarını, en yüksek benzerlik skorunu (`max_similarity`) baz alarak aşar. Böylece sistemin hatalı reddetme (*False Negative*) oranı zamanla sıfıra yaklaşır.
* **Veri Zehirlenmesi (Model Poisoning) Koruması:** İzole klasör yapısı ve matematiksel erken durdurma (*Early Stopping*) optimizasyonları sayesinde, alakasız ürünler (örneğin adaptör seçiliyken yüklenen bir kahve makinesi) sisteme girdiğinde 900+ referanslık havuzda kilitlenme yaratmadan saniyeler içinde tespit edilir ve sistem zekasının zehirlenmesi engellenir.
