import threading
import os
import sys
import time
import discord
from discord.ext import commands
import customtkinter as ctk
import logging
import textwrap
from utils.common import clear_screen, Color
from validation.token import check_token_validity
from bot.commands import *



bot = main()

token = None  # Define token as a global variable


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
            bot_thread = threading.Thread(target=bot.run, args=(token, ))
            logging.disable()
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