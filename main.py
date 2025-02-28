import argparse
import os
from cryptography.fernet import Fernet


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
    if args.version:
       print("version : 0.0.2")
    elif args.reverse:
       print("sa")
    elif args.silent:
        silent = args.silent
        print("sesiz moda geçti")
    homePath = getHome() #kullanıcnın home dizininin yolunu alıyorum path varmı yokmu bunun kontrollerini yapıyorum
    infectionPath = infectionFolder(homePath) #home dizinine infection adında bir dosya yoksa oluşturuyor
    key = generate_key() #bana bir şifreleme anahtarı oluşturup dosyaya kaydediyor sonradan dosyaya kaydetme işin kaldırabilirim

if __name__ == "__main__":
    main()
