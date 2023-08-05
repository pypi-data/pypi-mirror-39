import os
import shutil
import structlog
from os import path
from glob import glob
import numpy as np
from collections import defaultdict

log = structlog.getLogger()


def validate_file_pairs(base_directory):
    """
    - Make directories
    - Delete resulting empty directories
    - Make a backup of the photos
    - Send the backup to a local directory
    - Send the report to a new sub-domain of anthonyagnone.com

    Report Structure
        - list of the file moves
        - list of the created directories
        - list of the deleted directories
        - list of file base names which did not have a {.jpg, .txt} pair

    :param str base_directory:
        Base directory to search for images under.
    :return tuple:
        bool: indication of success
        msg: supporting description message
    """

    paths_valid = []
    paths_invalid = []
    for root, dirs, files in os.walk(base_directory):
        for fn in files:
            base, ext = path.splitext(fn)
            # for each assumed {.jpg, .txt} pair, use .jpg as the anchor file for looking for the
            # other two.
            if ext.lower() in (".jpg", ".jpeg"):
                base_path = path.join(root, base)
                if path.exists("{}.txt".format(base_path)):
                    log.debug("{} is a valid pair.".format(base_path))
                    paths_valid.append(base_path)
                else:
                    log.error("{} is not a valid pair.".format(base_path))
                    paths_invalid.append(base_path)

    return paths_valid, paths_invalid


def read_keyword(fn):
    keyword = None
    with open(fn, 'r') as fp:
        for line in fp:
            if "beeb" in line and ":" in line:
                keyword = line.split(":")[1].strip()
    return keyword


def file_parts(fn_path):
    base_dir = path.dirname(fn_path)
    base_fn = path.basename(fn_path)
    return [base_dir] + list(path.splitext(base_fn))


def make_file_list(dir_files):
    return [path.join(root, f) for root, _, files in os.walk(dir_files) for f in files]


def parse_file_pairs(file_list):
    pairs = defaultdict(dict)
    for f in file_list:
        base_dir, base_fn, ext = file_parts(f)
        key = path.join(base_dir, base_fn)
        pairs[key][ext] = True
    return pairs


def lower_extension(fn):
    base_dir, base_fn, ext = file_parts(fn)
    return path.join(base_dir, base_fn) + ext.lower()


def lower_extensions(dir_base):
    for root, _, files in os.walk(dir_base):
        for f in files:
            fn_old = path.join(root, f)
            fn_new = lower_extension(fn_old)
            if fn_old != fn_new:
                shutil.move(fn_old, fn_new)


def ensure_dir(dir_name):
    if not path.isdir(dir_name):
        os.makedirs(dir_name)


def move_files(files, directory):
    """
    Move an unknown/invalid file set to the designated unknown directory.
    :param files: files to move
    :param directory: destination directory
    :return :
    """
    ensure_dir(directory)

    for f in files:
        dir_name, base_fn, ext = file_parts(f)
        log.msg("symlink created: {} -> {}".format(f, path.join(directory, base_fn) + ext))
        os.symlink(
            f,
            path.join(directory, base_fn) + ext
        )


def do2(dir_base):

    lower_extensions(dir_base)
    file_list = make_file_list(dir_base)
    file_pairs = parse_file_pairs(file_list)

    for base_fn, ext_map in file_pairs.items():
        if ext_map.pop('.txt', False):
            # try to parse the keyword from the txt file
            keyword = read_keyword(base_fn + '.txt')
            if keyword:
                # check for existence of the .jpg
                if ext_map.pop('.jpg', False):
                    # move the txt and jpg file to the validated directory
                    move_files(
                        [base_fn + '.txt', base_fn + '.jpg'],
                        path.join(dir_base, keyword))

        # if any other extensions are remaining for this file group, move to unknowns
        if len(ext_map) > 0:
            move_files(
                [base_fn + ext for ext in ext_map.keys()],
                path.join(dir_base, "unknown"))


def do(dir_base):
    """
    - Make directories
    - Delete resulting empty directories
    - Make a backup of the photos
    - Send the backup to a local directory
    - Send the report to a new sub-domain of anthonyagnone.com

    Report Structure
        - list of the file moves
        - list of the created directories
        - list of the deleted directories
        - list of file base names which did not have a {.jpg, .txt} pair

    :param str dir_base:
        Base directory to search for images under.
    :return tuple:
        bool: indication of success
        msg: supporting description message
    """

    dir_unknowns = path.join(dir_base, 'unknown')
    paths_moved = []
    dirs_created = []
    dirs_removed = []
    keywords = set()

    fns_valid, fns_invalid = validate_file_pairs(dir_base)

    # report any invalid pairs
    if len(fns_invalid) > 0:
        log.error("{} invalid file pairs detected.".format(len(fns_invalid)))
        if not path.isdir(dir_unknowns):
            os.mkdir(dir_unknowns)

    for fn in np.unique(fns_valid):
        keyword = read_keyword(fn + ".txt")

        if keyword:
            dir_keyword = path.join(dir_base, keyword)

            # if this is a new keyword, create its directory
            if keyword not in keywords:
                log.msg("New keyword found: {}. Creating directory".format(keyword))
                if not path.isdir(dir_keyword):
                    os.mkdir(dir_keyword)
                dirs_created.append(dir_keyword)
                keywords.add(keyword)

            # move the file into the keyword directory
            log.msg("Moving {} to {}.".format(fn, dir_keyword))
            for file_to_move in glob(fn + '.*'):
                shutil.move(file_to_move, dir_keyword)
            os.remove(path.join(dir_keyword, path.basename(fn) + ".txt"))
        else:
            # keyword not successfully found -- add to unknowns
            for file_to_move in glob(fn + '.*'):
                shutil.move(file_to_move, path.join(dir_unknowns, path.basename(fn)))

    for fn in fns_invalid:
        log.msg("Moving {} to {}.".format(fn, dir_unknowns))
        for file_to_move in glob(fn + '.*'):
            shutil.move(file_to_move, dir_unknowns)

    # remove any empty directories that the file movement creates
    for root, dirs, files in os.walk(dir_base):
        for d in dirs:
            dir_cur = path.join(root, d)
            if is_empty_directory(dir_cur):
                log.msg("Detected empty directory {}. Removing.".format(dir_cur))
                dirs_removed.append(dir_cur)
                os.rmdir(dir_cur)

    return 0, "Success"


def is_empty_directory(dir_name):
    return len(os.listdir(dir_name)) == 0


def undo():
    pass
