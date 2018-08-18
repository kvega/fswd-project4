# Catalog Project

## Prerequisites
* [Python 2](https://www.python.org/download/releases/2.0/)
* `flask`
* `sqlalchemy`
* `oauth2client`
* `httplib2`
* `requests`
* [SQLite](https://www.sqlite.org/)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)


## Project Setup
* Clone or download the preconfigured [VM from Udacity](http://github.com/udacity/fullstack-nanodegree-vm)
* Extract VM configuration files
* Access project directory on host system and run `vagrant up` to start the VM
* Use `vagrant ssh` to access the guest system
* `cd` into `/vagrant/(project dir)` on the guest
* Use `python database_setup.py` to create the database
* Use `python populate_database.py` to populate the database


## Running the Program
* (optional) `chmod +x application.py` to make program executable
* Otherwise, use `python application.py` to start
    * Open browser and navigate to localhost:8000 to interact with the catalog


Enjoy!