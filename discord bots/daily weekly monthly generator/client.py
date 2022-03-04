import configparser
import discord
from discord.ext import commands
import time
import datetime
import requests

# Server lib
import mysql.connector
# Import functions from our mysql_server_initializing.py
import mysql_server_initializing as sv_helper

owner_id = 'owner_id'

# Read our bot token from config file
config = configparser.ConfigParser()
config.read('settings.ini')
token = config['DEFAULT']['token']

sv_helper.check_if_database_exists()

# Declare intents and initialize client
intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.command()
async def stock(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) and str(ctx.message.author.id) == owner_id:
        with open('data.txt', 'r') as file:
            await ctx.send(f'Current stock: {len(file.readlines())}')
            file.close()

            
@client.command()
async def clear(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) and str(ctx.message.author.id) == owner_id:
        with open('data.txt', 'r+') as file:
            file.truncate(0)
            file.seek(0)
            file.close()
            
            
@client.command()
async def refill(ctx):
    # Return if userid isnt owner or isnt in dms
    if isinstance(ctx.channel, discord.channel.DMChannel) and str(ctx.message.author.id) == owner_id:
        if ctx.message.attachments:
            file_url = requests.get(ctx.message.attachments[0].url, stream=True)
            if file_url.status_code == 200:

                url_content = file_url.text
                with open('data.txt', 'r+') as f:
                    before_lines = f.readlines()
                    if len(before_lines) == 0:
                        f.write(f'{url_content}')
                    else:
                        f.write(f'\n{url_content}')
                    f.close()
                    sv_helper.fix_datafile_spacing()

                    file = open('data.txt', 'r')
                    after_lines = file.readlines()
                    file.close()
                    await ctx.send(f'Successfully saved {len(after_lines) - len(before_lines)} entries.')
            else: await ctx.send('Couldn\'t fetch file from discord servers. Please try again later.')
        else: await ctx.send('Please attach **1** file (formatted as .txt).')

@client.command()
async def dgen(ctx):
    #Daily gen command
    
    user_id = ctx.message.author.id
    user_exists = False

    # connect to database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='generator_db'
    )

    # select our 'users' database
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM `users`')
    for x in cursor:
        if str(x[0]) == str(user_id):
            user_exists = True
    
    if not user_exists:
        cursor.execute(f"""
        INSERT INTO `users` (userid, unixtime_daily, unixtime_weekly, unixtime_monthly)
        VALUES ({user_id}, {0}, {0}, {0});
        """)
        mydb.commit()
    
    cursor.execute(f'SELECT * FROM `users` WHERE userid={user_id}')
    myresult = cursor.fetchall()
    last_use = int(myresult[0][1]) # daily cooldown

    delta = datetime.timedelta(seconds=(86400 - (int(time.time()) - last_use)))
    delta_text = ''
    hours = delta.days * 24 + delta.seconds/3600
    minutes = float('0.' + str(hours).split('.')[1]) * 60
    seconds = int(str(float('0.' + str(minutes).split('.')[1]) * 60).split('.')[0])
    hours = int(str(hours).split('.')[0])
    minutes = int(str(minutes).split('.')[0])
    delta_text += f'{hours} hour{hours > 1 and "s" or ""}, {minutes} minute{minutes != 1 and "s" or ""}, {seconds} second{seconds != 1 and "s" or ""} ' 

    file = open('data.txt', 'r')


    if int(time.time()) - last_use > 86400:
        if len(file.readlines()) >= 1:

            cursor.execute(f"""
            UPDATE `users` 
            SET unixtime_daily = '{int(time.time())}'
            WHERE userid = {user_id};
            """)
            mydb.commit()

            code = sv_helper.return_and_delete()

            await ctx.send(code)
        else:
            await ctx.send(f'Daily entry is not available right now. Please try again later. (Stock: {len(file.readlines())})')
    else:
        await ctx.send(f'Using too frequently! (wait {delta_text})')


