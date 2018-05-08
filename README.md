# UIUC Course GPA Predictor
### Created By: _Michael Shea_
## Goal
The goal of this project is to be able to predict the average GPAs of current and future courses at UIUC using previous GPA data and Machine Learning.

## Desired Outcome
I hope that students will be able to use this data to help decide what class to take in an upcoming semester, similarly to the way they do with [previous GPA data visualizations](http://waf.cs.illinois.edu/discovery/gpa_of_every_course_at_illinois/). This will require the predicted data to also be visualized - which will be worked on once the model and predictions are completed.

## How to Reproduce My Results
1. Fork the project. Make sure all python libraries that imported in the code are installed on your local machine. Node.js is needed to run the JavaScript files.
2. Open and run _data_cleanup.py_. It should create a file called _filteredComplete.csv_. This file contains all the training and testing data from previous semesters.
3. Open and run _GetMajorData.js_, which is located in the _future courses_ folder. This should create the file _MajorData.json_, which holds the json data of an API response from [the Course Explorer API](https://courses.illinois.edu/cisdocs/explorer) the contains info on all the majors that courses will be offered for. This data is needed for the next step.
4. Open and run _GetCoursesByMajor.js_, which is located in the _future courses_ folder. This will take a few minutes to run. For each major found in the _MajorData.json_, it will save all of the info regarding courses for that major for the semester specified in the code. This data is stored in json format in the folder _MajorsData_.
5. Open and run _FutureCourses.js_, which is located in the _future courses_ folder. This will create a file called _course_teacher.csv_. This file is all of the course data for the semester specified in the code in the format of the data created in step 2.
6. Open and run _NextYearData.py_. This will create a file called _course_teacher_full.csv_. This is the same thing as _course_teacher.csv_, except the teachers name are in the correct format.
7. Now it is time to create a model using _classifier.py_. This is still a word in progress!
