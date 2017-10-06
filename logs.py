#!/bin/env python3.6

import psycopg2
import psycopg2.extras
from datetime import datetime

DBNAME = "news"


# Generates a report of the 3 most popular articles in the database as plain
# text table showing the article title and how many views each article has
# recieved


def most_popular_articles_report():
    select_statement = "SELECT title, count(*) AS views " \
                       "FROM articles JOIN log " \
                       "ON '/article/' || articles.slug = log.path " \
                       "GROUP BY title ORDER BY views DESC LIMIT 3"
    report_data = get_data(select_statement)
    report_title = '3 Most Popular Articles'
    widths = [40, 8]  # widths of printed columns
    columns = []
    for cd in report_data['column_description']:  # add column names to report
        columns.append(cd[0])

    print_tabular_report(widths, columns, report_data['posts'], report_title)


# Generates a report of the most popular authors by page views as a plain text
# table ranking the authors by pageviews showing the author's name and how many
# page views their articles have revieved

def most_popular_authors_report():
    select_statement = "SELECT name, count(*) AS views FROM authors " \
                       "JOIN articles ON authors.id = articles.author " \
                       "JOIN log ON '/article/' || articles.slug = log.path " \
                       "GROUP BY name " \
                       "ORDER BY views DESC"
    report_data = get_data(select_statement)
    report_title = 'Author Popularity by Article Page Views'
    widths = [40, 8]  # widths of printed columns
    columns = []
    for cd in report_data['column_description']:  # add column names to report
        columns.append(cd[0])

    print_tabular_report(widths, columns, report_data['posts'], report_title)


# Generates a report of the days that have an error rate of more than 1%
# displayed in a list format showing the date, the error rate as
# a percentage of page views per error and the total error count


def dates_with_errors_over_one_percent_report():
    select_statement = "WITH error_agg_table AS ( " \
                       "SELECT time::DATE AS date, count(*) AS errors " \
                       "FROM log WHERE status != '200 OK' " \
                       "GROUP BY date ), " \
                       "views_agg_table AS ( " \
                       "SELECT time::DATE AS date, count(*) AS views " \
                       "FROM log GROUP BY date )" \
                       "SELECT error_agg_table.date AS date, " \
                       "error_agg_table.errors, " \
                       "views_agg_table.views " \
                       "FROM views_agg_table JOIN error_agg_table " \
                       "ON error_agg_table.date = views_agg_table.date " \
                       "WHERE errors::DECIMAL / views >= 0.01" \
                       "ORDER BY error_agg_table.errors DESC LIMIT 10"

    raw_data = get_data_as_dictionary(select_statement)
    report_data = format_date_in_table(raw_data, 'date')
    report_data = add_error_rate(report_data)
    report_title = 'Dates with page view errors in excess of 1%'

    print_dates_with_errors_over_one_percent_report(report_data, report_title)


# takes the date object from a dictionary or table and formats it into an
# easily read US format.  It converts the value in the dictionary to the
# new value and then returns the dictionary


def format_date_in_table(table, key):
    for row in table:
        row[key] = datetime.strftime(row[key], '%B %d, %Y')
    return table


# Adds an error rate column to the dictionary. It calculates the error rate
# and then formats it into an easily read format. Once formatted it adds the
# new element to a the dictionary


def add_error_rate(report_data):
    for row in report_data:
        errors = row['errors']
        views = row['views']
        row['error_rate'] = '{0:.2%}'.format(float(errors) / float(views))

    return report_data


# This is the query statement for the tabular type reports.  It executes the
# query and then adds it to a dictionary along with the column names.
# Finally it returns the resultant dictionary


def get_data(select_statement):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(select_statement)
    report_data = {'posts': c.fetchall(), 'column_description': c.description}
    db.close()
    return report_data


# This is the query statement for the list type reports.  It executes the
# query and then converts it to a dictionary of dictionaries where column names
# beoome keys. Finally it returns the resultant dictionary


def get_data_as_dictionary(select_statement):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c.execute(select_statement)
    result_set = c.fetchall()
    db.close()
    report_data = []
    for row in result_set:
        report_data.append(dict(row))
    return report_data


# This prints the tabular style report.  It attempts to mimic the command line
# query printout using plain text.


def print_tabular_report(widths, columns, posts, report_title):
    tavnit = '|'
    separator = '+'
    for w in widths:
        tavnit += " %-" + "%ss |" % (w,)
        separator += '-' * w + '--+'

    print('')
    print(report_title)
    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in posts:
        print(tavnit % row)
    print(separator)
    print('')


# This prints the list style report.  It displays the results as a sentence.


def print_dates_with_errors_over_one_percent_report(report_data, report_title):
    print('')
    print(report_title)
    print('')
    for row in report_data:
        print("{} - {} of page views had errors with {} errors in {} views".
              format(row['date'], row['error_rate'], row['errors'],
                     row['views']))
    print('')


if __name__ == "__main__":
    most_popular_articles_report()
    most_popular_authors_report()
    dates_with_errors_over_one_percent_report()
