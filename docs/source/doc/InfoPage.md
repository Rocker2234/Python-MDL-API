# InfoPage

For retriveing the information on movies/dramas there is a function used to scrape the 
data from the specified webpage and a container class to store the results in an effective
manner.

## **info()**

_def_ **info**(url: str)
***
This function is used to retrieve movie/drama data from the webpage.

### Parameters:
- **link**(str) - The url for the MDL webpage containing information on Movies/Dramas. 

### Raises:
- **InvalidURLError** - The entered URL was not a valid one.
- **NotMDLError** - The entered URL did not belong to MDL.
- **RequestTimeoutError** - There was some error getting the responce form the server.
- **BadHttpResponseError** - Did not get a positive responce from the server.

### Returns:
All the data that was extracted from the webpage in the _InfoPage_ object.

### Return type:
_InfoPage_

## **InfoPage**

_class_ **InfoPage**  

This is the container _class_ whose object contains all the data extracted form the webpage.

### Supported Operations:
`str(x)` - Will return the name of the Cast/Artist the object contains details about.

### Attributes:

- **title**(str) - Name of the movie/drama.
- **thumbnail**(str) - A link to thumnail obtained directly from the website.
- **type**(str) - Indicates weather it is a drama or a movie.
- **url**(str) - The url that was used for scraping the data.
- **ratings**(str) - The rating that the movie has.
- **synopsis**(str) - A short pllot of the movie/drama.
- **casts**(list) - All actors that were involved in the movie/drama.
- **native**(str) - The name of the movie in its native language.
- **gnere**(str) - The genere the movie belongs to.
- **duration**(str) - The runtime of moive or each episode of a drama.
- **country**(str) - The country of origin.
- **aka**(list) - Aliases of the movie/drama.
- **director**(str) - The person who directed the movie/drama.
- **screenwriter**(str) - The writer of the movie/drama.
- **date**(str) - The release date of the movie/drama.
- **reco**(list) - The recomendatons MDL suggests based on the current movie/drama.
- **reviews**(list) - The user reviews for the current movie/drama.

>Note: `reco` and `reviews` are empty at the time of object creation. 
> It will be poppulated only after calling the `get_recomendations()` and `get_reviews()`
> methods respectively.

### Methods:

_def_ **save**(self, file)
***
Saves the data in the object to a file in JSON format.

#### Parameters:
- **file**(str) - The name of the file to save the data into.

#### Returns:
Returns a boolean value that indicates weather the data was saved successfully or not.

#### Return Type:
_bool_  

_def_ **to_json**(self)
***
Returns a json formatted string of the data present in the object.

#### Returns:
The json formatted string.

#### Return Type:
str  

_def_ **dumps**(self)
***
Returns a _dict_ of data with attributes as keys and value as attribute's value.

#### Returns:
A _dict_ of data present in the object.

#### Return Type:
dict  

_def_ **get_recomendations**(self)
***
Used to get recomendations based on current movie/drama. The data will be stored in _reco_.


_def_ **get_reviews**(self)
***
Used to get reviews current movie/drama. The data will be stored in _reviews_.
