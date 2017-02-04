import os
import fnmatch

def count_lines_in_file(file):
    content = open(file).read()
    lines_count = content.count('\n')
    return lines_count

def get_files_list(targetdir, mask):
    findfiles = []

    for dirpath, dirs, files in os.walk(targetdir):
        for file_name in files:
            full_name = os.path.join(dirpath, file_name)
            if fnmatch.fnmatch(full_name, mask):
                findfiles.append(full_name)
    return findfiles


def get_info_from_log(pattern, textfind, bound):
    files = get_files_list(curdir, pattern)
    for file in files:
        target_line=0
        found = False
        cnt_lines =0
        with open(file) as curfile:
            #обработка файла
            cnt_lines = count_lines_in_file(curfile.name)
            for i, line in enumerate(curfile):
                if textfind in line:
                    target_line = i
                    found = True
                    print("Lines from file " + file)
                if found and i-target_line<=bound:
                    print(line, end='')
        if found:
            print("+++++++++++++++++++++++++++")


os.chdir(os.path.dirname(__file__))
curdir = os.getcwd() + "\\logs"
#cnt = count_lines_in_file(curdir + "\\test_log.log")
#fls = get_files_list(curdir, "*.log")
get_info_from_log("*.log", "404", 2)
