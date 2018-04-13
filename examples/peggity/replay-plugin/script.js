(function ()
{
    "use strict";

    Replay.prototype.boardSize = 16;
    Replay.prototype.rendererWidth = 1080;
    Replay.prototype.rendererHeight = 1080;
    Replay.prototype.playIncrement = 1;


    Replay.prototype.initPlugin = function ()
    {
        this.board = [];
        for (var row = 0; row < this.boardSize; row++) {
            this.board.push([]);
            for (var col = 0; col < this.boardSize; col++) {
                this.board[row].push(0);
            }
        }
    };

//---------------------------------------------------------------------------//

    Replay.prototype.loadTextures = function ()
    {
        this.addTexture("empty", "empty.png");
        this.addTexture("p1", "p1.png");
        this.addTexture("p1winner", "p1winner.png");
        this.addTexture("p2", "p2.png");
        this.addTexture("p2winner", "p2winner.png");
    };

//---------------------------------------------------------------------------//

    Replay.prototype.loadSprites = function ()
    {
        for (var row = 0; row < this.boardSize; row++) {
            this.sprites[row] = {};
            for (var col = 0; col < this.boardSize; col++) {
                this.sprites[row][col] = {};
                this.sprites[row][col]["empty"] = new PIXI.Sprite(this.textures["empty"]);
                this.sprites[row][col]["p1"] = new PIXI.Sprite(this.textures["p1"]);
                this.sprites[row][col]["p1winner"] = new PIXI.Sprite(this.textures["p1winner"]);
                this.sprites[row][col]["p2"] = new PIXI.Sprite(this.textures["p2"]);
                this.sprites[row][col]["p2winner"] = new PIXI.Sprite(this.textures["p2winner"]);
                this.sprites[row][col]["empty"].visible = false;
                this.sprites[row][col]["p1"].visible = false;
                this.sprites[row][col]["p1winner"].visible = false;
                this.sprites[row][col]["p2"].visible = false;
                this.sprites[row][col]["p2winner"].visible = false;
            }
        }
    };

//---------------------------------------------------------------------------//

    Replay.prototype.generateGamestate = function ()
    {
        this.clearBoard();
        for (var i = 0; i < this.moveNumber; i++) {
            var playerNum = (i % 2) + 1;
            var data = this.round["moves"][i]["data"];
            var parts = data.split(",");
            var row = parseInt(parts[1]);
            var col = parseInt(parts[2]);
            if (row < this.boardSize && col < this.boardSize) {
                this.board[row][col] = playerNum;
            }
        }

        if (this.moveNumber == this.round["moves"].length) {
            this.checkWin();
        }
    };

    Replay.prototype.clearBoard = function()
    {
        for (var row = 0; row < this.boardSize; row++) {
            for (var col = 0; col < this.boardSize; col++) {
                this.board[row][col] = 0;
            }
        }
    };

    Replay.prototype.checkWin = function()
    {
        for (var row = 0; row < this.boardSize; row++) {
            for (var col = 0; col < this.boardSize; col++) {
                this.checkHorizontalWin(row, col);
                this.checkVerticalWin(row, col);
                this.checkLeftToRightDiagonal(row, col);
                this.checkRightToLeftDiagonal(row, col);
            }
        }
    };

    Replay.prototype.checkHorizontalWin = function(row, col)
    {
        if (col < this.boardSize-4) {
            var i;
            var potentialWinSet = [];
            for (i = col; i < col+5; i++) {
                potentialWinSet.push(this.board[row][i]);
            }
            if (this.checkWinForSet(potentialWinSet)) {
                for (i = col; i < col+5; i++) {
                    this.board[row][i] += 2;
                }
            }
        }
    };

    Replay.prototype.checkVerticalWin = function(row, col)
    {
        if (row < this.boardSize-4) {
            var potentialWinSet = [];
            for (var i = row; i < row+5; i++) {
                potentialWinSet.push(this.board[i][col]);
            }
            if (this.checkWinForSet(potentialWinSet)) {
                for (i = row; i < row+5; i++) {
                    this.board[i][col] += 2;
                }
            }
        }
    };

    Replay.prototype.checkLeftToRightDiagonal = function(row, col)
    {
        if (row < this.boardSize-4 && col < this.boardSize-4) {
            var potentialWinSet = [];
            for (var i = 0; i < 5; i++) {
                potentialWinSet.push(this.board[row+i][col+i]);
            }
            if (this.checkWinForSet(potentialWinSet)) {
                for (i = 0; i < 5; i++) {
                    this.board[row+i][col+i] += 2;
                }
            }
        }
    };

    Replay.prototype.checkRightToLeftDiagonal = function(row, col)
    {
        if (row < this.boardSize-4 && col >= 4) {
            var potentialWinSet = [];
            for (var i = 0; i < 5; i++) {
                potentialWinSet.push(this.board[row+i][col-i]);
            }
            if (this.checkWinForSet(potentialWinSet)) {
                for (i = 0; i < 5; i++) {
                    this.board[row+i][col-i] += 2;
                }
            }
        }
    };

    Replay.prototype.checkWinForSet = function(setOfFive)
    {
        var firstPiece = setOfFive[0];
        if (firstPiece == 0) {
            return false;
        } else {
            var count = 0;
            for (var i = 0; i < 5; i++) {
                if (setOfFive[i] == firstPiece) {
                    count++;
                }
            }
            return count == 5;
        }
    };

//---------------------------------------------------------------------------//

    Replay.prototype.render = function ()
    {
        for (var row = 0; row < this.boardSize; row++) {
            for (var col = 0; col < this.boardSize; col++) {
                var x = (col + 1) * 60;
                var y = (row + 1) * 60;
                switch (this.board[row][col]) {
                    case 1:
                        this.drawP1(row, col, x, y);
                        break;
                    case 2:
                        this.drawP2(row, col, x, y);
                        break;
                    case 3:
                        this.drawP1Winner(row, col, x, y);
                        break;
                    case 4:
                        this.drawP2Winner(row, col, x, y);
                        break;
                    default:
                        this.drawEmpty(row, col, x, y);
                        break;
                }
            }
        }
    };

    Replay.prototype.drawP1 = function(row, col, x, y)
    {
        this.sprites[row][col]["p1"].position.x = x;
        this.sprites[row][col]["p1"].position.y = y;
        this.sprites[row][col]["p1"].visible = true;
        this.sprites[row][col]["p1winner"].visible = false;
        this.sprites[row][col]["p2"].visible = false;
        this.sprites[row][col]["p2winner"].visible = false;
        this.sprites[row][col]["empty"].visible = false;
    };

    Replay.prototype.drawP1Winner = function(row, col, x, y)
    {
        this.sprites[row][col]["p1winner"].position.x = x;
        this.sprites[row][col]["p1winner"].position.y = y;
        this.sprites[row][col]["p1"].visible = false;
        this.sprites[row][col]["p1winner"].visible = true;
        this.sprites[row][col]["p2"].visible = false;
        this.sprites[row][col]["p2winner"].visible = false;
        this.sprites[row][col]["empty"].visible = false;
    };

    Replay.prototype.drawP2 = function(row, col, x, y)
    {
        this.sprites[row][col]["p2"].position.x = x;
        this.sprites[row][col]["p2"].position.y = y;
        this.sprites[row][col]["p1"].visible = false;
        this.sprites[row][col]["p1winner"].visible = false;
        this.sprites[row][col]["p2"].visible = true;
        this.sprites[row][col]["p2winner"].visible = false;
        this.sprites[row][col]["empty"].visible = false;
    };

    Replay.prototype.drawP2Winner = function(row, col, x, y)
    {
        this.sprites[row][col]["p2winner"].position.x = x;
        this.sprites[row][col]["p2winner"].position.y = y;
        this.sprites[row][col]["p1"].visible = false;
        this.sprites[row][col]["p1winner"].visible = false;
        this.sprites[row][col]["p2"].visible = false;
        this.sprites[row][col]["p2winner"].visible = true;
        this.sprites[row][col]["empty"].visible = false;
    };

    Replay.prototype.drawEmpty = function(row, col, x, y)
    {
        this.sprites[row][col]["empty"].position.x = x;
        this.sprites[row][col]["empty"].position.y = y;
        this.sprites[row][col]["p1"].visible = false;
        this.sprites[row][col]["p1winner"].visible = false;
        this.sprites[row][col]["p2"].visible = false;
        this.sprites[row][col]["p2winner"].visible = false;
        this.sprites[row][col]["empty"].visible = true;
    }

}).call(this);
