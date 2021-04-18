import discord
from discord.ext import commands
import pymongo
import asyncio

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["moderation"]
client = commands.Bot(command_prefix=".")
color = discord.Color.blue()

@client.event
async def on_ready():
    print("Bot is ready.")

def remove_member(ctx, member, action, reason):
    embed = discord.Embed(description=f"{action} `{member}.`", color=color)
    embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
    embed.add_field(name="Reason", value=reason if reason is not None else "")
    return embed

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None,):
    await ctx.ban(member, reason=reason)
    embed = remove_member(ctx, member, "Banned", reason)
    await ctx.send(embed=embed)

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None,):
    await ctx.kick(member, reason=reason)
    embed = remove_member(ctx, member, "Kicked", reason)
    await ctx.send(embed=embed)

@client.command()
async def delete(ctx, amount: int, member: discord.Member=None):
    if member is None:
        await ctx.purge(limit=amount+1)
        embed = discord.Embed(description=f"Cleared `{amount}` messages!", color=color)
        embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

    else:
        deleted = 0
        async for message in ctx.history(limit=None):
            if deleted == amount:
                break
            else:
                if message.author == member:
                    deleted += 1
                    await message.delete()
