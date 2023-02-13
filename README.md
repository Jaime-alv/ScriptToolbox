# scripts

Day to day scripts.

Scripts run under python 3.10, no need for virtual environments.

Call them from console, like:

```py
python3 script_name.py
```

## rename_folder.py

Rename two folders back and forth.

Set desired folders in Constant and let it go.

```python
class Constants(NamedTuple):
    """Class system with constants."""
    # original folder name
    FOLDER: str = ".m2"
    # surname used for original folder
    DEFAULT: str = "default"
    # alternative name
    ALT: str = "Carrefour"
    # where to look for FOLDER
    HOME: str = "HOME"
    # join character script uses for rename
    JOIN: str = "_"
```

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
