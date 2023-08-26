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

bot = commands.Bot(command_prefix="/",
                   intents=discord.Intents.all())

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

@bot.command()
async def test_play(ctx, arg1 = None, arg2 = None):
    if arg1.lower() in ["h", "help"]:
        await ctx.send("Usage: /test_play [total number of players] [number of werewolves]")
        return

    #num of player conditions
    if arg2 is not None:
        if valid_player_numbers(int(arg1), int(arg2)):
            await ctx.send(str(ctx.author)+" wants to start a game with "+arg1+" players and "+arg2+" werewolves.")
        else:
           await ctx.send("Too many werewolves.")
    elif arg1:
        await ctx.send(str(ctx.author)+" wants to start a game with "+arg1+" players.")
    else:
        await ctx.send("You haven't entered the number of players.")
    
# function to manage player number check
def valid_player_numbers(total, werewolves):
    good = total - werewolves
    if werewolves>= good:
        return False
    else:
        return True


@bot.command()
# Make Button?
async def play(ctx):
    button1 = Button(label="Don't click me ;_;", style=discord.ButtonStyle.blurple)
    button2 = Button(label="I would ask you to start the game.", style=discord.ButtonStyle.green)
    button3 = Button(label="Warning: I'm broken", style=discord.ButtonStyle.red)
    players_joined = 0

    async def button1_callback(interaction):
        nickname = interaction.user.nick
        username = interaction.user
        if nickname == None:
            await interaction.response.send_message(f"{username} has clicked a button! Blasphemous!")
        else:
            await interaction.response.send_message(f"{nickname} ({username}) has clicked a button! Blasphemous!")
        #players_joined += 1
        #print(players_joined)
        message = await interaction.original_response()
        await message.edit(f"New or old message?")

    async def button2_callback(interaction):
        message = await interaction.original_response()
        print(message)
        await interaction.edit_original_response("New or old message first method?")
        await message.edit("New or old message?")

    async def button_boring_callback(interaction):
        await interaction.response.send_message("Oh. You clicked the other button.")

    button1.callback = button1_callback
    button2.callback = button2_callback
    button3.callback = button_boring_callback

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    #view.remove_item(button)
    start_message = await ctx.send(f"Username of some sort has started a game! 🐺\n {players_joined}/666 players joined", view=view)

bot.run(TOKEN)

"""class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="what is on the button", style=discord.ButtonStyle.gray)
    async def function_name(self, int: discord.Interaction):
        await int.response.send_message("button clicked")"""
