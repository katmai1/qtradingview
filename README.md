# QTradingView
PyQt App for TradingView...

## Demo

![Image not found](/ruta/a/la/imagen.jpg)

---

## Prepare develop environment with anaconda

create and active environment.

    'conda create -n env_name python=3.7'
    'conda activate env_name'

install PyQt5

    'conda install -c anaconda pyqt'

install dependencies

    'pip install fbs coloredlogs peewee ccxt beautifulsoup4 html5lib PyQtWebEngine'


## Usage (with fbs)

Run in develop environment

    'fbs run'

Compile for your system

    'fbs freeze'

Create linux installer (ubuntu, arch)

    'fbs installer'

> **fbs** have more options to deploy, for windows, mac and docker. [tutorial](https://github.com/mherrmann/fbs-tutorial).

---

Pending features:

- alarm system
- favorite markets
- ...
