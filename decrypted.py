import os
from cryptography.fernet import Fernet


def GetinfectionPath(homePath):
    DirList = os.listdir(homePath)
    for i in DirList:
        if i == "infection":
            full_path = os.path.join(homePath, i)
            if (os.path.isdir(full_path)):
                return(full_path)
    return None
    
def getInfectionFiles(infectionPath):
    file_list = []

    for root, dirs, files in os.walk(infectionPath):
        for file in files:
            full_path = os.path.join(root, file)
            file_list.append(full_path)
    return file_list
        
def decrypedFile(homePath, key):
    InfectionPath = GetinfectionPath(homePath)
    InfectionFiles = getInfectionFiles(InfectionPath)
    cipher = Fernet(key)
    
    
    for i in InfectionFiles:
         # Dosya içeriğini oku
        with open(i, "rb") as f:
            encrypted_data = f.read()

        # Şifreyi çöz
        decrypted_data = cipher.decrypt(encrypted_data)

        # Yeni dosya adını oluştur (.ft uzantısını kaldır)
        original_filename = os.path.splitext(i)[0]  # ".ft" uzantısını kaldırır

        # Çözülmüş dosyayı kaydet
        with open(original_filename, "wb") as f:
            f.write(decrypted_data)

        # Şifreli dosyayı sil
        os.remove(i)

        print(f"✔️ {i} dosyası çözüldü ve {original_filename} olarak kaydedildi.")


