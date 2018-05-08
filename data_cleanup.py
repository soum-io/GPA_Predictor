'''
By: Michael Shea

This python script will convert all the raw api request data in the "raw/" folder
to a cleaned version called filteredComplete.csv, which will be the files used 
to train the models.
'''

import csv
import os
import numpy as np

# These are the files that contain the raw api request data.
files = np.array(os.listdir('raw/'))
# Not using winter course data for now (may change later)
files = np.array([file for file in files if "wi" not in file])

# create new file to put clean data in
with open('filtered.csv', 'w', newline='' ) as newcsvfile:
    writer = csv.writer(newcsvfile, delimiter = ',', 
                                quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    # coloumns we will be using for our filtered data: 
    #   course       - course abr and #
    #   teacher      - last, first middle
    #   year         - current year start from 2010 (first year we have data from)
    #                  e.g. if the year is spring 2011, the value is 2.0 (we give 2010
    #                  a value of 1.0). If the year is fall 2011, the value is
    #                  2.666 (each year is split into fall, summer, and spring)
    #   years taught - the amount of years the teacher has been teaching since 2010. 
    #                  e.g. if the first record of the teacher we have was in fall 2011
    #                  and the year is spring 2013, then this value will be 2.666
    #   gpa          - Average gpa of course
    writer.writerow(['course', 'teacher', 'year', 'years taught', 'gpa'])

#loop through the data in the raw api request files in the folder "raw"
for file in range(files.size):  
    with open('raw/' + files[file], newline='') as csvfile:
        with open('filtered.csv', 'a', newline='' ) as newcsvfile:
            writer = csv.writer(newcsvfile, delimiter = ',', 
                                quotechar = '"', quoting=csv.QUOTE_MINIMAL)
            # get eyar of course and normalize it with 2009, as described above.
            # if the term is spring - do not add to this number
            # if the term is summer - add 1/3 year
            # if ther term is fall  - add 2/3 year
            term_number = int(files[file][2:6]) - 2009.0
            if files[file][:2] == "su":
                term_number = term_number + 1/3
            elif files[file][:2] == "fa":
                term_number = term_number + 2/3
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            # over the years, the data format changed. That is what is being accounted for here
            # as the differnece is in if it has a column for course subject or not.
            # for the column in the filtered data "years taught", that will be 
            # calulated later, so "YT" will be used as a place holder
            if 'Course Subject' in headers:
                for row in reader:
                    writer.writerow([row['Course Subject'] + row['Course Number'],
                          row['Primary Instructor'], term_number, "YT", row['Average Grade']])
            else:
                for row in reader:
                    writer.writerow([row['Subject'] + row['Course'],
                          row['Primary Instructor'], term_number, "YT", row['Average Grade']])    
    
    

# loop through filtered file just created and store the first year each professor
# started teaching in a dictionary
professor_info = {} # professor mapped to first year taught
with open('filtered.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['teacher'] not in professor_info.keys():
            professor_info[row['teacher']] = row['year']
            continue
        if professor_info[row['teacher']] > row['year']:
            professor_info[row['teacher']] = row['year']


    
 
# create new updated filtered file
with open('filteredComplete.csv', 'w', newline='' ) as newcsvfile:
    writer = csv.writer(newcsvfile, delimiter = ',', 
                                quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    # same columns as last one
    writer.writerow(['course', 'teacher', 'year', 'years taught', 'gpa'])


# iterator filtered.csv to complete filteredComplete.csv that will contain true
# years taught values
with open('filtered.csv','r', newline='') as csvfile:
    with open('filteredComplete.csv', 'a', newline='' ) as newcsvfile:
        writer = csv.writer(newcsvfile, delimiter = ',', 
                            quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'N/A' in row.values():
                continue 
            # set all classes' years_taught column to 0 if missing professor name
            if(row['teacher'] == ''):
                writer.writerow([row['course'], row['teacher'],
                  row['year'], 0.0, 
                  row['gpa']])
                continue
            # years taught column is year - starting year
            writer.writerow([row['course'], row['teacher'],
                  row['year'], float(row['year']) - float(professor_info[row['teacher']]), 
                  row['gpa']])
