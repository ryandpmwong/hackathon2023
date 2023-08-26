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

#@tree.command(name = "hello", description = "My first application Command", guild=discord.Object(id=1144540988753326131))

#async def first_command(interaction):
#    await interaction.response.send_message("Hello!")

bot = commands.Bot(command_prefix="/",
                        intents=discord.Intents.all())


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1144540988753326131))
    # print "ready" in the console when the bot is ready to work
    print("ready")
async def on_ready():
#    await tree.sync(guild=discord.Object(id=1144540988753326131))
    print("Ready!")

# make the slash command
@tree.command(name="name", description="description")
async def slash_command(interaction: discord.Interaction):    
    await interaction.response.send_message("command")

@bot.command()
# Make Button?
async def hello(ctx):
    button1 = Button(label="Don't click me ;_;", style=discord.ButtonStyle.blurple)
    button2 = Button(label="I would ask you to start the game.", style=discord.ButtonStyle.green)
    button3 = Button(label="Warning: I'm broken", style=discord.ButtonStyle.red)
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    #view.remove_item(button)
    await ctx.send("Username of some sort has started a game! 🐺\n x/y players joined", view=view)

bot.run(TOKEN)

"""class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="what is on the button", style=discord.ButtonStyle.gray)
    async def function_name(self, int: discord.Interaction):
        await int.response.send_message("button clicked")"""