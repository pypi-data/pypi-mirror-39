import requests
from bs4 import BeautifulSoup
import requests_html
import lxml.html as lh
import pandas as pd
import csv
import datetime

def extract(table,begin,col,output,raw):
    
    ### Initialize all lists and dictionary ###
    d = {}
    for x in range(0,col):
        globals()["column_" + str(x)] = []

    ### Function to process rows that doesnt have any rowspan ###
    def process_all_columns(row):
        for num, cell in enumerate(row):
            if 'rowspan' in cell.attrs:
                for span in range(0,int(cell.attrs['rowspan'])):
                    globals()["column_" + str(num)].append(cell)
            else:
                globals()["column_" + str(num)].append(cell)
        return column_0

    ### Function to store the length of each list ###
    def refresh_dict():
        d = {}
        for j in range(0,col):
            d[j] = len(globals()["column_" + str(j)])
        return d

    ### Function to get the list which has lesser number of elements ###
    def get_list_to_populate():
        minval = min(d.values()) #find which column array has lesser values
        res = [k for k, v in d.items() if v==minval] #if more than 1 has lesser values
        return res

    ### Function to process rows which has rowspan ###
    def process_partial_columns(row):
        lists = get_list_to_populate()
        for num, cell in enumerate(row):
            if 'rowspan' in cell.attrs:
                for span in range(0,int(cell.attrs['rowspan'])):
                    globals()["column_" + str(lists[num])].append(cell)
            else:
                globals()["column_" + str(lists[num])].append(cell)
        return lists

    ### Main code which calls all functions to process the data ###
    rowbegin = begin
    rows = table.findAll('tr')
    while rowbegin < len(rows):
        current_row = rows[rowbegin].select('td')
        current_total_columns = len(current_row)
        if current_total_columns == col: #if there is no rowspan
            process_all_columns(current_row)
            d = refresh_dict()
        else: #if there is rowspan
            process_partial_columns(current_row)
            d = refresh_dict()
        rowbegin+=1
    
    ### Convert the different lists - column_1, column_2 etc. to a single list - pdlist###
    i = 0
    pdlist = []
    while i < len(rows)-begin:
        dt = []
        x = 0
        while x < col:
            if raw == 'Y':
                dt.append(globals()["column_" + str(x)][i])
            else:
                dt.append(globals()["column_" + str(x)][i].text)
            x+=1
        pdlist.append(dt)
        i+=1

    ### Convert list to necessary formats ###
    if output == 'list':
         return pdlist
    elif output == 'dataframe':
        df = pd.DataFrame(pdlist)
        return df
    elif output == 'csv':
        df = pd.DataFrame(pdlist)
        df.to_csv("html-table-" + str(datetime.datetime.now().strftime("%I %M %p on %B %d, %Y")) + '.csv')
        return 'Success! The Table data is exported to CSV'    