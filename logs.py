#!/bin/env python3.6

import psycopg2
import psycopg2.extras
from datetime import datetime

DBNAME = "news"


def most_popular_articles_report():
    select_statement = "SELECT title, count(*) AS views " \
                       "FROM articles JOIN log " \
                       "ON '/article/' || articles.slug = log.path " \
                       "GROUP BY title ORDER BY views DESC LIMIT 3"
    report_data = get_data(select_statement)
    report_title = '3 Most Popular Articles'
    widths = [40, 8]
    columns = []
    for cd in report_data['column_description']:
        columns.append(cd[0])

    print_tabular_report(widths, columns, report_data['posts'], report_title)


def most_popular_authors_report():
    select_statement = "SELECT name, count(*) AS views FROM authors " \
                       "JOIN articles ON authors.id = articles.author " \
                       "JOIN log ON '/article/' || articles.slug = log.path " \
                       "GROUP BY name " \
                       "ORDER BY views DESC"
    report_data = get_data(select_statement)
    report_title = 'Author Popularity by Article Page Views'
    widths = [40, 8]
    columns = []
    for cd in report_data['column_description']:
        columns.append(cd[0])

    print_tabular_report(widths, columns, report_data['posts'], report_title)


def dates_with_greatest_errors_report():
    select_statement = "SELECT time::DATE AS date, count(*) FILTER(" \
                       "WHERE status != '200 OK') AS errors, " \
                       "count(*) AS views " \
                       "FROM log " \
                       "GROUP BY date ORDER BY errors DESC LIMIT 10"

    raw_data = get_data_as_dictionary(select_statement)
    report_data = format_date_in_table(raw_data, 'date')
    report_data = add_error_rate(report_data)
    report_title = 'Dates with greatest number of page view errors'

    print_dates_with_greatest_errors_report(report_data, report_title)


def format_date_in_table(table, key):
    for row in table:
        row[key] = datetime.strftime(row[key], '%B %d, %Y')
    return table


def add_error_rate(report_data):
    for row in report_data:
        errors = row['errors']
        views = row['views']
        row['error_rate'] = '{0:.2%}'.format(float(errors) / float(views))

    return report_data


def get_data(select_statement):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(select_statement)
    report_data = {'posts': c.fetchall(), 'column_description': c.description}
    db.close()
    return report_data


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


def print_dates_with_greatest_errors_report(report_data, report_title):
    print('')
    print(report_title)
    print('')
    for row in report_data:
        print("{} - {} of page views had errors ({} errors)".
              format(row['date'], row['error_rate'], row['errors']))
    print('')


dates_with_greatest_errors_report()
