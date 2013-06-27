**SetInspektor**

This is my first attempt at flickr web application, its written using web2py(http://www.web2py.com) and python flickr_api(http://code.google.com/p/python-flickr-api/) uses OAuth 2.0 to authenticate users and 
get read permission.

It's rather simple:
It fetches a list of user sets and allows to choose one to be compared against the filenames
from a folder on user's computer. Then tells the user which filenames are missing from the set.

Currently hosted on Google App Engine at http://setinspektor.appspot.com
