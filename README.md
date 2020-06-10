# QTradingView

PyQt App for TradingView. Recommends login to autosave your draws.

## Demo

![Image not found](demo.png)

---

## Prepare develop environment with anaconda

create and active environment.

    'conda create -n env_name python=3.7'
    'conda activate env_name'

install PyQt5

    'conda install -c anaconda pyqt'

install dependencies

    'pip install -r requeriments/linux.txt'


create database

    './devtool-update_database_models.sh'

## Usage (with fbs)

Run in develop environment

    'fbs run'

Compile for your system

    'fbs freeze'

Create linux installer (ubuntu, arch)

    'fbs installer'

> **fbs** have more options to deploy, for windows, mac and docker. [tutorial](https://github.com/mherrmann/fbs-tutorial).


## Developer utils

After create/edit UI files

    './devtool-convert_ui_files.sh'

After modify database models

    './devtool-update_database_models.sh'

