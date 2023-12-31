'''
Needs inputs of player objects?? as well as the thread ID's???? and I think that's it???????
Or should there be a game object where it stores all players and threads n stuff

And should be able to output who died/was eliminated

(technically none of the above works properly but I'll get to it)
'''

import os
import asyncio
import discord
import random

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ui import Select, View
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())
bot = Bot(command_prefix='/', intents=discord.Intents.default())

class Round():
    def __init__(self, players, threads):
        self.attacked = None  # username
        self.protected = None
        self.voted = None
        self.players = players  # a list of player objects
        self.threads = threads  # dict of for {'everyone' 'werewolves': Thread object}
        self.game_result = None
        
        self.werewolf_options = self.construct_werewolf_options()
        self.werewolf_votes = {k.get_user(): None for k in players if k.get_side() == 'Bad'}
        self.ww_votes_message = None
        self.werewolf_timeup = False

        self.everyone_options = self.construct_everyone_options()
        self.everyone_votes = {k.get_user(): None for k in players}
        self.everyone_votes_message = None
        self.everyone_timeup = False
        
        print('Round init done')

    def get_player(self, username):
        '''Assumes there are no two players with the same username but i think thats a given anyway'''
        for player in self.players:
            if player.get_user().name == username:
                return player

    def update_game_result(self):
        print('update_game_result')
        sides = [player.get_side() for player in self.players if player.is_alive()]
        if sides.count('Bad') >= sides.count('Good'):
            self.game_result = 'Werewolves win'
        elif sides.count('Bad') == 0:
            self.game_result = 'Villagers win'
    
    def construct_werewolf_options(self) -> list:
        print('contructing werewolf options')
        options = []
        print('aaaaaaa')
        print(self.players)
        for player in self.players:
            user = player.get_user()
            print(player.get_user().name)

            if player.get_side() != 'Bad' and player.is_alive():
                print(user.name)
                options.append(discord.SelectOption(label=user.name, description='Vote to kill ' + user.name))
        return options

    async def print_current_ww_votes(self, channel, votes):
        print('generating current votes')
        cv_message = "Current votes:"
        for voter in votes:
            if votes[voter] is not None:
                # idk man
                cv_message += f"\n{voter.name} voted for: {votes[voter]}"
        if self.ww_votes_message is None:
            self.ww_votes_message = await channel.send(cv_message)
        else:
            await self.ww_votes_message.edit(content=cv_message)

    def get_attacked(self, votes):
        print('going to be attacked')
        voted_players = list(votes.values())
        for voted_player in voted_players:
            if voted_player is None or voted_player != voted_players[0]:
                #non unanimous vote so choose on at random
                filtered_list = list(filter(lambda x: x is not None, voted_players))
                if len(filtered_list) == 0:
                    #no one voted for a thingo
                    return random.choice([player for player in self.players if player.get_side() != 'Bad' and player.is_alive()])
                else:
                    return random.choice(list(set(filtered_list)))
        return voted_players[0]

    async def werewolf_select(self, idk, options):
        print("ww_select start")
        select = Select(placeholder="Vote for a player to kill", options=options)
        
        print("yep")
        
        
        async def werewolf_callback(interaction):
            if not self.werewolf_timeup:
                self.werewolf_votes[interaction.user] = select.values[0]
                await self.print_current_ww_votes(self.threads['werewolves'],
                                               self.werewolf_votes)
                await interaction.response.defer()
        select.callback = werewolf_callback

        view = View()

        view.add_item(select)
        print('finished constructing select view')
        print(view)
        await idk.send("Vote ps")
        await idk.send("Vote for a player to kill", view=view)





    def construct_everyone_options(self) -> list:
        print('contructing options')
        options = []
        try:
            for player in self.players:
                user = player.get_user()
                options.append(discord.SelectOption(label=user.name, description='Vote to eliminate ' + user.name))
        except:
            print(f'User with ID {player} not found?')
        return options

    async def print_current_all_votes(self, channel, votes):
        cv_message = "Current votes:"
        for voter in votes:
            if votes[voter] is not None:
                cv_message += f"\n{voter.name} voted for: {votes[voter]}"
        if self.everyone_votes_message is None:
            self.everyone_votes_message = await channel.send(cv_message)
        else:
            await self.everyone_votes_message.edit(content=cv_message)

    def my_func(self, x):
        if x is None:
            return 'Skip'
        else:
            return x

    def get_voted(self, votes):
        
        voted_players = list(votes.values())
        voted_players = [self.my_func(x) for x in voted_players]
        voted_set = set(voted_players)
        largest = [0, []]
        for vote in voted_set:
            num_of_votes = voted_players.count(vote)
            if num_of_votes > largest[0]:
                largest = [num_of_votes, [vote]]
            elif num_of_votes == largest[0]:
                largest[1].append(vote)
        if len(largest[1]) > 1:
            # tie
            return 'Tie'
        else:
            return largest[1][0]

    async def everyone_select(self, ctx, options):
        select = Select(placeholder="Vote for a player to eliminate", options=options)
        
        
        async def everyone_callback(interaction):
            if not self.everyone_timeup:
                self.everyone_votes[interaction.user] = select.values[0]
                await self.print_current_all_votes(self.threads['everyone'],
                                               self.everyone_votes)
                await interaction.response.defer()
        select.callback = everyone_callback

        view = View()
        view.add_item(select)
        
        await ctx.send("Who do you think is a werewolf?", view=view)





    

    async def run_night(self):
        #werewolf_options = self.construct_werewolf_options()
        # type "Start of night [night_number]:" in the werewolf channel
        # put the werewolf select in the werewolf channel
        # do stuff depending on what the werewolves voted for
        print('Night start')
        ww_thread = self.threads['werewolves']
        await self.werewolf_select(ww_thread, self.werewolf_options)
        print("sent select to werewolf")
        await self.timer(ww_thread, 30)
        print("count down for werewolf")
        self.werewolf_timeup = True
        await ww_thread.send("Voting has ended")
        self.attacked = self.get_attacked(self.werewolf_votes)
        await ww_thread.send(f"You have chosen to kill: {self.attacked}")
        self.get_player(self.attacked).kill()
        self.update_game_result()
        if self.game_result == 'Werewolves win':
            pass
        else:
            await self.run_day()

    async def run_day(self):
        all_thread = self.threads['everyone']
        await all_thread.send(f"{self.attacked} has been murdered!")
        await all_thread.send("Discuss who you think is a werewolf. Voting begins at the end of the timer")
        await self.timer(all_thread, 45)
        await self.everyone_select(all_thread, self.everyone_options)
        await self.timer(all_thread, 15)
        self.everyone_timeup = True
        await all_thread.send("Voting has ended")
        self.voted = self.get_voted(self.everyone_votes)
        if self.voted == 'Tie':
            await all_thread.send("Tie detected! Skipping elimination this round.")
        elif self.voted == 'Skip':
            await all_thread.send("You have chosen to skip elimination this round.")
        else:
            await all_thread.send(f"You have chosen to eliminate: {self.voted}")
            self.get_player(self.voted).kill()
            self.update_game_result()

    def get_game_result(self):
        return self.game_result

    async def timer(self, ctx, seconds): # bot
        time = int(seconds)
        if time >= 60:
            seconds_output = str(time%60)
            if len(seconds_output) == 1:
                seconds_output = f"0{seconds_output}"
            message = await ctx.send(f"Time left: {time//60}:{seconds_output}")
        elif time < 60:
            message = await ctx.send(f"Time left: {time}")
        while True:
            try:
                await asyncio.sleep(1)
                time -= 1
                if time >= 60:
                    seconds_output = str(time%60)
                    if len(seconds_output) == 1:
                        seconds_output = f"0{seconds_output}"
                    await message.edit(content=f"Time left: {time//60}:{seconds_output}")
                elif time < 60:
                    await message.edit(content=f"Time left: {time}")
                if time <= 0:
                    await message.edit(content="Time's up!")
                    break
            except:
                break

'''
@client.event
async def main():
    channel = client.get_channel(1144596818995466280)
    id_list = [1030359292647321601,
               490790539042619393,
               1122876194665271428,
               624203419628077060,
               500433894043287562]
    roles = ['villager',
             'villager',
             'werewolf',
             'villager',
             'villager']
    TEST_PLAYERS = {}
    for i, user_id in enumerate(id_list):
        user = await client.fetch_user(user_id)
        TEST_PLAYERS[user_id] = [user,roles[i]]
    this_round = Round(TEST_PLAYERS)
    await this_round.run_night()

client.run(TOKEN)
'''
