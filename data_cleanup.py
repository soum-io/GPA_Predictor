'''
By: Michael Shea

This python script will convert all the raw api request data in the "raw/" folder
to a cleaned version called filteredComplete.csv, which will be the files used
to train the models.
'''

import csv
import os
import numpy as np

# create directory if needed that will be needed in future steps
if not os.path.exists('future_courses/MajorsData'):
    os.makedirs('future_courses/MajorsData')

# These are the files that contain the raw api request data.
files = np.array(os.listdir('raw/'))
# Not using winter course data for now (may be used in later updates)
files = np.array([file for file in files if "wi" not in file])

# create new file to put clean data in
with open('filtered.csv', 'w', newline='' ) as newcsvfile:
    writer = csv.writer(newcsvfile, delimiter = ',',
                                quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    # coloumns we will be using for our filtered data. Note that we will use
    # embeddings of our data as part of the ML model, so that is fine that
    # we are assigning some of them ints where their value will not really matter:
    #   course           - course abr and #
    #   teacher          - last, first middle
    #   year             - current year start from 2010 (first year we have data from)
    #   semester         - current semester. (1 - spring, 2 - summer, 3 - fall)
    #   semesters taught - the amount of semesters the teacher has been teachin
    #                      since fall 2010
    #   gpa              - Average gpa of course
    writer.writerow(['course', 'teacher', 'year', 'semester', 'semesters taught', 'gpa'])

# loop through the data in the raw api request files in the folder "raw"
for file in range(files.size):
    with open('raw/' + files[file], newline='') as csvfile:
        with open('filtered.csv', 'a', newline='' ) as newcsvfile:
            writer = csv.writer(newcsvfile, delimiter = ',',
                                quotechar = '"', quoting=csv.QUOTE_MINIMAL)
            # get semester of course and normalize it with 2010, starting at 1.
            # if the term is spring - do not add to this number
            # if the term is summer - add 1 semester
            # if ther term is fall  - add 2 semesters
            semester = 1
            year = int(files[file][2:6])
            if files[file][:2] == "su":
                semester = 2
            elif files[file][:2] == "fa":
                semester = 3
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            # over the years, the data format changed. That is what is being accounted for here
            # as the differnece is in if it has a column for course subject or not.
            # for the column in the filtered data "semesters taught", that will be
            # calulated later, so "ST" will be used as a place holder
            if 'Course Subject' in headers:
                for row in reader:
                    writer.writerow([row['Course Subject'] + row['Course Number'],
                          row['Primary Instructor'], year, semester, "ST", row['Average Grade']])
            else:
                for row in reader:
                    writer.writerow([row['Subject'] + row['Course'],
                          row['Primary Instructor'], year, semester, "ST", row['Average Grade']])



# loop through filtered file just created and store the first semester each professor
# started teaching in a dictionary
professor_info = {} # professor mapped to first year taught
with open('filtered.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # 1 is spring, 2 is summer, 3 is fall
        if row['teacher'] not in professor_info.keys():
            professor_info[row['teacher']] = [int(row['year']), int(row['semester'])]
            continue
        # both year and semester must be greater to replace value
        if professor_info[row['teacher']][0] +  round(professor_info[row['teacher']][1]/10,1) > int(row['year']) + round(int(row['semester'])/10,1):
            professor_info[row['teacher']] = [int(row['year']) , int(row['semester'])]




# create new updated filtered file
with open('filteredComplete.csv', 'w', newline='' ) as newcsvfile:
    writer = csv.writer(newcsvfile, delimiter = ',',
                                quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    # same columns as last one
    writer.writerow(['course', 'teacher', 'year', 'semester', 'semesters taught', 'gpa'])


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
            # set all classes' 'semesters taught' and 'teacher' column to -1 if
            # missing professor name - wont have numerical of comparison to due
            # future embeddings
            if(row['teacher'] == ''):
                writer.writerow([row['course'], -1,
                  row['year'],row['semester'], -1,
                  row['gpa']])
                continue
            years_taught = int(row['year']) - professor_info[row['teacher']][0]
            semester_dif = int(row['semester']) - professor_info[row['teacher']][1]
            # 3 semesters a year
            semesters_taught = years_taught*3 + semester_dif

            # write same row but add semesters_taught calculation
            writer.writerow([row['course'], row['teacher'],
                  row['year'], row['semester'], semesters_taught,
                  row['gpa']])

# remove filtered.csv as it is not needed anymore - uncomment
# to also keep it saved for debugging purposes
# os.remove("filtered.csv")
