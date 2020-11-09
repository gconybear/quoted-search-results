## QSR 

*What*

A script to retrieve the quoted-search-results (QSR) for any query or set of queries

*Why* 

The [QSR](https://www.noviceaffiliate.com/seo-tip-1-finding-the-real-qsr-quoted-search-results-in-google-search/) represents the number of web pages currently ranking for a query on google. Can be thought of as a measure of competition. 

*How* 

This script uses selenium to automatically scroll to the last page and retrieve the qsr from the "results-stats" element in the DOM 

To run, simply alter the "PATH" variable in the qsr.py script to the path of your local chromedriver and call the 
**get_QSR** function with a query (5 words or less for now - can easily be changed) 



**Note - if parsing a large number of queries, consider adding a time.sleep() command in the function because google will recognize that you are a bot 
