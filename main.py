import argparse

def arg_parse():
    parser = argparse.ArgumentParser(description="Stockholm")
    parser.add_argument('-v', '--version', action='store_true', help='show the version of the program')
    parser.add_argument('-r', '--reverse', type=str, help='Followed by the key entered as an argument to reverse the infection.')
    parser.add_argument('-s', '--silent', action='store_true', help='In which case the program will not produce any output.')

    args = parser.parse_args()

    if args.version:
        print("Version: 0.0.1")
    elif args.reverse:
        print(f"Reversing infection with key: {args.reverse}")
    elif args.silent:
        print("Silent mode activated.")

    return args

def main():
    args = arg_parse()
    if args.version:
        print("Version information shown")
    elif args.reverse:
        print(f"Reversed with key: {args.reverse}")
    elif args.silent:
        print("No output (silent mode)")

if __name__ == "__main__":
    main()
