import datetime
import decimal
import time

import discord
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# bot token
bot_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

options = Options()
options.headless = True
driver_path = r"C:\Users\riis\PycharmProjects\stuudium_bot_recode\chromedriver.exe"

client = discord.Client()
bot_prefix = "!"


class helpers:
    connection = None
    cursor = None
    database = None
    username = None

    def connect_to_database_and_return_username_password(self, database, data=None):
        if data is None:
            data = {
                "username": None
            }
        self.database = database
        self.connection = mysql.connector.connect(user="root", password="p[]90", host="localhost", port=3306,
                                                  database="bot_schema", auth_plugin="mysql_native_password")
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        self.cursor.execute("SET SQL_SAFE_UPDATES=0")
        self.cursor.execute(f"SELECT * FROM bot_schema.userdata")
        self.username = str(data["username"])
        if data["username"]:
            should_send_error = True
            username_row = None
            for row in self.cursor:
                if self.username == row["discord"]:
                    should_send_error = False
                    username_row = row
                    break
            if should_send_error:
                return "err_user_not_found"

            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            return {
                "username": username_row["username"],
                "password": username_row["password"]
            }

    async def connect_to_database_and_send_automatic_homework(self, database, func):
        connection = mysql.connector.connect(user="root", password="p[]90", host="localhost", port=3306,
                                             database="bot_schema",
                                             auth_plugin="mysql_native_password")
        self.cursor = connection.cursor(buffered=True, dictionary=True)
        self.cursor.execute("SET SQL_SAFE_UPDATES=0")
        self.cursor.execute(f"SELECT * FROM bot_schema.{database}")

        for row in self.cursor:
            userid = int(decimal.Decimal(row["userid"]))
            try:
                user = await func(user_id=userid)
            except:
                try:
                    userid = userid + 1
                    user = await func(user_id=userid)
                except:
                    try:
                        userid = userid - 2
                        user = await func(user_id=userid)
                    except:
                        print("no")
                        return "err_no_user_found"
            await bot_client().debug(f"[ func 'auto_message()' ] sending message to {user}.")
            await bot_client().send_homework(message=None, author=user)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def stuudium_return_homework_data(stuudium_username, stuudium_password, homework_filter):
        driver_homework = webdriver.Chrome(driver_path, options=options)
        driver_homework.get("https://nrg.ope.ee/auth/")
        driver_homework.maximize_window()
        driver_homework.find_element(By.CLASS_NAME, "username").send_keys(stuudium_username)
        driver_homework.find_element(By.CLASS_NAME, "password").send_keys(stuudium_password)
        driver_homework.find_element(By.CLASS_NAME, "button").send_keys(Keys.ENTER)
        time.sleep(1)
        only_today = False
        only_all = False

        if homework_filter is None:
            print("Filtering only tomorrow")
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")
        elif homework_filter == "today":
            print("Filtering only today")
            only_today = True
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")
        elif homework_filter == "all":
            print("Filtering only all")
            only_all = True
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")

        try:
            # driver_hw.find_element_by_class_name("show-future").click()
            driver_homework.find_element(By.XPATH, "//*[contains(@class, \"show-future\")]").click()
        except:
            pass

        homework = []
        for element in todo_elements:
            elem = element.find_element(By.CLASS_NAME, "todo")

            subject_date = element.get_attribute("data-date").replace(str(datetime.datetime.now().year), '')
            subject_date = subject_date.replace(str((datetime.datetime.now() + datetime.timedelta(days=365)).year), '')

            should_continue = False
            if homework_filter is None or only_today:
                today_day = str((datetime.date.today()).day)
                today_month = str((datetime.date.today()).month)
                tomorrow_day = str((datetime.date.today() + datetime.timedelta(days=1)).day)
                tomorrow_month = str((datetime.date.today() + datetime.timedelta(days=1)).month)

                if len(today_day) < 2:
                    today_day = "0" + today_day
                if len(today_month) < 2:
                    today_month = "0" + today_month
                if len(tomorrow_day) < 2:
                    tomorrow_day = "0" + tomorrow_day
                if len(tomorrow_month) < 2:
                    tomorrow_month = "0" + tomorrow_month

                if homework_filter is None and subject_date[:2] == tomorrow_month and subject_date[2:] == tomorrow_day:
                    should_continue = True
                elif only_today and subject_date[:2] == today_month and subject_date[2:] == today_day:
                    should_continue = True
            elif only_all:
                should_continue = True

            if should_continue:
                subject_name = elem.find_element(By.CLASS_NAME, "subject_name").text

                try:
                    subject_description = elem.find_element(By.CLASS_NAME, "todo_content").text
                except:
                    subject_description = " "
                if "Kontrolltöö" in elem.text:
                    subject_description = f"[KT] {subject_description}"
                homework.append({
                    "date": f"{subject_date[:2]}.{subject_date[2:]}",
                    "name": subject_name,
                    "desc": subject_description
                })
        driver_homework.close()
        return homework

    def connect_to_database_and_register_user(self, database, data=None):
        self.connection = mysql.connector.connect(user="root", password="p[]90", host="localhost", port=3306,
                                                  database="bot_schema",
                                                  auth_plugin="mysql_native_password")
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        self.cursor.execute("SET SQL_SAFE_UPDATES=0")
        self.cursor.execute(f"SELECT * FROM bot_schema.{database}")
        self.username = str(data['message'].author)

        existing_user = False
        for row in self.cursor:
            if self.username == row["discord"]:
                existing_user = True

        if existing_user:
            print("override")
            self.cursor.execute("UPDATE `userdata` SET `username` = %s, `password` = %s WHERE `discord` = %s",
                                (data['username'], data['password'], str(data['message'].author)))
            self.cursor.execute("SELECT * FROM bot_schema.authed_users")
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            return "succesfully_updated_userdata"
        else:
            print("new")
            self.cursor.execute("INSERT INTO `userdata` VALUES(%s,%s,%s)",
                                (self.username, data['username'], data['password']))
            self.cursor.execute("SELECT * FROM bot_schema.authed_users")
            self.cursor.execute(f"INSERT INTO `authed_users` VALUES(%s, %s);",
                                (self.username, data['message'].author.id))
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            return "succesfully_saved_userdata"

    def connect_to_database_and_wipe_data(self, username):
        self.connection = mysql.connector.connect(user="root", password="p[]90", host="localhost", port=3306,
                                                  database="bot_schema",
                                                  auth_plugin="mysql_native_password")
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        self.cursor.execute("SET SQL_SAFE_UPDATES=0")
        print(username)
        self.cursor.execute("DELETE FROM bot_schema.authed_users WHERE discord = %s", (username,))
        self.cursor.execute(f"DELETE FROM bot_schema.userdata WHERE discord = %s", (username,))

        self.connection.commit()
        self.cursor.close()
        self.connection.close()


