/*
 This file drives the visualization of the battleship games on the TU CSE game server.
 To the best of my knowledge, Johnathan Geisler wrote the first version of this in the spring of 2016.
 My name is Andrew Blomenberg and I picked up the project in January of 2017.
 I do not know why this is wrapped in an anonymous function that calls itself, but it works, so
 */
(function ()
{
    "use strict";

    //these are simply the sizes needed to make sprites 60x60
    Replay.prototype.rendererWidth = 1380;
    Replay.prototype.rendererHeight = 720;

    //Time between rendered moves (in seconds)
    Replay.prototype.playIncrement = 0.5;

    //names of the sprites that appear as pegs on the board
    Replay.prototype.sprite_names = ["hit", "miss", "duplicate", "duplicate-hit"];

    //Holds information about each of the ships on the board. See init_ships for more detail
    Replay.prototype.ships={};

    //Array to store the frames of the water animation
    Replay.prototype.frames = [];

    //True if the legend is visible
    Replay.prototype.legend_shown = false;

    //True if the winner has been shown
    Replay.prototype.winner_shown = false;

    /*
     How I understand the structure of gamestate:
     The object usually has two properties which are the names of the players.
     Each player has properties for all the columns (1-10) and a "ships" property.
     Each column had properties for all the rows. The value of each row is the type of tile at that row and column.
     (see the translate function for more details on tile types)
     Each ships property has the same nested column and row properties, but the columns are associated with -1 or
     a number that represents a ship.
     This ship number is stored in two locations. In the outer layer, it can be replaced with an X if a hit is scored,
     but the inner layer ("ships") does not change and can be used to display kills
     */
    Replay.prototype.defaultGamestate = function ()
    {
        var self = this;

        var gamestate = {};
        for (var name in self.round.results)
        {
            gamestate[name] = [];
            gamestate[name]["ships"] = [];
            for (var col = 0; col < 10; col += 1)
            {
                gamestate[name][col] = [];
                gamestate[name]["ships"][col] = [];
                for (var row = 0; row < 10; row += 1)
                {
                    gamestate[name][col][row] = "~";
                    gamestate[name]["ships"][col][row] = -1;
                }
            }

            //each ship on a given board has an associated number 0-5
            //as the ships are placed, nextShip is incremented.
            gamestate[name].nextShip = 0;
        }

        return gamestate;
    };

    /*
     This function is part of the replay plugin API
     It is like a constructor for any data structures
     */
    Replay.prototype.initPlugin = function ()
    {
        this.init_ships();
    };

    /*
    Initialises the ships object
     */
    Replay.prototype.init_ships=function()
    {
        for (var board of [0,1])
        {
            this.ships[board]={};
            for (var shipNum=0; shipNum<6; shipNum++)
            {
                this.ships[board][shipNum]={};
                for(var sunk=0; sunk<2; sunk++)
                {
                    this.ships[board][shipNum][sunk] = {};
                    this.ships[board][shipNum][sunk].length = -1;
                    this.ships[board][shipNum][sunk].startLoc = [-1, -1]; //starting location
                    this.ships[board][shipNum][sunk].direction = 0; //1 is horizontal and 2 is vertical

                    //The ship must be moved into position once, but only once.
                    // This is set to true when the ship is moved
                    this.ships[board][shipNum][sunk].inPosition = false;

                    //This stores the name of the ship's sprite.
                    this.ships[board][shipNum][sunk].spriteName = "";
                }
            }
        }
    };

    /*
    Returns the opponent of the player passed as a parameter.
    For example, opponent("CleanPlayer") returns "DumbPlayer"
     */
    Replay.prototype.opponent = function (player)
    {
        var self = this;

        for (var name in self.round.results)
        {
            if (name !== player)
            {
                return name;
            }
        }

        return "";
    };

    /*
    Returns the board number(0 or 1) of a given player
    Whichever player is on the left is board number 0
     */
    Replay.prototype.board_from_player=function(player)
    {
        for (var name in this.round.results)
        {
            if (name===player)
                return 0;
            return 1;
        }

    };

    /*
    This accesses the ships board and replaces any of the given ship number with K+ the ship number
    This means that it is still possible to access which ship was where, but you will need to use .charAt()
     */
    Replay.prototype.killShip = function (board, shipNumber)
    {
        var self = this;

        for (var col = 0; col < 10; col += 1)
        {
            for (var row = 0; row < 10; row += 1)
            {
                if (board["ships"][col][row] === shipNumber)
                {
                    board[col][row] = "K"+shipNumber;
                }
            }
        }
    };

    /*
    This is a recursive function that generates a board object for the value of this.moveNumber.
    moveNumber 1 is the first move.
    It is recursive because it is necessary to know all prior moves to generate a given move.
     */
    Replay.prototype.generateGamestate = function ()
    {
        var self = this;

        //Move "0" is the default game board
        if (self.moveNumber === 0)
        {
            self.gamestate = self.copy(self.defaultGamestate());
            return;
        }

        var moveIndex = self.moveNumber - 1;
        var currentMove = self.round.moves[moveIndex];

        //Already calculated the gamestate, move on
        if ("gamestate" in currentMove)
        {
            self.gamestate = self.parseJSON(currentMove.gamestate);
        } else
        {
            self.moveNumber -= 1;
            self.generateGamestate();
            self.moveNumber += 1;
        }

        if (moveIndex <= 0)
        {
            self.gamestate = self.copy(self.defaultGamestate());
        } else
        {
            self.gamestate
                = self.copy(self.round.moves[moveIndex - 1].gamestate);
        }

        var moveData = self.parseJSON(currentMove["data"]);
        var player = moveData["player"];


        if (moveData["action"] === "place")
        {
            //boardNum is 0 or 1, board is an object
            var boardNum= self.board_from_player(self.opponent(player));
            var board = self.gamestate[self.opponent(player)];

            //this ship has just been placed and is not sunk, so I am using [0]
            self.ships[boardNum][board.nextShip][0].length=moveData.length;
            self.ships[boardNum][board.nextShip][0].startLoc=
                [moveData.col,moveData.row]; // a two-element array
            self.ships[boardNum][board.nextShip][0].direction=moveData.direction;

            if (moveData.length == 3)
                self.ships[boardNum][board.nextShip][0].spriteName = "cruiser";
            else if (moveData.length == 4)
                self.ships[boardNum][board.nextShip][0].spriteName = "battleship";
            else
                self.ships[boardNum][board.nextShip][0].spriteName = "carrier";

            if (moveData["direction"] === 1)
            {
                for (var c = moveData["col"];
                     c < moveData["col"] + moveData["length"];
                     c += 1)
                {
                    board[c][moveData["row"]] = board.nextShip;
                    board["ships"][c][moveData["row"]] = board.nextShip;
                }
            } else if (moveData["direction"] === 2)
            {
                for (var r = moveData["row"];
                     r < moveData["row"] + moveData["length"];
                     r += 1)
                {
                    board[moveData["col"]][r] = board.nextShip;
                    board["ships"][moveData["col"]][r] = board.nextShip;
                }
            } else
            {
                // unknown direction
            }

            board.nextShip += 1;
        } else if (moveData["action"] === "shot")
        {

            var board = self.gamestate[player];
            if (moveData["result"] === "K")
            {
                //if there is a kill, another ship is created with the sunk version of the sprite
                var boardNum= self.board_from_player(player);
                var shipNum=board[moveData["col"]][moveData["row"]];

                this.ships[boardNum][shipNum][1].length = this.ships[boardNum][shipNum][0].length;
                this.ships[boardNum][shipNum][1].startLoc = this.ships[boardNum][shipNum][0].startLoc;
                this.ships[boardNum][shipNum][1].direction = this.ships[boardNum][shipNum][0].direction;
                this.ships[boardNum][shipNum][1].inPosition = false;
                this.ships[boardNum][shipNum][1].spriteName = this.ships[boardNum][shipNum][0].spriteName+"-sunk";

                self.killShip(board,shipNum);
            } else
            {
                //This handles hits and misses
                board[moveData["col"]][moveData["row"]] = moveData["result"];
            }
        } else
        {
            // unknown move type
        }

        currentMove["gamestate"] = self.copy(self.gamestate);
    };
    /*
    This uses the legend sprites to display al legend in the top left
    */
    Replay.prototype.show_legend=function()
    {
        if (this.legend_shown)
            return;
        this.legend_shown=true;

        //These positions are not sacred or anything. I just found some stuff that worked.
        this.sprites["hit"].legend.sprite.position.set(0,0);
        this.sprites["hit"].legend.sprite.visible=true;
        this.sprites["hit"].legend.label.position.set(60,15);
        this.sprites["hit"].legend.label.visible=true;

        this.sprites["miss"].legend.sprite.position.set(130,0);
        this.sprites["miss"].legend.sprite.visible=true;
        this.sprites["miss"].legend.label.position.set(190,15);
        this.sprites["miss"].legend.label.visible=true;

        this.sprites["duplicate"].legend.sprite.position.set(280,0);
        this.sprites["duplicate"].legend.sprite.visible=true;
        this.sprites["duplicate"].legend.label.position.set(340,15);
        this.sprites["duplicate"].legend.label.visible=true;

        this.sprites["duplicate-hit"].legend.sprite.position.set(550,0);
        this.sprites["duplicate-hit"].legend.sprite.visible=true;
        this.sprites["duplicate-hit"].legend.label.position.set(610,15);
        this.sprites["duplicate-hit"].legend.label.visible=true;
    };
    /*
    This function is part of the Replay API
    It is responsible for showing and moving all the sprites
    I cheated a bit because the two grids and water animations are not shown in this function.
     */
    Replay.prototype.render = function ()
    {
        var self = this;
        var wasHit=false;

        self.show_legend();

        //I am assuming that at the end of the match there is a winner and showing it in that case
        if(self.round.moves.length==self.moveNumber)
            self.show_winner();
        else
            self.hide_winner();

        var boardNum = 0; //this is incremented after the first iteration of the outer loop
        for (var board in self.gamestate)
        {
            for (var col = 0; col < 10; col += 1)
            {
                for (var row = 0; row < 10; row += 1)
                {
                    //this is used to display a duplicate-hit sprite instead of treating all duplicates the same
                    wasHit=self.sprites["hit"][boardNum][col][row].visible ||
                           self.sprites["duplicate-hit"][boardNum][col][row].visible;

                    for (var name of self.sprite_names)
                    {
                        self.sprites[name][boardNum][col][row].visible = false;
                        this.hide_any_ship(boardNum,col,row);
                    }

                    //spriteName holds the standard english representation of a tile like 'X'
                    var spriteName = self.translate(self.gamestate[board][col][row]);

                    if (spriteName == "ship")
                        this.display_ship(boardNum, self.gamestate[board][col][row], 0); //display a non-sunk ship
                    else if (spriteName != "water")
                    {
                        if(spriteName=="kill")
                        {
                            var shipNum=parseInt((self.gamestate[board][col][row]).charAt(1));
                            this.display_ship(boardNum, shipNum, 1); //display a sunk ship
                            spriteName="hit"; //also display a hit
                        }

                        //Hits and kills are both shown with the same sprite
                        if (spriteName == "kill")
                            spriteName = "hit";

                        if(spriteName=="duplicate"&&wasHit)
                            spriteName="duplicate-hit";

                        self.sprites[spriteName][boardNum][col][row].visible = true;
                    }
                }
            }

            boardNum += 1;
        }
    };

    /*
    This is part of the Replay API.
    This is called around the time that the page loads.
    It uses self.addTexture to add all the sprite textures into the textures object.
     */
    Replay.prototype.loadTextures = function ()
    {
        var self = this;

        for (var name of self.sprite_names)
        {
            var pic = name + ".png";
            self.addTexture(name, pic);
        }

        self.addTexture("cruiser", "cruiser.png");
        self.addTexture("battleship", "battleship.png");
        self.addTexture("carrier", "carrier.png");
        self.addTexture("cruiser-sunk", "cruiser-sunk.png");
        self.addTexture("battleship-sunk", "battleship-sunk.png");
        self.addTexture("carrier-sunk", "carrier-sunk.png");

        self.addTexture("grid", "grid.png");

        //loads all the frames of the water animation with addTextures
        for (var i = 1; i < 30; i++)
        {
            var fileName = "water_frame" + i + ".png";
            self.addTexture(fileName, fileName);
            this.frames.push(self.textures[fileName]);
        }
    };

    /*
     Simple helper to set the position of a sprite given an abstracted row and column
     */
    Replay.prototype.setPosition = function (sprite, board, col, row)
    {
        sprite.position.x = 60 + board * 660 + col * 60;
        sprite.position.y = 60 + row * 60;
    };

    /*
     Places a sprite of type name and on every grid location on each board
     It loads each sprite from this.textures which is provided by the file that calls this file.
     */
    Replay.prototype.create_tile_sprites = function (name)
    {
        var self = this;


        self.sprites[name] = [];
        for (var board = 0; board < 2; board += 1)
        {
            self.sprites[name][board] = [];

            for (var col = 0; col < 10; col += 1)
            {
                self.sprites[name][board][col] = [];

                for (var row = 0; row < 10; row += 1)
                {
                    self.sprites[name][board][col][row]
                        = new PIXI.Sprite(self.textures[name], name);
                    self.sprites[name][board][col][row].visible = false;
                    self.setPosition(self.sprites[name][board][col][row],
                        board, col, row);
                }
            }
        }
    };
    /*
    Places six of each kind of ship on each board and makes them invisible
    This does not position the ships like create_tile_sprites does
     */
    Replay.prototype.create_ship_sprites=function()
    {
        for (var shipName of
            ["cruiser", "battleship", "carrier","cruiser-sunk", "battleship-sunk", "carrier-sunk"])
        {
            this.sprites[shipName]={};
            for (var board of [0,1])
            {
                this.sprites[shipName][board]={};
                for(var shipNum=0; shipNum<6; shipNum++)
                {
                    var sprite = new PIXI.Sprite(this.textures[shipName]);
                    sprite.visible=false;

                    this.sprites[shipName][board][shipNum] = sprite;
                }
            }
        }
    };
    /*
    Creates a sprite of the specified name and a label to go along with it.
    This also does not set the positions
     */
    Replay.prototype.create_legend_sprites=function(name)
    {
        var labelText="";
        if(name=="hit")
            labelText="Hit";
        else if(name== "miss")
            labelText="Miss";
        else if (name=="duplicate")
            labelText="Duplicate Miss";
        else if (name=="duplicate-hit")
            labelText="Duplicate Hit";

        var sprite = new PIXI.Sprite(this.textures[name]);
        sprite.visible=false;
        this.sprites[name].legend={};
        this.sprites[name].legend.sprite = sprite;
        this.sprites[name].legend.label =
            new PIXI.Text(labelText,{fontFamily: "Arial", fontSize: 18, fill: "white"});
    };

    /*
    Creates the sprites to display the winner at the end of the game
     */
    Replay.prototype.create_winner_sprites=function()
    {
        var font={fontFamily: "Arial", fontSize: 18, fill: "white", stroke:"black", strokeThickness:4};

        this.sprites["winMsg"]=new PIXI.Text("",font);
        this.sprites["shotsMade"]=new PIXI.Text("",font);

        this.sprites["winMsg"].anchor.x=0.5;
        this.sprites["shotsMade"].anchor.x=0.5;


        this.sprites["winMsg"].scale.set(2.6,2.6);
        this.sprites["shotsMade"].scale.set(1.2,1.2);


        this.sprites["winMsg"].position.set(690,120);
        this.sprites["shotsMade"].position.set(690,270);


        this.sprites["winMsg"].visible = false;
        this.sprites["shotsMade"].visible = false;

    };

    /*
     This function is part of the replay plugin API. It is called around the time that the page loads.
     The idea is to add all the sprites to the stage before doing anything with them
     */
    Replay.prototype.loadSprites = function ()
    {
        var self = this;

        this.create_ship_sprites();
        for (var name of self.sprite_names)
        {
            self.create_tile_sprites(name);
            self.create_legend_sprites(name);
        }

        this.sprites["grid"]={};
        this.sprites["grid"][0]=new PIXI.Sprite(this.textures["grid"]);
        this.sprites["grid"][1]=new PIXI.Sprite(this.textures["grid"]);

        this.sprites["grid"][0].scale.set(2,2);
        this.sprites["grid"][1].scale.set(2,2);

        this.sprites["grid"][0].position.set(60,60);
        this.sprites["grid"][1].position.set(720,60);

        this.create_winner_sprites();

        var movieR = new PIXI.extras.MovieClip(this.frames);
        var movieL = new PIXI.extras.MovieClip(this.frames);

        //puts them in the background of each board
        movieR.position.set(720, 60);
        movieL.position.set(60, 60);

        //may remove these when I make bigger frames but for now they are half-sized
        movieR.scale.set(2.4, 2.4);
        movieL.scale.set(2.4, 2.4);

        //60fps is just unnecessary
        movieR.animationSpeed = 0.25;
        movieL.animationSpeed = 0.25;
        movieR.play();
        movieL.play();

        this.stage.addChild(movieR);
        this.stage.addChild(movieL);
    };

    /*
    Displays the specified ship on the specified board
    Each ship is represented by numbers 0-5.
    Information about them is stored in this.ships
     */
    Replay.prototype.display_ship=function (board,shipNum,sunk)
    {
        var shipData=this.ships[board][shipNum][sunk];
        var shipSprite=this.sprites[shipData.spriteName][board][shipNum];

        if(shipData.inPosition)
        {
            shipSprite.visible=true;
            return;
        }

        //all of the sprites are vertical, so they need to be rotated if the direction is horizontal
        if(shipData.direction==1)
        {
            shipSprite.pivot.set(30,30);
            shipSprite.rotation=-1.5708;
            shipSprite.pivot.set(60,0);
        }

        this.setPosition(shipSprite,board,shipData.startLoc[0],shipData.startLoc[1]);

        shipData.inPosition=true;
        shipSprite.visible=true;
    };

    /*
     Displays the match winner and a few statistics.
     */
    Replay.prototype.show_winner=function()
    {
        var shotsMade=this.round.moves.length;
        shotsMade-=10;
        shotsMade/=2;

        this.winner_shown=true;

        var winner="";
        for(var playerName in this.round.results)
        {
            if (this.round.results[playerName].result=="Win")
                winner=playerName;
        }

        this.sprites["winMsg"].text=winner+" Wins!";
        this.sprites["shotsMade"].text= "Shots made: "+shotsMade;

        this.sprites["winMsg"].visible=true;
        this.sprites["shotsMade"].visible=true;
    };

    /*
     hides the winner and statistics text
     */
    Replay.prototype.hide_winner=function()
    {
        if(this.winner_shown)
        {
            this.sprites["winMsg"].visible = false;
            this.sprites["shotsMade"].visible = false;
        }
    };

    /*
    Hides a ship if it exists on the given coordinates
     */
    Replay.prototype.hide_any_ship=function (board,col,row)
    {

        for (var shipNum = 0; shipNum < 6; shipNum++)
        {
            for(var sunk=0; sunk<2; sunk++)
            {
                if (this.ships[board][shipNum][sunk].startLoc[0] == col &&
                    this.ships[board][shipNum][sunk].startLoc[1] == row)
                {
                    var shipName = this.ships[board][shipNum][sunk].spriteName;
                    this.sprites[shipName][board][shipNum].visible = false;
                }
            }
        }
    };
    
    /*
    Helper to translate between English names and the symbols used in gameState
     */
    Replay.prototype.translate = function (name)
    {
        if (name == "X")
            return "hit";
        if (name == "*")
            return "miss";
        if (name == "!")
            return "duplicate";
        if (name == "!X")
            return "duplicate-hit";
        if (name == "~")
            return "water";
        if (name<6&&name>=0)
            return "ship";
        if (name.charAt(0)=="K")
            return "kill";
    }

}).call(this);
