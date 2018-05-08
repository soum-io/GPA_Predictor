'''
By: Michael Shea

This python scripts uses the future class information created by the
javascript files and makes the data model-ready (aka correct format as 
data returned by the gpa api request). This is accomplished by
turning the generated future classes data's teachers names into full names, 
since the course explorer api used by the javacript code 
only returns first letter of first name for each teacher.
'''
import pandas as pd
import numpy as np



# create dictionary of teacher names in future course data with teacher names
# from previous gpa filtered data. Note that only the first letter of the first
# name was given to us for the future data, so there may be some name clashes
# (e.i. multiple teachers have the same last name and first letter of their 
# first name). To try to correct this, we first create the normal teacher
# pairing down below. If there are duplicates, we try to see if only one version
# of the slimmed name exist in the department the teacher in the future course 
# is teaching in. If duplicates still exist, we try to see if the future course
# the teacher is teaching was a course a matching teacher taught in previous 
# years. If there are still duplicates on any level, we can not distinguish 
# teacher by name anymore, so we will leave the name field  blank. 

prof_dict = {} # dict that will be used for normal pairing
prof_class_dict = {} # dict that will be used for teacher - department pairing
prof_major_dict = {} # dict that will be used for teacher - course pairing

orig_data = pd.read_csv("filteredComplete.csv")
for index, row in orig_data.iterrows():
    if(pd.isnull(orig_data.loc[index,"teacher"])):
        print(index)
        continue
    space_idx = row["teacher"].find(' ')
    shortned_name = row["teacher"][:space_idx+2]
    major_full = ''.join([i for i in row["course"] if not i.isdigit()])
    major = row["course"]
    if shortned_name not in prof_dict:
        
        prof_dict[shortned_name] = [row["teacher"]]
        prof_class_dict[shortned_name] = {major : [row["teacher"]]}
        prof_major_dict[shortned_name] = {major_full : [row["teacher"]]}
    else:
        if row["teacher"] not in prof_dict[shortned_name]:
            prof_dict[shortned_name].append(row["teacher"])
        if major not in prof_class_dict[shortned_name]:
            prof_class_dict[shortned_name][major] = [row["teacher"]]
        elif row["teacher"] not in prof_class_dict[shortned_name][major]:
            prof_class_dict[shortned_name][major].append(row["teacher"])
        if major_full not in prof_major_dict[shortned_name]:
            prof_major_dict[shortned_name][major_full] = [row["teacher"]]
        elif row["teacher"] not in prof_major_dict[shortned_name][major_full]:
            prof_major_dict[shortned_name][major_full].append(row["teacher"])

# create dictionary that stores the smallest year the teacher was on record            
start_year_dict = {}
for index, row in orig_data.iterrows():
    if row["teacher"] not in start_year_dict:
        start_year_dict[row["teacher"]] = row["year"]
    else:
        if start_year_dict[row["teacher"]] > row["year"]:
            start_year_dict[row["teacher"]] = row["year"]
            
            
# update teacher name and years the teacher taught (defaults to 0 if new tacher
# or teacher without duplicates is not found)
new_data = pd.read_csv("course_teacher_no_dup.csv")
for index, row in new_data.iterrows():
    old_name = row["teacher"]
    major_full = ''.join([i for i in row["course"] if not i.isdigit()])
    major = row["course"]
    try:
        if old_name not in prof_dict:
            val = np.NaN
            row["teacher"] = val
            new_data.set_value(index,"teacher",val)
        elif len(prof_dict[old_name]) == 1:
            val = prof_dict[old_name][0]
            row["teacher"] = val
            new_data.set_value(index,"teacher",val)
        elif len(prof_major_dict[old_name][major_full]) == 1:
            val = prof_major_dict[old_name][major_full][0]
            row["teacher"] = val
            new_data.set_value(index,"teacher",val)
        elif len(prof_class_dict[old_name][major]) == 1:
            val = prof_class_dict[old_name][major][0]
            row["teacher"] = val
            new_data.set_value(index,"teacher",val)
        else:
            val = np.NaN
            row["teacher"] = val
            new_data.set_value(index,"teacher",val)
    except:
        val = np.NaN
        row["teacher"] = val
        new_data.set_value(index,"teacher",val)
    
    if(pd.isnull(new_data.loc[index,"teacher"]) or (row["teacher"] not in start_year_dict)):
        new_data.set_value(index,"years taught",str(0.0))
    else:
        years_t = str(float(row["year"]) - float(start_year_dict[row["teacher"]]))
        new_data.set_value(index,"years taught",years_t)
        
# create new filed with correctly formatted data
new_data.to_csv("course_teacher_full.csv", index = False)       
    

    
    







    
        






