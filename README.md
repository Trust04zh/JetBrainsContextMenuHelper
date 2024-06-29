Tool for keep JetBrains application (installed via JetBrains Toolbox) entries to your version in context menu on Windows.

Toolbox App 2.0 has modified the installation paths for applications, allowing these paths to be used as permanent ones. For more details, refer to [official blog](https://blog.jetbrains.com/toolbox-app/2023/08/toolbox-app-2-0-overhauls-installations-and-updates/). Script for earlier versions of Toolbox can be found under `v1` branch.

```
> python .\JetBrainsDirectoryContextMenuHelper.py -h
usage: JetBrainsDirectoryContextMenuHelper.py [-h] (-a | -d)

optional arguments:
  -h, --help    show this help message and exit
  -a, --add     create or update entries
  -d, --delete  remove entries
```