import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from utils.common import clear_screen, Color
import time
import textwrap
import os

def main():
    intents = discord.Intents.all()

    global bot
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.remove_command("help")


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
            "mmd": ["delete bulk messages in the selected channel", ["channel_id", "amount (optional)"]],
            "mms": ["send many messages in the selected channel", ["channel_id", "content (without spaces)", "amount (optional)"]],
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
            elif command == 'mmd' or command == 'massmessagedelete':
                await mass_message_delete(params)
            elif command == 'mms' or command == 'massmessagesend':
                await mass_message_send(params)
                
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

        print(Color.GREEN + str(amount) + " Roles with the name " + role_name + " have been created." + Color.ENDC)
    
    @bot.event
    async def mass_message_delete(params):
        if len(params) < 1:
            print(Color.FAIL + "Please specify at least one parameter" + Color.ENDC)
            return
        channel_id = params[0] if len(params) >= 1 else None
        if channel_id is None:
            print(Color.FAIL + "Please specify a channel ID" + Color.ENDC)
            return

        try:
            channel = guild.get_channel(int(channel_id))
        except:
            print(Color.FAIL + "Please specify a valid channel ID" + Color.ENDC)
            return
        # check if the channel is in the guild

        try:
            amount = int(params[1]) if len(params) >= 2 else 10
        except:
            print(Color.FAIL + "Please enter a valid number" + Color.ENDC)
            return
        
        if amount < 1 or amount > 50:
            print(Color.FAIL + "Please specify an amount between 1 and 50" + Color.ENDC)
            return
        
        for _ in range(amount):
            try:
                await channel.purge(limit=1)
                print(Color.YELLOW + f"Message {_ + 1} has been deleted" + Color.ENDC)
            except discord.errors.Forbidden:
                print(Color.FAIL + "I don't have permissions to delete messages" + Color.ENDC)
                return
        
        print(Color.GREEN + f"Deleted {amount} messages in the channel {channel.name}" + Color.ENDC)  
    
    @bot.event  
    async def mass_message_send(params):
        if len(params) < 1:
            print(Color.FAIL + "Please specify at least one parameter" + Color.ENDC)
            return
        channel_id = params[0] if len(params) >= 1 else None
        if channel_id is None:
            print(Color.FAIL + "Please specify a channel ID" + Color.ENDC)
            return
        content = params[1] if len(params) >= 2 else None
        if content is None:
            print(Color.FAIL + "Please specify a content" + Color.ENDC)
            return
        try:
            channel = guild.get_channel(int(channel_id))
        except:
            print(Color.FAIL + "Please specify a valid channel ID" + Color.ENDC)
            return
        try:
            amount = int(params[2]) if len(params) >= 3 else 10
        except:
            print(Color.FAIL + "Please enter a valid number" + Color.ENDC)
            return
        
        if amount < 1 or amount > 50:
            print(Color.FAIL + "Please specify an amount between 1 and 50" + Color.ENDC)
            return
        for _ in range(amount):
            try:
                await channel.send(content)
                print(Color.YELLOW + f"Message {_ + 1} has been sent" + Color.ENDC)
            except discord.errors.Forbidden:
                print(Color.FAIL + "I don't have permissions to send messages" + Color.ENDC)
                return
            
        print(Color.GREEN + f"Sent {amount} messages in the channel {channel.name}" + Color.ENDC)


    return bot


