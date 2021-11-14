import discord
from discord.ext.tasks import loop
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import datetime
import time
import mysql.connector
import decimal
# import mariaDB

# bot token
bot_token = "************************.******.***************************"

# define browser driver options for better understanding
options = Options()
# don't run chrome as a window
options.headless = True
# define chrome browser driver path
driver_path = r"C:\Users\riis\PycharmProjects\PythonBot\browsers\chromedriver.exe"
# initialize driver with custom options
driver = webdriver.Chrome(driver_path, options=options)

# bot intents in server
intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot_prefix = "!"

"""
# kodu database, pooleli
cnx = mysql.connector.connect(user="root", password="12345", host="localhost", port=3306, database="bot_schema", auth_plugin="mysql_native_password")
cursor = cnx.cursor(buffered=True, dictionary=True)
cursor.execute("SET SQL_SAFE_UPDATES=0")
"""

# login time start
login_time_Start = datetime.datetime.now()


# Debug function to send logs to a discord channel
async def p(message):
    print(message)
    await client.get_channel(887632300148416524).send(message)


# on message send
@client.event
async def on_message(message):
    # time start for logging time
    time_help_start = datetime.datetime.now()
    time_start_help_ms = time_help_start.microsecond

    # database user
    database_discord = str(message.author)
    # database connect
    cnx = mysql.connector.connect(user="root", password="12345", host="localhost", port=3306, database="bot_schema",
                                  auth_plugin="mysql_native_password")
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("SET SQL_SAFE_UPDATES=0")
    cursor.execute("SELECT * FROM bot_schema.userdata")

    # message timestamp
    hour = message.created_at.hour
    minute = message.created_at.minute
    second = message.created_at.second

    # time formatting shit
    if message.created_at.hour < 10:
        hour = f"0{message.created_at.hour}"
    if message.created_at.minute < 10:
        minute = f"0{message.created_at.minute}"
    if message.created_at.second < 10:
        second = f"0{message.created_at.second}"

    # if message isn't related to homework command
    if not message.content.startswith("!hw " or message.content == "!hw"):
        # don't print message when using auth command
        # and when user is bot
        if message.author == client.user and not message.content.startswith("!auth "):
            # if message is in dm, print logs according to that
            if isinstance(message.channel, discord.channel.DMChannel):
                await p(f" [ {hour}:{minute}:{second} | DM ] Bot: {message.content}")
            elif not message.channel.id == 887632300148416524:
                await p(f" [ {hour}:{minute}:{second} | {message.channel.guild.name} ->"
                        f" {message.channel.name} ] Bot: {message.content}")
        else:
            # if message doesn't start with auth
            if not message.content.startswith("!auth "):
                #  if sent message is in dms or not, format printed message
                if isinstance(message.channel, discord.channel.DMChannel):
                    await p(f" [ {hour}:{minute}:{second} | DM ] {message.author}: {message.content}")
                else:
                    await p(f" [ {hour}:{minute}:{second} | {message.channel.guild.name} ->"
                            f" {message.channel.name} ] {message.author}: {message.content}")
            else:
                if isinstance(message.channel, discord.channel.DMChannel):
                    await p(f" [ {hour}:{minute}:{second} | DM ] {message.author} used !auth.")
                else:
                    await p(f" [ {hour}:{minute}:{second} | {message.channel.guild.name} ->"
                            f" {message.channel.name} ] {message.author} used !auth.")
    else:
        await p(f"{message.author} requested data from nrg.edu.ee/auth/.")

    # if bot sends message, fuck that
    if message.author == client.user:
        return

    # test command
    if message.content.startswith('!test ') or message.content == "!test":
        msg = "{0.author.mention} initialized \"!test\"".format(message)
        await message.channel.send(msg)

    # ██╗  ██╗███████╗██╗     ██████╗
    # ██║  ██║██╔════╝██║     ██╔══██╗
    # ███████║█████╗  ██║     ██████╔╝
    # ██╔══██║██╔══╝  ██║     ██╔═══╝
    # ██║  ██║███████╗███████╗██║
    # ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝
    #
    elif message.content.startswith("!help ") or message.content == "!help":
        # set message as embed
        msg = discord.Embed(
            title=f"- __Help__",
            description=f"- !help -> sends this embed\n"
                        f"- !auth -> authenticates you on the server (need to do before using !hw)\n"
                        f"- !hw -> sends homework from stuudium to your dms\n"
                        f"- !msgs -> sends all messages\n"
                        f"- !grades -> send latest 3 grades\n"
                        f"- !ping -> pings the server"
        )
        # set embed author to user that requested this shit + easter egg link :flushed:
        msg.set_author(name=message.author, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        # set embed thumbnail to nrg logo because i can
        msg.set_thumbnail(
            url="https://nrg.edu.ee/sites/nrg.edu.ee/files/styles/hitsa_core_logo/public/ruutjuurega_0"
                ".png?itok=dNstk4JL")
        time_delta = datetime.datetime.now() - time_help_start
        # set message footer to debug shit
        msg.set_footer(
            text=f"Response: {time_delta.microseconds / 1000000} sec | "
                 f"Total: {datetime.datetime.now().microsecond - time_start_help_ms} sec")
        # send embed
        await message.channel.send(embed=msg)

    # ██╗  ██╗██╗    ██╗
    # ██║  ██║██║    ██║
    # ███████║██║ █╗ ██║
    # ██╔══██║██║███╗██║
    # ██║  ██║╚███╔███╔╝
    # ╚═╝  ╚═╝ ╚══╝╚══╝
    #
    elif message.content.startswith("!hw ") or message.content == "!hw":
        if message.author == client.user:
            return

        # run browser
        driver_hw = webdriver.Chrome(driver_path, options=options)

        # define username and password variable
        username = ""
        password = ""

        # set should send error to true
        should_send_error = True

        # Select all from userdata datafile
        cursor.execute("select * from bot_schema.userdata")
        # iterate through each row
        for row in cursor:
            # if discord user is found, don't send error message
            if database_discord == row["discord"]:
                should_send_error = False

        # if author was not found, send error message
        if should_send_error:
            msg1 = discord.Embed(
                title="__Login Data__",
                description=f"Send your email and password in this format to get stuudium data:\n"
                            f"!auth email:password\n\n"
            )
            # send error embed
            await message.author.send(embed=msg1)
            # close out of the loop
            return

        # open datafile with usernames and passwords
        cursor.execute("SELECT * FROM bot_schema.userdata")
        for row in cursor:
            # if discord user is found, set shit
            if database_discord == row["discord"]:
                username = row["username"]
                password = row["password"]

        await p(f"[DEBUG] {message.author} used hw. email@: {username}")

        # initialize embed
        data_send = discord.Embed(
            title=f"Homework for {message.author}",
        )

        # define time start for getting web elements for homework
        # time_start = datetime.datetime.now()
        time_finished_start = datetime.datetime.now()

        # load up the page in chrome
        driver_hw.get("https://nrg.ope.ee/auth/")
        driver_hw.maximize_window()
        # find website elements to log in
        driver_hw.find_element_by_class_name("username").send_keys(username)
        driver_hw.find_element_by_class_name("password").send_keys(password)
        driver_hw.find_element_by_class_name("button").send_keys(Keys.ENTER)
        # log in time
        # time_end = datetime.datetime.now()

        """
        print(
            f'Executed startup successfully. Waited {(time_end - time_start).microseconds / 1000000} seconds for '
            webpage '
            initialization.')
        """

        # send user message that the bot is working
        wait = await message.author.send("Fetching data...")

        # get all homework classes
        todo_elements = driver_hw.find_elements_by_class_name("todo_container")
        # try to get future homework
        try:
            driver_hw.find_element_by_class_name("show-future").click()
        except:
            # if we couldn't get future homework, send error message
            await message.author.send("Couldn't get homework. Is login data correct?")
            return

        # time start for getting homework elements
        time_start = datetime.datetime.now()

        # for each element in homework elements
        for element in todo_elements:
            elem = element.find_element_by_class_name("todo")

            # get subject date
            subject_date = element.get_attribute("data-date").replace(str(datetime.datetime.now().year), '')
            # print(f"Homework for {subject_date[:2]}.{subject_date[2:]}\n")

            # subject name and description
            subject_name = elem.find_element_by_class_name("subject_name").text

            # try to find hw description
            try:
                subject_description = elem.find_element_by_class_name("todo_content").text # elem.find_elements_by_xpath("//*[contains(@class, \"todo_content\")]")[hw_iter].text
            # can't find? set description blank
            except:
                subject_description = " "
            # if the homework is an exam, add a notification
            if "Kontrolltöö" in elem.text:
                subject_description = f"[KT] {subject_description}"
            # if subject_name != "":
            #   print(f"Subject : {subject_name}\nDescription: {subject_description}\n")

            # add homework field to embed
            data_send.add_field(
                name=f"{subject_date[2:]}.{subject_date[:2]} {subject_name}",
                value=subject_description,
            )

        # close browser
        driver_hw.close()
        # get time end phase
        time_end = datetime.datetime.now()
        # calculate time delta
        time_delta = time_end - time_start

        # debug footer for embed
        data_send.set_footer(
            text=f"Webelements: {time_delta.microseconds / 1000000} sec | "
                 f"Total: {datetime.datetime.now() - time_finished_start} sec")

        # debug message in console
        """
        print(f"Got all webelements in {time_delta.microseconds / 1000000} seconds.")
        print(f"Total: {datetime.datetime.now() - time_finished_start}.")
        """

        # send embed
        await message.author.send(embed=data_send)
        # delete "Fetching data..." message
        await wait.delete()

    # ██████╗ ██╗███╗   ██╗ ██████╗
    # ██╔══██╗██║████╗  ██║██╔════╝
    # ██████╔╝██║██╔██╗ ██║██║  ███╗
    # ██╔═══╝ ██║██║╚██╗██║██║   ██║
    # ██║     ██║██║ ╚████║╚██████╔╝
    # ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝
    #
    elif message.content.startswith('!ping ') or message.content == "!ping":
        msg = "{0.author.mention} pong!".format(message)
        msg = f"{msg} ({client.latency} sec)"
        # send message
        await message.channel.send(msg)

    #  █████╗ ██╗   ██╗████████╗██╗  ██╗
    # ██╔══██╗██║   ██║╚══██╔══╝██║  ██║
    # ███████║██║   ██║   ██║   ███████║
    # ██╔══██║██║   ██║   ██║   ██╔══██║
    # ██║  ██║╚██████╔╝   ██║   ██║  ██║
    # ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
    #
    elif message.content.startswith("!auth ") or message.content == "!auth":
        # if command isn't in dms send error
        if not isinstance(message.channel, discord.channel.DMChannel):
            await message.channel.send(f"Message isn't in dms!")
            return

        # split received message to save data
        try:
            message.content.split(':')[1]
        except:
            # if message was incorrectly formatted, return out of the function
            await message.author.send("- Formatting error. (!auth email:password)")
            return

        username = message.content.split()[1].split(':')[0]
        password = message.content.split()[1].split(':')[1]

        # open users datafile
        cursor.execute("SELECT * FROM bot_schema.userdata")
        for row in cursor:
            # if message author exists, override their auth data
            if database_discord == row["discord"]:
                # update datafile
                cursor.execute("UPDATE `userdata` SET `username` = %s, `password` = %s WHERE `discord` = %s",
                               (username, password, database_discord))
                cnx.commit()

                # sending embed (feedback msg)
                override_auth_message = discord.Embed(
                    title="__Auth Response__",
                    description=f"Overriding your last auth!\n"
                )
                await message.author.send(embed=override_auth_message)

            # else add them to database
            else:
                # add user to datafile
                cursor.execute("INSERT INTO `userdata` VALUES(%s,%s,%s)", (database_discord, username, password))
                await p("[DEBUG] Added to database.")
                cnx.commit()

            # user is authed successfully (feedback msg)
            auth_message = discord.Embed(
                title="",
                description=f"Authenticated!\n"
            )
            await message.author.send(embed=auth_message)
        message_author_id = str(message.author.id)
        cursor.execute("SELECT * FROM bot_schema.authed_users")
        try:
            cursor.execute("INSERT INTO `authed_users` VALUES((%s));" % message_author_id)
        except:
            return

    # ███╗   ███╗███████╗ ██████╗ ███████╗
    # ████╗ ████║██╔════╝██╔════╝ ██╔════╝
    # ██╔████╔██║███████╗██║  ███╗███████╗
    # ██║╚██╔╝██║╚════██║██║   ██║╚════██║
    # ██║ ╚═╝ ██║███████║╚██████╔╝███████║
    # ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚══════╝
    #
    elif message.content.startswith("!msgs") or message.content == "!msgs":
        # don't run if bot sent command
        if message.author == client.user:
            return

        # run browser
        driver_msgs = webdriver.Chrome(driver_path, options=options)

        # define username and password variable
        username = ""
        password = ""

        # set should send error to true
        should_send_error = True

        # Select all from userdata datafile
        cursor.execute("select * from bot_schema.userdata")
        # iterate through each row
        for row in cursor:
            # if discord user is found, don't send error message
            if database_discord == row["discord"]:
                should_send_error = False

        # if author was not found, send error message
        if should_send_error:
            msg1 = discord.Embed(
                title="__Login Data__",
                description=f"Send your email and password in this format to get stuudium data:\n"
                            f"!auth email:password\n\n"
            )
            # send error embed
            await message.author.send(embed=msg1)
            # close out of the loop
            return

        # open datafile with usernames and passwords
        cursor.execute("SELECT * FROM bot_schema.userdata")
        for row in cursor:
            # if discord user is found, set shit
            if database_discord == row["discord"]:
                username = row["username"]
                password = row["password"]

        # define message as discord embed
        data_send = discord.Embed(
            title=f"Messages for {message.author}",
        )

        # time shit for the command
        # time_start = datetime.datetime.now()
        time_finished_start = datetime.datetime.now()

        # open browser in login website -> redirect to messages website later
        driver_msgs.get("https://nrg.ope.ee/auth/?return=%2Fopen-inbox%3Fapp-return%3D%252F")

        # same shit vgfshjuoijhvdwfgjohgrwJHOGRWFJOFBSVOJIUP
        driver_msgs.find_element_by_class_name("username").send_keys(username)
        driver_msgs.find_element_by_class_name("password").send_keys(password)
        driver_msgs.find_element_by_class_name("button").send_keys(Keys.ENTER)
        # time_end = datetime.datetime.now()

        """
        print(
            f'Executed startup successfully. Waited {(time_end - time_start).microseconds / 1000000} seconds for '
            webpage '
            initialization.')
        """

        # send user feedback message, that the bot is working
        wait = await message.author.send("Fetching data...")
        time.sleep(1)

        # find all messages
        messages = driver_msgs.find_elements_by_class_name("post-main-wrapper")

        # debug timer
        time_start = datetime.datetime.now()

        # for each message in messages
        for element in messages:
            try:
                # define shit and give them values n shit
                author = element.find_element_by_class_name("post-author").text
                date = element.find_element_by_class_name("post-date").text
                title = element.find_element_by_class_name("post-title").text
                short_description = element.find_element_by_class_name("post-body-preview").text

                # if author, date and title exist, continue
                if not (author and date and title):
                    continue

                # add field to embed
                data_send.add_field(
                    name=f"{author} | {date} | {title}",
                    value=f"{short_description}...",
                )
            finally:
                continue

        # close browser
        driver_msgs.close()

        # time calculation shit
        time_end = datetime.datetime.now()
        time_delta = time_end - time_start

        # debug footer
        data_send.set_footer(
            text=f"Webelements: {time_delta.microseconds / 1000000} sec | "
                 f"Total: {datetime.datetime.now() - time_finished_start} sec")

        data_send.set_author(name="> hyperlink (click me)", url="https://nrg.ope.ee/suhtlus/")

        """
        print(f"Got all webelements in {time_delta.microseconds / 1000000} seconds.")
        print(f"Total: {datetime.datetime.now() - time_finished_start}.")
        """

        # send embed
        await message.author.send(embed=data_send)
        # delete earlier feedback message
        await wait.delete()

    #  ██████╗ ██████╗  █████╗ ██████╗ ███████╗███████╗
    # ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
    # ██║  ███╗██████╔╝███████║██║  ██║█████╗  ███████╗
    # ██║   ██║██╔══██╗██╔══██║██║  ██║██╔══╝  ╚════██║
    # ╚██████╔╝██║  ██║██║  ██║██████╔╝███████╗███████║
    #  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝
    #
    elif message.content.startswith("!grades") or message.content == "!grades":
        # yaya same shit
        if message.author == client.user:
            return

        # open browser
        driver_grds = webdriver.Chrome(driver_path, options=options)

        # define username and password variable
        username = ""
        password = ""

        # set should send error to true
        should_send_error = True

        # iterate through each row
        for row in cursor:
            # if discord user is found, don't send error message
            if database_discord == row["discord"]:
                should_send_error = False

        # if author was not found, send error message
        if should_send_error:
            msg1 = discord.Embed(
                title="__Login Data__",
                description=f"Send your email and password in this format to get stuudium data:\n"
                            f"!auth email:password\n\n"
            )
            # send error embed
            await message.author.send(embed=msg1)
            # close out of the loop
            return

        cursor.execute("SELECT * FROM bot_schema.userdata")
        # open datafile with usernames and passwords
        for row in cursor:
            # if discord user is found, set shit
            if database_discord == row["discord"]:
                username = row["username"]
                password = row["password"]

        # embed title
        data_send = discord.Embed(
            title=f"Grades for {message.author}",
        )

        #  debug time shit
        # time_start = datetime.datetime.now()
        time_finished_start = datetime.datetime.now()

        # open auth website
        driver_grds.get("https://nrg.ope.ee/auth/")

        # old shit
        driver_grds.find_element_by_class_name("username").send_keys(username)
        driver_grds.find_element_by_class_name("password").send_keys(password)
        driver_grds.find_element_by_class_name("button").send_keys(Keys.ENTER)
        # time_end = datetime.datetime.now()

        """
        print(
            f'Executed startup successfully. Waited {(time_end - time_start).microseconds / 1000000} seconds for '
            webpage '
            initialization.')
        """

        # feedback message
        wait = await message.author.send("Fetching data...")

        # get all grades classes
        grades = driver_grds.find_elements_by_class_name("stream-entry")

        try:
            # find older grades
            driver_grds.find_element_by_class_name("daily-summaries-navigate").click()
        except:
            # feedback message if everything fails
            await message.author.send("Couldn't get grades. Exiting.")
            return

        time_start = datetime.datetime.now()

        # define max grades
        max_grades = 2
        cur_grades = 0

        for element in grades:
            try:
                # max grades clamp
                if cur_grades > max_grades:
                    break

                # define grades subject and grade we got
                grade_subject = element.find_element_by_class_name("stream-entry-context").text
                grade_grade = element.find_element_by_class_name("grade-current").text

                # add field
                data_send.add_field(
                    name=f"{grade_subject}",
                    value=f"Hinne {grade_grade}",
                )
                cur_grades += 1
            finally:
                continue

        # close browser
        driver_grds.close()
        # debug timer
        time_end = datetime.datetime.now()
        time_delta = time_end - time_start

        # debug footer
        data_send.set_footer(
            text=f"Webelements: {time_delta.microseconds / 1000000} sec | "
                 f"Total: {datetime.datetime.now() - time_finished_start} sec")

        """
        print(f"Got all webelements in {time_delta.microseconds / 1000000} seconds.")
        print(f"Total: {datetime.datetime.now() - time_finished_start}.")
        """
        # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        await message.author.send(embed=data_send)
        # delete feedback message
        await wait.delete()

    cnx.commit()
    cursor.close()
    cnx.close()


@loop(seconds=1)
async def auto_message():
    curtime = datetime.datetime.now()
    tomorrow = curtime + datetime.timedelta(days=1)
    if curtime.hour == 17 and curtime.minute == 0 and curtime.second == (0 or 1):
        # database connect
        loop_cnx = mysql.connector.connect(user="root", password="p[]90", host="localhost", port=3306,
                                           database="bot_schema",
                                           auth_plugin="mysql_native_password")
        loop_cursor = loop_cnx.cursor(buffered=True, dictionary=True)
        loop_cursor.execute("SET SQL_SAFE_UPDATES=0")
        loop_cursor.execute("SELECT * FROM bot_schema.authed_users")
        for row in loop_cursor:
            userid = int(decimal.Decimal(row["userid"]))
            try:
                user = await client.fetch_user(userid)
                await p(f"[ DEBUG ] Sent {user} homework data.")
            except: # userid seems to be bugge from time to time so this is needed :/
                try:
                    userid = userid + 1
                    user = await client.fetch_user(userid)
                    await p(f"[ DEBUG ] Sent {user} homework data.")
                except:
                    try:
                        userid = userid - 2
                        user = await client.fetch_user(userid)
                        await p(f"[ DEBUG ] Sent {user} homework data.")
                    except:
                        print()
            try:
                await user.send("Kell on viis!")
            except:
                return

            # homework
            in_loop_cursor = loop_cnx.cursor(buffered=True, dictionary=True)
            in_loop_cursor.execute("SET SQL_SAFE_UPDATES=0")

            # run browser
            driver_hw = webdriver.Chrome(driver_path, options=options)

            # define username and password variable
            username = ""
            password = ""

            # set should send error to true
            should_send_error = True

            # Select all from userdata datafile
            in_loop_cursor.execute("select * from bot_schema.userdata")
            # iterate through each row
            for loop_row in in_loop_cursor:
                # if discord user is found, don't send error message
                if str(user) == loop_row["discord"]:
                    should_send_error = False

            # if author was not found, send error message
            if should_send_error:
                msg1 = discord.Embed(
                    title="__Login Data__",
                    description=f"Send your email and password in this format to get stuudium data:\n"
                                f"!auth email:password\n\n"
                )
                # send error embed
                await user.send(embed=msg1)
                # close out of the loop
                return

            # open datafile with usernames and passwords
            in_loop_cursor.execute("SELECT * FROM bot_schema.userdata")
            for loop_row in in_loop_cursor:
                # if discord user is found, set shit
                if str(user) == loop_row["discord"]:
                    username = loop_row["username"]
                    password = loop_row["password"]

            # initialize embed
            data_send = discord.Embed(
                title=f"Tomorrow's homework for {user}",
            )

            # define time start for getting web elements for homework
            # time_start = datetime.datetime.now()
            time_finished_start = datetime.datetime.now()

            # load up the page in chrome
            driver_hw.get("https://nrg.ope.ee/auth/")

            # find website elements to log in
            driver_hw.find_element_by_class_name("username").send_keys(username)
            driver_hw.find_element_by_class_name("password").send_keys(password)
            driver_hw.find_element_by_class_name("button").send_keys(Keys.ENTER)
            # log in time
            # time_end = datetime.datetime.now()

            """
            print(
                f'Executed startup successfully. Waited {(time_end - time_start).microseconds / 1000000} seconds for '
                webpage '
                initialization.')
            """

            # send user message that the bot is working
            wait = await user.send("Fetching data...")

            # get all homework classes
            todo_elements = driver_hw.find_elements_by_class_name("todo_container")
            # try to get future homework
            try:
                driver_hw.find_element_by_class_name("show-future").click()
            except:
                # if we couldn't get future homework, send error message
                await user.send("Couldn't get homework. Is login data correct?")
                return

            # time start for getting homework elements
            time_start = datetime.datetime.now()

            # for each element in homework elements
            for element in todo_elements:
                # get subject date
                subject_date = element.get_attribute("data-date").replace(str(datetime.datetime.now().year), '')
                # print(f"Homework for {subject_date[:2]}.{subject_date[2:]}\n")

                # subject name and description
                subject_name = element.find_element_by_class_name("subject_name").text
                subject_description = element.find_element_by_class_name("todo_content").text

                # if the homework is an exam, add a notification
                if "Kontrolltöö" in element.text:
                    subject_description = f"[KT] {subject_description}"
                # if subject_name != "":
                #   print(f"Subject : {subject_name}\nDescription: {subject_description}\n")

                # add homework field to embed
                work_day = subject_date[2:]
                work_month = subject_date[:2]
                if work_month[0] == "0":
                    work_month = work_month.replace("0", "")
                if work_day == str(tomorrow.day) and work_month == str(tomorrow.month):
                    data_send.add_field(
                        name=f"{subject_date[2:]}.{subject_date[:2]} {subject_name}",
                        value=subject_description,
                    )
            # close browser
            driver_hw.close()
            # get time end phase
            time_end = datetime.datetime.now()
            # calculate time delta
            time_delta = time_end - time_start

            # debug footer for embed
            data_send.set_footer(
                text=f"Webelements: {time_delta.microseconds / 1000000} sec | "
                     f"Total: {datetime.datetime.now() - time_finished_start} sec")

            # debug message in console
            """
            print(f"Got all webelements in {time_delta.microseconds / 1000000} seconds.")
            print(f"Total: {datetime.datetime.now() - time_finished_start}.")
            """

            # send embed
            await user.send(embed=data_send)
            # delete "Fetching data..." message
            await wait.delete()

        loop_cnx.commit()
        loop_cursor.close()
        loop_cnx.close()


# on client load send message
@client.event
async def on_ready():
    # database connect
    cnx = mysql.connector.connect(user="root", password="12345", host="localhost", port=3306, database="bot_schema",
                                  auth_plugin="mysql_native_password")
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("SET SQL_SAFE_UPDATES=0")

    # Main
    # cursor.execute("CREATE TABLE IF NOT EXISTS authed_users(userid DOUBLE NOT NULL PRIMARY KEY) ENGINE=storage_engine")

    """ALTER TABLE `bot_schema`.`authed_users` ADD PRIMARY KEY (`userid`);"""

    # Exit
    cnx.commit()
    cursor.close()

    # print login info
    await p(f"Logged in as {client.user.name}")
    # print how long it took to initialize bot
    await p(f"Logging in took: {datetime.datetime.now() - login_time_Start}.\n")
    auto_message.start()


# woo run bot
client.run(bot_token)
