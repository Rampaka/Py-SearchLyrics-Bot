import discord, lyricsgenius, sys, os, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from ..config import *
from ..module import *

genius = lyricsgenius.Genius(key)

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="가사",
        description="노래 가사를 가져오는 기능입니다.",
            options=[
                create_option(
                name="아티스트",
                description="Artist Name",
                option_type=3,
                required=True
                ),
                create_option(
                name="제목",
                description="Song Title",
                option_type=3,
                required=True
            )
        ]
    )

    async def GetLyrics(self, ctx, 아티스트: str, 제목: str):
        embed = discord.Embed(title='🔎 검색 중',description=f"**`{아티스트}`** 님의 **`{제목}`**(을)를 찾는 중 이예요!", colour=0x3B88C3)
        message = await ctx.send(embed=embed)
        artist = await GetArtist(아티스트)
        if artist == None:
            embed = discord.Embed(title='🔄 아티스트 검색',description=f"**`{아티스트}`** 님을 찾을 수 없어요!", colour=0x3B88C3)
            await message.edit(embed=embed)
        else:
            song = artist.song(제목)
            if song == None:
                embed = discord.Embed(title='🔄 가사 검색',description=f"**`{아티스트}`** 님의 **`{제목}`**(을)를 찾을 수 없습니다.", colour=0x3B88C3)
                await message.edit(embed=embed)
            else:
              SongList = await SplitList(song.lyrics.split('['), 3)
              SongPage = 0
              embed = discord.Embed(title=f'☑ {song.artist}ㅣ{song.title}',description=f"**```ini\n{await ListToText(SongList,SongPage)}```**", colour=0x3B88C3)
              embed.set_footer(text=f'[ {SongPage+1} / {len(SongList)} ]')
              await message.edit(embed=embed)
              if len(SongList) == 1:
                  return

              await message.add_reaction("◀")
              await message.add_reaction("⏹")
              await message.add_reaction("▶")
              SongPage = 0

              while True:
                def check(reaction, user):
                    return str(reaction.emoji) in ['◀','⏹','▶'] and user == ctx.author and message.id == reaction.message.id
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120, check=check)
                except asyncio.TimeoutError:
                    return

                if (str(reaction.emoji) == '▶'):
                    await reaction.remove(user)
                    if not SongPage + 1 == len(SongList):
                        SongPage = SongPage + 1
                        embed=discord.Embed(title=f'☑ {song.artist}ㅣ{song.title}',description=f"**```ini\n{await ListToText(SongList,SongPage)}```**", colour=0x3B88C3)
                        embed.set_footer(text=f'[ {SongPage+1} / {len(SongList)} ]')
                        await message.edit(embed=embed)

                if (str(reaction.emoji) == '⏹'):
                    await message.delete()
                    return

                if (str(reaction.emoji) == '◀'):
                    await reaction.remove(user)
                    if not 0 > SongPage-1:
                        SongPage = SongPage - 1
                        embed=discord.Embed(title=f'☑ {song.artist}ㅣ{song.title}',description=f"**```ini\n{await ListToText(SongList,SongPage)}```**", colour=0x3B88C3)
                        embed.set_footer(text=f'[ {SongPage+1} / {len(SongList)} ]')
                        await message.edit(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))