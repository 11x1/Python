# Prob has shit ton of exploits (ie. can delete whole system)
# Also very basic
import js2py

# Discord bot shit
import discord
from discord.ext import commands

# Discord bot code
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!execjs'):
            if isinstance(message.channel, discord.channel.DMChannel):
                content = message.content.replace('!execjs', '')
                content = content.replace('```js', '').replace('```', '').replace("console.log", "return ")
                content = 'function a() {' + content + '} a()'
                print(content)
                if content:
                    await message.reply(f'```js\noutput (js): {js2py.eval_js(content)}```')


client = MyClient()
client.run('token')
