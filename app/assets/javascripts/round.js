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

    /*
     * Replay
     * Displays a Replay of a given round
     * element (HTMLDomElement) Element to render to
     * MatchID (string)
     * RoundID (string)
     */
    var Replay = function(element, MatchID, RoundID) {
        var self = this;

        self.MatchID = MatchID;
        self.RoundID = RoundID;

        self.element = element;

        self.round = {};
        self.status = true;

        self.init();
    }

    /*
     * init()
     * Start the replay object, generate the layout elements, and load the round file
     */
    Replay.prototype.init = function() {
        var self = this;

        self.generateLayout();
        self.loadRound();
    }

    /*
     * roundLoaded()
     * Run after the round has been loaded
     */
    Replay.prototype.roundLoaded = function() {
        var self = this;
        self.displayMoves();
    }

    /*
     * generateLayout()
     * Creates HTML elements for the viewer
     */
    Replay.prototype.generateLayout = function() {
        var self = this;

        self.elements = {};

        self.elements["moves-viewer"] = document.createElement("ol");
        self.elements["controls"] = document.createElement("div");

        for (var key in self.elements) {
            self.elements[key].classList.add(key);
            self.element.appendChild(self.elements[key]);
        }
    }

    /*
     * displayMoves()
     * Generates HTML for displaying moves navigation to the user
     */
    Replay.prototype.displayMoves = function() {
        var self = this;

        var movesViewer = self.elements["moves-viewer"];

        var move, view;
        for (var i = 0; i < self.round.moves.length; i++) {
            move = self.round.moves[i];
            view = document.createElement("li");
            view.textContent = move["description"];
            movesViewer.appendChild(view);
        }        
    }

    /*
     * loadRound()
     * Load the round JSON file given the matchID and the roundID
     */
    Replay.prototype.loadRound = function() {
        var self = this;

        //Create URL to json file file
        self.roundJsonUrl = [window.location.protocol + "//" + window.location.host, "match-logs", self.MatchID, self.RoundID + ".json"].join("/")

        var callback = {
            success: function(data) {
                self.round = JSON.parse(data);
                self.roundLoaded();
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
