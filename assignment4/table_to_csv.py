
# Author: Jakob Valen
# Student ID: V00943160
# Class: SENG 265, Fall 2019
# Assignment_4
import csv
import sys
import os 
import re

# Master_dict will store all of our data for our html file
# Each table will have its own dictionary of rows
# For each row in each table, the row will have a dictionary of
# data that is stored within that row
Master_dict = {}

def main():

    # Check if a input file was piped in via the terminal
    if(os.isatty(sys.stdin.fileno())):
        sys.stderr.write("ERROR: Please pipe (<) the html file you wish to input \n")
        sys.exit(6)
    # We will gather all data from standard input and append it to one long string
    html_file = ""
    for line in sys.stdin:
        # Replace all new line characters so that all data is appeneded to the html_file string
        line = line.replace("\n","")
        html_file+=line
    # Check if the input file from standard input is empty
    if(html_file == ""):
        sys.stderr.write("ERROR: Empty input file \n")
        sys.exit(6)
    # Find all table tags, for each table, we will make a dictionary for that table
    table_counter = 0
    break_counter = 0

    for tables in re.finditer("<table.*?>(.*?)</table>",html_file,re.IGNORECASE):
        data_counter = 0 # The number of items in each row
        row_counter = 0 # The number of rows in each table
        max_row_length = 0
        headers_counter = 0
        headers_tag = False # False if no "<th>" tag was found
        table_counter+=1
        Master_dict["TABLE %s:"%(table_counter)] = {}

        # Find all the row tags, for each row, we will make a dictionary for that row
        for rows in re.finditer("<tr.*?>(.*?)</tr.*?>",tables.group(),re.IGNORECASE):
            data_counter = 0
            row_counter+=1
            Master_dict["TABLE %s:"%(table_counter)]["ROW_%s"%(row_counter)] = {}

            #If there was a header tag, add them to our dictionary
            if(re.search("<th.*?>",html_file) != None):
                headers_tag = True

                for headers in re.finditer("<th.*?>(.*?)</th.*?>",rows.group(),re.IGNORECASE):
                    data_counter+=1
                    headers_counter+=1
                    top_part = headers.group().index(">")
                    bottom_part = headers.group().lower().index("</th")
                    value  = headers.group()[top_part+1:bottom_part]
                    # Replace mutliple whitespaces with one single whitespace
                    value = re.sub(" +"," ",value)
                    # Strip any remaining whitespace around the data
                    value = value.strip()
                    if(value == " "):
                        value = ""
                    Master_dict["TABLE %s:"%(table_counter)]["ROW_%s"%(row_counter)]["COL_%s"%(data_counter)] = value

            # Find all the data for each row, and add it to our dictionary
            for data in re.finditer("<td.*?>(.*?)</td.*?>",rows.group(),re.IGNORECASE):
                if(headers_tag):
                    max_row_length = 0
                elif(data_counter>max_row_length):
                    max_row_length = data_counter
                data_counter+=1
                top_part = data.group().index(">")
                bottom_part = data.group().lower().index("</td")
                value = data.group()[top_part+1:bottom_part]
                # Replace multiple whitespaces with one single whitespace
                value = re.sub(" +"," ",value)
                # Strip any remaining whitespace around the data
                value = value.strip()
                if(value == " "):
                    value = ""
                Master_dict["TABLE %s:"%(table_counter)]["ROW_%s"%(row_counter)]["COL_%s"%(data_counter)] = value

            # While our current row has less data than the number of headers, append an empty coloumn
            # This only happens if there where any headers in our table
            while(data_counter < headers_counter):
                data_counter+=1
                Master_dict["TABLE %s:"%(table_counter)]["ROW_%s"%(row_counter)]["COL_%s"%(data_counter)] = ""
            # While our current row has less data than our max row, append an empty coloumn
            while(data_counter <= max_row_length):
                data_counter+=1
                Master_dict["TABLE %s:"%(table_counter)]["ROW_%s"%(row_counter)]["COL_%s"%(data_counter)] = ""

        # Count how many break statments there are in the html file so that we can output them appropraitley later
        if(re.search("<br.*?/>",html_file,re.IGNORECASE) != None):
            break_counter+=1


    # If no tables were found in the html file, print an error message
    if(table_counter == 0):
        sys.stderr.write("ERROR: No html tables found in the input file \n")
        sys.exit(6)
    # Once all the table data has been organized into our dictionary, we will output the contents to standard output
    output_writer = csv.writer(sys.stdout)

    for tables in Master_dict:
        tables_list = []
        tables_list.append(tables)
        output_writer.writerow(tables_list)

        for rows in Master_dict[tables]:
            rows_list = []

            for cols in Master_dict[tables][rows]:
                rows_list.append(Master_dict[tables][rows][cols])

            output_writer.writerow(rows_list)
        # Output any line breaks after each table
        if(break_counter>0):
            break_counter-=1
            output_writer.writerow("")

if __name__ == '__main__':
    main()
