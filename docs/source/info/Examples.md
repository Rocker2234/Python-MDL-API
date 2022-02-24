# Examples

Search for **Gold** with minimum rating of 7 and released in the year of 2010.

```py
results = PyMDL.search('gold', score='7+', year=2010)
```

Use the first result of the above search to get info on all of its data.

```py
full_info = results.get(0)
```

Save all the information extracted into a json file named `info.json`.

```python
full_info.save('info.json')
```

