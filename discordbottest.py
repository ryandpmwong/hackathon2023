import os
import asyncio
import discord
import random
#import datetime

from discord.ext import commands
from discord.ui import Select, View
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())

class Round():
    def __init__(self, players):
        self.attacked = None  # username
        self.protected = None
        self.voted = None
        self.players = players
        
        self.werewolf_options = self.construct_werewolf_options()
        self.werewolf_votes = {k: None for (k, v) in players.items() if v == 'werewolf'}
        self.ww_votes_message = None
        self.werewolf_timeup = False

        self.everyone_options = self.construct_everyone_options()
        self.everyone_votes = {k: None for (k, v) in players.items()}
        self.everyone_votes_message = None
        self.everyone_timeup = False

    def construct_werewolf_options(self) -> list:
        options = []
        for player in self.players:
            if self.players[player] != 'werewolf':
                options.append(discord.SelectOption(label=player, description='Vote to kill ' + player))
        return options

    async def print_current_ww_votes(self, channel, votes):
        cv_message = "Current votes:"
        for voter in votes:
            if votes[voter] is not None:
                cv_message += f"\n{voter.name} voted for: {votes[voter]}"
        if self.ww_votes_message is None:
            self.ww_votes_message = await channel.send(cv_message)
        else:
            await self.ww_votes_message.edit(content=cv_message)

    def get_attacked(self, votes):
        voted_players = list(votes.values())
        for voted_player in voted_players:
            if voted_player is None or voted_player != voted_players[0]:
                #non unanimous vote so choose on at random
                filtered_list = list(filter(lambda x: x is not None, voted_players))
                if len(filtered_list) == 0:
                    #no one voted for a thingo
                    return random.choice([x for x in self.players if self.players[x] != 'werewolf'])
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
                await self.print_current_ww_votes(client.get_channel(1144596818995466280),
                                               self.werewolf_votes)
                await interaction.response.defer()
        select.callback = werewolf_callback

        view = View()
        view.add_item(select)
        
        await idk.send("Vote for a player to kill", view=view)





    def construct_everyone_options(self) -> list:
        options = []
        for player in self.players:
            options.append(discord.SelectOption(label=player, description='Vote to eliminate ' + player))
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
                await self.print_current_all_votes(client.get_channel(1144596818995466280),
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
        channel = client.get_channel(1144596818995466280)
        await self.werewolf_select(channel, self.werewolf_options)
        await timer(channel, 15)
        self.werewolf_timeup = True
        await channel.send("Voting has ended")
        self.attacked = self.get_attacked(self.werewolf_votes)
        await channel.send(f"You have chosen to kill: {self.attacked}")
        await self.run_day()

    async def run_day(self):
        channel = client.get_channel(1144596818995466280)
        await channel.send(f"{self.attacked} has been murdered!")
        await self.everyone_select(channel, self.everyone_options)
        await timer(channel, 30)
        self.everyone_timeup = True
        await channel.send("Voting has ended")
        self.voted = self.get_voted(self.everyone_votes)
        if self.voted == 'Tie':
            await channel.send("Tie detected! Skipping elimination this round.")
        elif self.voted == 'Skip':
            await channel.send("You have chosen to skip elimination this round.")
        else:
            await channel.send(f"You have chosen to eliminate: {self.voted}")

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await main()
    #channel = client.get_channel(1144596818995466280)
    #await thisround.werewolf_select(channel, thisround.werewolf_options)

'''
def main():
    bot = commands.Bot(command_prefix='/',intents=discord.Intents.default())
    print('1')
    channel = client.get_channel(1144596818995466280)
    print('2')
    await channel.send("Hello world!")
    print('3')
'''
async def timer(ctx, seconds):
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
                #await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
                break
        except:
            break
    
async def main():
    #bot = commands.Bot(command_prefix='/',intents=discord.Intents.default())
    print('1')
    channel = client.get_channel(1144596818995466280)
    print('2')
    #await channel.send("Hello world!")
    PLAYERS = {'player1': 'werewolf',
               'player2': 'villager',
               'player3': 'villager',
               'player4': 'villager',
               'player5': 'werewolf',
               'player6': 'villager',
               'player7': 'villager',}
    this_round = Round(PLAYERS)
    await this_round.run_night()
    print('3')

client.run(TOKEN)

#main()
