# Importing 'PIL' (Python Image Processing Library) to save each frame
# Importing 'os' library to create a subdirectory called output
import math
import os
import shutil
from time import sleep
import requests
from PIL import Image

# Discord bot shit
import discord
from discord.ext import commands

# Discord bot code
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Needed
imgbbapikey = 'img bb api key'
discordbottoken = 'discord bot token'

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!convert gif to lua'):
            if isinstance(message.channel, discord.channel.DMChannel):
                if message.attachments:
                    image_url = requests.get(message.attachments[0].url)
                    if image_url.status_code == 200:
                        gif_name = f"{message.author}.gif"
                        status_message = await message.reply("Starting...")
                        if os.path.isfile(gif_name):
                            os.remove(gif_name)

                        with open(gif_name, 'w') as file:
                            file.close()

                        with open(gif_name, 'wb') as f:
                            f.write(image_url.content)
                            await status_message.edit(content="File retrieved successfully.")
                            f.close()

                        if os.path.isdir(f"output-{message.author}"):
                            for filename in os.listdir(f"output-{message.author}"):
                                file_path = os.path.join(f"output-{message.author}", filename)
                                try:
                                    if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.unlink(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                            os.rmdir(f"output-{message.author}")

                        # Make a directory and open our gif file
                        os.mkdir(f"output-{message.author}")

                        await status_message.edit(content="Directories created...")

                        imageObject = Image.open(gif_name)
                        # Iterate through our gif (everything else here should be understandable)
                        for frame in range(0, imageObject.n_frames):
                            imageObject.seek(frame)
                            imageObject.save(f"output-{message.author}/frame_{frame}.png")

                        await status_message.edit(content="Frames extracted...")
                        sleep(1)
                        # image uploading shit
                        import imgbbpy

                        imgbb_api_key = imgbbapikey

                        image_urls = []

                        async def main(image_iter):
                            imgbb_client = imgbbpy.AsyncClient(imgbb_api_key)
                            loaded_image = await imgbb_client.upload(file=f'output-{message.author}/frame_{image_iter}.png')
                            image_urls.append(loaded_image.url)

                        image_status = await message.reply(f"Starting uploading... (0/{imageObject.n_frames} | 0.00%)")

                        for i in range(0, imageObject.n_frames):
                            await main(image_iter=i)
                            await image_status.edit(content=f"Starting uploading... ({i + 1}/{imageObject.n_frames} | {math.floor(((i+1)/imageObject.n_frames)*10000)/100}%...)")

                        frame_content = ""
                        for image in range(0, len(image_urls)):
                            frame_content += f"    Http.Get('{image_urls[image]}'),\n"

                        with open(f"{message.author}-out.lua", "w") as output_lua_file:
                            output_lua_file.write(f"local frames = \u007b\n{frame_content}\n\u007d")

                        await message.reply(file=discord.File(f"C:\\Users\\riis\\PycharmProjects\\Kool\\{message.author}-out.lua"))

                        imageObject.close()
                        os.remove(f"{message.author}.gif")
                        os.remove(f"{message.author}-out.lua")
                        if os.path.isdir(f"output-{message.author}"):
                            for filename in os.listdir(f"output-{message.author}"):
                                file_path = os.path.join(f"output-{message.author}", filename)
                                try:
                                    if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.unlink(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                            os.rmdir(f"output-{message.author}")
                else:
                    await message.reply("No attachments!")
            else:
                await message.reply('Message has to be in DMs!')


client = MyClient()
client.run(discordbottoken)
