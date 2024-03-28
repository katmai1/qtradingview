NOTE:
The original PyQt version had many problems because it required a very specific python development environment. To solve this, there is a C++ version in another repository.

https://github.com/katmai1/qtradingview2

------------------------------------

# QTradingView

PyQt App for TradingView.

Recommends simple login to autosave your draws. 


![Image not found](icons/screenshots/demo.png)  

---
---

## **Index**


- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)

---
---
***

  
### **Features**

- Includes the most cryptocurrencies exchanges available in tradingview.
- Complete lists of available markets, with symbol filter.
- Favorite and margin lists.
- Portfolio.
- Ads remove.

--- 


### **Installation**

QTradingView needs an environment with Python3 and Qt5

#### ___Prepare environment___

    
- Install [Anaconda](https://docs.anaconda.com/anaconda/install/)

- Create and active environment.
    ```
    conda create -n env_name python=3.7
    conda activate env_name
    ```

- Install PyQt5
    ```
    conda install -c anaconda pyqt
    ```


#### __QTradingView from source code__

```
    pip install poetry
    git clone https://github.com/katmai1/qtradingview
    cd qtradingview

```

---

### **Usage**
---
---


#### Install PyQt5 libs using anaconda

Create and active environment.
```
conda create -n env_name python=3.7
conda activate env_name
```

Install PyQt5 and dependencies
```
conda install -c anaconda pyqt
```

install
```
pip install qtradingview
```

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
pip install -r requirements.txt
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


