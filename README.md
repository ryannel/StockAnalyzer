# StockAnalyzer

# Setup
* [Download](https://www.python.org/downloads/) and install the latest version of python 3.x
    * Make sure python has been added to your path by running `which python` and ensuring it's pointing to the correct `python.exe`
* Install app dependencies by running: `python -m pip install pandas backtrader jsonlines`
* Clone the project: `git clone https://github.com/ryannel/StockAnalyzer`

# Running the project
* Execute the project by running `python main.py`

# Other Useful Dependencies

# Graphviz
Graph viz is a plotting library that will allow you to visualize several types of models

* [Download Graphvix msi file](https://graphviz.gitlab.io/_pages/Download/Download_windows.html)
* Add the graphviz bin file to your path default location is: `C:\Program Files (x86)\Graphviz2.38\bin`
* install the python library `python -m pip install graphviz`

# TA-Lib (Optional)
If you would like to leverage TA-Lib for the creation of technical indicators

Install Ta-Lib by downloading the appropriate whl file for your python version:
* Check your python version by running `python --version`
* [Navigate to the Fluorescence Dynamics repository](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib) and find the TA-Lib section
* Select the .whl file that matches your python version. Cp38 refers to python 3.8. If you have python 3.7 64bit installed then `TA_Lib‑0.4.17‑cp37‑cp37‑win_amd64.whl` would be appropriate
* Download the file and run `python -m pip install <TA_LIB-xxxxx.whl>`

# Supported Indicators
https://www.backtrader.com/docu/indautoref/