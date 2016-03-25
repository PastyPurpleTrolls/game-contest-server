(function () {
    "use strict";

    Replay.prototype.rendererWidth = 750;
    
    Replay.prototype.playIncrement = 0.5;

    Replay.prototype.rendererLoaded = function() {
        var self = this;

        //Set background color
        self.renderer.backgroundColor = 0x6F8DBD;
    }

    Replay.prototype.loadSprites = function() {
        var self = this; 
        
        self.sprites["playerName"] = new PIXI.Text("", {font: '30px Helvetica', fill: 0xffffff, align: 'center'});
        //Center sprite in renderer
        self.sprites["playerName"].anchor.x = 0.5;
        self.sprites["playerName"].position.x = self.renderer.width / 2;
        self.sprites["playerName"].position.y = 20;

        self.sprites["letter"] = new PIXI.Text('Waiting', {font : '90px Helvetica', fill : 0xffffff, align : 'center'});
        //Center sprite in the middle of the renderer
        self.sprites["letter"].anchor.set(0.5, 0.5);
        self.sprites["letter"].position.set(self.renderer.width / 2, self.renderer.height / 2);
    }

    Replay.prototype.generateGamestate = function() {
        var self = this;

        //Move "0", default gamestate
        if (self.moveNumber === 0) {
            self.gamestate = false;
            return;
        }

        var moveIndex = self.moveNumber - 1;
        var currentMove = self.round.moves[moveIndex];

        var moveData = self.parseJSON(currentMove["data"]);
        
        self.gamestate = moveData;
    }

    Replay.prototype.render = function() {
        var self = this;

        //Get the letter from the gamestate
        var letter = (self.gamestate) ? self.gamestate[1] : "Waiting";
        var playerName = (self.gamestate) ? self.gamestate[0] : "";
       
        //Update the player name
        self.sprites["playerName"].text = playerName;
        
        //Set the letter in the renderer
        self.sprites["letter"].text = letter;
    }

    
}).call(this);
