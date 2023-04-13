# QOREx

Quality Of Results Explorer takes data from a CSV file and display the data in a web app. 

## Getting Started

You need to have Python 3.10 or later installed (check with `python --version`). Then do the following:

```
git clone git@github.com:drummondj/qorex.git
cd qorex
pip install -r requirements.txt
```

There are 2 example files:

* `example.csv` - contains raw data extracted from experiments
* `example.py` - describes how QOREx should process the data from `example.csv`

To run the examples:

```
python qorex.py --csv example.csv --config example.py
```

Then use your web browser to visit http://127.0.0.1:8050

