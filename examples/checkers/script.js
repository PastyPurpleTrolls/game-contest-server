(function() {
    "use strict";

    Replay.prototype.rendererWidth = 722;
    Replay.prototype.rendererHeight = 728;

    Replay.prototype.pieces = {
        "red": [3, 4],
        "black": [1, 2],
        3: "red",
        4: "redKing",
        1: "black",
        2: "blackKing"
    };

    
    Replay.prototype.initPlugin = function() {
        var self = this;

        self.boardPositions = self.generateBoardPositions(8, 90, 91);
    }

    Replay.prototype.generateBoardPositions = function(rows, incrementX, incrementY) {
        var self = this;
                
        var positions = [];

        var row, col;
        for (var i = 0; i < rows; i++) {
            row = [];
            
            for (var y = 0; y < rows; y++) {
                col = [y*incrementX, i*incrementY];
                row.push(col);
            }

            positions.push(row);
        }        

        return positions;
    }

    Replay.prototype.defaultGameState = [
        [0, 1, 0, 1, 0, 1, 0, 1], 
        [1, 0, 1, 0, 1, 0, 1, 0], 
        [0, 1, 0, 1, 0, 1, 0, 1], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [3, 0, 3, 0, 3, 0, 3, 0], 
        [0, 3, 0, 3, 0, 3, 0, 3], 
        [3, 0, 3, 0, 3, 0, 3, 0]
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
 
        //Reset the gamestate
        self.gamestate = [];
 
        //Already calculated the gamestate, move on
        if ("gamestate" in self.currentMove) {
            self.gamestate = self.parseJSON(self.currentMove.gamestate);
        } else {
            //Get the colors associated with the names of each player in this game
            var colors = self.parseJSON(self.round.info);

            //Search for delta at least 10 moves from the current one
            var deltaStep = 10;
            
            //Store delta move and index
            var deltaMove = {};
            var deltaIndex = self.currentMoveIndex;

            //Step backward through moves to find the most recent defined deltastep
            for (deltaIndex = self.currentMoveIndex; deltaIndex > self.currentMoveIndex - deltaStep && deltaIndex > 0; deltaIndex--) {
              deltaMove = self.round.moves[deltaIndex];
              if ("gamestate" in deltaMove) {
                  self.gamestate =  self.copy(self.parseJSON(deltaMove["gamestate"]));
                  break;
              }
            }
            
            //default gamestate if we didn't find a delta gamestate
            if (self.gamestate.length === 0) {
                self.gamestate = self.copy(self.defaultGameState);
            } else {
                //Don't recalculate the gamestate
                deltaIndex += 1;
            }

            var move, moveData, currentPlayerColor, moveString, moveSpots,
                fromRow, fromCol, toRow, toCol, playerPiece, kingRow;
            //Move forward and generate the gamestates for each move along the way
            for (var i = deltaIndex; i <= self.currentMoveIndex; i++) {
                move = self.round.moves[i];
                moveData = self.parseJSON(move["data"]);
                
                currentPlayerColor = colors[moveData[0]];
                
                //Create move spots array by splitting on ":"
                moveSpots = moveData[1].split(":");

                //Loop through each move made by the player in this turn and set the board accordingly
                for (var j = 0; j < moveSpots.length - 1; j++) {
                    fromRow = self.rowMap[moveSpots[j][0]];
                    fromCol = parseInt(moveSpots[j][1]);

                    //Go forward one element in the array to find where the player moved to
                    toRow = self.rowMap[moveSpots[j + 1][0]];
                    toCol = parseInt(moveSpots[j + 1][1]);

                    playerPiece = self.gamestate[fromRow][fromCol];
                    
                    //Calculate king conversion (whether the player became a king on this turn)
                    kingRow = (currentPlayerColor === "black") ? 0 : 7;
                    if (toRow === kingRow) {
                        playerPiece = self.pieces[currentPlayerColor][1];
                    }
                    
                    //Reset old spot and move to new spot
                    self.gamestate[fromRow][fromCol] = 0;
                    self.gamestate[toRow][toCol] = playerPiece;
                }
 
                //Copy gamestate to move to allow for caching
                move["gamestate"] = self.copy(self.gamestate);
            }
        }
    }

    Replay.prototype.render = function() {
        var self = this;

        var numPieces = 12;
        var numBlackPieces = 0;
        var numRedPieces = 0;

        var rowI, row, colI, col, pieceType, sprite, position;
        for (rowI = 0; rowI < self.gamestate.length; rowI++) {
            row = self.gamestate[rowI];
            //loop through columns
            for (colI = 0; colI < row.length; colI++) {
                col = row[colI];

                //Don't do anything with empty spots
                if (col === 0) continue;

                pieceType = self.pieces[col];
                
                //Detect piece color
                if (pieceType === "black" || pieceType === "blackKing") {
                    sprite = self.sprites["blackPieces"][numBlackPieces];
                    numBlackPieces += 1;
                } else {
                    sprite = self.sprites["redPieces"][numRedPieces];
                    numRedPieces += 1;
                }
 
                sprite.visible = true;
            
                //Set texture of sprite to match piece type
                sprite.texture = self.textures[pieceType];

                position = self.boardPositions[rowI][colI];

                sprite.position.x = position[0];
                sprite.position.y = position[1];
            }
        }

        //Hide pieces that aren't being used anymore
        for (var i = numBlackPieces; i < numPieces; i++) {
            self.sprites["blackPieces"][i].visible = false;
        }
        for (var i = numRedPieces; i < numPieces; i++) {
            self.sprites["redPieces"][i].visible = false;
        }
    }

    Replay.prototype.loadTextures = function() {
        var self = this;

        self.addTexture("checkerboard", "checkerboard.png");
        self.addTexture("red", "white.png");
        self.addTexture("black", "black.png");
        self.addTexture("redKing", "whiteKing.png");
        self.addTexture("blackKing", "blackKing.png");
    }

    Replay.prototype.loadSprites = function() {
        var self = this;

        //Load checkerboard and set 1 pixel to the left
        self.sprites["checkerboard"] = new PIXI.Sprite(self.textures["checkerboard"]);
        self.sprites["checkerboard"].position.x = -1;


        //Load pieces
        self.sprites["blackPieces"] = [];
        self.sprites["redPieces"] = [];

        var numPieces = 12;

        for (var i = 0; i < numPieces; i++) {
            self.sprites["blackPieces"][i] = new PIXI.Sprite(self.textures["black"]);
            self.sprites["redPieces"][i] = new PIXI.Sprite(self.textures["red"]);
        }
    }

}).call(this)
