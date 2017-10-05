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

**Dates with page view errors of greater than 1%**

This is a report of the days that have had page view errors of greater than 1%. The 
report displayed in a list format. It displays the date, the error rate as
a percentage of page views per error and the total error count

## Setup
This setup describes the use of the program with Vagrant.  Dependencies include
Python 3.6, PostgreSQL, psycopg2 and datetime

The vagrant machine and basic setup can be found here - https://github.com/udacity/fullstack-nanodegree-vm

Install the vagrant machine and `vagrant up`

The postgreSQL data can be found here https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

Unzip the file and place its contents in the virtual machine's `vagrant/` 
directory.  To import the data into the database, SSH into the `vagrant/`
directory and run `psql -d news -f newsdata.sql`.  This produces the database
called "news".

Clone this repository into the `vagrant/` directory.


## Running the program

To run the program SSH into the `fswdn-logs-analysis/` directory and type
 `python3 logs.py` in the console 


Formatting of tabular reports was accomplished by modifying the code suggested 
here https://stackoverflow.com/questions/10865483/print-results-in-mysql-format-with-python/#answer-20383011
