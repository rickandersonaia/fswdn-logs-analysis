#!/bin/env python3.6

import psycopg2

DBNAME = "news"

def most_popular_articles_report():
    select_statement = "SELECT title, count(*) as views FROM articles JOIN log " \
                       "ON '/article/' || articles.slug = log.path " \
                       "GROUP BY title ORDER BY views DESC LIMIT 3"
    report_data = get_data(select_statement)
    report_title = '3 Most Popular Articles'
    widths = [40,8]
    columns = []
    for cd in report_data['column_description']:
        columns.append(cd[0])

    print_tabular_report(widths, columns, report_data['posts'], report_title)


def most_popular_authors_report():
    select_statement = "SELECT name, count(*) as views FROM authors " \
                       "JOIN articles ON authors.id = articles.author " \
                       "JOIN log ON '/article/' || articles.slug = log.path " \
                       "GROUP BY name " \
                       "ORDER BY views DESC"
    report_data = get_data(select_statement)
    report_title = 'Author Popularity by Article Page Views'
    widths = [40,8]
    columns = []
    for cd in report_data['column_description']:
        columns.append(cd[0])

    print_tabular_report(widths, columns, report_data['posts'], report_title)


def dates_with_greatest_errors_report():
    select_statement = "SELECT title, count(*) as views FROM articles JOIN log " \
                       "ON '/article/' || articles.slug = log.path " \
                       "GROUP BY title ORDER BY views DESC LIMIT 3"
    report_data = get_data(select_statement)
    report_title = 'Dates with greatest number of errors'
    widths = [20,8]
    columns = []
    for cd in report_data['column_description']:
        columns.append(cd[0])

    print_tabular_report(widths, columns, report_data['posts'], report_title)



def get_data(select_statement):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(select_statement)
    report_data = {'posts':c.fetchall(), 'column_description':c.description}
    db.close()
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


most_popular_authors_report()
