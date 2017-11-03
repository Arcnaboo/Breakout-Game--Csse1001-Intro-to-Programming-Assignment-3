# Breakout-Game--Csse1001-Intro-to-Programming-Assignment-3
Clone of the original Assignment submission

Assignment mark: 7 out of 7

CSSE1001 ASSIGNMENT 3
TASK 3 – ADVANCED FEATURES

1) Level Class
This class designed to process level information separately from the Model().
It uses GridInfo and it takes Json level file as an argument.
Upon called, this class creates walls for the level, separates blocks from locations, 
converts Row Column pairs to X, Y coordinates

2) Random Level Generator
This method is implemented inside the level class, upon called on, it creates a random level file. 
It uses random.random() method several times and assigns blocks according to results.
Equal chance block can be in any R, C pairs between [1,12], 
50% chance block is bluegreen with 20 points or red with 10 points, around 20% chance
block has extra_block variable, around 20% chance block has extra clone ball(more information on advanced feature 3) 
and around 20% chance block has paddle_delta, if block has paddle_delta 50% chance it increases the paddle or 50% chance decreases. 
This merhod can be called by clicking random level button in game interface, that moment game would create new level and 
start the game on that level.

3) Clone ball (Extra ball)
This variable is given randomly to lucky blocks in the random level generator, 
it is represented with ball2.gif, this ball2.gif file can be found in assign3_extras.zip. 
Upon a block which has clone ball is destroyed, game adds another playable ball with ball2.gif as image to the game, 
this ball is special and if this ball dies player do not lose life, if actual player ball dies in the meantime, 
game normally resets main ball to paddle and in the meantime the purple(clone ball) still in play.

4) Cheat mode
This mode is pretty much destroys a pattern of blocks from the game, 
approximately half of the blocks in game would be destroyed upon user clicking the CHEAT button 
in the game interface, this is added so players can head to further levels easier. When cheat is used, 
player do not receive any points from destroyed blocks.

5) New Game
User can click file menu and start a new game

6) Load level
User can click file menu and select load level, this method will ask for a json file, 
and any level.json file can be read by the application and player can play that specific level.
