var express = require("express");
var app = express();
var path = require("path");

var port = process.env.PORT || 3000;

app.use("/test", express.static(path.join(__dirname, "test")));
app.use("/test", express.static(path.join(__dirname, "..", "test")));

// As we don't have hashes on the urls, the best way to serve the index files
// appears to be to be to closely filter the url and match appropriately.
function serveIndex(req, res) {
  "use strict";

  return res.sendFile(path.join(__dirname, standaloneContentDir, "index.html"));
}

app.listen(3000);

var baseUrl = "http://localhost:" + port + "/";

console.log("Tests are viewable at " + baseUrl + "test/");
console.log("Use this for development only.");

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
