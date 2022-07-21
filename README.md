# Pillars-of-Power-1
My first try at a game - a simple turn based RTS. This is version 1 - a simple command line version made in python.

Welcome to budget HOI4:
Budget HOI4 is a turn based game.
Each turn the player can choose to attack or ally another nation until all nations are gone.
At the beginning of the game, you will get a table showing all the nations, their ideologies and their manpower.
Different ideologies have different advantages and disadvantages:
 - Fascist nations have a very high manpower but find it virtually impossible to ally other nations
 - Communist nations have a moderately high manpower but can only ally other communist nations.
 - Democratic nations have a low manpower but find it very easy to ally to other nations
 - Monarchist nations have a moderately low manpower but can ally any democratic or monarchist nation 
You win the game by being either the only nation left or there only being you and your allies remaining.
How you get there is up to you!
---------------------------------
How to play each turn:
---------------------------------
You have one of three commands you can input each turn.
These turns must be inputted exactly for them to go through.
They are:
 - ally [nation number]
Ie: "ally 15"
This will send an ally request to this nation.
 - attack [nation number]
Ie: "attack 4"
This will attack another nation and their allies. You cannot attack one of your own allies.
- ''
Entering nothing will skip your turn, allowing you to regenerate manpower before you make your next move. 
Either way, your manpower will regen every turn at a rate of 2% per turn. (Manpower is a constant function of population, ideology modifier and total losses)
-----------
Allying:
-----------
Before going into specifics, allying is not a faction-like system. Allies are personal to a nation and are not linked between nations in this game (ie if 'A' is allied to 'B' and 'B' is allied to 'C', then 'A' has no relation to 'C' despite 'B' being allied to both). 
As a base:
Fascist nations will have a -100 modifier and will never ally another nation
All other nations will have a -20 modifier to allying other nations
This modifier is changed based on:
 - For communist nations:
Whether you are also communist (+ 15)
Whether you border them (+ 10)
 - For democratic nations:
Whether you are also democratic (+ 20)
Whether you are monarchist (+ 10)
Whether you border them (+ 10)
 - For monarchist nations: 
Whether you are also monarchist (+ 10)
Whether you are democratic (+ 10)
Whether you border them (+ 10)
As long as their ally opinion is greater than or equal to 0, they will accept.
- What does an ally do:
An ally will count as coming to war with you if you are attacked or you attack someone else, effectively combining your forces.
Note that if you try to ally someone and they decline, this will still take up your turn so be careful and know the system!
-----------
Attacking:
-----------
Attacking is a simple mechanic.
You select another nation to attack and the game finds out the total manpower of you and all your allies, as well as the total manpower of them and all their allies.
NOTE: 
YOU CAN ONLY ATTACK NEIGHBOURING NATIONS
If you do attempt to attack a non-neighbour, it will tell you that you do not border this nation, and will not take up your turn, allowing you to redo your commands.
The alliance/nation with the highest manpower will win and a portion of all of them and their Allies' manpowers, as well as the allies of the now lost defendant, will be taken off.
Specifically, the losses of any war will be 6 (+ or - 2)% of your total manpower in the battle
If you successfully invade another nation, you will gain their tile(s) on the board as your own meaning you now border more nations.
If you are attacked and lose, the game will automatically end.
If both manpower sizes are equal (this is very rare!), the battle will end in a stalemate where everyone on both sides lose manpower, but no tiles are gained or lost.
