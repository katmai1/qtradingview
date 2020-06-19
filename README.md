# QTradingView

PyQt App for TradingView. Recommends login to autosave your draws.

## Demo

![Image not found](demo.png)

---

## Prepare develop environment with anaconda

create and active environment.
`conda create -n env_name python=3.7`
`conda activate env_name`

install PyQt5
`conda install -c anaconda pyqt`

install dependencies
`pip install -r requeriments/linux.txt`

run
`python app/main.py`

## Developer tips

After create/edit UI files
`./devtool-convert_ui_files.sh`

After modify database models
`cd app && python db.py migrate && cd ..`

