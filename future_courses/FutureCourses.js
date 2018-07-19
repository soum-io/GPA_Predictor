/*
By: Michael Shea

Takes json info created in other js files for each majors' courses and then
add the data for each course to a csv file that is formatted correctly so that
the models created in the python files can use the data to predict the course
gpa. The only thing that is not perfectly formatted is the teachers' names, as
the course explorer api only return the first letter of the first name instead
of the whole first name. This is fixed in NextYearData.py
*/

var fs = require('fs')
var parseString = require('xml2js').parseString;
var http = require('https');
var fs = require('fs');

//input current info for semester here:
var year = 2018;
var semester = "spring";

if(semester === "spring"){
  semester = 1;
} else if (semester === "summer" ){
  semester = 2;
} else {
  semester = 3;
}
// fucntion used is from http://antrikshy.com/blog/fetch-xml-url-convert-to-json-nodejs
// pass in the url of a api request that will return XML data, and turn it into
// a json file that will be saved locally given in the path parameter.
function xmlToJson(url, callback, path) {
  var req = http.get(url, function(res) {
    var xml = '';

    res.on('data', function(chunk) {
      xml += chunk;
    });

    res.on('error', function(e) {
      callback(e, null);
    });

    res.on('timeout', function(e) {
      callback(e, null);
    });

    res.on('end', function() {
      parseString(xml, function(err, result) {
        callback(null, result, path);
      });
    });
  });
}

// callback function to the xmlToJson function above
function callback(err, data, path) {
  if (err) {
    return console.err(err);
  }
  fs.writeFile(path, JSON.stringify(data, null, 2), function(err) {
    if(err) {
        return console.log(err);
    }

    console.log(path + " was saved!");
  });
}


// class that will hold the required information for each future course. The
// constructor is given a json data file as well as x and i varaibles with
// represent which course in the data is being looked at. This is made clear
// down below
class Section{
  constructor(x,i,obj){
    this.abrCollege = obj["ns2:subject"]["$"]["id"]
    var listOfCourses = obj["ns2:subject"]["cascadingCourses"][0]["cascadingCourse"]
    this.number = listOfCourses[x]["detailedSections"][0]["detailedSection"][0]["parents"][0]["course"][0]["$"]["id"]
    this.shortAbr = this.abrCollege + this.number

    var course = obj["ns2:subject"]["cascadingCourses"][0]["cascadingCourse"][x];
    var section = course["detailedSections"][0]["detailedSection"][i]
    var tempProfessors =section["meetings"][0]["meeting"][0]["instructors"][0]["instructor"]
    var professors = []
    this.professor = "N/A"
    try{
      var tprofessors = []
      tempProfessors.forEach(function(ele){
        tprofessors.push(ele["_"])
      })
      professors = tprofessors
      this.professor = professors[0]
    }
    catch(error){}
    this.type = section["meetings"][0]["meeting"][0]["type"][0]["_"]
}}

// create new file for future course data, and initialize it with feature labels
fs.writeFile("./course_teacher.csv", "course,teacher,year,semester,semesters taught\n",function(err){
  if(err){throw err;}
})

// folder that holds the json info for major's courses
var majors_folder = './MajorsData/';

// loop through each majors data, collect the required course info using the
// class above, and write to course_teacher.csv the needed data fields
fs.open('./course_teacher.csv', 'a', 666, function( err, id ) {
  // loop through each major
  fs.readdirSync(majors_folder).forEach(major_file => {
    fs.readFile("./MajorsData/" + major_file, 'utf8', function (err, data) {
        var obj = JSON.parse(data)
        var courseLength = obj["ns2:subject"]["cascadingCourses"][0]["cascadingCourse"].length
        // loop through each course
        for(x = 0; x < courseLength; x++){
            var sectionLength = obj["ns2:subject"]["cascadingCourses"][0]["cascadingCourse"][x]["detailedSections"][0]["detailedSection"].length
            // loop through each section in current course
            for(i = 0; i < sectionLength; i++){
              // create course object that will be used to write to csv file
              var section = new Section(x,i,obj)
              try{
                // only use lecture sections
                if(section.professor != 'N/A' && section.type.includes("Lecture")){
                  // the (9.0+2.0/3.0) is the current year for fall 2018. Change if needed for other years
                  var to_write = section.shortAbr + ',"' +section.professor+'",'+(year).toString() + ',' + semester.toString() + '\n'
                  fs.write( id, to_write, null, 'utf8', function(){})
                }
              }
              catch(error){}
            }
          }
          if (err) throw err; // we'll not consider error handling for now

      if (err) throw err; // we'll not consider error handling for now
    })
  })
})
