# Searching
There are two methods and one class that contains the search results.
One of the method _search()_ is used for movies/drama information retrieval 
and the other _search_people()_ is used for Casts/Artists who have their profiles on the website.
It is same as searching for some term on the website. 
## **search()**

_def_ **search**(name, page = 1, style = None, year=None, eps = None, score = None,
           match_all = True, max_results = 20)
***
This function is used to search the website for movies/dramas.

### Parameters:
- **name**(str) - This is the search term given for searching.
- **page**(int) - This is the search page number for that specific search term that is being searched in. Similar to what you see on the website.
- **style**(str) - This represents the country of origin.  
This is always equal to the smaller text visible on the website after the title when searched for something.
This is used to filter the results obtained.  
- **year**(Union[int, str]) - This represents the year of release.  
This is used to filter the results obtained.
- **eps**(int) - This represents the number of episodes that specified drama had.  
This is used to filter the results obtained.
- **score**(str) - This represents the rating of the movie/drama.  
This is used to filter the results obtained.
- **match_all**(bool) - To check if all the filters should match for the result.  
Similar to `OR` and `AND` operation, but will be applied on filters.  
Applies `AND` operation if true, else will apply `OR`.
- **max_results**(int) - The maximum number of results that can be returned by the search.

> For filtering with score, you can use - or + to indicate lesser/grater than the 
> current score. E.g. 7.1+ will match all results with score >=7.1

### Returns:
The search results or None if no results are found.

### Return type:
Union[SearchResult, None]  

## **search_people()**

_def_ **search_people**(name, page = 1, max_results = 20, 
                    nationality = None)
***
This function is used to search the website for Casts/Artists.

### Parameters:
- **name**(str) - This is the search term given for searching.
- **page**(int) - This is the search page number for that specific search term that is being searched in. Similar to what you see on the website.
- **max_results**(int) - The maximum number of results that can be returned by the search.
- **nationality**(str) - This represents the Person's nationality.  
This is always equal to the smaller text visible on the website after the title when searched for something.
This is used to filter the results obtained.

### Returns:
The search results or None is if no results are found.

### Return type:
Union[PeopleSearchResult, None]

## **SearchResult**
_class_ **SearchResult**

This is the container for all the search results.

### Supported Operations:

`x[index]` - Will return name present in _names_ at the specified _index_ if index is _int_ or _url_ if index is _str_. Raises TypeError otherwise.  
`len(x)` - Will return the number of elements in the _SearchResult_.  
`str(x)` - Will return the list of _names_ in _str_ format.

### Attributes:
- **names**(tuple) - It is tuple of all the movie/Drama names that were returned from search().
- **urls**(dict) - It is a dict of all the urls that lead to the movie/drama website.  
Keys are names and value is the url. Both are of type str.

### Methods:
_def_ **get**(self, x)
***
Returns the complete data for the specified search term.
#### Parameters:
- **x**(Union[int, str]) - The index(int) of _names_ or the name(str) itself for which the data will be scraped.

#### Returns:
The complete information of all the data that will be scraped from the webpage.

#### Return Type:
InfoPage  

_def_ **get_all**(self, limit)
***
Returns the complete data for all the search results present in the _SearchResult_.
#### Parameters:
- **limit**(int) - Will limit the number of items to first n items.

#### Returns:
A list of InfoPage objects of data of each SearchResult item.

#### Return type:
list(InfoPage)



## **PeopleSearchResult**
_class_ **PeopleSearchResult**

This is the container for all the search results.

### Supported Operations:

`x[index]` - Will return name present in _names_ at the specified _index_ if index is _int_ or _url_ if index is _str_. Raises TypeError otherwise.  
`len(x)` - Will return the number of elements in the _PeopleSearchResult_.  
`str(x)` - Will return the list of _names_ in _str_ format.

### Attributes:
- **names**(tuple) - It is tuple of all the movie/Drama names that were returned from search().
- **urls**(dict) - It is a dict of all the urls that lead to the movie/drama website.  
Keys are names and value is the url. Both are of type str.

### Methods:
_def_ **get**(self, x)
***
Returns the complete data for the specified search term.
#### Parameters:
- **x**(Union[int, str]) - The index(int) of _names_ or the name(str) itself for which the data will be scraped.

#### Returns:
The complete information of all the data that will be scraped from the webpage.

#### Return Type:
InfoPage  

_def_ **get_all**(self, limit)
***
Returns the complete data for all the search results present in the _PeopleSearchResult_.
#### Parameters:
- **limit**(int) - Will limit the number of items to first n items.

#### Returns:
A list of InfoPage objects of data of each PeopleSearchResult item.

#### Return type:
list(InfoPage)
