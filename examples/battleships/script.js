(function() {
    "use strict";

    Replay.prototype.rendererWidth = 1150;
    Replay.prototype.rendererHeight = 600;

    //Time between rendered moves (in seconds)
    Replay.prototype.playIncrement = 0.5;

    Replay.prototype.defaultGamestate = function() {
	var gamestate = {};
	for (var name of self.round.results.keys()) {
	    gamestate[name] = [];
	    for (var col = 0; col < 10; col += 1) {
		gamestate[name][col] = [];
		for (var row = 0; row < 10; row += 1) {
		    gamestate[name][col][row] = "~";
		}
	    }
	}

	return gamestate;
    }

    Replay.prototype.initPlugin = function() {
    }

    Replay.prototype.opponent = function(player) {
	for (var name of self.round.results.keys()) {
	    if (name !== player) {
		return name;
	    }
	}

	return "";
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
	    generateGamestate();
	    self.moveNumber += 1;
	}

	self.gamestate = self.copy(self.round.moves[moveIndex - 1]);
	var moveData = self.parseJSON(currentMove["data"]);
	var player = moveData["player"];

	if (moveData["action"] === "place") {
	    var board = self.gamestate[opponent(player)];
	    if (moveData["dir"] === 1) {
		for (var c = moveData["col"];
		     c < moveData["col"] + moveData["length"];
		     c += 1)
		{
		    board[c][moveData["row"]] = board.nextShip;
		}
	    } else if (moveData["dir"] === 2) {
		for (var r = moveData["row"];
		     r < moveData["row"] + moveData["length"];
		     r += 1)
		{
		    board[moveData["col"]][r] = board.nextShip;
		}
	    } else {
		// unknown direction
	    }

	    board.nextShip += 1;
	} else if (moveData["action"] === "shot") {
	    var board = self.gamestate[player];
	    board[moveData["col"]][moveData["row"]] = moveData["result"];
	} else {
	    // unknown move type
	}

	currentMove["gamestate"] = self.copy(self.gamestate);
    }

    Replay.prototype.render = function() {
	var self = this;

	var boardNum = 0;
	for (var board of self.moves.results.keys()) {
	    for (var col = 0; col < 10; col += 1) {
		for (var row = 0; row < 10; row += 1) {
		    switch (self.gamestate[board][col][row]) {
		      case "~":
			self.sprites["waters"][boardNum][col][row].visible = true;
			break;

		      case "X":
			self.sprites["hits"][boardNum][col][row].visible = true;
			break;

		      case "*":
			self.sprites["misses"][boardNum][col][row].visible = true;
			break;

		      case "K":
			self.sprites["kills"][boardNum][col][row].visible = true;
			break;

		      case "!":
			self.sprites["dups"][boardNum][col][row].visible = true;
			break;

		      default:
			self.sprites["ships"][boardNum][col][row].visible = true;
			break;
		    }
		}
	    }

	    boardNum += 1;
	}
    }

    Replay.prototype.loadTextures = function() {
	var self = this;

	self.addTexture("board", "board.png");
	self.addTexture("water", "water.png");
	self.addTexture("ship", "ship.png");
	self.addTexture("hit", "hit.png");
	self.addTexture("miss", "miss.png");
	self.addTexture("kill", "kill.png");
	self.addTexture("dup", "dup.png");
    }

    Replay.prototype.setPosition = function(sprite, board, col, row) {
	sprite.position.x = 50 + board * 550 + col * 50;
	sprite.position.y = 50 + row * 50;
    }

    Replay.prototype.loadSprites = function() {
	var self = this;

	self.sprites["boards"][0] = new PIXI.Sprite(self.textures["board"]);
	self.sprites["boards"][1] = new PIXI.Sprite(self.textures["board"]);

	for (var board = 0; board < 2; board += 1) {
	    for (var col = 0; col < 10; col += 1) {
		for (var row = 0; row < 10; row += 1) {
		    self.sprites["waters"][board][col][row]
			= new PIXI.Sprite(self.textures["water"]);
		    self.sprites["waters"][board][col][row].visible = true;
		    setPosition(self.sprites["waters"][board][col][row],
				board, col, row);

		    self.sprites["ships"][board][col][row]
			= new PIXI.Sprite(self.textures["ship"]);
		    self.sprites["ships"][board][col][row].visible = false;
		    setPosition(self.sprites["ships"][board][col][row],
				board, col, row);

		    self.sprites["hits"][board][col][row]
			= new PIXI.Sprite(self.textures["hit"]);
		    self.sprites["hits"][board][col][row].visible = false;
		    setPosition(self.sprites["hits"][board][col][row],
				board, col, row);

		    self.sprites["misses"][board][col][row]
			= new PIXI.Sprite(self.textures["miss"]);
		    self.sprites["misses"][board][col][row].visible = false;
		    setPosition(self.sprites["misses"][board][col][row],
				board, col, row);

		    self.sprites["kills"][board][col][row]
			= new PIXI.Sprite(self.textures["kill"]);
		    self.sprites["kills"][board][col][row].visible = false;
		    setPosition(self.sprites["kills"][board][col][row],
				board, col, row);

		    self.sprites["dups"][board][col][row]
			= new PIXI.Sprite(self.textures["dup"]);
		    self.sprites["dups"][board][col][row].visible = false;
		    setPosition(self.sprites["dups"][board][col][row],
				board, col, row);
		}
	    }
	}
    }

}).call(this)
