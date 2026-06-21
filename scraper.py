import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def trendyol_yorum_kazici(urun_url, klasor_adi="trendyol_gercek_veriler", maksimum_resim=15):
    # 1. Klasör Hazırlığı
    if not os.path.exists(klasor_adi):
        os.makedirs(klasor_adi)
        
    # 2. Tarayıcıyı "İnsan" gibi davranacak şekilde maskeleme
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--start-maximized") # Sayfayı tam ekran aç

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("🔗 Ürün sayfasına gidiliyor...")
        driver.get(urun_url)
        time.sleep(4) # Sayfanın ilk yüklemesi için bekle
        
        print("📜 Yorumlar bölümüne kaydırılıyor...")
        # Yorumların yüklenmesi için sayfayı yavaşça aşağı kaydırıyoruz
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(3)

        print("🔍 Resim etiketleri aranıyor...")
        # Ekran görüntüsünde bulduğun nokta atışı CSS seçici: data-testid="slide" altındaki img'ler
        resim_elementleri = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="slide"] img')
        
        resim_url_listesi = []
        for img in resim_elementleri:
            src = img.get_attribute("src")
            if src and src not in resim_url_listesi:
                # Trendyol görsellerinin daha kaliteli (büyük) halini indirmek için URL manipülasyonu
                # Küçük önizleme (mnresize/300/300) yerine orijinal boyutu istiyoruz
                if "mnresize" in src:
                    # URL'deki boyut sınırlandırma kısmını temizleyerek büyük resmi alıyoruz
                    parcalar = src.split("/")
                    for p in parcalar:
                        if "mnresize" in p:
                            src = src.replace(p + "/", "")
                
                resim_url_listesi.append(src)
            
            if len(resim_url_listesi) >= maksimum_resim:
                break
                
        if not resim_url_listesi:
            print("⚠️ Hiç yorum resmi bulunamadı! Sayfa aşağı kaydırılamamış veya class değişmiş olabilir.")
            return

        print(f"📊 {len(resim_url_listesi)} adet gerçek kullanıcı yorum resmi bulundu. İndirme başlıyor...")
        
        # 3. Resimleri Klasöre İndirme
        for sira, url in enumerate(resim_url_listesi):
            try:
                img_data = requests.get(url).content
                dosya_yolu = f"{klasor_adi}/yorum_{sira + 1}.png"
                with open(dosya_yolu, 'wb') as f:
                    f.write(img_data)
                print(f"✅ Başarıyla İndirildi: {dosya_yolu}")
            except Exception as e:
                print(f"❌ Resim indirilemedi: {e}")
                
    except Exception as e:
        print(f"💥 Bir hata oluştu: {e}")
    finally:
        driver.quit()
        print("🏁 Tarayıcı kapatıldı, işlem tamam.")

# ---- 🚀 BOTU ÇALIŞTIRMA ----
if __name__ == "__main__":
    # Test etmek istediğin, bol fotoğraflı yorumu olan herhangi bir Trendyol ürün linkini buraya yapıştır:
    trendyol_link = "https://www.trendyol.com/apple/20-watt-usb-c-hizli-sarj-guc-adaptoru-md3j4tu-a-p-924532595/yorumlar?boutiqueId=689770&merchantId=968"
    
    if "BURAYA_" in trendyol_link:
        print("🛑 Lütfen kodun en altındaki 'trendyol_link' kısmına gerçek bir ürün linki yapıştırın!")
    else:
        trendyol_yorum_kazici(trendyol_link, klasor_adi="apple_adaptor_gercek_yorumlar", maksimum_resim=10)