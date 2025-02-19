import discord
from googletrans import Translator

TOKEN = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()
translator = Translator()

@client.event
async def on_ready():
    print('==============================')
    print('ログインしました・。・v')
    print('ユーザー名: ' + client.user.name)
    print(client.user.id)
    print('==============================')
    await client.change_presence(activity=discord.Game(name="[ ! ] ただの翻訳botだよ(*'▽')", type=1))

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
                embed = discord.Embed(title='変換結果', color=0xffff00)
                embed.add_field(name='Before', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
            else:
                convert_string = translator.translate(str, src=befor_lang, dest='ja')
                embed = discord.Embed(title='変換結果', color=0xffff00)
                embed.add_field(name='Before', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
        else:
            # !trans [A（元言語（Cの言語））]-[B（変換後言語）]=[C（AからBに翻訳したい文章）]
            # 例) !trans ja-el=私はこうだと思います。
            #     結果→ Before: 私はこうだと思います。 After: Νομίζω ότι είμαι αυτό.
            trans, str = list(say.split('='))
            befor_lang, after_lang = list(trans.split('-'))
            convert_string = translator.translate(str, src=befor_lang, dest=after_lang)
            embed = discord.Embed(title='変換結果', color=0xffff00)
            embed.add_field(name='Before', value=str)
            embed.add_field(name='After', value=convert_string.text, inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith('!detect'):
        # !detect [検証したい文章]
        # !detect こんにちは！
        # 結果→ この文字列の言語は ja です。
        say = message.content
        s = say[8:]
        detect = translator.detect(s)
        m = 'この文字列の言語は **' + detect.lang + '** です。'
        await message.channel.send(m)

client.run(TOKEN)