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
    var Replay = function(element, assetsUrl, MatchID, RoundID) {
        var self = this;

        self.MatchID = MatchID;
        self.RoundID = RoundID;
        self.assetsUrl = assetsUrl;

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
        self.initRenderer();
        self.loadRound();
    }

    /*
     * roundLoaded()
     * Run after the round has been loaded
     */
    Replay.prototype.roundLoaded = function() {
        var self = this;
        self.displayMoves();
        self.loadMove(2);
    }

    /*
     * parseJSON()
     * Helper function, replaces all single quotes with double quotes and parses the string as JSON
     * string {string} String to parse
     */
    Replay.prototype.parseJSON = function(string) {
        var self = this;
        
        try {
            string = string.replace(/'/gi, '"');
            var obj = JSON.parse(string);
        } catch(e) {
            var obj = {};
        }

        return obj;
    }

    /*
     * generateLayout()
     * Creates HTML elements for the viewer
     */
    Replay.prototype.generateLayout = function() {
        var self = this;

        self.elements = {};

        self.elements["renderer"] = document.createElement("div");
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
     * loadMove()
     * Display a move in the renderer
     * move {int} Index of move in moves object
     */
    Replay.prototype.loadMove = function(move) {
        var self = this;

        self.currentMoveIndex = (move > self.round.moves.length || move < 0) ? 0 : move;
        self.currentMove = self.round.moves[self.currentMoveIndex];

        self.generateGameState();
        //self.renderGame();
    }

    /*
     * generateGameState()
     * Generate the current gamestate based upon the current move
     * Stub function, define in plugin
     */
    Replay.prototype.generateGameState = function() {}

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
                console.log("round", self.round);
                self.roundLoaded();
            },
            error: function(data) {
                throw new Exception("Can't load round file");
            }
        };

        $http(self.roundJsonUrl).get().then(callback.success).catch(callback.error);
    }

    Replay.prototype.render = function(gamedata) {}


    /*
     * initRenderer()
     * Generates PIXI canvas element
     */
    Replay.prototype.initRenderer = function() {
        var self = this;
    
        self.stage = new PIXI.Stage(0x66FF99);
        console.log(self);
        self.renderer = PIXI.autoDetectRenderer(self.rendererWidth, self.rendererHeight);
        
        self.elements["renderer"].appendChild(self.renderer.view);
        
        self.loadTextures();

        self.sprites = {};
        self.loadSprites();

        self.spawnSprites();

        requestAnimationFrame(self.animate.bind(self));
    }


    /*
     * animate()
     * Update renderer state on every animation frame
     */
    Replay.prototype.animate = function() {
        var self = this;

        self.renderer.render(self.stage);

        requestAnimationFrame(self.animate.bind(self));
    }

    /*
     * loadTextures()
     * Stub function, defined in plugin
     * Loads all the textures
     */
    Replay.prototype.loadTextures = function() {}

    /* 
     * loadSprites()
     * Assign textures to sprites and load them in the view
     * Stub function, defined in plugin
     */
    Replay.prototype.loadSprites = function() {}


    /*
     * spawnSprites()
     * Add sprites to stage
     */
    Replay.prototype.spawnSprites = function() {
        var self = this;
        for (var key in self.sprites) {
            self.spritesHelper(self.sprites[key]);
        }
    }

    /*
     * spritesHelper()
     * Recursively loop through sprites object and add new sprites to stage
     * obj {object} List of sprites or sprite
     */
    Replay.prototype.spritesHelper = function(obj) {
        var self = this;
        if ("_texture" in obj) {
            self.stage.addChild(obj);            
        } else {
            for (var key in obj) {
                if (obj.hasOwnProperty(key)) {
                    self.spritesHelper(obj[key]);
                }
            }
        }         
    }

    /*
     * addTexture()
     * Add a texture to the textures object
     * name {string} name of the texture
     * url {string} Relative URL of the texture
     */
    Replay.prototype.addTexture = function(name, url) {
        var self = this;

        if (!self.textures) self.textures = {};
        if (name in self.textures) return;

        self.textures[name] = PIXI.Texture.fromImage(self.assetsUrl + url);
    }


    //Export class
    window.Replay = Replay
}).call(this)
