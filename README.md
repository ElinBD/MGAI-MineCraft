# MGAI-MineCraft

Repository for the final assignment of the MGAI course at Leiden 20/21.

## Installation of MCedit

===== REPO =====
```bash
git clone --recursive https://github.com/mcgreentn/GDMC
```
===== PACKAGES =====

* Python==2.7.16
* numpy==1.16.5
* pygame==1.9.4 *
* pyyaml==5.1.2
* pillow==6.2.0
* ftputil==3.4 *
* PyOpenGL==3.1.5
* PyOpenGL-accelerate==3.1.5
* xlib

* = must be this version

===== SETUP =====
```bash
python setup.py build_ext --inplace
```
```python
if fails:
	pip install --upgrade cython
	if fails:
		get visual c++ 9.0 from: http://aka.ms/vcpython27
```

===== RUN =====

```bash
python mcedit.py
```
