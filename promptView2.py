import discord
from discord.ui import Button, View
from discord.ext import commands
import discord.ext
#from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

class MakeButtons:

    def __init__(self):
        self.all_players_thread = None
        self.werewolves_thread = None
        self.dead_thread = None

    async def create_start_prompt(self):
        return

#@tree.command(name = "hello", description = "My first application Command", guild=discord.Object(id=1144540988753326131))

#async def first_command(interaction):
#    await interaction.response.send_message("Hello!")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

"""@bot.command()
# Make Button?
async def hello(ctx):
    classMaybe = """


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1144540988753326131))
    # print "ready" in the console when the bot is ready to work
    print("ready")
async def on_ready():
#    await tree.sync(guild=discord.Object(id=1144540988753326131))
    print("Ready!")

########## I'm really sorry I don't know how to use classes and can't run this with them ############
global num_players_global_blasphemy
num_players_global_blasphemy = 0
global players_joined_message

@bot.command()
async def play_game(ctx, arg1 = None, arg2 = None):
    """Runs on /test_play [num players] [num werewolf]"""
    if arg1 != None and arg1.lower() in ["h", "help"]:
        await ctx.send("Usage: /test_play [total number of players] [number of werewolves]")
        return
    
    global num_players_global_blasphemy
    nickname = ctx.author.nick
    username = ctx.author
        
    async def button_join_callback(interaction):
        global num_players_global_blasphemy
        """Prints username/nicknames and a message"""
        nickname = interaction.user.nick
        username = interaction.user
        if nickname == None:
            await interaction.response.send_message(f"{username} has clicked a button! Blasphemous!")
        else:
            await interaction.response.send_message(f"{nickname} ({username}) has clicked a button! Blasphemous!")
        num_players_global_blasphemy += 1
        players_joined_message.edit(content=(f"15/{arg1} players joined"))
        #players_joined += 1
        #print(players_joined)
        #message = await interaction.original_response()
        #await message.edit()

    async def button_start_callback(interaction):
        global num_players_global_blasphemy
        await interaction.response.send_message(f"Sleep is great for you")
        message = await interaction.original_response()
        #print(message)
        #await interaction.edit_original_response("New or old message first method?")
        await message.edit(content="There is no sleep in Ba Sing Se")

    async def button_boring_callback(interaction):
        await interaction.response.send_message("Oh. You clicked the other button.")

    button_join = Button(label="Join Game", style=discord.ButtonStyle.blurple)
    button_start = Button(label="Start Game", style=discord.ButtonStyle.green, disabled=False)
    button3 = Button(label="Warning: I'm broken, Cancel", style=discord.ButtonStyle.red)

    #num of player conditions
    if arg2 is not None:
        if valid_player_numbers(int(arg1), int(arg2)):
            players_joined = 0

            #await ctx.send(str(ctx.author)+" wants to start a game with "+arg1+" players and "+arg2+" werewolves.")

            button_join.callback = button_join_callback
            button_start.callback = button_start_callback
            button3.callback = button_boring_callback

            view = View()
            view.add_item(button_join)
            view.add_item(button_start)
            view.add_item(button3)
            #view.remove_item(button)

            num_players_global_blasphemy = 0
            if nickname != None:
                start_message = await ctx.send(f"{nickname} ({username}) has started a {arg2} werewolf game! 🐺")
            else:
                start_message = await ctx.send(f"{username} has started a {arg2} werewolf game! 🐺")
                                                
            players_joined_message = await ctx.send(f"{players_joined}/{arg1} players joined")
            button_message = await ctx.send(view=view)
            
        else:
           await ctx.send("Too many werewolves. Please enter a lower amount of werewolves.")

    elif arg1:

        players_joined = 0

        #await ctx.send(str(ctx.author)+" wants to start a game with "+arg1+" players and "+arg2+" werewolves.")

        button_join.callback = button_join_callback
        button_start.callback = button_start_callback
        button3.callback = button_boring_callback

        view = View()
        view.add_item(button_join)
        view.add_item(button_start)
        view.add_item(button3)
        #view.remove_item(button)

        num_players_global_blasphemy = 0
        if nickname != None:
            start_message = await ctx.send(f"{nickname} ({username}) has started a game! 🐺")
        else:
            start_message = await ctx.send(f"{username} has started a game! 🐺")

        players_joined_message = await ctx.send(f"{players_joined}/{arg1} players joined")
        button_message = await ctx.send(view=view)
        #await ctx.send(str(ctx.author)+" wants to start a game with "+arg1+" players.")
    else:
        await ctx.send("You haven't entered the number of players.")
    
# function to manage player number check
def valid_player_numbers(total, werewolves):
    good = total - werewolves
    if werewolves >= good:
        return False
    else:
        return True

bot.run(TOKEN)

"""class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="what is on the button", style=discord.ButtonStyle.gray)
    async def function_name(self, int: discord.Interaction):
        await int.response.send_message("button clicked")"""
