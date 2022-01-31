import os
import time
import discord
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# define browser driver options for better understanding
options = Options()
# don't run chrome as a window
options.headless = False
# define chrome browser driver path
# initialize driver with custom options
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# bot intents in server
intents = discord.Intents.default()
client = discord.Client(intents=intents)

website = 'https://nrg.edupage.org/timetable/'


class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    # on message receive
    async def on_message(self, message):
        if message.author == self.user or not message.content.startswith('!tunniplaan'):
            return

        # make the string easier to work with
        content = message.content.replace('!tunniplaan', '')
        klass = '11b'
        if '10a' in content:
            klass = '10a'
        elif '10b' in content:
            klass = '10b'
        elif '10c' in content:
            klass = '10c'
        elif '11a' in content:
            klass = '11a'
        elif '11b' in content:
            klass = '11b'
        elif '11c' in content:
            klass = '11c'
        elif '12a' in content:
            klass = '12a'
        elif '12b' in content:
            klass = '12b'
        elif '12c' in content:
            klass = '12c'

        feedback = await message.reply(f'Leian tunniplaani {klass} jaoks...')

        driver.get(website)
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@title="Klass(id)"]')))
        klassid_btn = driver.find_element(By.XPATH, '//*[@title="Klass(id)"]')
        klassid_btn.click()
        # get all elements in class dropdown
        klassid_dropdown = driver.find_element(By.CLASS_NAME, 'dropDownPanel').find_elements(By.TAG_NAME, 'li')
        for element in klassid_dropdown:
            if element.text == klass:
                element.click()
        time.sleep(1)
        path = f'temp/tunniplaan{klass}.png'
        # take a screenshot of the page and save it to path
        driver.find_element(By.TAG_NAME, 'body').screenshot(path)
        await feedback.delete()
        await message.reply(file=discord.File(f'{os.getcwd()}/temp/tunniplaan{klass}.png'))


bot = Bot(command_prefix="!", self_bot=False)
bot.run('bot_token')
