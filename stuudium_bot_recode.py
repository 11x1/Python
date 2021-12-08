import time

import discord
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector

# bot token
bot_token = "***********************************************************"

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
        only_next_day = False

        if homework_filter is None:
            print("No filtering")
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")
        elif homework_filter == "today":
            print("Filtering only today")
            only_today = True
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")
        elif homework_filter == "next_day":
            print("Filtering only tomorrow")
            only_next_day = True
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
            if only_next_day or only_today:
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

                if only_next_day and subject_date[:2] == tomorrow_month and subject_date[2:] == tomorrow_day:
                    should_continue = True
                elif only_today and subject_date[:2] == today_month and subject_date[2:] == today_day:
                    should_continue = True
            else:
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


class bot_client(discord.Client):
    async def debug(self, *message):
        print(*message)
        await self.get_channel(id=887632300148416524).send([*message])

    async def on_ready(self):
        await self.debug(f"Logged in as {self.user.name}")

    @client.event
    async def on_message(self, message):
        # Ignoreeri "roboti" enda sõnumeid
        if message.author == self.user:
            return

        if len(message.content) == 3 and message.content == bot_prefix + "hw" or message.content.startswith(bot_prefix + "hw "):
            returned_data = helpers().connect_to_database_and_return_username_password(database="userdata", data={
                "username": message.author})
            if returned_data == "err_user_not_found":
                await message.channel.send(embed=discord.Embed(
                    title="__Not authenticated!__",
                    description=f"Send your email and password in this format to get stuudium data:\n"
                                f"!auth email:password\n\n"
                ))
                return

            request_type = None

            if len(message.content) > 4:
                s = message.content.split(" ")
                if "today" in s:
                    request_type = "today"
                elif "tomorrow" in s:
                    request_type = "next_day"
            waiting_msg = await message.channel.send("Gathering data, please wait (~1 second).")
            hw = helpers().stuudium_return_homework_data(returned_data["username"], returned_data["password"], homework_filter=request_type)
            print(hw)
            data_send = discord.Embed(
                title=f"Homework for {message.author}",
            )
            for hw_data in hw:
                data_send.add_field(
                    name=f"{hw_data['date']} | {hw_data['name']}",
                    value=f"{hw_data['desc']}"
                )
            await waiting_msg.delete()
            await message.channel.send(embed=data_send)


bot_client().run(bot_token)
