import mysql_connection as server
import stuudium_web as web

import discord
from discord.ext import commands


# bot token
bot_token = "ODgzMzA4MjA4MTEyOTUxMzU3.YTIC3w.U3BIBmcPrGIBh3h20aAC71fOspY"


intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@client.command()
async def hw(ctx, time=None):
    message = ctx

    author = message.author
    user = message.channel

    returned_data = server.connect_to_database_and_return_username_password(
        user_id=author.id
    )

    if returned_data == "err_user_not_found":
        await user.send(embed=discord.Embed(
            title="__Not authenticated!__",
            description=f"Send your email and password in this format to get stuudium data:\n"
                        f"!auth email password\n\n"
        ))
        return

    if time is not None and not time == 'today' and not time == 'all':
        request_type = None
    else: request_type = time

    waiting_msg = await user.send("Gathering data, please wait (~1 second).")
    hw = web.stuudium_return_homework_data(
        returned_data["username"],
        returned_data["password"],
        homework_filter=request_type
    )

    data_send = discord.Embed(
        title=f"Homework for {author}",
    )
    for hw_data in hw:
        data_send.add_field(
            name=f"{hw_data.date} | {hw_data.name}",
            value=f"{hw_data.desc}"
        )

    if not hw:
        if request_type is None: request_type = 'tomorrow'
        data_send.add_field(
            name=f"No homework for {request_type}",
            value=f"Yay! (?)"
        )

    await waiting_msg.delete()
    await user.send(embed=data_send)


@client.command()
async def msgs(ctx, filter_type=None, max_msgs=9):
    returned_data = server.connect_to_database_and_return_username_password(
        ctx.author.id
    )

    if returned_data == "err_user_not_found":
        await ctx.channel.send(embed=discord.Embed(
            title="__Failed to authenticate!__",
            description=f"Send your email and password in this format to get stuudium data:\n"
                        f"`!auth email password`\n\n"
        ))
        return

    type_messages = None
    if filter_type == 'unread':
        type_messages = "only-unread"

    waiting_msg = await ctx.channel.send("Gathering data, please wait (~1 second).")
    msgs = web.stuudium_return_message_data(
        returned_data['username'],
        returned_data['password'],
        type_messages,
        int(max_msgs),
    )

    data_send = discord.Embed(
        title=f"Messages for {ctx.author}",
    )
    for msg_data in msgs:
        data_send.add_field(
            name=f"{msg_data.date} | {msg_data.name}",
            value=f"{msg_data.desc}"
        )
    data_send.set_author(name="> hyperlink (click me)", url="https://nrg.ope.ee/suhtlus/")

    await waiting_msg.delete()
    await ctx.channel.send(embed=data_send)

@client.command()
async def grades(ctx, max_grades=9):
        returned_data = server.connect_to_database_and_return_username_password(
            ctx.author.id
        )

        if returned_data == "err_user_not_found":
            await ctx.channel.send(embed=discord.Embed(
                title="__Failed to authenticate!__",
                description=f"Send your email and password in this format to get stuudium data:\n"
                            f"`!auth email password`\n\n"
            ))
            return

        waiting_msg = await ctx.channel.send("Gathering data, please wait (~1 second).")

        grade_data = web.stuudium_return_grade_data(
            returned_data['username'],
            returned_data['password'],
            int(max_grades),
        )

        data_send = discord.Embed(
            title=f"Grades for {ctx.author}"
        )

        for grade in grade_data:
            data_send.add_field(
                name=grade.name,
                value=grade.grade
            )

        await waiting_msg.delete()
        await ctx.channel.send(embed=data_send)

@client.command()
async def help(ctx, command_name=None):
    message = ctx
    commands = ["help", "hw", "auth", "msgs", "deauth", "grades"]
    bot_prefix = await client.get_prefix(message)
    help_tabs = {
        "help": {
            "name": "help",
            "desc": "Returns information about commands.",
            "usage": f"Usage: \n `{bot_prefix}help [optional: command name]`"
        },
        "hw": {
            "name": "homework",
            "desc": "Returns homework data from stuudium.",
            "usage": f"Usage: \n `{bot_prefix}hw [optional: time (today, tomorrow, all) | default: tomorrow]`"
        },
        "auth": {
            "name": "authenticate",
            "desc": "Authenticates user with given username and password for stuudium.",
            "usage": f"Usage: \n `{bot_prefix}auth username password`"
        },
        "msgs": {
            "name": "messages",
            "desc": "Returns messages from stuudium.",
            "usage": f"Usage: \n `{bot_prefix}msgs [optional: type (default, unread)]`"
        },
        "deauth": {
            "name": "deauthorize",
            "desc": "Removes your data from the server and removes your access from using commands.",
            "usage": f"Usage: \n `{bot_prefix}deauth`"
        },
        "grades": {
            "name": "grades",
            "desc": "Returns your grades.",
            "usage": f"Usage: \n `{bot_prefix}grades [optional: number of grades to return | default: 9]`"
        },
    }

    if command_name:
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

@client.command()
async def auth(ctx, email, password):
    message = ctx

    author = message.author
    user = message.channel

    status = server.connect_to_database_and_register_user(
        userid = author.id,
        username = email,
        password = password
    )

    if status == 'succesfully_updated_userdata':
        await user.send(embed=discord.Embed(
            title="__Authenticated!__",
            description=f"Your data has been updated.\n"
                        f"You can now use the commands."
        ))
    elif status == 'succesfully_saved_userdata':
        await user.send(embed=discord.Embed(
            title="__Authenticated!__",
            description=f"Your data has been saved.\n"
                        f"You can now use the commands."
        ))
    else:
        await user.send(embed=discord.Embed(
            title="__Error!__",
            description=f"Something went wrong.\n"
                        f"Please try again."
        ))

@client.command()
async def deauth(ctx):
    status = server.connect_to_database_and_wipe_data(
        ctx.author.id
    )

    if status == 'deleted_userdata':
        await ctx.channel.send(embed=discord.Embed(
            title="__Deauthenticated!__",
            description=f"Your data has been removed.\n"
                        f"You can no longer use the commands."
        ))
    else:
        await ctx.channel.send(embed=discord.Embed(
            title="__Error!__",
            description=f"Something went wrong.\n"
                        f"Please try again."
        ))

client.run(bot_token)