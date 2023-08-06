# Funhouse - Funguana's Time Series Pre-processing library for our crypto trading bot

`Funhouse` is a simple small library that is created to easily standardize pre-processing for our trading bot. It's based on TA-Lib and Pandas.

The entire goal we have for this library is to modularize the processing for Funguana's Bot. It allows us to organize better.

Funhouse currently only supports price and TA data. In the future it'll support text data as well.



## What makes `Funhouse` better?
Currently it's only the simpler interface and modular library available for what we need.


## How does it work?
It's a simple builder pattern to extract the information we need given a data set. 



### Example:
---
```python
from funtime import Store, Converter
from funpicker import Query
from funhouse import TA, index_time

# Create a library and access the store you want
store = Store().create_lib("ticker.Price").get_store()
tickstore = store["ticker.Price"]


# Get the bittrex price
hourly_bittrex_eth = Query().set_crypto("ETH").set_fiat("USD").set_exchange("bittrex").set_period("hour").set_limit(500).get()

# Get the price dataframe
bittrex_frame_hr = Converter.to_dataframe(hourly_bittrex_eth)

# Get the newly indexed time
bittrex_frame_hr = index_time(bittrex_frame)

tframe = TA(bittrex_frame_hr)

# We're getting all of the necessary TA indicators
tframe.SMA().SMA(100).RSI().RSI(window=30).BOLL().ATR().FIBBB()

# Get the main indicators
tframe.main
```


**Output**
```
              price       SMA_30    SMA_100     SMA_250
timestamp
2018-08-20  6269.90  7081.856000  7070.8227  9146.76444
2018-08-21  6491.11  7051.605000  7048.6392  9106.85724
2018-08-22  6366.13  7006.542667  7025.5715  9061.90236
2018-08-23  6538.95  6944.647000  7006.1594  9010.67620
2018-08-24  6708.96  6895.938000  6989.8012  8961.24920
2018-08-25  6749.56  6856.348333  6976.5864  8912.35816
2018-08-26  6720.60  6807.605333  6961.3133  8869.14576
2018-08-27  6915.73  6763.767333  6947.9782  8830.96080
2018-08-28  7091.38  6726.254000  6933.5620  8796.79784
2018-08-29  7052.00  6688.785333  6919.8855  8770.34596
2018-08-30  6998.76  6664.234000  6909.9456  8740.75516
2018-08-31  6970.31  6642.881000  6904.5910  8713.47660
```


## How to install

Make sure to install mongodb at the very beginning. The instructions are different for different operating systems. Then run:

```
pip install funhouse
```

Or you can use `pipenv` for it:

```
pipenv install funhouse
```


## Roadmap
---
This application aims to be a general preprocessing library for the user. In the future, we'll aim to add the following features:


### Future Features:
- [] Preprocessing pipeline system
    - [] multicore parallezation using numba and dask
    - More streamlined system to increase swapout functionality. 
- [] Text analysis
    - [] PCA decomposition
    - [] Topic Analysis using wikipedia as base
- Technical analysis
    - [] More TA
