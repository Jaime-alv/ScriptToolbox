# scripts

Day to day scripts.

Scripts run under python 3.10, no need for virtual environments.

Call them from console, like:

```py
python3 script_name.py
```

## rename_folder.py

Rename two folders back and forth while preserving content.

Useful for working with different configuration folders that compete for the same name.

### Usage

Activate script with python global executable and add your target folder name

```shell
python3 ./script/rename_folder.py <folder>
```

This will rename `folder` to `folder_original`, create a new `folder` if not exist, and get a logging message in your screen.

If script is activated once more, `folder_original` is again `folder` and there is a new `folder_alt` with the old content.

Content is preserved.

By default, looks for `<folder>` at current working directory.

### help

```shell
python3 ./script/rename_folder.py -h
```

Prints help and show the different options and flags that exist.

- `-p`, `--path` absolute path where target folder is.
- `-j`, `--join` joining character between folder.
- `-d`, `--default` surname append for original folder.
- `-a`, `--alternative` surname append for new folder.

## switcher.py

Built to work with kube forwarder from Windows.

Kube forwarder -> [GitHub](https://github.com/pixel-point/kube-forwarder)

Re write certificate paths with Windows style slashes and connect with the WSL.

```python
class Constants(NamedTuple):
    """Constants."""

    # original file created by kubernetes
    ORIGIN: str = ".kube/config"
    # file kube forwarder read
    DESTINY: str = ".kube/config_abs"
    # absolute path to WSL2
    WSL_PATH: str = r"\\wsl$\Ubuntu"
    # folder location in WSL2
    HOME: str = "HOME"
```

## rename_items.py

Rename all files that start with several fields inside a given directory.

Set different cases in FileStart

```python
class FileStart(Enum):
    """All start strings reside here."""

    CASE_ONE = "IMG-"
    CASE_TWO = "VID-"
```

```python
class Constant(NamedTuple):
    """General constants."""

    # Append string if file already exists.
    NEW_FILE: str = "_"
    # String to substitute starting strings with.
    SUBSTITUTE_WITH: str = ""
```
