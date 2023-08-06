import os
from shutil import copyfile


def ls(directory: str) -> list:
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def safe_copy_files(files, src_dir, target_dir):
    mkdir_p(target_dir)
    for file in files:
        copyfile(os.path.join(src_dir, file), os.path.join(target_dir, file))


def mkdir_p(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