@client.command()
async def wgen(ctx):
    # Weekly gen command
    
    user_id = ctx.message.author.id
    user_exists = False

    # connect to database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='generator_db'
    )

    # select our 'users' database
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM `users`')
    for x in cursor:
        if str(x[0]) == str(user_id):
            user_exists = True
    
    if not user_exists:
        cursor.execute(f"""
        INSERT INTO `users` (userid, unixtime_daily, unixtime_weekly, unixtime_monthly)
        VALUES ({user_id}, {0}, {0}, {0});
        """)
        mydb.commit()
    
    cursor.execute(f'SELECT * FROM `users` WHERE userid={user_id}')
    myresult = cursor.fetchall()
    last_use = int(myresult[0][2]) # weekly cooldown

    delta = datetime.timedelta(seconds=(604800 - (int(time.time()) - last_use)))
    delta_text = ''
    hours = delta.days * 24 + delta.seconds/3600
    minutes = float('0.' + str(hours).split('.')[1]) * 60
    seconds = int(str(float('0.' + str(minutes).split('.')[1]) * 60).split('.')[0])
    hours = int(str(hours).split('.')[0])
    minutes = int(str(minutes).split('.')[0])
    delta_text += f'{hours} hour{hours > 1 and "s" or ""}, {minutes} minute{minutes != 1 and "s" or ""}, {seconds} second{seconds != 1 and "s" or ""} ' 

    file = open('data.txt', 'r')
    
    if int(time.time()) - last_use > 604800:
        if len(file.readlines()) >= 3:
            cursor.execute(f"""
            UPDATE `users` 
            SET unixtime_weekly = '{int(time.time())}'
            WHERE userid = {user_id};
            """)
            mydb.commit()
            code1 = sv_helper.return_and_delete()
            code2 = sv_helper.return_and_delete()
            code3 = sv_helper.return_and_delete()
            
            await ctx.send(code1)
            await ctx.send(code2)
            await ctx.send(code3)
        else:
            await ctx.send(f'Weekly entries (3x) are not available right now. Please try again later. (Stock: {len(file.readlines())})')
    else:
        await ctx.send(f'Using too frequently! (wait {delta_text})')
    
    file.close()

@client.command()
async def mgen(ctx):
    # Monthly gen command
    
    user_id = ctx.message.author.id
    user_exists = False

    # connect to database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='generator_db'
    )

    # select our 'users' database
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM `users`')
    for x in cursor:
        if str(x[0]) == str(user_id):
            user_exists = True
    
    if not user_exists:
        cursor.execute(f"""
        INSERT INTO `users` (userid, unixtime_daily, unixtime_weekly, unixtime_monthly)
        VALUES ({user_id}, {0}, {0}, {0});
        """)
        mydb.commit()
    
    cursor.execute(f'SELECT * FROM `users` WHERE userid={user_id}')
    myresult = cursor.fetchall()
    last_use = int(myresult[0][3]) # monthly cooldown

    delta = datetime.timedelta(seconds=(2678400 - (int(time.time()) - last_use)))
    delta_text = ''
    hours = delta.days * 24 + delta.seconds/3600
    minutes = float('0.' + str(hours).split('.')[1]) * 60
    seconds = int(str(float('0.' + str(minutes).split('.')[1]) * 60).split('.')[0])
    hours = int(str(hours).split('.')[0])
    minutes = int(str(minutes).split('.')[0])
    delta_text += f'{hours} hour{hours > 1 and "s"}, {minutes} minute{minutes != 1 and "s" or ""}, {seconds} second{seconds != 1 and "s" or ""} ' 

    file = open('data.txt', 'r')
    
    if int(time.time()) - last_use > 2678400:
        if len(file.readlines()) >= 5:
            cursor.execute(f"""
            UPDATE `users` 
            SET unixtime_monthly = '{int(time.time())}'
            WHERE userid = {user_id};
            """)
            mydb.commit()

            code1 = sv_helper.return_and_delete()
            code2 = sv_helper.return_and_delete()
            code3 = sv_helper.return_and_delete()
            code4 = sv_helper.return_and_delete()
            code5 = sv_helper.return_and_delete()

            await ctx.send(code1)
            await ctx.send(code2)
            await ctx.send(code3)
            await ctx.send(code4)
            await ctx.send(code5)
        else:
            await ctx.send(f'Monthly entries (5x) are not available right now. Please try again later. (Stock: {len(file.readlines())})')
    else:
        await ctx.send(f'Using too frequently! (wait {delta_text})')
    
    file.close()


# Run the bot
client.run(token)
