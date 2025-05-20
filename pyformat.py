import compileall
import marshal
import zlib
import base64
import sys
import os

def create_encoded_loader(original_file_path, output_loader_path):
    """
    Belirtilen Python dosyasının içeriğini derleyip, sıkıştırıp,
    Base64 ile kodlar ve bu kodlanmış veriyi çalıştıran bir yükleyici
    betiği oluşturur.
    """
    try:
        # 1. Orijinal kaynak kodunu oku
        # 'utf-8' encoding kullanarak okumak genellikle güvenlidir
        with open(original_file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # 2. Kaynak kodu bir 'code object'e derle
        # compile() fonksiyonu, kodu çalıştırmadan derler.
        # 'original_file_path' vermek, hata mesajlarının doğru dosyayı göstermesini sağlar.
        code_obj = compile(source_code, original_file_path, 'exec')

        # 3. 'code object'i bayt dizisine dönüştür (Marshal)
        # marshal.dumps(), code object'ini Python'ın anlayacağı bir bayt formatına çevirir.
        marshaled_code = marshal.dumps(code_obj)

        # 4. Marshal edilmiş bytecode'u sıkıştır
        # zlib, bytecode'un boyutunu küçültmeye yardımcı olur.
        compressed_bytecode = zlib.compress(marshaled_code)

        # 5. Sıkıştırılmış bytecode'u Base64 ile kodla
        # Base64, ikili veriyi (bytecode) metin tabanlı bir formata çevirir.
        # .decode('ascii') yaparak elde edilen byte dizisini, içine gömeceğimiz string formatına çeviririz.
        encoded_bytecode = base64.b64encode(compressed_bytecode).decode('ascii')

        # 6. Yükleyici (Loader) betiğin içeriğini oluştur
        # Bu string, yeni oluşturulacak .py dosyasının içeriği olacaktır.
        # '{encoded_bytecode}' placeholder'ına yukarıda elde ettiğimiz Base64 stringi gelecek.
        loader_script_content = f"""
import base64
import zlib
import marshal
import sys

# Orijinal betiğin kodlanmış ve sıkıştırılmış bytecode'u
# Bu kısım otomatik olarak doldurulacak
encoded_bytecode = '{encoded_bytecode}'

try:
    # Base64'ten geri çöz
    compressed_bytecode = base64.b64decode(encoded_bytecode)

    # Sıkıştırmayı aç
    bytecode = zlib.decompress(compressed_bytecode)

    # Bytecode'tan code object'i yükle
    code_obj = marshal.loads(bytecode)

    # Code object'i çalıştır
    # exec() fonksiyonu kodu dinamik olarak çalıştırır.
    # {{'__name__': '__main__'}} vererek, çalıştırılan kodun
    # ana betik gibi davranmasını sağlarız (örneğin if __name__ == '__main__': blokları çalışır).
    exec(code_obj, {{'__name__': '__main__'}})

except Exception as e:
    # Hata durumunda bilgi ver
    print(f"Kodlanmış betiği çalıştırırken bir hata oluştu: {{e}}")
    # İsteğe bağlı olarak programı hata kodu ile sonlandırabilirsiniz
    # sys.exit(1)

""" # Üç tırnak içine alarak çok satırlı string oluşturduk

        # 7. Yükleyici betiğini çıktı dosyasına yaz
        with open(output_loader_path, 'w', encoding='utf-8') as f_out:
            # .strip() kullanarak baştaki ve sondaki boş satırları kaldırabiliriz
            f_out.write(loader_script_content.strip())

        print(f"Başarılı: Kodlanmış ve yükleyici içeren betik '{output_loader_path}' olarak oluşturuldu.")
        print("\nUNUTMAYIN:")
        print("- Bu yöntem kodu GİZLER ancak ŞİFRELEMEZ. Geri çözülmesi (decompile) MÜMKÜNDÜR.")
        print("- Güvenlik amacıyla değil, sadece ilk bakışta kodun okunmasını engellemek için kullanılır.")
        print("- 'exec()' kullanımı dikkatli olmayı gerektirir.")


    except FileNotFoundError:
        print(f"Hata: '{original_file_path}' dosyası bulunamadı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        import traceback
        traceback.print_exc() # Hatayı daha detaylı görmek için

# ##### Nasıl Kullanılır #####
# 1. Yukarıdaki kodun tamamını bilgisayarınızda veya telefonunuzda bir Python dosyasına kaydedin.
#    Örnek: `generate_loader.py`
# 2. Terminal veya komut istemcisini kullanarak bu betiği çalıştırın:
#    `python generate_loader.py`
# 3. Sizden istenecek:
#    - Kodlamak istediğiniz orijinal .py dosyasının adı (örn: `galeri bt yalanı.py`)
#    - Oluşturulacak yükleyici .py dosyasının adı (örn: `yukleyici_galeri.py`)
# 4. Betik çalıştıktan sonra, belirttiğiniz isimde yeni bir `.py` dosyası oluşacaktır.
#    Bu yeni `.py` dosyası, artık sizin dağıtabileceğiniz ve Python'ın çalıştırabileceği,
#    ama insanlar için okunması zor olan betiktir.

# Betiğin ana program gibi çalışmasını sağlayan kontrol bloğu
if __name__ == "__main__":
    print("### Python Kodunu Kodlanmış Yükleyiciye Dönüştürme Aracı ###")

    # Kullanıcıdan dosya isimlerini al
    original_py_file = input("Kodlamak istediğiniz orijinal .py dosyasının adı (örn: galeri bt yalanı.py): ")
    output_loader_file = input("Oluşturulacak yükleyici .py dosyasının adı (örn: yukleyici_galeri.py): ")

    # Fonksiyonu çağırarak işlemi başlat
    create_encoded_loader(original_py_file, output_loader_file)

