var express = require("express");
var app = express();
var path = require("path");

var port = process.env.PORT || 3000;

// Set the current directory to a static folder since we'll need to access 'converter.js' from our webpage.
app.use("/app", express.static(__dirname));
// Make sure our tests are accessible.
app.use("/test", express.static(path.join(__dirname, "..", "test")));

var server = app.listen(port, function () {
  var host = server.address();
  var baseUrl = "http://" + host.address + ":" + host.port;
  console.log("Tests are viewable at " + baseUrl + "/test/");
});

// Handle SIGTERM signal.
function shutdown(cb) {
  "use strict";

  try {
    server.close(function() {
      process.exit(0);
      if (cb !== undefined) {
        cb();
      }
    });
  } catch (ex) {
    console.log(ex + " while calling server.close)");
  }
}

process.on("SIGTERM", shutdown);
