import importlib
import subprocess
import sys

# İndirilecek kütüphanelerin listesi
required_libraries = [
    'pyTelegramBotAPI',
    'pyfiglet',
    'requests',
    'colorama'
]

def install_library(library):
    """Belirtilen kütüphaneyi yükler."""
    try:
        # Kütüphanenin yüklü olup olmadığını kontrol et
        importlib.import_module(library)
        print(f"{library} zaten yüklü.")
    except ImportError:
        print(f"{library} yükleniyor...")
        try:
            # pip ile kütüphaneyi yükle
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            print(f"{library} başarıyla yüklendi.")
        except subprocess.CalledProcessError:
            print(f"{library} yüklenirken hata oluştu. Lütfen internet bağlantınızı kontrol edin veya komutu manuel çalıştırın: pip install {library}")

def main():
    print("Kütüphaneler kontrol ediliyor ve yükleniyor...\n")
    for lib in required_libraries:
        install_library(lib)
    print("\nTüm kütüphaneler kontrol edildi ve gerekli olanlar yüklendi.")

if __name__ == "__main__":
    main()
