import os
import argparse

def get_file_names(folderpath, out="output.txt"):
    """ takes a path to a folder and writes all filenames in the folder to a specified output file"""
    with open(out, "a") as file_object:
        for file_name in os.listdir(folderpath):
            file_object.write(file_name + "\n")
    

def get_all_file_names(folderpath, out="output.txt"):
    """takes a path to a folder and write all filenames recursively (files of all sub folders to)"""
    with open(out, "a") as file_object:
        for root, dirs, files in os.walk(folderpath):
            for file_name in files:
                file_object.write(file_name + "\n")
    

def print_line_one(file_names):
    """takes a list of filenames and print the first line of each"""
    for file_name in file_names:
        with open(file_name) as file_object:
            print(file_object.readline().rstrip())

def print_emails(file_names):
    """takes a list of filenames and print each line that contains an email (just look for @)"""
    for file_name in file_names:
        with open(file_name) as file_object:
            for line in file_object:
                if "@" in line:
                    print(line.rstrip())

def write_headlines(md_files, out="output.txt"):
    """takes a list of md files and writes all headlines (lines starting with #) to a file"""
    with open(out, "a") as output_file:
        for md_file in md_files:
            with open(md_file) as file_object:
                for line in file_object:
                    if line.startswith("#"):
                        output_file.write(line.rstrip() + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to handin week 2. Exercise 2')
    parser.add_argument('input_path', help='The path of the folder to consume', nargs='*')
    parser.add_argument("--file", dest="file_name", help="If given will write the content to file_name", required=False)
    parser.add_argument("--all", dest="all", help="If given will write the content to file_name", required=False, action="store_true")
    parser.add_argument("-lo", "--lineone", dest="line_one", help="If given will print the first line in each file", required=False, action='store_true')
    parser.add_argument("-e", "--email", dest="email", help="If given will print all the lines which contains an email", required=False, action='store_true')
    parser.add_argument("-hl", "--headline", dest="headline", help="If given will write every headline in a list of files to a single file", required=False, action='store_true')

    args = parser.parse_args()

    if args.line_one:
        print_line_one(args.input_path)
    elif args.email:
        print_emails(args.input_path)
    elif args.headline:
        if args.file_name:
            write_headlines(args.input_path, args.file_name)
        else:
            write_headlines(args.input_path)
    elif args.all:
        for path in args.input_path:
            if args.file_name:
                get_all_file_names(path, args.file_name)
            else:
                get_all_file_names(path)
    else:
        for path in args.input_path:
            if args.file_name:
                get_file_names(path, args.file_name)
            else:
                get_file_names(path)

    