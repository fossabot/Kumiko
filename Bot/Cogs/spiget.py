import json
import os
import re

import discord
import requests
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


def resource_search(search):
    link = f"https://api.spiget.org/v2/search/resources/{search}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spiget = json.loads(data)
    return spiget


def resource_author(search):
    link = f"https://api.spiget.org/v2/search/resources/{search}/author"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv2 = json.loads(data)
    return spigetv2


def latest_resource_version(search):
    link = f"https://api.spiget.org/v2/search/resources/{search}/versions/latest"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv3 = json.loads(data)
    return spigetv3


class SpigetV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spiget-search")
    async def on_message(self, ctx, *, search: str):
        resource = resource_search(search)
        resourcev2 = resource_author(search)
        resourcev3 = latest_resource_version(search)
        thumbnail = "https://www.spigotmc.org/" + resource[0]["icon"]["url"]
        file_size = str(resource[0]["file"]["size"]) + str(
            resource[0]["file"]["sizeUnit"]
        )
        download_url_false = "https://spigotmc.org/" + \
            str(resource[0]["file"]["url"])
        try:
            if str(resource[0]["file"]["type"]) == "external":
                embedVar = discord.Embed()
                embedVar.add_field(
                    name="Plugin Info",
                    value=f"Name >> {resource[0]['name']}\nTag >> {resource[0]['tag']}\nAuthor >> {resourcev2[0]['name']}\nDownloads >> {resource[0]['downloads']}\nRating >> {resource[0]['rating']['average']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Tested Versions",
                    value=str(resource[0]["testedVersions"])
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", ""),
                    inline=False,
                )
                embedVar.add_field(
                    name="Supported Languages",
                    value=f"{resource[0]['supportedLanguages']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Latest Plugin Version",
                    value=f"{resourcev3[0]['name']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Downloads",
                    value=f"Type >> {resource[0]['file']['type']}\nSize >> {file_size}\nURL >> {resource[0]['file']['url']}",
                    inline=False,
                )
                embedVar.set_thumbnail(url=str(thumbnail))
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed()
                embedVar.add_field(
                    name="Plugin Info",
                    value=f"Name >> {resource[0]['name']}\nTag >> {resource[0]['tag']}\nAuthor >> {resourcev2[0]['name']}\nDownloads >> {resource[0]['downloads']}\nRating >> {resource[0]['rating']['average']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Tested Versions",
                    value=str(resource[0]["testedVersions"])
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", ""),
                    inline=False,
                )
                embedVar.add_field(
                    name="Supported Languages",
                    value=f"{resource[0]['supportedLanguages']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Latest Plugin Version",
                    value=f"{resourcev3[0]['name']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Downloads",
                    value=f"Type >> {resource[0]['file']['type']}\nSize >> {file_size}\nURL >> {download_url_false}",
                    inline=False,
                )
                embedVar.set_thumbnail(url=str(thumbnail))
                await ctx.send(embed=embedVar)
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(SpigetV2(bot))
