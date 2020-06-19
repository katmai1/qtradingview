# QTradingView

PyQt App for TradingView. Recommends simple login to autosave your draws. (Login with google account or others not works because try open a new tab...)

## Demo

![Image not found](demo.png)
---

## Prepare develop environment with anaconda

Create and active environment.

`conda create -n env_name python=3.7`
`conda activate env_name`

Install PyQt5

`conda install -c anaconda pyqt`

Install dependencies

`pip install -r requeriments/linux.txt`

Run

`python app/run.py`

## Compile

Uninstall fbs if installed (fbs use v3.4)

`pip uninstall fbs`

Install pyinstaller

`pip install pyinstaller`

Build

`python build.py`

- You can found the binary in '_build/dist', this process is tested in Debian10, and probably works in several Linux.

- Also works in Windows without build.py (need replace linux paths format)


## Developer tips

After create/edit UI files

`./devtool-convert_ui_files.sh`


