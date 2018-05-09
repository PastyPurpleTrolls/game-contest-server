// For help, see http://aires.cse.taylor.edu/help/writing_replay_plugin

(function ()
{
    "use strict";

    Replay.prototype.rendererWidth = 1080;
    Replay.prototype.rendererHeight = 1080;
    Replay.prototype.playIncrement = 1;


    /*
     * initPlugin()
     * Called immediately after initialization of the Replay object. This hook
     * should be used for any logic that needs to be precomputed.
     * Note: the round log will not be available when this function is called.
     */
    Replay.prototype.initPlugin = function ()
    {

    };


    /*
     * loadTextures()
     * Load any required textures into the PIXI context. Textures are added to
     * the "this.textures" object.
     */
    Replay.prototype.loadTextures = function ()
    {
        // this.addTexture("example", "example.png");
    };


    /*
     * loadSprites()
     * Load any PIXI sprites on initial load. New sprites should be defined on
     * "this.sprites" as a new key:value pair.
     */
    Replay.prototype.loadSprites = function ()
    {
        // this.sprites["example"] = new PIXI.Sprite(this.textures["example"]);
    };


    /*
     * generateGamestate()
     * Called whenever a new move is loaded. Any logic that is required in
     * order to generate a gamestate should be executed in this method.
     */
    Replay.prototype.generateGamestate = function ()
    {

    };


    /*
     * render()
     * Renders the current move gamestate to the WebGL context. Called
     * immediately after "this.generateGamestate()".
     */
    Replay.prototype.render = function ()
    {

    };

}).call(this);
