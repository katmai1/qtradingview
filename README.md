# QTradingView

PyQt App for TradingView.

Recommends simple login to autosave your draws. 

## Features

- Includes the most cryptocurrencies exchanges available in tradingview.
- Complete lists of available markets, with symbol filter.
- Favorite and margin lists.
- Portfolio.
- Ads remove.

## Demo

![Image not found](icons/screenshots/demo.png)

---
## Running from source using Anaconda

Create and active environment.
```
conda create -n env_name python=3.7
conda activate env_name
```

Install PyQt5 and dependencies
```
conda install -c anaconda pyqt
pip install -r requeriments.txt
```

Run
```
python apprun.py
```


*Can be install without Anaconda if install all PyQt5 dependencies manually.


---


#### Troubleshot

##### Database issues after an update

Probably the last update does changes into database and this changes are not applied automatically. You can try update tables manually.
    

```
- If running from source:
    python apprun.py --updatedb

- If running compiled release:
    qtradingview --updatedb

* This function works fine whe running from source code, with a compiled version sometimes not update correctly.
```

If issue persist you can delete database to force his create again.

```
- If running from source:
    python apprun.py --deletedb

- If running compiled release:
    qtradingview --deletedb
```


