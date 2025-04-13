import os
from cryptography.fernet import Fernet

def GetinfectionPath(homePath):
    DirList = os.listdir(homePath)
    for i in DirList:
        if i == "infection":
            full_path = os.path.join(homePath, i)
            if os.path.isdir(full_path):
                return full_path
    return None

def getInfectionFiles(infectionPath):
    file_list = []
    
    # 'infection' klasörü altındaki tüm dosyaları bulur
    for root, dirs, files in os.walk(infectionPath):
        for file in files:
            full_path = os.path.join(root, file)
            file_list.append(full_path)
    return file_list
        
def decrypedFile(homePath, key, silent):
    InfectionPath = GetinfectionPath(homePath)
    
    # Eğer infection klasörü yoksa, hata mesajı verebiliriz
    if not InfectionPath:
        print("❌ 'infection' not found!")
        return
    
    InfectionFiles = getInfectionFiles(InfectionPath)
    cipher = Fernet(key)

    for i in InfectionFiles:
        # Eğer dosya .ft uzantısına sahipse, şifreli dosya olduğunu kabul ederiz
        if not i.endswith(".ft"):
            continue

        with open(i, "rb") as f:
            encrypted_data = f.read()

        # Şifreli veriyi çöz
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
        except Exception as e:
            print(f"❌ Hata çözülürken oluştu: {i} - {str(e)}")
            continue
        
        # Orijinal dosya adını ve yolunu bul
        relative_path = os.path.relpath(i, InfectionPath)  # infection altındaki yol
        original_filename = os.path.join(InfectionPath, relative_path[:-3])  # .ft uzantısını kaldır

        # Klasör yapısını oluştur
        os.makedirs(os.path.dirname(original_filename), exist_ok=True)

        # Çözülmüş veriyi kaydet
        with open(original_filename, "wb") as f:
            f.write(decrypted_data)

        # Şifreli dosyayı sil
        os.remove(i)
        if not silent:
            print(f"✔️ {i} dosyası çözüldü ve {original_filename} olarak kaydedildi.")
