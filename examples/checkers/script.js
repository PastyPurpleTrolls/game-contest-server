(function() {
    "use strict";

    Replay.prototype.rendererWidth = 722;
    Replay.prototype.rendererHeight = 728;

    Replay.prototype.pieces = {
        "red": [3, 4],
        "black": [1, 2]
    };

    Replay.prototype.gamestate = [
        [0, 1, 0, 1, 0, 1, 0, 1], 
        [1, 0, 1, 0, 0, 0, 1, 0], 
        [0, 1, 0, 1, 0, 1, 0, 1], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 3, 0, 3, 0, 3, 0, 3], 
        [3, 0, 3, 0, 3, 0, 3, 0], 
        [0, 3, 0, 3, 0, 3, 0, 3]
    ];

    Replay.prototype.rowMap = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
    };


    Replay.prototype.generateGameState = function() {
        var self = this;

        var colors = JSON.parse(self.round.info);
        
        //Already calculated the gamestate, move on
        if ("gamestate" in self.currentMove) {
            self.gamestate = JSON.parse(self.currentMove.gamestate);
        } else {
            var deltaStep = 10;
            var gamestate = [];
            
            var deltaMove = {};
            var deltaIndex = self.currentMoveIndex;

            //Step backward through moves to find the most recent defined deltastep
            for (deltaIndex = self.currentMoveIndex; deltaIndex > self.currentMoveIndex - deltaStep && deltaIndex >= 0; deltaIndex--) {
              deltaMove = self.round.moves[deltaIndex];
              if ("gamestate" in deltaMove) break;
            }

            //Gamestate has never been generated, add the default gamestate
            if (!("gamestate" in deltaMove)) deltaMove["gamestate"] = self.gamestate.slice(0);
            if (deltaIndex === self.currentMoveIndex) return;


            var move, moveData, currentPlayerColor, opponentPlayerColor, moveString, moveSpots;
            //Move forward and generate the gamestates for each move along the way
            for (var i = (deltaIndex + 1); i <= self.currentMoveIndex; i++) {
                move = self.round.moves[i];
                moveData = self.parseJSON(move["data"]);
                
                currentPlayerColor = colors[moveData[0]];
                opponentPlayerColor = (currentPlayerColor === "black") ? "red" : "black"; 
                console.log(currentPlayerColor, opponentPlayerColor);
                
                moveSpots = moveData[1].split(":");
                console.log(moveSpots);

                for (var j = 0; j < moveSpots.length - 1; j++) {
                    var fromRow = self.rowMap[moveSpots[j][0]];
                    var fromCol = parseInt(moveSpots[j][1]);
                    console.log(fromRow, fromCol);

                    var toRow = self.rowMap[moveSpots[j + 1][0]];
                    var toCol = parseInt(moveSpots[j + 1][1]);

                    var playerPiece = self.gamestate[fromRow][fromCol];
                    var king = false;
                    if ([2, 4].indexOf(playerPiece) !== -1) {
                        king = true;
                    }
                }
    
                //Update move with gamedata
                move["gamestate"] = self.gamestate.slice(0);
            }
        }
    }

    Replay.prototype.loadTextures = function() {
        var self = this;

        self.addTexture("checkerboard", "checkerboard.png");
        self.addTexture("white", "white.png");
        self.addTexture("black", "black.png");
        self.addTexture("whiteKing", "whiteKing.png");
        self.addTexture("blackKing", "blackKing.png");
    }

    Replay.prototype.loadSprites = function() {
        var self = this;
       
        //Load checkerboard and set 1 pixel to the left
        self.sprites["checkerboard"] = new PIXI.Sprite(self.textures["checkerboard"]);
        self.sprites["checkerboard"].position.x = -1;


        //Load pieces
        self.sprites["blackPieces"] = [];
        self.sprites["whitePieces"] = [];

        var numPieces = 12;

        for (var i = 0; i < numPieces; i++) {
            self.sprites["blackPieces"][i] = new PIXI.Sprite(self.textures["black"]);
            self.sprites["whitePieces"][i] = new PIXI.Sprite(self.textures["white"]);
        }
    }

}).call(this)
