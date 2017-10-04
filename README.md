# fswdn-logs-analysis
## Logs Analysis Project - Udacity Full Stack Web Developer Nanodegree

This program creates 3 reports

**Most Popular Articles**

This is a report of the 3 most popular articles in the database as plain
text table. It displays the article title and how many views each article has
received

**Most Popular Authors**

This is a report of the most popular authors by page views as a plain text
table.  It ranks the authors by page views displaying the author's name and 
how many page views their articles have relieved

**Dates with greatest number of page view errors**

This is a report of the 10 days that have had the most page view errors. The 
report displayed in a list format. It displays the date, the error rate as
a percentage of page views per error and the total error count

## Running the program

To run the program type `python3 logs.py` in the console from the directory 
that this repository resides.  It is dependent on the database 
configuration for the Udacity Full Stack Web Developer Nanodegree course


Formatting of tabular reports was accomplished by modifying the code suggested 
here https://stackoverflow.com/questions/10865483/print-results-in-mysql-format-with-python/#answer-20383011
