# Needed libraries:
# Selenium: https://pypi.org/project/selenium/
# Discord.py: https://pypi.org/project/discord.py/ 
import discord
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import datetime

# replace bot_token with your bot token
# If you don't have a bot:
# Create an application in discord developer portal: https://discord.com/developers/applications
# create a bot for your application and replace bot_token with your bot token
bot_token = "your bot token"

# Download corresponding chrome driver from: https://chromedriver.chromium.org/downloads
# (chromedriver_win32.zip) and extract it anywhere.
# Replace the field with the correct path
options = Options()
driver_path = r"chromedriver path"
options.headless = True
driver = webdriver.Chrome(driver_path, options=options)

datafile_path = r"login data file path"

client = discord.Client()

time_start = datetime.datetime.now()

@client.event
async def on_message(message):
    time_start_help = datetime.datetime.now()
    time_start_help_ms = time_start_help.microsecond

    hour = message.created_at.hour
    minute = message.created_at.minute
    second = message.created_at.second

    if not message.content.startswith("!hw " or message.content == "!hw"):
        if message.author == client.user:
            if isinstance(message.channel, discord.channel.DMChannel):
                print(f" [ {hour}:{minute}:{second} | DM ] Bot: {message.content}")
            else:
                print(f" [ {hour}:{minute}:{second} | {message.channel.guild.name} ->"
                      f" {message.channel.name} ] Bot: {message.content}")
        else:
            if message.created_at.hour < 10:
                hour = f"0{message.created_at.hour}"
            if message.created_at.minute < 10:
                minute = f"0{message.created_at.minute}"
            if message.created_at.second < 10:
                second = f"0{message.created_at.second}"

            if isinstance(message.channel, discord.channel.DMChannel):
                print(f" [ {hour}:{minute}:{second} | DM ] {message.author}: {message.content}")
            else:
                print(f" [ {hour}:{minute}:{second} | {message.channel.guild.name} ->"
                      f" {message.channel.name} ] {message.author}: {message.content}")
    else:
        print(f"{message.author} requested data from nrg.edu.ee/auth/.")

    if message.author == client.user:
        return

    if message.content.startswith('!test ') or message.content == "!test":
        msg = "{0.author.mention} initialized \"!test\"".format(message)
        await message.channel.send(msg)

    if message.content.startswith("!help ") or message.content == "!help":
        msg = discord.Embed(
            title=f"- __Help__",
            description=f"- !help -> sends this embed\n"
                        f"- !auth -> authenticates you on the server (need to do before using !hw)\n"
                        f"- !hw -> sends homework from stuudium to your dms\n"
                        f"- !ping -> pings the server"
        )
        msg.set_author(name=message.author, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        msg.set_thumbnail(url="https://nrg.edu.ee/sites/nrg.edu.ee/files/styles/hitsa_core_logo/public/ruutjuurega_0"
                              ".png?itok=dNstk4JL")
        msg.set_footer(
            text=f"Response: {(datetime.datetime.now() - time_start_help)} sec"
                 f" ({(datetime.datetime.now().microsecond - time_start_help_ms) / 1000000} ms)")

        await message.channel.send(embed=msg)

    if message.content.startswith("!hw ") or message.content == "!hw":
        if message.author == client.user:
            return

        username = ""
        password = ""
        should_send_error = True

        with open(datafile_path, "r") as file:
            lines = file.readlines(file.__sizeof__())
            for line in lines:
                a = line.split(":")
                for elem in a:
                    if elem == str(message.author):
                        should_send_error = False

        if should_send_error:
            msg1 = discord.Embed(
                title="__Login Data__",
                description=f"Send your email and password in this format to get stuudium data:\n"
                            f"!auth email:password\n\n"
            )
            await message.author.send(embed=msg1)
            return

        with open(datafile_path, "r") as file:
            for line in file:
                if str(message.author) in line:
                    data = line.split(":")
                    username = str(data[1])
                    password = str(data[2].strip())

        data_send = discord.Embed(
            title="homework",
        )

        time_start = datetime.datetime.now()
        time_finished_start = datetime.datetime.now()
        driver.get("https://nrg.ope.ee/auth/")

        driver.find_element_by_class_name("username").send_keys(username)
        driver.find_element_by_class_name("password").send_keys(password)
        driver.find_element_by_class_name("button").send_keys(Keys.ENTER)
        time_end = datetime.datetime.now()

        print(
            f'Executed startup successfully. Waited {(time_end - time_start).microseconds / 1000000} seconds for '
            f'webpage '
            f'initialization.')

        await message.author.send("Fetching data...")

        todo_elements = driver.find_elements_by_class_name("todo_container")
        try:
            driver.find_element_by_class_name("show-future").click()
        except:
            await message.author.send("Couldn't get future homework.")
        time_start = datetime.datetime.now()
        for element in todo_elements:
            subject_date = element.get_attribute("data-date").replace(str(datetime.datetime.now().year), '')
            # print(f"Homework for {subject_date[:2]}.{subject_date[2:]}\n")

            subject_name = element.find_element_by_class_name("subject_name").text
            subject_description = element.find_element_by_class_name("todo_content").text
            if "Kontrolltöö" in element.text:
                subject_description = f"[KT] {subject_description}"
            # if subject_name != "":
            #   print(f"Subject : {subject_name}\nDescription: {subject_description}\n")

            data_send.add_field(
                name=f"{subject_date[2:]}.{subject_date[:2]} {subject_name}",
                value=subject_description,
            )

        time_end = datetime.datetime.now()
        time_delta = time_end - time_start

        data_send.set_footer(
            text=f"Webelements: {time_delta.microseconds / 1000000} sec | "
                 f"Total: {datetime.datetime.now() - time_finished_start} sec")

        print(f"Got all webelements in {time_delta.microseconds / 1000000} seconds.")
        print(f"Total: {datetime.datetime.now() - time_finished_start}.")
        await message.author.send(embed=data_send)
        driver.close()

    if message.content.startswith('!ping ') or message.content == "!ping":
        msg = "{0.author.mention} pong!".format(message)
        msg = f"{msg} ({client.latency} sec)"
        await message.channel.send(msg)

    if message.content.startswith("!auth ") or message.content == "!auth":
        if not isinstance(message.channel, discord.channel.DMChannel):
            await message.channel.send(f"Message isn't in dms!")
            return

        try:
            message.content.split()[1].split(':')
        except:
            await message.author.send("- Formatting error. (!auth email:password)")
            return

        with open(datafile_path, "r") as file:
            all_text = ""
            for line in file:
                a = line.split(":")
                # print(str(message.author) == a[0], message.author, a[0])
                if str(message.author) == a[0]:
                    msg1 = discord.Embed(
                        title="__Auth Response__",
                        description=f"Already authenticated!\n"
                    )
                    await message.author.send(embed=msg1)
                    return
                all_text += line[:len(line)]

            with open(datafile_path, "w") as file2:
                file2.write(
                    f"{all_text}{message.author}:{message.content.split()[1].split(':')[0]}:"
                    f"{message.content.split()[1].split(':')[1]}:\n")
                msg1 = discord.Embed(
                    title="__Auth Response__",
                    description=f"Authenticated!\n"
                )
                print(f"{message.author} authenticated!")
                await message.author.send(embed=msg1)


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    print(f"Logging in took: {datetime.datetime.now() - time_start}.\n")


client.run(bot_token)
