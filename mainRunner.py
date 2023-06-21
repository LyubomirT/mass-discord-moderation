import threading
import os
import sys
import time
import discord
from discord.ext import commands
import customtkinter as ctk
import requests
import textwrap

def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')  # Clear screen for Windows
    else:
        os.system('clear')  # Clear screen for Unix-based systems


class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BLUE = '\033[94m'
    WARNING = '\033[93m'

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

token = None  # Define token as a global variable

def check_token_validity(token):
    headers = {
        'Authorization': f'Bot {token}'
    }
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    return response.status_code == 200


def runCLI():
    time.sleep(1)
    ascii_art = '''
\033[93m        .88b  d88.       d8888b.        .88b  d88. \033[0m
\033[93m        88'YbdP`88       88   `8D       88'YbdP`88 \033[0m
\033[93m        88  88  88       88    88       88   88  88 \033[0m
\033[93m        88  88  88       88    88       88   88  88 \033[0m
\033[93m        88  88  88       88   .8D       88  .8D  88 \033[0m
\033[93m        YP  YP  YP       Y8888D'        YP   YP  YP \033[0m

\033[93m                Mass Discord Moderation               \033[0m
    '''

    for line in ascii_art.splitlines():
        print(line)
        time.sleep(0.1)

    def getToken():
        global token
        token = input("\nAuthenticate with your token (leave empty if you don't have one): ")
        if token == '':
            print("To get a Discord Bot Token, follow these instructions:")
            print("1. Go to the Discord Developer Portal website: https://discord.com/developers/applications.")
            print("2. Log in to your Discord account or create a new one if you don't have an account.")
            print("3. Click on the 'New Application' button at the top right corner.")
            print("4. Give your application a name. This will be the name of your bot. For example, 'My Discord Bot.'")
            print("5. Click on the 'Create' button to create the application.")
            print("")
            print("Once you have created the application, follow the remaining steps in the portal to create a bot and obtain its token.")
            print("Make sure to treat your bot token like a password and keep it secure. Do not share it with anyone or include it in public code repositories.")
            print("")
            print("See more detailed instructions here: https://discord.com/developers/docs")
            getToken()
            return

        time.sleep(0.3)
        print("\nChecking token validity...")
        if check_token_validity(token):
            print(Color.GREEN + "Token Valid. Signing in..." + Color.ENDC)
            # Run the bot in a thread with the token
            bot_thread = threading.Thread(target=bot.run, args=(token,))
            bot_thread.start()
            return
        else:
            print(Color.FAIL + "Token Invalid. Please try again." + Color.ENDC)
            getToken()
            return
    getToken()

    cli_finished.set()

def switch_to_cli():
    clear_screen()
    app.destroy()
    # Start the CLI thread
    cli_thread = threading.Thread(target=runCLI)
    cli_thread.start()

app = ctk.CTk()
app.title("Confirmation")
app.geometry("300x200")

label = ctk.CTkLabel(app, text="Launch CLI", font=("Roboto", 20))   
label.pack(pady=20)

cli_button = ctk.CTkButton(app, text="Proceed", command=switch_to_cli)
cli_button.pack(pady=10)

# Flag or event to indicate if CLI functionality has finished
cli_finished = threading.Event()

app.mainloop()

