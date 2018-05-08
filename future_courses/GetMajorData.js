/*
By: Michael Shea

In the Javascript file, we call the course explorer api to obtain majors of
future courses in XML. The data is then converted into json and saved.
*/

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
  //console.log(JSON.stringify(data, null, 2)) ;
}

// url for the years data that you want. Simply update year if needed in the url
var url1 = 'https://courses.illinois.edu/cisapp/explorer/catalog/2018/fall.xml'

// file path for data to go
var filePath = "C:/Users/mikes/Desktop/GPA_Predictor/future_courses/MajorData.json";

xmlToJson(url1,callback, filePath);
