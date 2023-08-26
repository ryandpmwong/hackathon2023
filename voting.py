from typing import Optional
import discord
import bot
import model

class MyView(discord.ui.View):
    #update with list of non werewolf players every round
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.alive_not_werewolves = []
        self.poll_options = []
            
    def populate_alive_not_werewolves(self, players):
        self.alive_not_werewolves = players
        for player in players:
            self.poll_options.append(discord.SelectOption(
                label=player.get_username(),
                description="Pick this if you like vanilla!"
        ))

    @discord.ui.select(# the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a player to kill!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = self.poll_options  # the list of options from which users can choose, a required field
    )
    
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        #COUNT VOTES IN HERE
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

'''@bot.command()
async def flavor(ctx):
    await ctx.send("Choose a flavor!", view=MyView())'''
