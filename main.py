import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os


load_dotenv()

token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Gamer"

@bot.event

async def on_ready():
    print(f'We are ready to go in {bot.user.name}')


@bot.event
async def on_member_join(member):
    await member.send(f"FAAAAAAAAAAhh {member.name} !! Welcome to the server")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "nigga" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - Don't use foul language!")

    await bot.process_commands(message)

# !hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned as {secret_role}")
    else :
        await ctx.send("Role doesn't exist!")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is now removed from {secret_role}")
    else :
        await ctx.send("Role doesn't exist!")


@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send(f"Welcome to the Club, {ctx.author.mention}!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"Sorry {ctx.author.mention}, you don't have the required role to access this command.")

@bot.command()
async def dm(ctx, *,msg):
    await ctx.author.send(msg)
    await ctx.send(f"{ctx.author.mention} - I have sent you a DM with your message - {msg}!")

@bot.command()
async def reply(ctx):
    await ctx.reply(f"{ctx.author.mention} - This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll", description=question,)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

bot.run(token, log_handler=handler, log_level=logging.DEBUG) 