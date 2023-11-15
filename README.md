# hackathon2023

You think this is functional? You think it will be functional by the end of this Hackathon?? Think Again! :D

# Were-bot, or Where-bot????? (v0.0.5, Hackathon variant)

You have stumbled upon a project made by a group of first-years in UQ, and they are terrible at debugging and cooperating. 

Imagine deciding on making a discord bot in python with only 6 months of experience in python.

Appearently, there are something called 'async function', which are like regular functions but more of a jerk.

The first day was spent purely searching up tutorials all over internet. 

"I had only slept for 6 hours in these two days" - by Amy

"AAAAAAAAAfgdyshjzdcjaysukjzygfvjgcaskghvfguyakhdghfcvkaghdjsg what are classes I haven't finished my introductory python course" - K

"why did we choose to make a discord bot when none of us knew how to make a discord bot?" - Ryan

"testing the same code with different bots at the same time is not a good idea (insert bots echoing each other)" - Bahareh

# What does it do?
The Were-bot is a discord bot that allows you to play the werewolf game (aka mafia) in your own discord server!

Supposedly.

Its most significant function is to make everyone in the dev team suffer :)

## List of commands

Typing *'Make me some threads'* when Were-bot is online will kidnap every single person in the server into a game of Werewolf.

Typing *'Clear all threads'* will delete all the threads (including the ones that are originally in the server)

Nobody knows if the command *'Delete thread {int}'* will work anymore. "I'm a little scared to figure out if it does." -K

### Useless commands

Were-bot will also respond to you if you say a greeting. It's up to you to figure out what those greetings may be.

The functionality for the bot to repeat and mock what you say has also been included, provided your channel is called 'testing'. A niche case, but something still useful for most of the community I'd bet.


## How does the game work?
Poorly

By typing *'Make me some threads'* it will pull people into the game and initiate games. By people we include those that are offline. So don't worry about not being able to find friends to play with: with Werebot, NO ONE CAN ESCAPE (you can by leaving threads actually), EVERYONE MUST PLAY

Game starts with night, Werewolves have 15 seconds to discuss who to kill next, and have 30 secs to vote.

After then it is the day, and villagers are supposed to vote out the werewolves amoung them, with a time equivanlently short.

The game continues until enough player have died so either werewolves have equal or more members than villagers, or all werewolves are voted out.

To actually run Were-bot, use the main-test file.

Order of operations:
main-test.py {
    -> creates a WereBot instance from bot.py {

    }
    -> Creates slash command cogs
    button.py {
        -> Creates commands (/start_game) to initate game view
        -> Once all players have been filled, it will allow you to start the game
    } -> Initiates game_a.WerewolfGame instance
}


##
we have attempted at making /commands for quick access and make join game buttons, but the buttons won't work and we ran out of time.
We may attempt to implement it in UQ CS bot in the future (Once we get rid of all the bugs) (? When did we say this?)

# To-dos(?)

Who knows if we'll ever actually do these, but I'd like to think we will.

### Bugs
* Werewolves currently unable to be voted off by villagers (we're giving those sussy Werewolves a chance). **Status:** unfixed

### Functionality
* Enable multiple rounds of a game. **Status:** unfinished

* Allow ability to skip vote timers if consensus is met (75% of players). **Status:** not implemented

* Prevent dead players from speaking in the threads, enable them to see all running threads (roles?). **Status:** unfinished

* Create a channel or thread in which dead players can speak in and see (but no living players can). **Status:** unfinished/not implemented

* Delete game threads and declare a win message after the game is won. **Status:** unfinished

* Give a summary of the game's events in said win message. **Status:** unfinished

* Add game initialisation messages (e.g. Welcome @[username] and @[username], you are this game's Werewolves! Pretend to be a villager by day and try not to be voted out for being too suspicious. Vote to kill someone now :) ). **Status:** unimplemented

* Prevent Werewolves from speaking to each other in the Werewolf thread when Day is active (need to communicate with group on whether this is the desired functionality). **Status:** not implemented

* Check that Were-bot can run correctly in multiple servers. **Status:** not done




### Menus/Interaction
* Create a button start menu that updates (disabling said buttons comes later) and can start the game, as well as cancel the game. **Status:** unfinished

* Slash Commands show up in list properly and actually run, with descriptions given etc. **Status:** unfinished like the lore of a lost epic (i.e. documentation)

* Disable/enable said buttons mentioned earlier when the number of players has been met. **Status:** unfinished

* Add support for specifying number of werewolves in a game in play command. **Status:** unfinished

* Allow nickname _and_ username support. **Status:** not implemented, it's not much anyway

* Pin messages by Were-bot. **Status:** not implemented, not really a priority


### Expansion/Stretch (maybe v0.1.0 and up?)
* Enable increased customisation of game settings (i.e. timers, number of each specific role). **Status:** not implemented

* Support for multiple games running simultaneously. **Status:** unfinished

* Graphical representation of current votes. **Status:** unimplemented. Don't hold your breath (or you'll asphyxiate long before this happens)

* Image representation of living and dead players. **Status:** unimplemented

* Inclusion of more roles. **Status:** Unimplemented and will be unimplemented until we get a game running with base roles, I'd think

* Tell an AI how you want to kill somebody. **Status:** unimplemented like the safety function of a washing machine while you're inside of it


# Version history (a singular entry)
## v0.0.5
Created after slaving away for two days at hackathon. Creates new threads for a game, allows for werewolf votes, player discussion, and villager votes (but only for one round), and contains some bugs for good measure.