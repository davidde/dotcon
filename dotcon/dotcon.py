#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import errno
import argparse


HOME = os.path.expanduser('~')

FORCE_SYMLINKS = False
LINK_SUBMODULES_WHOLE = True

# Dotfile directory to symlink, relative to $HOME:
# (Custom paths can be provided interactively with `-d/--dir` flag.)
DOTFILE_DIR = '.dotfiles'
# Identifies directories that should be linked as a whole:
WHOLE_DIR_ID = '\u2B50' # Default: Unicode White Medium Star = '\u2B50'


def main():
    parser = argparse.ArgumentParser(description='Dotfile configuration management made easy.')
    add_arguments(parser)
    args = parser.parse_args()

    if not args.dir:
        args.dir = os.path.join(HOME, DOTFILE_DIR)
    elif not args.dir.startswith('/'):
        args.dir = os.path.join(os.getcwd(), args.dir)

    dotcon_home = os.path.join(args.dir, 'home')

    if os.path.isdir(dotcon_home):
        symlink_recursive(dotcon_home)
    else:
        print('"{}" does not exist.'.format(dotcon_home))

def add_arguments(parser):
    parser.add_argument('-d', '--dir', help='Relative or absolute path to dotfile directory. Defaults to `~/.dotfiles`.')

def symlink_recursive(directory):
    """
    Recursively symlink all files in "directory" to $HOME.

    "directory" should have a directory structure identical to $HOME,
    because the symlink destination is acquired by replacing "directory"
    in the symlink source path with the $HOME path.

    This means all files in "directory" are linked literally.
    E.g. for `/home/myuser/.dotfiles/home` as input "directory", the VScode `settings.json` file
         should be located at `/home/myuser/.dotfiles/home/.config/Code/User/settings.json`
         and will be linked to `/home/myuser/.config/Code/User/settings.json`.

    Exceptions to this rule:
    - Directories terminating in `WHOLE_DIR_ID`.
      In this case the directory is linked as a whole, instead of its individual files.
    - Submodules when the boolean `LINK_SUBMODULES_WHOLE` is set.
      In this case submodule directories are also linked as a whole, instead of their individual files.
    """
    print('\nSymlinking files in "{}" recursively:\n'.format(directory))

    for source in paths_to_link(directory):
        path_rel_to_home = os.path.relpath(source, directory)
        if path_rel_to_home.endswith(WHOLE_DIR_ID):
            path_rel_to_home = path_rel_to_home[:-1]
        dest = os.path.join(HOME, path_rel_to_home)
        print('  * ', end='')
        symlink(source, dest)

    print('\nFinished setting up all symlinks.')

def paths_to_link(directory):
    """
    Yield all paths that should be linked literally:
    - By default all files inside `~/.dotfiles/home/`.
    - Directories terminating in `WHOLE_DIR_ID` (Default: Unicode White Medium Star = \u2B50 = ⭐)
      are returned as directory, with their child paths skipped.
    - If `LINK_SUBMODULES_WHOLE` is set, submodules (directories containing `.git`)
      are also returned as directory, with their child paths skipped.
    """
    directories_to_link = []
    for (dirpath, _dirnames, filenames) in os.walk(directory):
    # This returns the current dirpath, a list of its child dirs,
    # and a list of its child files for each iteration, each time with all names
    # relative to the current dirpath. dirpath starts at directory and
    # gradually moves down to the innermost directories.
        if dirpath.startswith(tuple(directories_to_link)):
            continue # Skip subdirs of linked directories

        if WHOLE_DIR_ID and dirpath.endswith(WHOLE_DIR_ID) or \
           LINK_SUBMODULES_WHOLE and '.git' in filenames:
            directories_to_link.append(dirpath)
            yield dirpath
            continue # Skip files of linked directories

        for filename in filenames:
            yield os.path.join(dirpath, filename)

def symlink(source, dest):
    global FORCE_SYMLINKS
    while True:
        try:
            if FORCE_SYMLINKS and os.path.exists(dest):
                print('"{}" exists.'.format(dest))
                print('    Forcing symlink:', end='\n      ')
                os.remove(dest)
            os.symlink(source, dest)
            print('{} -> {}\n'.format(dest, source))
        except OSError as e:
            # Destination file already exists:
            if e.errno == errno.EEXIST:
                if FORCE_SYMLINKS == None:
                    print('"{}" exists. Skipped.\n'.format(dest))
                    break
                print('"{}" already exists.'.format(dest))
                print('    Overwrite with symlink?')
                print('      Defaults to "n" (no overwrite).')
                print('      "all" will overwrite ALL existing destination files without further prompting.')
                print('      "none" will skip all existing destination files without further prompting.')
                prompt = '\n      [y/N/all/none] '
                overwrite = validate_input(prompt, ('n', '', 'y', 'a', 'all', 'none'))
                if overwrite in ('y', 'all', 'a'):
                    if overwrite == 'all' or overwrite == 'a':
                        FORCE_SYMLINKS = True
                    print('      Forcing symlink:', end='\n        ')
                    os.remove(dest)
                    continue
                else:
                    if overwrite == 'none':
                        FORCE_SYMLINKS = None
                    print('        "{}" skipped.\n'.format(dest))

            # Destination directory does not exist:
            elif e.errno == errno.ENOENT:
                dest_dir = os.path.split(dest)[0]
                os.makedirs(dest_dir)
                print('Created directory "{}" since it did not exist.'.format(dest_dir), end='\n    ')
                continue
            else:
                raise e
        break

def validate_input(prompt, allowed):
    input_value = input(prompt)
    while input_value.lower() not in allowed:
        print('        Not a valid choice.')
        input_value = input(prompt)
    return input_value


if __name__ == '__main__':
    main()