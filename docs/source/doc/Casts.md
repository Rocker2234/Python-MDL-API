# Casts
For operations to be performed on casts/artists there is the method(_casts()_) that
retrieves the data form the webpage and a class(_Cast_) for storing it.

## **casts()**

_def_ **casts**(url: str)
***
This function is used to retrieve data from the webpage.

### Parameters:
- **link**(str) - The url for the MDL webpage containing information on Casts/Artists. 

### Raises:
- **InvalidURLError** - The entered URL was not a valid one.
- **NotMDLError** - The entered URL did not belong to MDL.
- **RequestTimeoutError** - There was some error getting the response from the server.
- **BadHttpResponseError** - Did not get a positive response from the server.

### Returns:
All the data that was extracted from the webpage in the _Cast_ object.

### Return type:
_Cast_

## **Cast**

_class_ **Cast**  

This is the container _class_ whose object contains all the data extracted form the webpage.

### Supported Operations:
`str(x)` - Will return the name of the Cast/Artist the object contains details about.

### Attributes:

- **name** - Name of the person.
- **description** - A short bio on the person.
- **url** - The url that was used for scraping the data.
- **thumbnail** - Thumbnail obtained directly from the website.
- **first_name** - First name of the person.
- **family_name** - Family name of the person.
- **native_name** - Native name of the person.
- **nationality** - Nationality of the person.
- **gender** - Gender of the person.
- **dob** - Date of birth of the person.
- **age** - Age of the person.
- **works** - All the performances or established works of movies/dramas done by the person.
- **aka** - Alias or also known as names of the person.

### Methods:

_def_ **save**(self, file, overwrite=False)
***
Saves the data in the object to a file in JSON format.

#### Parameters:
- **file**(str) - The name of the file to save the data into.
- **overwrite**(bool) - A boolean that indicates weather to overwrite data if it already exists.

#### Returns:
Returns a boolean value that indicates whether the data was saved successfully or not.

#### Return Type:
_bool_

>Note: In some scenarios, two or more different people will have the same name. 
> In that case, the name will change to `<name>(n)`. Where n is a number that starts
> from 1 and increments by one each time a conflict is found. Starts from 2nd person
> with the same name.

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
