# Needed libraries:
# Selenium: https://pypi.org/project/selenium/
# Discord.py: https://pypi.org/project/discord.py/ 
import discord
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

# replace bot_token with your bot token
# If you don't have a bot:
# Create an application in discord developer portal: https://discord.com/developers/applications
# create a bot for your application and replace bot_token with your bot token
bot_token = "your bot token"
options = webdriver.ChromeOptions()

# Download corresponding chrome driver from: https://chromedriver.chromium.org/downloads
# (chromedriver_win32.zip) and extract it anywhere.
# Replace the 2 fields with correct paths
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
chrome_driver_binary = r"C:\Users\riis\PycharmProjects\SeleniumTest\Browsers\chromedriver.exe"

client = discord.Client()

time_start = datetime.datetime.now()

@client.event
async def on_message(message):
    if not message.content.startswith("!hw"):
        print(f"{message.author}: {message.content}")
    else:
        print(f"{message.author} fetched data.")

    if message.author == client.user:
        return
    if message.content.startswith('!test'):
        msg = "{0.author.mention} initialized \"!test\"".format(message)
        await message.channel.send(msg)
    elif message.content.startswith("!help"):
        msg = discord.Embed(
            title=f"- __Help__",
            description=f"- !help -> sends this embed.\n"
                        f"- !hw -> sends homework from stuudium to your dms.\n"
                        f"- !ping -> pings the server.",
        )
        msg.set_author(name=message.author, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        msg.set_thumbnail(url="https://nrg.edu.ee/sites/nrg.edu.ee/files/styles/hitsa_core_logo/public/ruutjuurega_0"
                              ".png?itok=dNstk4JL")

        await message.channel.send(embed=msg)

    elif message.content.startswith("!hw"):
        if message.author == client.user:
            return

        if not isinstance(message.channel, discord.channel.DMChannel):
            await message.channel.send(f"Message isn't in dms!")
            return

        msg1 = discord.Embed(
            title="__Login Data__",
            description=f"Send your email and password in this format to get stuudium data:\n"
                        f"email:password\n\n"
                        f"If entered correctly, just wait a bit."
        )

        await message.author.send(embed=msg1)

        try:
            data = message.content.split()[1].split(":")

            data_send = discord.Embed(
                title="homework",
            )
            username = data[0]
            password = data[1]

            time_start = datetime.datetime.now()
            time_finished_start = datetime.datetime.now()
            driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
            driver.get("https://nrg.ope.ee/auth/")

            driver.find_element_by_class_name("username").send_keys(username)
            driver.find_element_by_class_name("password").send_keys(password)
            driver.find_element_by_class_name("button").send_keys(Keys.ENTER)
            time_end = datetime.datetime.now()

            print(
                f'Executed startup successfully. Waited {(time_end - time_start).microseconds / 1000000} seconds for '
                f'webpage '
                f'initialization.')
            time.sleep(5)

            todo_elements = driver.find_elements_by_class_name("todo_container")
            driver.find_element_by_class_name("show-future").click()
            time_start = datetime.datetime.now()
            subject_last_date = ""
            for element in todo_elements:
                subject_date = element.get_attribute("data-date")
                if subject_date != subject_last_date:
                    subject_last_date = subject_date
                    subject_date = subject_last_date.replace(str(datetime.datetime.now().year), '')
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

            print(f"Got all webelements in {time_delta.microseconds / 1000000} seconds.")
            print(f"Total: {datetime.datetime.now() - time_finished_start}.")
            await message.author.send(embed=data_send)
            time.sleep(20)
            driver.close()
        except:
            await message.author.send("Fetching failed. Is formatting correct?")
        finally:
            print(f"Message sent.")
    elif message.content.startswith('!ping'):
        msg = "{0.author.mention} pong!".format(message)
        msg = f"{msg} ({(datetime.datetime.now().microsecond - message.created_at.microsecond) / 10000} sec)"
        await message.channel.send(msg)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    print(f"Logging in took: {datetime.datetime.now() - time_start}.\n")

client.run(bot_token)
