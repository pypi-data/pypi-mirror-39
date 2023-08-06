# tmobile_call_log
Creates bar charts and pie charts from call logs. Processes CSV files
downloaded directly from T-Mobile's website (customer interface). Works as of
2017.

# Installation
To install tmobile_call_log, use pip (or similar):
```{.sourceCode .bash}
pip install tmobile-call-log
```

# Documentation

## Create log object to compile all data

* `data_dir` is the directory where all the call logs (downloaded csv files)
are located.
* `ignore_number` is any other number that is also yours and appears in the
log (e.g., Google voice number).

```python
log = CallActivity(data_dir='./data/', ignore_number='(123) 555-1234')
```

## Plot bar charts

Plots bar charts for call time and call quantity using the top `n`
most frequent phone numbers.
```python
log.plot_bar(n=15)
```


## Plot pie charts

Plots pie charts for call time and call quantity using the top `n`
most frequent phone numbers.
```python
log.plot_pie(n=9)
```
