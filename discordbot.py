from discord.ext import commands
from googletrans import Translator
import discord
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()
translator = Translator()

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!trans'):
        say = message.content
        say = say[7:]
        if say.find('-') == -1:
            str = say
            detact = translator.detect(str)
            befor_lang = detact.lang
            if befor_lang == 'ja':
                convert_string = translator.translate(str, src=befor_lang, dest='en')
                embed = discord.Embed(title='変換結果', color=0xff0000)
                embed.add_field(name='Befor', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
            else:
                convert_string = translator.translate(str, src=befor_lang, dest='ja')
                embed = discord.Embed(title='変換結果', color=0xff0000)
                embed.add_field(name='Befor', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
        else:
            trans, str = list(say.split('='))
            befor_lang, after_lang = list(trans.split('-'))
            convert_string = translator.translate(str, src=befor_lang, dest=after_lang)
            embed = discord.Embed(title='変換結果', color=0xff0000)
            embed.add_field(name='Befor', value=str)
            embed.add_field(name='After', value=convert_string.text, inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith('!detect'):
        say = message.content
        s = say[8:]
        detect = translator.detect(s)
        m = 'この文字列の言語はたぶん ' + detect.lang + ' です。'
        await message.channel.send(m)    

bot.run(token)
