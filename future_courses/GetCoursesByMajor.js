/*
By: Michael Shea

This javascript file uses 2018Data.json to get a list of all majors that have
courses next semester, then call the api to get the future course data for each
major
*/

var fs = require('fs')
var parseString = require('xml2js').parseString;
var http = require('https');
var fs = require('fs');


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

// loop through each major in the MajorData.json, and call the api to get course
// info for the major for desired year, and save the json info in the folder
// MajorsData
var data_file = './MajorData.json'
fs.readFile(data_file, 'utf8', function (err, data) {
    if (err) throw err; // we'll not consider error handling for now
    var obj = JSON.parse(data)
    var data = obj["ns2:term"]["subjects"][0]["subject"]
    data.forEach(function(ele){
      var abr = ele["$"]["id"]
      // change the year here if fall 2018 is not desired
      var first_part = "https://courses.illinois.edu/cisapp/explorer/schedule/2018/fall/"
      var second_part = ".xml?mode=cascade"
      var url_major = first_part + abr + second_part
      var major_file_path =__dirname+"/MajorsData/"+abr+ ".json"
      xmlToJson(url_major, callback, major_file_path)
      console.log(url_major)
    })
  }
)
