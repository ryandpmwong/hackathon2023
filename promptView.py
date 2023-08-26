import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

botThing = commands.Bot(command_prefix="/",
                        intents=discord.Intents.all())

@botThing.command()
# Make Button?
async def hello(ctx):
    button = Button(label="Don't click me ;_;", style=discord.ButtonStyle.blurple)
    view = View()
    view.add_item(button)
    #view.remove_item(button)
    await ctx.send("Hi", view=view)

botThing.run(TOKEN)

"""class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="what is on the button", style=discord.ButtonStyle.gray)
    async def function_name(self, int: discord.Interaction):
        await int.response.send_message("button clicked")"""