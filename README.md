# QOREx

Quality Of Results Explorer takes data from a CSV file and displays the data in a web app.
It uses the amazing open source `dash` package along with `dash_bootstrap_components` to make everything look nice.

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

Here is an example of what the dashboard looks like:

![QOR Explorer - Google Chrome 14_04_2023 09_56_17](https://user-images.githubusercontent.com/166857/231996358-158aeeb1-c0c6-47ea-9d6f-0f8b2c70e4e4.png)

At the top there is a table that you can use to select rows from the CSV file.

The selected rows are then displayed in the bottom table. Use the toggle switches to display/hide different groups of metrics.

