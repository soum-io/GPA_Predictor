/*
By: Michael Shea

In the Javascript file, we call the course explorer api to obtain majors of
future courses in XML. The data is then converted into json and saved.
*/
// fill these out to obtain desired data
var year = 2018
var semester = 'spring'

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

// url for the year and semester data that you want. 

var url1 = 'https://courses.illinois.edu/cisapp/explorer/catalog/' + year + '/' + semester + '.xml'

// file path for data to go
var filePath = __dirname+"/MajorData.json";

xmlToJson(url1,callback, filePath);
