
import os
import hashlib

def get_file_hash(filepath):
    """Dosyanın MD5 özetini çıkarır."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

def find_duplicates(parent_folder):
    duplicates = {}
    print(f"Tarama başlatılıyor: {parent_folder}")
    
    for root, dirs, files in os.walk(parent_folder):
        for filename in files:
            path = os.path.join(root, filename)
            try:
                file_hash = get_file_hash(path)
                if file_hash:
                    if file_hash in duplicates:
                        duplicates[file_hash].append(path)
                    else:
                        duplicates[file_hash] = [path]
            except Exception as e:
                print(f"Hata: {path} okunamadı - {e}")

    results = {h: p for h, p in duplicates.items() if len(p) > 1}
    
    if not results:
        print("Aynı dosya bulunamadı.")
        return

    print(f"\nBulunan {len(results)} grup kopya dosya:")
    for h, paths in results.items():
        print(f"\nHash: {h}")
        for p in paths:
            print(f"  - {p}")
            
    confirm = input("\nDosyaları silmek istiyor musunuz? (Sadece 'evet' yazarsanız silinir): ")
    if confirm.lower() == 'evet':
        for h, paths in results.items():
            for p in paths[1:]:
                try:
                    os.remove(p)
                    print(f"Silindi: {p}")
                except Exception as e:
                    print(f"Silinemedi: {p} - {e}")

if __name__ == "__main__":
    folder = input("Taranacak klasör yolunu girin: ")
    if os.path.exists(folder):
        find_duplicates(folder)
    else:
        print("Geçersiz klasör yolu.")
