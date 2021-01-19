# Automate migration from python 2 to python 3
This package is self contained.
You have py2 and py3 environments and requirements.txt which is already installed.

## Run migration
To run the migration you have to specify in `config.yml` the absolut path to your py2 scripts folder
and optional relative paths to folders you want to exclude from migration, e.g.

```
python2to3:
  clone: False
  pylint-before-futurize: False
  futurize: False
  path: /home/dmitry/zeev-stxnet/Tools_AutoBuild_1108_1740-19-08-2020-17-59-46-484309
  exclude:
    - venv
    - some-other-package
  replace-in-files:
    src:
    dest:
```
Then execute the following from the project directory:

`venv/bin/python migrate/main.py`

## Run tests
`stestr run`
