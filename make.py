# filename: make.py
import os
from subprocess import call

# configuration:
keyword_for_main_tex = "main"


if __name__ == "__main__":

    tex_root_directory = os.getcwd()

    for root, _, files in os.walk("."):
       for file_name in files:
            # check, if file name ends with `tex` and starts with the keyword
            if file_name[-3:] == "tex" and file_name[0:len(keyword_for_main_tex)] == keyword_for_main_tex:
                os.chdir(root) # go in the direcotry
                os.system("latexmk -lualatex "+ file_name) # run latexmk on the mainfile
                os.chdir(tex_root_directory) # go back to root directory in case of relative pathes