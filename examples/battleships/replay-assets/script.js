(function() {
    "use strict";

    Replay.prototype.rendererWidth = 1150;
    Replay.prototype.rendererHeight = 600;

    //Time between rendered moves (in seconds)
    Replay.prototype.playIncrement = 0.5;

    Replay.prototype.defaultGamestate = function() {
	var self = this;

	var gamestate = {};
	for (var name in self.round.results) {
	    gamestate[name] = [];
	    gamestate[name]["ships"] = [];
	    for (var col = 0; col < 10; col += 1) {
		gamestate[name][col] = [];
		gamestate[name]["ships"][col] = [];
		for (var row = 0; row < 10; row += 1) {
		    gamestate[name][col][row] = "~";
		    gamestate[name]["ships"][col][row] = -1;
		}
	    }

	    gamestate[name].nextShip = 0;
	}

	return gamestate;
    }

    Replay.prototype.initPlugin = function() {
    }

    Replay.prototype.opponent = function(player) {
	var self = this;

	for (var name in self.round.results) {
	    if (name !== player) {
		return name;
	    }
	}

	return "";
    }

    Replay.prototype.killShip = function(board, shipNumber) {
	var self = this;

	for (var col = 0; col < 10; col += 1) {
	    for (var row = 0; row < 10; row += 1) {
		if (board["ships"][col][row] === shipNumber) {
		    board[col][row] = "K";
		}
	    }
	}
    }

    Replay.prototype.generateGamestate = function() {
	var self = this;

	//Move "0" is the default game board
	if (self.moveNumber === 0) {
	    self.gamestate = self.copy(self.defaultGamestate());
	    return;
	}

	var moveIndex = self.moveNumber - 1;
	var currentMove = self.round.moves[moveIndex];

	//Already calculated the gamestate, move on
	if ("gamestate" in currentMove) {
	    self.gamestate = self.parseJSON(currentMove.gamestate);
	} else {
	    self.moveNumber -= 1;
	    self.generateGamestate();
	    self.moveNumber += 1;
	}

	if (moveIndex <= 0) {
	    self.gamestate = self.copy(self.defaultGamestate());
	} else {
	    self.gamestate
		= self.copy(self.round.moves[moveIndex - 1].gamestate);
	}

	var moveData = self.parseJSON(currentMove["data"]);
	var player = moveData["player"];

	if (moveData["action"] === "place") {
	    var board = self.gamestate[self.opponent(player)];
	    if (moveData["direction"] === 1) {
		for (var c = moveData["col"];
		     c < moveData["col"] + moveData["length"];
		     c += 1)
		{
		    board[c][moveData["row"]] = board.nextShip;
		    board["ships"][c][moveData["row"]] = board.nextShip;
		}
	    } else if (moveData["direction"] === 2) {
		for (var r = moveData["row"];
		     r < moveData["row"] + moveData["length"];
		     r += 1)
		{
		    board[moveData["col"]][r] = board.nextShip;
		    board["ships"][moveData["col"]][r] = board.nextShip;
		}
	    } else {
		// unknown direction
	    }

	    board.nextShip += 1;
	} else if (moveData["action"] === "shot") {
	    var board = self.gamestate[player];
	    if (moveData["result"] === "K") {
		self.killShip(board, board[moveData["col"]][moveData["row"]]);
	    } else {
		board[moveData["col"]][moveData["row"]] = moveData["result"];
	    }
	} else {
	    // unknown move type
	}

	currentMove["gamestate"] = self.copy(self.gamestate);
    }

    Replay.prototype.pic_names = ["~", "ship", "X", "*", "K", "!"];

    Replay.prototype.render = function() {
	var self = this;

	var boardNum = 0;
	for (var board in self.gamestate) {
	    for (var col = 0; col < 10; col += 1) {
		for (var row = 0; row < 10; row += 1) {
		    for (var name of self.pic_names) {
			self.sprites[name][boardNum][col][row].visible = false;
		    }

		    var sprite = self.gamestate[board][col][row];

		    if (sprite >= 0) {
			self.sprites["ship"][boardNum][col][row].visible = true;
		    } else {
			self.sprites[sprite][boardNum][col][row].visible = true;
		    }
		}
	    }

	    boardNum += 1;
	}
    }

    Replay.prototype.loadTextures = function() {
	var self = this;

	for (var name of self.pic_names) {
	    var pic = name + ".png";
	    self.addTexture(name, pic);
	}
    }

    Replay.prototype.setPosition = function(sprite, board, col, row) {
	sprite.position.x = 50 + board * 550 + col * 50;
	sprite.position.y = 50 + row * 50;
    }

    Replay.prototype.create_sprites = function(name, vis) {
	var self = this;

	self.sprites[name] = [];
	for (var board = 0; board < 2; board += 1) {
	    self.sprites[name][board] = [];

	    for (var col = 0; col < 10; col += 1) {
		self.sprites[name][board][col] = [];

		for (var row = 0; row < 10; row += 1) {
		    self.sprites[name][board][col][row]
			= new PIXI.Sprite(self.textures[name]);
		    self.sprites[name][board][col][row].visible = vis;
		    self.setPosition(self.sprites[name][board][col][row],
				     board, col, row);
		}
	    }
	}
    }

    Replay.prototype.loadSprites = function() {
	var self = this;

	for (var name of self.pic_names) {
	    self.create_sprites(name, name === "~");
	}
    }

}).call(this)
