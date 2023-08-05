# py-html-table Package

This is a simple package which uses beautifulSoup to extract HTML Table data along which has rowspan.

## Installation

pip install py-html-table

## Declare

import py_html_table.py_html_table as pyht

## Parameters

Parameter | Meaning | Sample Values
----------|---------|--------
table | python variable containing html code of table | any variable name
begin | No.of rows to begin scrapping. Starts from 0 | 2
col | Total No.of columns in the table. Starts from 1 | 5
output | Type of output that you need | list (or) dataframe (or) csv
raw | 'Y' to get exact content inside table cell. 'N' to get only text | 'Y' or 'N'

### NOTE: All variable names has to be provided as input to the package
## Usage Example

import requests\
from bs4 import BeautifulSoup\
import requests_html\
import lxml.html as lh\
import py_html_table.py_html_table as pyht

url = 'https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States' \
session = requests_html.HTMLSession()\
r = session.get(url)\
content = BeautifulSoup(r.content, 'lxml')\
all_tables = content.select(".wikitable") \
table = all_tables[0] \
col = 9\
begin = 2\
output = 'dataframe'\
raw = 'N'\
pyht.extract(table,begin,col,output,raw)