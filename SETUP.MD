# National Integration Adaptors - MHS SETUP
___
**Note:** Setup for Windows would differ only in commands and keyboard shortcuts used
___
### 1. OpenTest And VPN initial setup (requires waiting for response from NHSD Services)
Find [THIS](https://github.com/nhsconnect/integration-adaptor-mhs/blob/develop/setup-opentest.md)
document useful for the setup of OpenTest necessary in order to make this project work
* [OpenVPN](https://openvpn.net/community-downloads/)
* [TunnelBlick VPN](https://tunnelblick.net/downloads.html)

Using TunnelBlick VPN, after receiving a response containing two files:
* Download both of them
* Remove `.txt` from `<filename>.ovpn.txt`, so it's an `.ovpn` extension file
  * **Note:** It was changed because of mail attachments policies 
* Open TunnelBlick, go into `Configurations` tab and simply drag the `.ovpn` configuration file into the box
* Choose `Only Me` when asked
  * **Note:** Might be prompted to confirm the action using system credentials

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

Install ``Python 3.9``:
```shell
  brew install python@3.9
  brew install pipenv
```

Note: If you have ``pyenv`` already installed, ``pipenv`` will get the global set Python version from it on installation

* Go into each of the directories in terminal (from the root directory of the project):
    * `common`
    * `integration-tests/integration_tests`
    * `mhs/common`
    * `mhs/spineroutelookup`
    * `mhs/inbound`
    * `mhs/outbound`


**Install dependencies for `Python 3.9` for each:**
```shell
  pipenv --python 3.9
```

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
* `exit` virtual environment shell
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

---
### 6. Adding certificate keys to .yaml configuration file

```
- MAKE SURE TO STORE THIS FILE SOMEWHERE OUTSIDE THE PROJECT TO AVOID IT BEING COMMITTED
- DO NOT SHARE THESE KEYS WITH OTHERS AS IT IS FOR YOUR PERSONAL USE ONLY
```

* Create a copy of [MHS CONFIGURATION FILE](https://github.com/nhsconnect/integration-adaptor-mhs/blob/develop/mhs-config.yaml)
  * Directory: `Root-folder-of-the-project/mhs-config.yaml`
* Look for `User-specific env variables`, don't change anything else
* Input `MHS_SECRET_PARTY_KEY`value from email's attached text file's `Party key`
* **NOTE FOR KEYS:** Make sure to have two empty spaces on each line if the key has pasted differently
  * Paste keys from new line leaving variable name with `|`, e.g. `MHS_SECRET_CLIENT_CERT: |`
* Input `MHS_SECRET_CLIENT_CERT` value from `Your endpoint certificate`
* Input `MHS_SECRET_CLIENT_KEY` value from `Your endpoint private key`
* Input `MHS_SECRET_CA_CERTS` values
  * First from `Endpoint issuing subCA certificate`
  * Second from `Root CA certificate`

### 7. Adding .yaml files to IntelliJ Run Configurations

* Find `main.py` files of `inbound`, `outbound` and `spineroutelookup` modules in project structure
* For each of them:
  * Right mouse click, `Modify Run Configuration...` (Should be under `Run` and `Debug` buttons)
  * In the `Edit Run Configuration` window:
    * Rename `main` to module name
    * Open `EnvFile` tab
  * EnvFile is disabled by default, so tick `Enable EnvFile` checkbox
  * Click `+` sign on top of the box below or press `⌘ + N` (Command + N) and `JSON/YAML file`
  * Specify path to the `.yaml` configuration file
  * Make sure it's enabled and click `Apply` and then `Ok`

**Note:** If there are any problems with not found imports or errors in any module's main script:
* Consider invalidating caches (`File` -> `Invalidate Caches` and select all) and see if the problem dissapeared after the restart
* If this didn't work, make sure your intelliJ and all plugins are up to date
  * This might change modules structure after indexing, but it doesn't have any impact on them

### 8. Attaching integration-tests configuration file to Run

```
- MAKE SURE TO STORE THIS FILE SOMEWHERE OUTSIDE THE PROJECT TO AVOID IT BEING COMMITTED
- DO NOT SHARE THESE KEYS WITH OTHERS AS IT IS FOR YOUR PERSONAL USE ONLY
```

* Create a copy of [MHS INTEGRATION TESTS CONFIGURATION FILE](https://github.com/nhsconnect/integration-adaptor-mhs/blob/develop/integration-tests/integration_tests/integration-test-env-example.yaml)
  * Directory: `/integration-tests/integration_tests/integration-test-env-example.yaml`
  * Optionally you might want to rename the file to `integration-tests.yaml`
* Fill the `INTEGRATION_TEST_ASID`'s empty `''` with a value of `ASID` from e-mail's attached text file  
* Choose the proper `MHS_PERSISTENCE_ADAPTOR` and `MHS_DB_ENDPOINT_URL`
* In IntelliJ, click the Select `Run/Debug Configuration` dropdown menu on the top toolbar and click `Edit Configurations...`
* Click `Edit Configuration Templates`
* Find `Python tests` -> `Unittests` template and open `EnvFile` tab
* EnvFile is disabled by default, so tick `Enable EnvFile` checkbox
* Click `+` sign on top of the box below or press `⌘ + N` (Command + N) and `JSON/YAML file`
* Specify path to the `.yaml` integration-tests configuration file
* Make sure it's enabled and click `Apply` and then `Ok`

### 8.1 Make running services easier

* Click the Select `Run/Debug Configuration` dropdown menu on the top toolbar and click `Edit Configurations...`
* Click `+` sign on top of window or press `⌘ + N` (Command + N) to add a new configuration and click `Compound`
* Rename the compound to `Run services`
* Add `inbound`, `outbound` and `spineroutelookup` modules to the `Compound`
* Click `Apply` to save changes

### 8.2 Make running tests easier

* Click the Select `Run/Debug Configuration` dropdown menu on the top toolbar and click `Edit Configurations...`
* For each module:
  * Right click on module root folder name -> `Mark Directory As` -> `Test Sources Root` (The green one)
  * Right click on module root folder name -> `Modify Run Configuration...`
  * Go to `EnvFile` tab, add `integration-tests.yaml` configuration file ([8 Attaching integration-tests configuration file to Run](#8-attaching-integration-tests-configuration-file-to-run))
  * You can change name to `UnitTests in <modulename>`, click `Apply` and `OK` button to save
  * Right click on module root folder name -> `Mark Directory As` -> `Unmark As Test Sources Root`
* Click `+` sign on top of window or press `⌘ + N` (Command + N) to add a new configuration and click `Compound`
* Rename the compound to `Run Unit Tests`
* Add all newly created `UnitTests in <modulename>` configurations to the compound

### 9. Running 

* Connect to the VPN you configured earlier
* Make sure Docker is running and from the root directory of the project, run:
```shell
./start-dependencies-docker-containers.sh
```
* Run the `Run Services` compound you made earlier
  * If you skipped this stage:
    * please refer to [8.1 Make running services easier](#81-make-running-services-easier) section
    * or start `inbound`, `outbound` and `spineroutelookup` modules to run parallelly

* When those services are running, `integration tests` should be passing

* Run the `Run Unit Tests` compound you made earlier
  * If you skipped this stage
    * please refer to [8.2 Make running tests easier](#82-make-running-tests-easier)
    * or run each Unit Test individually