@bot.event
async def on_ready():
    guilds = bot.guilds
    if guilds:
        def getGuild():
            clear_screen()
            print(Color.YELLOW + "The bot is added to the following guilds:" + Color.ENDC)
            for guildg in guilds:
                print(f'{Color.YELLOW}{guilds.index(guildg) + 1}. {guildg.name} | {guildg.id}{Color.ENDC}')
                time.sleep(0.1)
            guildNumber = input("\nEnter the number of the guild you want the manipulation to take place: ")
            try:
                if int(guildNumber) > len(guilds):
                    print(Color.FAIL + "Invalid guild number" + Color.ENDC)
                    getGuild()
                    return
                elif int(guildNumber) < 1:
                    print(Color.FAIL + "Invalid guild number" + Color.ENDC)
                    getGuild()
                    return
                else:
                    global guild
                    guild = guilds[int(guildNumber) - 1]
                    clear_screen()
                    print(Color.YELLOW + "Please enter your commands below. Type 'help' for a list of commands" + Color.ENDC)
                    return
            except:
                print(Color.FAIL + "Invalid guild number" + Color.ENDC)
                getGuild()
                return
        
        getGuild()
    else:
        clear_screen()
        print(Color.WARNING + "The bot is not added to any guilds (servers). Please consider adding the bot to a server for this to work." + Color.ENDC)
        return

    # Set the flag or event to indicate that the CLI functionality has finished
    Cli_options = {
        "help": ["get help about how to use the bot", None],
        "mb": ["ban all members in the selected guild below the bot in the hierarchy", None],
        "mu": ["unban all banned members in the selected guild", None],
        "mk": ["kick all members in the selected guild below the bot in the hierarchy", None],
        "mrd": ["delete all roles in the selected guild below the bot in the hierarchy", None],
        "mre": ["change something of all roles in the selected guild below the bot in the hierarchy to something else", ["role_name", "color", "hoist", "mentionable"]],
        "mnc": ["change the nicknames of all members in the selected guild below the bot in the hierarchy to something else", ["member_id", "nickname"]],
        "mcd": ["delete all channels in the selected guild, available to delete for the bot", None],
        "mce": ["change something of all channels in the selected guild to something else", ["channel_id", "name", "topic"]],
        "mcc": ["create many channels specifying the set up for each of them in the selected guild", ["name", "topic", "channel_type", "amount"]],
        "mrc": ["create many roles specifying the set up for each of them in the selected guild", ["role_name", "color", "hoist", "mentionable", "amount"]],
        "cg": ["change the guild where the changes will be applied", ["guild_id"]],
        "exit": ["closes the app", None]
    }

    def getOption():
        option = input()
        option = option.strip()
        command = option.split()[0]
        params = option.split()[1:]
        return command, params

    command, params = getOption()

    while command != 'exit':
        if command == 'help':
            print("List of commands:")
            print("Name                          Description                                   Parameters\n")
            for command, data in Cli_options.items():
                description = data[0]
                parameters = data[1]
                parameter_string = ", ".join(parameters) if parameters else "None"

                # Wrap the description to a maximum width of 60 characters
                wrapped_description = textwrap.wrap(description, width=30)

                # Print the command, wrapped description, and parameters
                print(f"{Color.BLUE}{command.ljust(30)}{Color.ENDC}{wrapped_description[0].ljust(30)}                {Color.YELLOW}{parameter_string}{Color.ENDC}")
                
                # Print additional lines if the description is longer than one line
                if len(wrapped_description) > 1:
                    for line in wrapped_description[1:]:
                        print(" " * 30 + line.ljust(30))
                
                print("\n")

        elif command == 'cg':
            getGuild()
        elif command == 'mb' or command == 'massban':
            await mass_ban()
        elif command == 'mu' or command == 'massunban':
            await mass_unban()
        elif command == 'mk' or command == 'masskick':
            await mass_kick()
        elif command == 'mrd' or command == 'massroledelete':
            await mass_role_delete()
        elif command == 'mre' or command == 'massroleedit':
            await mass_role_edit(params)
        elif command == 'mnc' or command == 'massnicknamechange':
            await mass_nickname_change(params)
        elif command == 'mcd' or command == 'masschanneldelete':
            await mass_channel_delete()
        elif command == 'mce' or command == 'masschanneledit':
            await mass_channel_edit(params)
        elif command == 'mcc' or command == 'masschannelcreate':
            await mass_channel_create(params)
        elif command == 'mrc' or command == 'massrolecreate':
            await mass_role_create(params)
        else:
            print("Invalid command. Type 'help' for a list of commands.")
        
        command, params = getOption()

    os._exit(0) 

@bot.event
async def mass_ban():
    for member in guild.members:
        try:
            if member != guild.me:
                await member.ban()
        except discord.errors.Forbidden:
            pass
    print(Color.GREEN + "All members except me have been banned. If there are some remaining members, means I don't have permission to ban them" + Color.ENDC)

