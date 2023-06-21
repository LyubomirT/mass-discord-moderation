# MDM (Mass Discord Moderation)

MDM (Mass Discord Moderation) is a command-line interface (CLI) application built with Python and Py-Cord. It provides various moderation features to perform bulk actions on a Discord server. The app allows you to ban, unban, kick members, delete and edit roles, change member nicknames, delete and create channels, and more.

## Installation

To use MDM, you need to have Python and the required dependencies installed on your system. Follow these steps to set up the application:

1. Clone the repository:

   ```bash
   git clone https://github.com/LyubomirT/mass-discord-moderation.git
   ```

2. Navigate to the project directory:

   ```bash
   cd where/the/files/are/stored
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the MDM CLI application, execute the following command:

```bash
python mainRunner.py
```

Upon running the command, the application will prompt you to authenticate with your Discord Bot Token. If you don't have a token, you can follow the instructions provided to obtain one. After entering a valid token, the application will sign in to Discord and display a list of guilds (servers) the bot is added to. 

You can then enter commands to perform various moderation actions. The available commands are:

- `help`: Get help about how to use the bot.
- `mb` or `massban`: Ban all members in the selected guild below the bot in the hierarchy.
- `mu` or `massunban`: Unban all banned members in the selected guild.
- `mk` or `masskick`: Kick all members in the selected guild below the bot in the hierarchy.
- `mrd` or `massroledelete`: Delete all roles in the selected guild below the bot in the hierarchy.
- `mre` or `massroleedit`: Change something of all roles in the selected guild below the bot in the hierarchy to something else.
- `mnc` or `massnicknamechange`: Change the nicknames of all members in the selected guild below the bot in the hierarchy to something else.
- `mcd` or `masschanneldelete`: Delete all channels in the selected guild available to delete for the bot.
- `mce` or `masschanneledit`: Change something of all channels in the selected guild to something else.
- `mcc` or `masschannelcreate`: Create many channels specifying the setup for each of them in the selected guild.
- `mrc` or `massrolecreate`: Create many roles specifying the setup for each of them in the selected guild.
- `cg`: Change the guild where the changes will be applied.
- `exit`: Close the application.

Enter `help` within the application to get a list of commands and their descriptions.

## To-Do

 - [x] Split the code into different files
 - [x] Add message management options
 - [ ] Add interactions within discord
 - [ ] Compile the app into an executable
 - [ ] Create a GUI version

## Contributing

The MDM project welcomes contributions from the open-source community. If you would like to contribute to the project, you can follow these steps:

1. Fork the repository: Click on the "Fork" button on the GitHub repository page (https://github.com/LyubomirT/mass-discord-moderation) to create a personal copy of the project.

2. Clone the forked repository: Clone the forked repository to your local machine using the following command:

   ```bash
   git clone https://github.com/your-username/repo-name.git
   ```

3. Navigate to the project directory:

   ```bash
   cd mass-discord-moderation
   ```

4. Create a new branch: Create a new branch for your contribution. It is recommended to use a descriptive branch name related to the feature or bug fix you're working on. You can create a new branch using the following command:

   ```bash
   git checkout -b your-branch-name
   ```

5. Make changes: Make the desired changes to the codebase using your preferred code editor or IDE. You can refer to the existing code and project structure to understand how things are implemented.

6. Test your changes: Before submitting your contribution, ensure that the application is working as expected. Run the application and verify that the new features or bug fixes are functioning correctly.

7. Commit your changes: Once you are satisfied with your changes, commit them to your local repository using the following commands:

   ```bash
   git add .
   git commit -m "Your commit message"
   ```

8. Push your changes: Push your changes to your forked repository on GitHub using the following command:

   ```bash
   git push origin your-branch-name
   ```

9. Create a pull request: Go to the original repository on GitHub (https://github.com/LyubomirT/mass-discord-moderation) and click on the "Pull request" button to create a new pull request. Provide a descriptive title and explanation of your changes in the pull request description.

Of course, if you don't want to contribute  code, you can create an issue with a feature request, or with a bug report. 

## Disclaimer

It's important to note that the MDM application performs bulk moderation actions on Discord servers. To ensure responsible use, please ensure that you have the necessary permissions and authority to perform such actions on the servers you use it with. The creator of the app cannot take responsibility for how you use the app or for any consequences that may arise.

## License

The MDM application is open-source and licensed under the [BSD 3-Clause License](https://github.com/LyubomirT/mass-discord-moderation/blob/main/LICENSE).