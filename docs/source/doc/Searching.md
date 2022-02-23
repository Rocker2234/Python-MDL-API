# Searching
## Searching the MDL website

There are two methods and one class that contains the search results.

### search()

_def_ **search**(name, page = 1, style = None, year=None, eps = None, score = None,
           match_all = True, max_results = 20) -> Union[SearchResult, None]

This function is used to search the website for movies/dramas.

#### Parameters:
- name(str) - This is the search term given for searching.
- page(int) - This is the search page number for that specific search term that is being searched in. Similar to what you see on the website.
- style(str) - This represents the country of origin.  
This is always equal to the smaller text visible on the website after the title when searched for something.
This is used to finter the results obtained.  
- year(Union[int, str]) - This represents the year of release.  
This is used to finter the results obtained.
- eps(int) - This represents the number of episodes that spesific drama had.  
This is used to finter the results obtained.
- score(str) - This represents the rating of the movie/drama.  
This is used to finter the results obtained.
- match_all(bool) - To check if all the filters should match for the result.  
Similar to `OR` and `AND` operation, but will be applied on filters.  
Applies `AND` operation if true, else will apply `OR`.
- max_results(int) - The maximum number of results that can be returned by the search.

#### Returns:
The search results or None is if no results are found.
#### Return type:
Union[SearchResult, None]

### SearchResult
_class_ **SearchResult**

This is the container for all the search results.

#### Supported Operations:

`x[index]` - Will return name present in _names_ at the spesified _index_ if index is _str_.  
`len(x)` - Will return the number of elements in the _SearchResult_.  
`str(x)` - Will return _names_ in _str_ format.

#### Attributes:
- names(tuple) - It is tuple of all the movie/Drama names that were returned from search().
- urls(dict) - It is a dict of all the urls that lead to the movie/drama website.  
Keys are names and value is the url. Both are of type str.

#### Methods:
_def_ **get**(self, x: Union[int, str])
___
Returns the complete data for the specified search term.
#### Parameters:
- x(Union[int, str]) - The index of _names_ or the name itself for which the data will be scraped.

#### Returns:
InfoPage

___
_def_ **get_all**(self, x: Union[int, str])
___
Returns the complete data for all the search results present in the _SearchResult_.
#### Parameters:
- limit(int) - Will limit the number of items to first n items.

#### Returns:
list(InfoPage)