class bot_client(discord.Client):
    async def debug(self, *message):
        print(*message)
        await self.get_channel(id=887632300148416524).send([*message])

    async def on_ready(self):
        await self.debug(f"Logged in as {self.user.name}")
        # client.loop.create_task(self.auto_message())

    @staticmethod
    async def send_homework(message, author=None):
        if message is None:
            author = author
            user = author
        else:
            author = message.author
            user = message.channel

        returned_data = helpers().connect_to_database_and_return_username_password(
            database="userdata",
            data={
                "username": author
            }
        )

        if returned_data == "err_user_not_found":
            await user.send(embed=discord.Embed(
                title="__Not authenticated!__",
                description=f"Send your email and password in this format to get stuudium data:\n"
                            f"!auth email:password\n\n"
            ))
            return

        request_type = "today"
        if message is not None and len(message.content) > 4:
            s = message.content.split(" ")
            if "all" == s[1]:
                request_type = "all"
            elif "tomorrow" in s[1]:
                request_type = "next_day"
            elif "today" in s[1]:
                request_type = "today"

        waiting_msg = await user.send("Gathering data, please wait (~1 second).")
        hw = helpers().stuudium_return_homework_data(
            returned_data["username"],
            returned_data["password"],
            homework_filter=request_type
        )

        data_send = discord.Embed(
            title=f"Homework for {author}",
        )
        for hw_data in hw:
            data_send.add_field(
                name=f"{hw_data['date']} | {hw_data['name']}",
                value=f"{hw_data['desc']}"
            )

        if not hw:
            data_send.add_field(
                name=f"No homework for {request_type}",
                value=f"Yay! (?)"
            )

        await waiting_msg.delete()
        await user.send(embed=data_send)

    @staticmethod
    async def send_help(message):
        commands = ["help", "hw", "auth", "msgs", "deauth"]
        help_tabs = {
            "help": {
                "name": "help",
                "desc": "Returns information about commands.",
                "usage": f"Usage: \n `{bot_prefix}help [optional: command name]`"
            },
            "hw": {
                "name": "homework",
                "desc": "Returns homework data from stuudium.",
                "usage": f"Usage: \n `{bot_prefix}hw [optional: time (today | tomorrow | all)]`"
            },
            "auth": {
                "name": "authenticate",
                "desc": "Authenticates user with given username and password for stuudium.",
                "usage": f"Usage: \n `{bot_prefix}auth username:password`"
            },
            "msgs": {
                "name": "messages",
                "desc": "Returns messages from stuudium.",
                "usage": f"Usage: \n `{bot_prefix}msgs`"
            },
            "deauth": {
                "name": "deauthorize",
                "desc": "Removes your data from the server and forbids you from using commands.",
                "usage": f"Usage: \n `{bot_prefix}deauth`"
            },
        }

        if len(message.content) > 6:
            command_name = message.content.split(" ")[1]

            if command_name in commands:
                data_send = discord.Embed(
                    title=f"**Help for command '{help_tabs[command_name]['name']}'**",
                    description=f"{help_tabs[command_name]['desc']} \n{help_tabs[command_name]['usage']}",
                )
            else:
                data_send = discord.Embed(
                    title=f"**Help for command '{help_tabs['help']['name']}'**",
                    description=f"{help_tabs['help']['desc']} \n{help_tabs['help']['usage']}",
                )
        else:
            help_commands = ""
            for cmd in commands:
                help_commands += f"- {bot_prefix + cmd}\n"

            data_send = discord.Embed(
                title=f"Help for {message.author}",
                description=help_commands,
            )

            data_send.set_footer(
                text=f"[+] Use `{bot_prefix}help command_name` to get more information about a command."
            )
        await message.channel.send(embed=data_send)

    @client.event
    async def on_message(self, message):
        # Ignoreeri "roboti" enda sõnumeid
        if message.author == self.user:
            return

        if len(message.content) == 3 and message.content == bot_prefix + "hw" or message.content.startswith("!hw "):
            await self.send_homework(message)

        elif len(message.content) == 5 and message.content == bot_prefix + "help" or message.content.startswith("!help "):
            await self.send_help(message)

        elif len(message.content) == 5 and message.content == bot_prefix + "auth" or message.content.startswith("!auth "):
            embed_pending_auth_msg = await message.channel.send(embed=discord.Embed(
                title=f"Authenticating {message.author}...",
                description="Please wait a moment."
            ))

            try:
                message.content.split(':')[1]
            except:
                # if message was incorrectly formatted, return out of the function
                await message.author.send("- Formatting error. (!auth email:password)")
                await embed_pending_auth_msg.delete()
                return
            username = message.content.split()[1].split(':')[0]
            password = message.content.split()[1].split(':')[1]
            request_state = helpers().connect_to_database_and_register_user(database="userdata", data={
                'username': username,
                'password': password,
                'message': message,
            })

            # request_state : succesfully_updated_userdata or succesfully_saved_userdata
            success_title = f"Successfully authenticated {message.author}!"
            print(request_state)
            if request_state == "succesfully_updated_userdata":
                success_description = f"Your last authentication was overriden."
            elif request_state == "succesfully_saved_userdata":
                success_description = f"You are now authenticated to use commands."

            await message.channel.send(embed=discord.Embed(
                title=success_title,
                description=success_description
            ))
            await embed_pending_auth_msg.delete()

        elif len(message.content) == 7 and message.content == bot_prefix + "deauth" or message.content.startswith("!deauth "):
            embed_pending_auth_msg = await message.channel.send(embed=discord.Embed(
                title=f"Deuthenticating {message.author}...",
                description="Please wait a moment."
            ))

            helpers().connect_to_database_and_wipe_data(username=str(message.author))

            await message.channel.send(embed=discord.Embed(
                title="Successfully deauthorized.",
                description="Your data has been wiped from the servers."
            ))
            await embed_pending_auth_msg.delete()

    async def auto_message(self):
        while True:
            curtime = datetime.datetime.now()
            if curtime.hour == 17 and curtime.minute == 0 and curtime.second == (0 or 1):
                print("running")
                await helpers().connect_to_database_and_send_automatic_homework(
                    database="authed_users",
                    func=self.fetch_user
                )


bot_client().run(bot_token)
