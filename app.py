import os
# OMP çakışmasını engellemek için en üstte olmalı
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import streamlit as st
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from ultralytics import YOLO
import glob
import time

st.set_page_config(page_title="Gelişmiş Toplu Moderasyon", layout="wide")
st.title("🛡️ Akıllı E-Ticaret Yorum Moderasyon Sistemi")
st.subheader("🤖 Dinamik Uzantı & İzole Referans Klasörü Mimarisi")

# Modelleri Önbelleğe Alarak Yükleme
@st.cache_resource
def modelleri_yukle():
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    yolo_model = YOLO("yolov8n.pt")
    return clip_model, clip_processor, yolo_model

with st.spinner("Yapay zeka modelleri yükleniyor, lütfen bekleyin..."):
    clip_model, clip_processor, yolo_model = modelleri_yukle()

# Yardımcı Fonksiyonlar
def coklu_resim_benzerlik_skoru(referans_resim_listesi, yorum_img):
    en_yuksek_skor = 0.0
    for ref_yolu in referans_resim_listesi:
        ref_img = Image.open(ref_yolu)
        inputs = clip_processor(images=[ref_img, yorum_img], return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = clip_model.get_image_features(**inputs)
            if hasattr(outputs, "image_embeds"): image_features = outputs.image_embeds
            elif hasattr(outputs, "pooler_output"): image_features = outputs.pooler_output
            else: image_features = outputs
                
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        similarity = torch.clamp(torch.matmul(image_features[0], image_features[1].transpose(0, -1)), 0, 1)
        skor = similarity.item() * 100
        if skor > en_yuksek_skor:
            en_yuksek_skor = skor
    return en_yuksek_skor

def kargo_kutusu_mu(yorum_img_obj):
    results = yolo_model(yorum_img_obj, verbose=False)
    for r in results:
        for box in r.boxes:
            c = box.cls
            etiket_ismi = yolo_model.names[int(c)]
            if etiket_ismi in ["suitcase", "handbag", "backpack"]:
                return True, etiket_ismi
    return False, None

# Sol Panel Ayarları ve Dinamik Klasör Veritabanı
st.sidebar.header("⚙️ Sistem Ayarları")
esik_degeri = st.sidebar.slider("CLIP Eşik Değeri (Threshold %)", min_value=50, max_value=90, value=65)

urunler = {
    "Tonny Black Spor Ayakkabı": {"ana_urun": "tonny_black_urun.png", "klasor": "tonny_ayakkabi"},
    "Apple 20W USB-C Güç Adaptörü": {"ana_urun": "apple_20w_adaptor_urun.png", "klasor": "apple_adaptor"},
    "Karaca Filtre Kahve Makinesi": {"ana_urun": "karaca_kahve_makinesi_urun.png", "klasor": "karaca_kahve_yorumlar"},
    "Jeven Brus Erkek Parfümü": {"ana_urun": "jeven_brus_parfum_urun.png", "klasor": "jeven_brus_parfum_yorumlar"}
}

secilen_urun = st.sidebar.selectbox("Test Edilecek Ürün Başlığı:", list(urunler.keys()))
hedef_klasor = urunler[secilen_urun]["klasor"]
ana_urun_resmi = urunler[secilen_urun]["ana_urun"]

# Alt referans klasörünü kontrol et
referans_klasor_yolu = f"{hedef_klasor}/referanslar"
if not os.path.exists(referans_klasor_yolu):
    os.makedirs(referans_klasor_yolu)

# CRITICAL FIX: Klasördeki png, jpg ve jpeg uzantılı TÜM referansları topluyoruz
referans_havuzu = [ana_urun_resmi]
for uzanti in ["*.png", "*.jpg", "*.jpeg"]:
    referans_havuzu.extend(glob.glob(f"{referans_klasor_yolu}/{uzanti}"))

# Ana Ekran Tasarımı
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### 📦 Aktif Referans Havuzu")
    st.info(f"🧠 Bu ürün için **{len(referans_havuzu)}** adet referans resim aktif hafızada!")
    if os.path.exists(ana_urun_resmi):
        # NOT: Deprecation uyarısını engellemek için use_container_width kullanıldı
        st.image(Image.open(ana_urun_resmi), caption="Fabrika Stüdyo Resmi", use_container_width=True)

with col2:
    st.write("### 💬 Yorum Klasöründen Resimleri Yükleyin")
    yuklenen_dosyalar = st.file_uploader("Resimleri seçin...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if yuklenen_dosyalar:
        if st.button("🚀 Toplu Denetimi Başlat ve Havuzu Büyüt"):
            st.write("---")
            
            toplam_dosya = len(yuklenen_dosyalar)
            ilerleme_cubugu = st.progress(0)
            durum_yazisi = st.empty()
            
            baslangic_zamani = time.time()
            
            onaylanan_sayisi = 0
            reddedilen_sayisi = 0
            yeni_eklenenler = 0
            
            for sira, dosya in enumerate(yuklenen_dosyalar):
                gecen_sure = time.time() - baslangic_zamani
                analiz_edilen = sira + 1
                
                ortalama_resim_suresi = gecen_sure / analiz_edilen
                kalan_resim_sayisi = toplam_dosya - analiz_edilen
                tahmini_kalan_sure = kalan_resim_sayisi * ortalama_resim_suresi
                
                durum_yazisi.info(
                    f"⏳ **Analiz Durumu:** {toplam_dosya} görselden {analiz_edilen}.si işleniyor... \n"
                    f"⏱️ **Tahmini Kalan Süre:** {tahmini_kalan_sure:.1f} saniye"
                )
                ilerleme_cubugu.progress(analiz_edilen / toplam_dosya)
                
                yorum_resim_obj = Image.open(dosya)
                
                with st.expander(f"📷 Dosya: {dosya.name}", expanded=True):
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.image(yorum_resim_obj, width=130)
                    with c2:
                        kutumu, tespit_edilen = kargo_kutusu_mu(yorum_resim_obj)
                        
                        if kutumu:
                            st.error(f"❌ **REDDEDİLDİ!** (Kargo/Paket Tespiti: {tespit_edilen})")
                            reddedilen_sayisi += 1
                        else:
                            skor = coklu_resim_benzerlik_skoru(referans_havuzu, yorum_resim_obj)
                            st.write(f"**En Yüksek Benzerlik Skoru:** %{skor:.2f}")
                            
                            if skor >= esik_degeri:
                                st.success(f"✅ **ONAYLANDI!**")
                                onaylanan_sayisi += 1
                                
                                # CRITICAL FIX: Orijinal dosyanın uzantısını (jpg mi png mi) dinamik olarak yakalıyoruz
                                dosya_uzantisi = os.path.splitext(dosya.name)[1].lower() # .jpg veya .png döner
                                benzersiz_id = time.time_ns()
                                yeni_ref_yolu = f"{referans_klasor_yolu}/onayli_{benzersiz_id}{dosya_uzantisi}"
                                
                                try:
                                    # Resmi kendi orijinal formatında kusursuzca kaydediyoruz
                                    yorum_resim_obj.save(yeni_ref_yolu)
                                    yeni_eklenenler += 1
                                except Exception as e:
                                    st.warning(f"Dosya kaydetme hatası: {e}")
                            else:
                                st.error(f"❌ **REDDEDİLDİ!** (Benzerlik Yetersiz)")
                                reddedilen_sayisi += 1
            
            durum_yazisi.empty()
            ilerleme_cubugu.empty()
            
            st.write("---")
            st.write("### 📊 Operasyon Özeti")
            st.success(f"💾 **Hafıza Güncellendi:** {yeni_eklenenler} adet yeni ev ortamı resmi `{hedef_klasor}/referanslar/` klasörüne başarıyla izole edildi.")
            
            col_onay, col_red = st.columns(2)
            col_onay.metric("Onaylanan", f"{onaylanan_sayisi} Adet")
            col_red.metric("Reddedilen", f"{reddedilen_sayisi} Adet")