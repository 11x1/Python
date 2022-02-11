from datetime import datetime

import discord
from discord import RequestsWebhookAdapter

omadisc = 'https://discord.com/api/webhooks/921371600396361738/UPsn1cVkg0m39VfUTlTovFHhsJRUTdBn84Oct8a5TU_hPxeFIYPrXWliFhFMNFgPJF2h'
klassidisc = 'https://discordapp.com/api/webhooks/921389875251527680/7tzKD2OW6qDWCbiykcpifjkB0tWIJzOSrOip9DQlIY1AvLGjOnn4Mh3gIHZ2XpBVDQi4/'

url_type = input('Select url (test or something else): ')
if 'test' in url_type:
    url = omadisc
elif 'klass' in url_type:
    url = klassidisc

webhook = discord.Webhook.from_url(url, adapter=RequestsWebhookAdapter())

title = input('Update name: ')
title = f'Code update | {title}'
file = input('Filename in current path: ')
has_url = input('Include reference url? (Y/N): ')
if has_url.lower() == 'y':
    ref_url = input('Reference url: ')

with open(file, 'r') as file:
    code = ''
    for line in file.readlines():
        code += line
    file.close()

timenow = datetime.now()
time = {
    'year': timenow.year,
    'month': timenow.month,
    'day': timenow.day,
    'hour': timenow.hour,
    'minute': timenow.minute
}

for keyvalue in time:
    time[keyvalue] = str(time[keyvalue])
    if len(time[keyvalue]) == 1:
        time[keyvalue] = f'0{time[keyvalue]}'

if has_url.lower() == 'y':
    embed = discord.Embed(
        title=title,
        url=ref_url,
        description=f'```py\n{code}```')
    embed.set_footer(
        text=f'Uploaded by khey#2341 on {time["year"]}-{time["month"]}-{time["day"]} [{time["hour"]}:{time["minute"]}]'
    )
else:
    embed = discord.Embed(
        title=title,
        description=f'```py\n{code}```')
    embed.set_footer(
        text=f'Uploaded by khey#2341 on {time["year"]}-{time["month"]}-{time["day"]} [{time["hour"]}:{time["minute"]}]'
    )

webhook.send(embed=embed)