@bot.event
async def mass_unban():
    banned_users = guild.bans()
    banned_members = [ban_entry.user async for ban_entry in banned_users]
    
    print(banned_members)
    
    if not banned_members:
        print(Color.FAIL + "There are no banned users on this guild." + Color.ENDC)
        return
    
    for banned_member in banned_members:
        try:
            await guild.unban(banned_member)
            print(Color.YELLOW + "User " + str(banned_member.name) + " has been unbanned." + Color.ENDC)
        except discord.errors.Forbidden:
            print(Color.FAIL + "I don't have permissions to unban members" + Color.ENDC)
            return
    
    print(Color.GREEN + "All banned users have been unbanned." + Color.ENDC)

@bot.event
async def mass_kick():
    for member in guild.members:
        if member != guild.me:
            try:
                await member.kick()
                print(Color.YELLOW + "User " + str(member.name) + " has been kicked." + Color.ENDC)
            except discord.errors.Forbidden:
                print(Color.FAIL + "I don't have permissions to kick the member " + member.name + Color.ENDC)
    print(Color.GREEN + "All members except me have been kicked. If there are some remaining members, means I don't have permission to kick them" + Color.ENDC)

@bot.event
async def mass_role_delete():
    for role in guild.roles:
            try:
                await role.delete()
                print(Color.YELLOW + "Role " + str(role.name) + " has been deleted." + Color.ENDC)
            except discord.errors.Forbidden:    
                print(Color.FAIL + "I don't have permissions to delete the role " + role.name + Color.ENDC)
            except discord.errors.NotFound:
                pass
            except discord.errors.HTTPException:
                pass
    print(Color.GREEN + "All roles below my top role have been deleted. If there are some remaining roles, means I don't have permission to delete them" + Color.ENDC)

@bot.event
async def mass_role_edit(params):
    role_name = params[0] if len(params) >= 1 else None
    color = params[1] if len(params) >= 2 else None
    hoist = params[2] if len(params) >= 3 else None
    mentionable = params[3] if len(params) >= 4 else None

    for role in guild.roles:
        if role < guild.me.top_role:
            try:
                if role_name is not None:
                    await role.edit(name=role_name)
                    print(Color.YELLOW + "Role " + str(role.name) + "'s name has been edited to " + str(role_name) + "." + Color.ENDC)
                if color is not None:
                    await role.edit(colour=color)
                    print(Color.YELLOW + "Role " + str(role.name) + "'s colour has been edited to " + str(color) + "." + Color.ENDC)
                if hoist is not None:
                    await role.edit(hoist=hoist)
                    print(Color.YELLOW + "Role " + str(role.name) + "'s hoist has been edited to " + str(hoist) + "." + Color.ENDC)
                if mentionable is not None:
                    await role.edit(mentionable=mentionable)
                    print(Color.YELLOW + "Role " + str(role.name) + "'s mentionable has been edited to " + str(mentionable) + "." + Color.ENDC)
            except discord.errors.Forbidden:
                print(Color.FAIL + "I don't have permissions to edit the role " + role.name + Color.ENDC)
                pass

    print(Color.GREEN + "All roles below my top role have been edited. If some roles are unchanged means I don't have permission to edit them" + Color.ENDC)

@bot.event
async def mass_nickname_change(params):
    member_id = params[0] if len(params) >= 1 else None
    nickname = params[1] if len(params) >= 2 else None

    for member in guild.members:
        if member != guild.me:
            if member_id is None or member.id == int(member_id):
                try:
                    await member.edit(nick=nickname)
                    print(Color.YELLOW + "Member " + str(member.name) + " has been changed to " + str(nickname) + "." + Color.ENDC)
                except discord.errors.Forbidden:
                    print(Color.FAIL + "I don't have permissions to change the nickname of member " + member.name + Color.ENDC)
                    pass

    print(Color.GREEN + "All members' nicknames below me have been changed. If some nicknames are unchanged means I don't have permission to change them" + Color.ENDC)

@bot.event
async def mass_channel_delete():
    for channel in guild.channels:
        if channel.permissions_for(guild.me).manage_channels:
            try:
                await channel.delete()
                print(Color.YELLOW + "Channel " + str(channel.name) + " has been deleted." + Color.ENDC)
            except discord.errors.Forbidden:
                print(Color.FAIL + "I don't have permissions to delete the channel " + channel.name + Color.ENDC)
                pass
    print(Color.GREEN + "All channels have been deleted. If there are some remaining channels, means I don't have permission to delete them" + Color.ENDC)

