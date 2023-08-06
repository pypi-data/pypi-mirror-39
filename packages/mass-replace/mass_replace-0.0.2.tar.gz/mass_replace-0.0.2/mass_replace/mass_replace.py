# -*- coding: utf-8 -*-
"""
mass_replace.py
~~~~~~~~~~~~~~~
WIP
"""
from sys import version_info
import os
import fileinput
import yaml
from pprint import pprint as pp


PYTHON_VER = (version_info.major, version_info.minor)


def resolve_wd(target_dir="mass_replace"):
    if target_dir in get_dirs():
        os.chdir(target_dir)
        resolve_wd(target_dir=target_dir)


def load_config(filename="config.yaml"):
    """Load a .yml config file as a dictionary and return it."""
    with open(filename, "r") as f_in:
        return yaml.safe_load(f_in)


def get_items():
    """Returns a list of files and folders in a directory"""
    return [x for x in os.listdir()]


def get_dirs():
    """Returns a list of all folders in the current working directory."""
    return [x for x in get_items() if os.path.isdir(x)]


def get_files():
    """Returns a list of all files in the current working directory."""
    return [x for x in get_items() if os.path.isfile(x)]


def file_find_replace(filename, text_to_search, replacement_text):
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end="")


def many_find_replace(filename, text_search_replace_dicts):
    for text_to_search, replacement_text in text_search_replace_dicts.items():
        file_find_replace(filename, text_to_search, replacement_text)


def discover_filetypes(root_folder=None, hard_copy="file_exts.txt"):
    """Walks through the specified `root_folder` and collects all file
    extension types.
    Writes the extension types to `file_exts.txt`."""
    if not root_folder:
        try:
            root_folder = load_config("config.yaml")["root_folder"]
            if root_folder is None:
                raise (FileNotFoundError)
        except FileNotFoundError:
            root_folder = os.getcwd()
    file_types = set()
    for _, _, filenames in os.walk(root_folder):
        f_types = [".{}".format(ext.split(".")[-1]) for ext in filenames]
        file_types.update(f_types)
    if hard_copy:
        with open(hard_copy, "w") as f_out:
            f_out.writelines("\n".join(file_types))
    return file_types


def mass_replace(root_folder=None, config=None, verbose=False):
    """Peforms find and replace operations on files nested in a root direcotry
    according to settings in the `config.yaml` file."""
    if not config:
        try:
            config = load_config("config.yaml")
        except FileNotFoundError:
            config = load_config("mass_replace/config.yaml")
    if not root_folder:
        root_folder = config["root_folder"]
    print("ROOT: {}".format(root_folder))
    replacement_pairs = config["replacement_pairs"]
    for i in replacement_pairs.items():
        print(i)
    counter = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        valid_files = [f for f in filenames if f.split(".")[-1] in config["filetypes"]]
        if verbose:
            print("=" * 79)
            print("\tCurrent Path - STEP:{}".format(counter))
            pp(dirpath)
            print("\tDirectories - STEP:{}".format(counter))
            pp(dirnames)
            print("\tFiles: - STEP:{}".format(counter))
            pp(filenames)
            print()
        counter += 1
        for fname in valid_files:
            print("|----{}".format(fname))
            many_find_replace("{}/{}".format(dirpath, fname), replacement_pairs)


if __name__ == "__main__":
    print("{0}\n{1}".format(__doc__, "*" * 79))
    print("discover_filetypes()\n", discover_filetypes.__doc__)
    pp(discover_filetypes(hard_copy=True))
    print(
        "{}\nmass_replace()\n{}\n{}".format(
            "*" * 79, mass_replace.__doc__, mass_replace(verbose=True)
        )
    )
