import git

from pathlib import Path
import os

# Utility functions

# Returns a list of strings of absolute paths to files containing extension ext at directory dir.
# function: get_files
# argument definitions:
#   dir = the directory to search for files
#   ext = file extension to find. it should use a regex value, eg. "*.txt"
#   recursive = boolean value for whether the search should be recursive
def get_files(dir, ext, recursive=True):

    if type(dir) is str:
        file_dir = Path(dir).resolve()
    elif type(dir) is Path:
        file_dir = dir.resolve()
    else:
        raise TypeError("dir must by of type Path or str")

    if (recursive):
        r_str = "**/"
    else:
        r_str = ""

    path_list = [path.resolve() for path in file_dir.glob(f"{r_str}{ext}")]
    path_str_list = [str(path) for path in path_list]

    return path_str_list

# Returns a list of strings of absolute paths to verilog files at dir
# function: get_verilog
# argument definitions:
#   dir = the directory to search for verilog
#   recursive = boolean value for whether the search should be recursive
def get_verilog(dir, recursive=True):
    verilog_list = []
    verilog_list.extend(get_files(dir=dir, ext='*.v', recursive=recursive))
    verilog_list.extend(get_files(dir=dir, ext='*.sv', recursive=recursive))
    verilog_list.extend(get_files(dir=dir, ext='*.svh', recursive=recursive))
    return verilog_list

# Returns a list of strings of absolute paths to vhdl files at dir
# function: get_vhdl
# argument definitions:
#   dir = the directory to search for vhdl
#   recursive = boolean value for whether the search should be recursive
def get_vhdl(dir, recursive=True):
    vhdl_list = []
    vhdl_list.extend(get_files(dir=dir, ext='*.vhd', recursive=recursive))
    vhdl_list.extend(get_files(dir=dir, ext='*.vhdl', recursive=recursive))
    return vhdl_list

# Returns the top level of the git repository from a given path
# function: get_git_root
# argument definitions:
#   path = the path to start the search for the git root. The path should be
#          inside of a git repository. An easy way to use this function is
#          by passing "__file__" as an argument from a git version-controlled file
def get_git_root(path):
    cwd = os.path.dirname(os.path.realpath(path))
    git_repo = git.Repo(cwd, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root

# Return a string of the file name from a string of the absolute path to that file.
# function: shorten_file_name
# argument definitions:
#   path = a string of the absolute path to a file
def shorten_file_name(path):
    file_name = str(Path(path).name)
    return file_name

# function: compile
# argument definitions:
#   path = a string of the absolute path to a file
def compile():
    raise NotImplementedError("function compile() has not been implemented yet.")

# function: run_sim
# argument definitions:
#   path = a string of the absolute path to a file
def run_sim():
    raise NotImplementedError("function run_sim() has not been implemented yet.")


