# Dotfile configuration manager
### :zap: Dotfile management made easy
- Simple and consistent
- Configurable yet intuitive
- Minimal codebase owing to a few common sense conventions

### :zap: There's no place like ... $HOME!
- Bring your own dotfiles and feel right at home
- Builds on the tool you already know: git
- No need to change habits or learn anything new

## Why another dotfile manager?
Most other tools seem to be large and unintuitive for the simplest use cases. Dotcon was conceived to be easy and intuitive from the get-go, and *remain* that way as things grow; with minimal learning curve.

This is accomplished by establishing a few simple conventions. The main one being that everything that should be linked to $HOME resides in a directory with the same hierarchy as the real $HOME. This makes it trivial to link everything in place without complicated configs; everything **"just works"**, by default.

## Directory conventions
These are the common directories and what they're used for:

* `home`: Everything that should be symlinked to $HOME literally.
* `lists`: All sorts of lists for automation purposes, e.g. packages and extensions.
* `scripts`: Executable scripts. `chmod u+x`'ed and added to path.
* `submodules`: All submodules conveniently in one place. If some submodule content needs to be symlinked to $HOME, it should simply be symlinked to `.dotfiles/home/`, from where Dotcon itself can take over.

By default, all files in the `.dotfiles/home/` directory will be linked to their equivalents in $HOME.  
Naturally you can add any other directories, e.g.:
* `dconf`
* `bookmarks`
* `etc`

Since some directories (e.g. `/etc/`) can contain files unsuitable for public disclosure, Dotcon is capable of working with different dotfile directories. This way you can have both public and private dotfiles if you're so inclined.

## Features
Dotcon's primary feature is **easy symlinking**.  
There is no need to maintain complicated configs; anything in `.dotfiles/home/` will be symlinked automatically to the right path.

**Features that may be implemented:**
* [x] Special unicode identifier (currently `⭐`/`U+2B50`) indicating which directories in `home` should be linked whole (instead of their individual files).  
  E.g.:
  - `~/.dotfiles/home/.config/vlc⭐/` links to `~/.config/vlc/`, while
  - `~/.dotfiles/home/.config/vlc/` links its content files to the same files inside `~/.config/vlc/`
* [ ] `-o, --overwrite` flag: To specify link overwriting behavior:
  - `none`: Do not overwrite existing destination files.
  - `all`: Overwrite all existing destination files.
  - `prompt`: Prompt for each individual file.
* [ ] `dotcon.toml` configuration file:
  - To enable easier customization of defaults.
  - To enable custom linking rules (`custom` dir next to `home`).
* [ ] `hosts` directory: To enable device-specific linking rules.
* [ ] ...

## Installation
Note you can easily testrun Dotcon without installing, by running `dotcon.py` directly:
```bash
git clone https://github.com/davidde/dotcon.git
chmod u+x ./dotcon/dotcon/dotcon.py
./dotcon/dotcon/dotcon.py
```
To use the `dotcon` command however, you'll need to either [install](#installing-from-source), or alias it to the binary:
```bash
# In ~/.zshrc or ~/.bashrc:

alias dot='~/dotcon/dotcon/dotcon.py'
# (Update paths to where you cloned)
```
The reason we're using the more unique `dotcon` as command/name, is that there are already a plethora of commands like `dot` and `dotty`. Using e.g. `dot` as a command would conflict with the other `dot`s. However, if you're not using these commands, there is no reason *not* to alias to `dot`. The shorter the better, right?

### Installing from source
```bash
git clone https://github.com/davidde/dotcon.git && cd dotcon
pip install .
```
Now you can just run `dotcon` without complications.

## Usage
| dotcon [-h] [-d DIR] |
|----------------------|


**Optional arguments:**
* `-h, --help`: Show help message and exit.
* `-d DIR, --dir DIR`: Relative or absolute path to dotfile directory. Defaults to `~/.dotfiles`.

**Examples:**
* `dotcon`  
  Symlink everything in `~/.dotfiles/home/` to its equivalent in `~`. By default, existing destination files are not overwritten.
* `dotcon -d .dotfolder`  
  Same, but for custom dotfiles location; symlink everything in `./.dotfolder/home/` to its equivalent in `~`.

**Repo's using Dotcon:**
* My very own [dotfiles](https://github.com/davidde/.dotfiles).
