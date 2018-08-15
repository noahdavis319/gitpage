# GitPage

GitPage is a Python-based Git web-app that uses pygit2 and Flask to provided a web 
interface similar to GitHub, GitLab, BitBucket, and more!

### Development for GitPage

It is recommended to develop for GitPage in a virtual environment.
```
virtualenv venv/
source venv/bin/activate
```
We then need to install `PyBuilder` to build the project.
```
pip install pybuilder
```
GitPage has a few dependencies that must be installed before building.

##### Dependencies

* cmake
* libcurl-devel
* openssh-devel
* python-devel
* libgit2 (see further below)

#### Installing libgit2

GitPage requires `libgit2`  to use `pygit2`, a Python-based binding for `libgit2`.  
There are two methods for getting `libgit2`.
1. Using GitPage's built in `install_libgit2` pybuilder task which will install `libgit2`
within the virtual environment. GitPage currently installs `libgit2 v0.27.0`.
2. Manually install the latest version of `libgit2` to the virtual environment.
See [Installing libgit2 in a Virtual Environment](#installing-libgit2-in-a-virtual-environment)

##### Installing libgit2 in a Virtual Environment
You can download and install `libgit2` by running the follow series of commands.  You will
need to visit [libgit2's release page](https://github.com/libgit2/libgit2/releases) to 
grab the latest version.
```
wget https://github.com/libgit2/libgit2/archive/{libgit2-version}.tar.gaz
mkdir libgit2
tar xzf {libgit2-version}.tar.gz --directory libgit2
cd libgit2
cmake .
make
sudo make install
```

#### Building GitPage
We can now build GitPage with `pybuilder`!
```
pyb -v
```

#### Installing GitPage
To install GitPage, run the `pybuilder` `install` task.
```
pyb -v install
```

#### Using GitPage
TODO