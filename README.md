# Valheim-Shared-Offline-Server
<p align="center"><img src="https://img2.storyblok.com/fit-in/1920x1080/f/157036/6000x3337/61023ec07d/skepp.jpg" alt="Valheim official media from https://www.valheimgame.com/pt/#media" width="1000" height="556"/></p>

# 
A program made for the game Valheim that makes possible multiple players share the same world at any time, without the need of a dedicated server  UNFINISHED YET
Autor: João André A.
# Why use?
If you have a group of friends that you play Valheim with, you must know how annoying it is to be able to play in the world only when the world's owner is online to host. With this program, any player can have the current world save of the owner and host it for other players to join, at any time, independent of the original owner's availability. All the player's progress will be saved and can be loaded by any of the players after. It is basically how an open server works, but cost-free, with quick save and load operations for the shared world save and any player from the server can host.

# How it Works?
It is a Python .exe, the source-code is available for personal edit if you wish to and to guarantee it is not a malicious program. Sorry if the code is a bit messy, I made it in 3 days. You can transform the .py in .exe on your local machine, with "pyinstaller --onefile ValheimSharedOfflineServer.py" or run it on the compiler. The code works by creating a connection with a setted up Github repository, where the local saves will be exported once you close the game. When you or your friends logged in again, the save will be imported from the Github repository to the local machine, where you can host for others to join. On the program, you have the option to SAVE, LOAD, or CREATE NEW WORLD that will create a folder to hold a specific world's saves and backups on Github. Be aware that Github do not support files sizes greater than 100mb, so does this program's version, but rarely a world save will supass this size. The code will not run without the header folder with settings.json file also, you must configure this file before running the program. While only one person needs to set up the Github repository, every player should install this program to work as intended.
<p align="center"><img src="https://img2.storyblok.com/fit-in/1000x1000/f/157036/802x1054/9da9082a5f/reeds.png" alt="Valheim official media from https://www.valheimgame.com" width="200" height="263"/></p>

## How to Set up?
### STEP 1: 
Download this .zip repository and extract in any directory. You can delete .py file if you wish, but .exe and header/settings.json are vital. 

### STEP 2: 
Set up the Github repository that will save your world files. Someone of the players who will use the server need to have an account on Github and create an empty and PRIVATE repository. The repository name is arbitrary. After that, you will need a Github Token to access and edit this repository. This token can be a bit trick to find, so here is the path. Logged in on Github, go to the upper right corner in your Profile Pic -> Settings -> Developer settings -> Personal access tokens -> Fine-granted tokens -> Generate new token. Be sure to select **Only select repositores** and choose the repository you just created for security. After that, **Add permissions** to pull, create, update, delete files and folders. In doubt and if you trust who you will give access to this repository, select every permission and check "Read and Write". The token will only appear once, so copy and save it. That's all you need from Github, from now on, you can just run the code.

### STEP 3: 
Open the header folder and edit the settings.json the fields (always insert values in the double quotes. Ex: "steamID": "" will become "steamID": "9999999" don't delete any comma):
  - username -> The name that will identify you when you save the world into the server
  - steamID -> Your Steam code, the same you use to send to someone as a Friend Request. You can find it on Steam -> Friends -> Add Friends. Necessary if you save the world on the steam cloud, which is the default game setting 
  - saveMode -> You can leave it blank or set to cloud or local. This will specify where the world is saved and where to save it. Leave it blank if you want the program to ask if it is local save or cloud save each time you run
  - localSavePath -> Your local save directory. You don't need to change much, just edit <Your_Pc_Username> to your actual pc username if you want to save locally. NOTE: LOCAL SAVES WERE NOT TESTED PROPERLY IN THIS VERSION
  - cloudSavePath -> Your cloud save directory. You don't need to change this path
  - guthubToken -> The token you just created. Send this token to your friends for them to set up on their header/settings.json also
  - githubRepository -> The path to your repository, the same as the URL but without the Github domain, just <YourProfileName>/<YourRepositoryName>
  - maxWorldSaves -> The number of saves you maintein at the Github repository. Useful for backup if needed.

## How to Use Valheim-Shared-Offline-Server:
If this is the first time running the program, or you want to add another world server, run the **command CREATE NEW WORLD to add a new world to the Github repository**. You must create or already have a world Valheim in-game with the same name.

Run the program before opening the game and run the **command LOAD to "open the server"**. This will get the last save from the Github repository and import it to your machine. If somebody used the server while you were offline, now you will have their progress. Just need to open the game, select the world and check Start Server to host to the other players. The program will inform, but be sure to load only if no one loaded and is currently hosting.

Run the program after closing the game and run the **command SAVE to "close the server"**. This will get the last save from your machine and export it to the Github repository. After that, anyone can start the program with the option LOAD to load your save and progress.

<p align="center"><img src="https://img2.storyblok.com/fit-in/1000x1000/f/157036/552x800/322109d551/build-2.png" alt="Valheim official media from https://www.valheimgame.com" width="276" height="400"/></p>

## May the wind blow in your crew's favor!
