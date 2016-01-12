(function() {
    "use strict";

    var Exception = function(message) {
        this.message = "ERROR: " + message;
        this.name = "UserException";
        console.error(this.message);
    }

    function $http(url) {

        // A small example of object
        var core = {

            // Method that performs the ajax request
            ajax: function (method, url, args) {

                // Creating a promise
                var promise = new Promise(function (resolve, reject) {

                    // Instantiates the XMLHttpRequest
                    var client = new XMLHttpRequest();
                    var uri = url;

                    if (args && (method === 'POST' || method === 'PUT')) {
                        uri += '?';
                        var argcount = 0;

                        for (var key in args) {
                            if (args.hasOwnProperty(key)) {
                                if (argcount++) {
                                    uri += '&';
                                }
                                uri += encodeURIComponent(key) + '=' + encodeURIComponent(args[key]);
                            }
                        }
                    }

                    client.open(method, uri);
                    client.send();

                    client.onload = function () {
                        if (this.status >= 200 && this.status < 300) {
                            // Performs the function "resolve" when this.status is equal to 2xx
                            resolve(this.response);
                        } else {
                            // Performs the function "reject" when this.status is different than 2xx
                            reject(this.statusText);
                        }
                    }

                    client.onerror = function () {
                        reject(this.statusText);
                    }
                });

                // Return the promise
                return promise;
            }
        };

        // Adapter pattern
        return {
            'get' : function(args) {
                return core.ajax('GET', url, args);
            },
                'post' : function(args) {
                    return core.ajax('POST', url, args);
                },
                'put' : function(args) {
                    return core.ajax('PUT', url, args);
                },
                'delete' : function(args) {
                    return core.ajax('DELETE', url, args);
                }
        };
    };

    var Replay = function(MatchID, RoundID) {
        var self = this;

        self.MatchID = MatchID;
        self.RoundID = RoundID;

        self.status = true;

        self.loadRound();
    }

    Replay.prototype.loadRound = function() {
        var self = this;

        //Create URL to json file file
        self.roundJsonUrl = [window.location.protocol + "//" + window.location.host, "match-logs", self.MatchID, self.RoundID + ".json"].join("/")

        var callback = {
            success: function(data) {
                self.round = JSON.parse(data);
                console.log(self.round);
            },
            error: function(data) {
                throw new Exception("Can't load round file");
            }
        };

        $http(self.roundJsonUrl).get().then(callback.success).catch(callback.error);
    }

    //Export class
    window.Replay = Replay
}).call(this)
