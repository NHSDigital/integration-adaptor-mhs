# National Integration Adaptors - MHS SETUP
___
### 1. OpenTest Setup (requires waiting for response from NHSD Services)
Find [THIS](https://github.com/nhsconnect/integration-adaptor-mhs/blob/develop/setup-opentest.md)
document useful for the setup of OpenTest necessary in order to make this project work
* [OpenVPN](https://openvpn.net/community-downloads/)
* [TunnelBlick VPN](https://tunnelblick.net/downloads.html)



___
### 2. Intellij IDEA initial setup
* Press `⌘ + ,` (Command + comma) to step into `Preferences` window
* Go to `Plugins` tab
* Install `EnvFile` and `Python` plugins
  * EnvFile - plugin that allows you to set env variables for run configurations from files
  * Python - plugin allowing for having some PyCharm functionalities in IntelliJ
* Restart IntelliJ IDEA to make sure the plugins are installed properly
* Open cloned project from folder or clone using VCS 
`git clone https://github.com/nhsconnect/integration-adaptor-mhs.git`
---
### 3. Terminal actions

Install ``Python 3.7``:
```shell
  brew install python@3.7
  brew install pipenv
```

Note: If you have ``pyenv`` already installed, ``pipenv`` will get the global set Python version from it on installation

* cd into each of the directories in terminal (from the root directory of the project):
    * ``common``
    * ``integration-tests/integration_tests``
    * ``mhs/common``
    * ``mhs/spineroutelookup``
    * ``mhs/inbound``
    * ``mhs/outbound``


**Install dependencies for `Python 3.7` for each:**
```shell
  pipenv --python 3.7
```

___
### 3.1 If you're getting a `Pystache 0.5.4` error
For each module:
* Open shell using `pipenv shell`
* Uninstall `setuptools` `pip uninstall -y setuptools`
* Install `setuptools 57.5.0` `pip install -Iv setuptools==57.5.0`
* Exit virtual environment shell with `exit`
* Try installing dependencies again `pipenv install --dev`

---
### 3.2 For MacOS users
* Go to terminal window where you have ``mhs/outbound`` directory open
* Install ``openssl`` and ``curl-openssl`` using
```shell
  brew install openssl
  brew install curl-openssl
```
* Open shell using ``pipenv shell`` (make sure you're still in ``mhs/outbound`` directory)
* Execute commands:
```shell
export PYCURL_SSL_LIBRARY=openssl
export LDFLAGS="-L/usr/local/opt/curl-openssl/lib"
export CPPFLAGS="-I/usr/local/opt/curl-openssl/include"

pip install --no-cache-dir --compile --ignore-installed --install-option="--with-openssl" --install-option="--openssl-dir=/usr/local/opt/openssl" pycurl
```
* `exit` virtual enviroment shell
___
### 4. Adding virtual enviroment SDKs

For each module:
* Check and copy the path to virtual enviroment `pipenv --venv` from terminal
* In IntelliJ press `⌘ + ;` (Command + semicolon) to open `Project Structure` window
* Go to `SDKs` under `Platform Settings`
* Click `+` sign on top of window or press `⌘ + N` (Command + N) and `Add Python SDK...`
* Make sure you're in `Virtualenv Enviroment` tab and click radio `Existing enviroment`
* In `Interpreter`, paste output copied from terminal adding `/bin/python3` and click `OK` button
  * e.g.:`/Users/<username>/.local/share/virtualenvs/outbound-vfKgBI9O/bin/python3`

___
### 5. Importing modules to the project

For each module:
* In IntelliJ press `⌘ + ;` (Command + semicolon) to open `Project Structure` window
* Go to `Modules` under `Project Settings`
* Click `+` sign on top of window or press `⌘ + N` (Command + N) and `Import Module`
* Point to the module you want to import
  * **Note:** Start with `mhs/common` first to avoid name clash of two `common`
* Make sure you're `creating module from existing sources`
* Click `next` button all the way to the finish
  * **Note:** Rename `common` to `mhs-common` if working on this module
* Select the corresponding `Module SDK` in `Dependencies` tab after clicking on newly imported module
* Click `Apply` button

