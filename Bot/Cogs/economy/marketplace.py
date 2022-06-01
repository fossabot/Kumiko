import asyncio
import uuid
from datetime import datetime

import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from economy_utils import KumikoEcoUtils
from exceptions import ItemNotFound

utilsMain = KumikoEcoUtils()
today = datetime.now()


class ecoMarketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    eco_marketplace = SlashCommandGroup(
        name="marketplace",
        description="Commands for Kumiko's Marketplace",
    )

    @eco_marketplace.command(name="add-item")
    async def ecoAddItem(
        self,
        ctx,
        *,
        name: Option(str, "The name of the item you wish to add"),
        description: Option(str, "The description of the item you wish to add"),
        amount: Option(int, "The amount you are willing to sell"),
        price: Option(int, "The price of the item"),
    ):
        """Adds an item into the marketplace"""
        dateEntry = today.strftime("%B %d, %Y %H:%M:%S")
        owner = ctx.user.id
        uuidItem = uuid.uuid4().hex[:16]
        await utilsMain.ins(
            uuidItem, dateEntry, owner, name, description, amount, price
        )
        await ctx.respond("Item added to the marketplace")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(name="view")
    async def ecoMarketplaceView(self, ctx):
        """View the marketplace"""
        try:
            mainObtain = await utilsMain.obtain()
            if len(mainObtain) == 0:
                raise ValueError
            else:
                paginator = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(items)["name"],
                            description=dict(items)["description"],
                        )
                        .add_field(
                            name="Amount", value=dict(items)["amount"], inline=True
                        )
                        .add_field(
                            name="Price", value=dict(items)["price"], inline=True
                        )
                        .add_field(name="Date Added", value=dict(items)["date_added"])
                        .add_field(
                            name="Owner",
                            value=f"{await self.bot.fetch_user(dict(items)['owner'])}",
                        )
                        .add_field(name="UUID", value=dict(items)["uuid"], inline=True)
                        for items in mainObtain
                    ],
                )
                await paginator.respond(ctx.interaction, ephemeral=False)
        except ValueError:
            embedErrorMain = discord.Embed()
            embedErrorMain.description = "There seems to be no items in the marketplace right now. Please try again..."
            await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(
        name="search",
    )
    async def ecoMarketplaceSearch(
        self, ctx, *, name: Option(str, "The name of the item you wish to search")
    ):
        """Search the marketplace"""
        try:
            mainGetItem = await utilsMain.getItem(name)
            if len(mainGetItem) == 0:
                raise ValueError
            else:
                paginator = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(item)["name"],
                            description=dict(item)["description"],
                        )
                        .add_field(
                            name="Amount", value=dict(item)["amount"], inline=True
                        )
                        .add_field(name="Price", value=dict(item)["price"], inline=True)
                        .add_field(name="Date Added", value=dict(item)["date_added"])
                        .add_field(
                            name="Owner",
                            value=f"{await self.bot.fetch_user(dict(item)['owner'])}",
                        )
                        .add_field(name="UUID", value=dict(item)["uuid"], inline=True)
                        for item in mainGetItem
                    ]
                )
                await paginator.respond(ctx.interaction, ephemeral=False)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = (
                "Sorry, but the search produced no results. Please try again"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(name="delete-all")
    async def ecoMarketplaceDeleteAll(self, ctx):
        """Deletes all of your items in the marketplace"""
        mainCheck = await utilsMain.obtainOnlyID(ctx.user.id)
        embed = discord.Embed()
        if dict(mainCheck)["owner"] == ctx.user.id:
            await utilsMain.delAll(ctx.user.id)
            await ctx.respond("All of your items have been deleted")
        else:
            embed.description = "Sorry, but you can't delete all of your items in the marketplace. This is more than likely due to the user not being the owner of said item(s)."
            await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(name="delete-one")
    async def ecoMarketplaceDeleteOne(
        self, ctx, *, name: Option(str, "The name of the item")
    ):
        """Deletes the specified item within the marketplace"""
        try:
            mainChecker = await utilsMain.obtainOnlyIDWithName(name, ctx.user.id)
            if mainChecker is None:
                raise ItemNotFound
            else:
                await utilsMain.delOneItem(name, ctx.user.id)
                await ctx.respond("Item deleted from the marketplace")
        except ItemNotFound:
            await ctx.respond("Sorry, but that item does not exist in the marketplace.")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(name="uuid")
    async def ecoMarketplaceSearchUUID(
        self, ctx, *, uuid: Option(str, "The UUID of the Item")
    ):
        """Searches the item via the UUID"""
        try:
            mainSearchUUID = await utilsMain.searchForID(uuid)
            if mainSearchUUID is None:
                raise ItemNotFound
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(item)["name"],
                            description=dict(item)["description"],
                        )
                        .add_field(
                            name="Amount", value=dict(item)["amount"], inline=True
                        )
                        .add_field(name="Price", value=dict(item)["price"], inline=True)
                        .add_field(name="Date Added", value=dict(item)["date_added"])
                        .add_field(
                            name="Owner",
                            value=f"{await self.bot.fetch_user(dict(item)['owner'])}",
                        )
                        .add_field(name="UUID", value=dict(item)["uuid"], inline=True)
                        for item in mainSearchUUID
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except ItemNotFound:
            embedItemNotFoundError = discord.Embed()
            embedItemNotFoundError.description = (
                "Sorry, but that item does not exist in the marketplace."
            )
            await ctx.respond(embed=embedItemNotFoundError)


def setup(bot):
    bot.add_cog(ecoMarketplace(bot))