@bot.event
async def mass_channel_edit(params):
    channel_id = params[0] if len(params) >= 1 else None
    name = params[1] if len(params) >= 2 else None
    topic = params[2] if len(params) >= 3 else None

    for channel in guild.channels:
        if channel.permissions_for(guild.me).manage_channels and (channel_id is None or channel.id == int(channel_id)):
            if name is not None:
                await channel.edit(name=name)
                print(Color.YELLOW + "Channel " + str(channel.name) + "'s name has been edited to " + str(name) + "." + Color.ENDC)
            if topic is not None:
                await channel.edit(topic=topic)
                print(Color.YELLOW + "Channel " + str(channel.name) + "'s topic has been edited to " + str(topic) + "." + Color.ENDC)
        else:
            print(Color.FAIL + "I don't have permissions to edit the channel " + channel.name + Color.ENDC)
            continue
            

    print(Color.GREEN + "All channels have been edited. If some channels are unchanged means I don't have permission to edit them" + Color.ENDC)

@bot.event
async def mass_channel_create(params):
    name = params[0] if len(params) >= 1 else None
    topic = params[1] if len(params) >= 2 else None
    channel_type = params[2] if len(params) >= 3 else None
    amount = params[3] if len(params) >= 4 else 10

    try:
        amount = int(amount)
    except:
        print(Color.FAIL + "Seems like the amount parameter is not an integer" + Color.ENDC)
        return

    if channel_type not in ['text', 'voice', 'category']:
        print(Color.FAIL + "Please specify a channel type. Must be 'text', 'voice', or 'category" + Color.ENDC)
        return
    if amount < 1 or amount > 50:
        print(Color.FAIL + "Please specify an amount between 1 and 50" + Color.ENDC)
        return
    if name is None:
        print(Color.FAIL + "Please specify a name" + Color.ENDC)
        return

    for i in range(amount):
        try:
            if channel_type == 'text':
                await guild.create_text_channel(name=name, topic=topic)
            elif channel_type == 'voice':
                await guild.create_voice_channel(name=name)
            elif channel_type == 'category':
                await guild.create_category(name=name)
            else:
                break
        except discord.errors.Forbidden:
            print(Color.FAIL + "I don't have permissions to create channels" + Color.ENDC)
            return

    print(Color.GREEN + f"Created {amount} {channel_type} channels with the name {name}." + Color.ENDC)

@bot.event
async def mass_role_create(params):
    if len(params) < 1:
        print(Color.FAIL + "Please specify at least one parameter" + Color.ENDC)
        return

    role_name = params[0]
    color = params[1] if len(params) >= 2 else None
    hoist = params[2] if len(params) >= 3 else False
    mentionable = params[3] if len(params) >= 4 else False
    amount = int(params[4]) if len(params) >= 5 else 10

    if amount < 1 or amount > 50:
        print(Color.FAIL + "Please specify an amount between 1 and 50" + Color.ENDC)
        return

    if mentionable not in ["true", "false"]:
        print(Color.FAIL + "Please specify a mentionable parameter in the form 'true' or 'false'" + Color.ENDC)
        return
    else:
        mentionable = mentionable.lower() == "true"

    if color is None:
        print(Color.FAIL + "Please specify a color in the form '#RRGGBB'" + Color.ENDC)
        return

    if hoist not in ["true", "false"]:
        print(Color.FAIL + "Please specify a hoist parameter in the form 'true' or 'false'" + Color.ENDC)
        return
    else:
        hoist = hoist.lower() == "true"

    try:
        color = discord.Color(int(color.replace("#", ""), 16))
    except ValueError:
        print(Color.FAIL + "Please specify a valid color in the form '#123456'" + Color.ENDC)
        return

    try:
        for _ in range(amount):
            await guild.create_role(name=role_name, color=color, hoist=hoist, mentionable=mentionable)
    except discord.errors.Forbidden:
        print(Color.FAIL + "I don't have permissions to create roles" + Color.ENDC)
        return

    print(Color.GREEN + amount + " Roles with the name " + role_name + " have been created." + Color.ENDC)


