## Virtual Environment
Setup a virtual environment before executing any build/test/release opearations.

```bash
$ virtualenv --python=python3.6 venv
...
Installing setuptools, pip, wheel...
done.
$ . venv/bin/activate
```

## Test
We use tox to run tests. After setting up a virtual environment, requirements and tox must be installed.

```bash
(venv) $ pip3 install -r requirements.txt
(venv) $ pip3 install tox
(venv) $ tox
...
  py36: commands succeeded
  linters: commands succeeded
  congratulations :)
```

## Build a development package
To build a package for development purposes, do the following.
```bash
(venv) $ python3 setup.py sdist bdist_wheel
running sdist
running egg_info
...
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/METADATA'
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/WHEEL'
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/top_level.txt'
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/RECORD'
removing build/bdist.macosx-10.9-x86_64/wheel
```

The packages will be in the generated `dist` directory
```bash
(venv) $ ls dist
titus_optimize-0.0.14+hlocal.g34f75d0.dirty-py3-none-any.whl titus_optimize-0.0.14+hlocal.g34f75d0.dirty.tar.gz
```
