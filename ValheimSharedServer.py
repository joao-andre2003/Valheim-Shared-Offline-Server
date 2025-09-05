# Valheim Shared Offline Server
# Autor: Joao Andre A. da Silva
 
from github import Github
from colorama import init, Fore, Style
import requests
import json
import subprocess
import datetime
import sys
import os
 
init();
class Debug:
    RED = Fore.RED;
    GREEN = Fore.GREEN;
    YELLOW = Fore.YELLOW;
    UNDERLINE = "\033[4m";
    END = Style.RESET_ALL;
    ERROR = f"{RED}[ERROR]{END} ";
    WARNING = f"{YELLOW}[WARNING]{END} ";
    SUCCESS = f"{GREEN}[SUCCESS]{END} ";
 
with open('header/settings.json', 'r') as file:
    SETTINGS = json.load(file)
SERVER_STATUS_FILE = "Server_Status.txt";
SERVER_STATUS_MODEL = "[SERVER STATUS]\nStatus: %s\nWho is hosting: %s";
IsServerActive = False;
IsLocalSaved = False;
Local_Path = "";
 
def Log(logType, message):
    print(logType + message);
    if logType == Debug.ERROR:
        input("Press ENTER to exit...");
        sys.exit(0);

def GetDateFromFile(fileName):
    return fileName.replace("auto-", "").replace("restore-", "")[fileName.find("backup_") + 7 : ].replace("-", "").replace(".db", ""); # backups have another '-' to separate hour from day
 
def GetContents(repo_obj, path=""):
    try:
        contents = repo_obj.get_contents(path);
       
        if len(contents) <= 0:
            Log(Debug.ERROR, f"There are no world saves available on the github server. Please, select the option {Debug.UNDERLINE}Create New World{Debug.END} at the start of the program for correctly set up.");
       
        if path != "":
            contents_path_time = [];
            for c in contents:
                contents_path_time.append(GetDateFromFile(c.path));
            contents_path_ordered = sorted(contents_path_time, reverse=True);
 
            _contents = contents;
            contents = [];
            for i in range(len(contents_path_time)):
                new_i = contents_path_ordered.index(contents_path_time[i]);
                if ".db" in _contents[new_i].path and "backup" in _contents[new_i].path:
                    contents.append(_contents[new_i]); # Order contents to date
       
        print(f"[Options = 1 ... {len(contents)}]");
        cnt = 1;
        for content_file in contents:
            print(f"       {cnt}. {content_file.path[content_file.path.find("/") + 1 : ]}", end=" ");
            if path != "":
                print(repo_obj.get_commits(path=content_file.path)[0].commit.message, end=" ");
            print("\n", end="");
            cnt += 1;
        return contents
    except Exception as e:
        Log(Debug.ERROR, f"Listing contents: {e}");
 
def SelectContent(contents):
    if len(contents) == 1:
        return contents[0].path;
 
    selectedContent = "";
    while True:
        try:
            cmd = input("   >> ");
            index = 0 if cmd == "" else int(cmd) - 1;
            selectedContent = contents[index].path;
            break;
        except:
            Log(Debug.WARNING, f"Invalid input. Use only numbers in the range of {Debug.UNDERLINE}[Options]{Debug.END}");
    return selectedContent;
 
def SelectOption(message, options, default=""):
    cmd = "";
    while cmd not in options:
        print(message);
        cmd = str.lower(input("   >> "));
        cmd = default if cmd == "" else cmd;
    return cmd;
 
def ShowServerStatus(repo_obj, path):
    status = repo_obj.get_contents(path + "/" + SERVER_STATUS_FILE).decoded_content.decode('utf-8');
    global IsServerActive;
    IsServerActive = False if "INACTIVE" in status else True;
    return f"\n{status}";
 
def UpdateServerStatus(repo_obj, worldName, status, username):
    update_status = repo_obj.get_contents(worldName + "/" + SERVER_STATUS_FILE);
    repo_obj.update_file(
        path= update_status.path,
        message= "Updating Status...",
        content= SERVER_STATUS_MODEL % (status, username),
        sha= update_status.sha
    );
    Log(Debug.SUCCESS, "Server Status updated.");
   
def CreateNewWorld(repo_obj):
    print(f"\n > What is the new world server name? (It need to be {Debug.UNDERLINE}the exactly same name{Debug.END} as your local saved world)");
    worldName = input("   >> ");
    newFiles = ["Server_Status.txt", worldName + ".db", worldName + ".fwl"];
    for file in newFiles:
        repo_obj.create_file(
            path= worldName + "/" + file,
            message= "New file",
            content= ""
        );
    Log(Debug.SUCCESS, "New world files created. Ready for load or save.\n\n");
 
def LoadWorld(repo_obj, worldName):
    global Local_Path, IsLocalSaved, IsServerActive;
    if IsServerActive:
        username = ShowServerStatus(repo_obj, worldName);
        username = username[username.find("\nWho is hosting: ") + 1 : ];
        Log(Debug.WARNING, f"The server is still {Debug.RED}OPEN{Debug.END}. {Debug.UNDERLINE + username + Debug.END}. Or the user may have forgot to load back the world to the Github server. Proceeding can {Debug.RED}DELETE{Debug.END} this user's world version progress or yours.");
        opt = SelectOption(" > Are you sure you want to continue? (y or N)",
                           ["y", "n"],
                           "n"
                           );
        if opt == "n":
            sys.exit(0);

    print(f"\n{Debug.UNDERLINE}[SELECTED {worldName}]{Debug.END} Select the save to be loaded (default=last): ");
    contents = GetContents(repo_obj, worldName);

    if contents[0].path[contents[0].path.find("/") + 1 : ] in os.listdir(Local_Path):
        opt = SelectOption(f" > {Debug.GREEN}Your save is up to date!{Debug.END} Nobody opened the server since your last save. Cancel operation? (Y or n)",
                           ["y", "n"],
                           "y"
                           );
        if opt == "y":
            return;

    selectedContent = SelectContent(contents);
    contents_to_import = [worldName + f"/{worldName}.db", worldName + f"/{worldName}.fwl", selectedContent];
    contents_to_import.append(selectedContent[ : selectedContent.find(".")] + ".fwl");
 
    imported_contents = [];
    for content in contents_to_import:
        imported_contents.append(content[content.find("/") + 1 : ]);
    
    print(f"[SELECTED {selectedContent[selectedContent.find("/") + 1 : ]}] Loading world to {"local world saves" if IsLocalSaved else "Steam's cloud world saves"}...");
    for i in range(len(contents_to_import)):
        worldSave = repo_obj.get_contents(contents_to_import[i]);

        if worldSave.encoding == "none":
            worldSave = requests.get(worldSave.download_url).content;
        else:
            worldSave = worldSave.decoded_content;
 
        with open(Local_Path + "/" + imported_contents[i], "wb") as world:
            print(imported_contents[i])
            world.write(worldSave);
    Log(Debug.SUCCESS, f"{worldName} save was loaded.")
 
def SaveWorld(repo_obj, worldName):
    global Local_Path, IsServerActive;
    if not IsServerActive:
        Log(Debug.WARNING, f"The server is {Debug.RED}NOT OPENED{Debug.END}. The last world version saved on the server is not this version of the world. Proceeding can {Debug.RED}DELETE{Debug.END} this user's world version progress or yours.");
        opt = SelectOption(" > Are you sure you want to continue? (y or N)",
                           ["y", "n"],
                           "n"
                           );
        if opt == "n":
            sys.exit(0);
    try:
        current_time = datetime.datetime.now();
        current_time_dmy = datetime.datetime.strftime(current_time, '%d/%m/%Y %H:%M:%S');
        commit_base_message = f"[{current_time_dmy} Saved by: {SETTINGS['Client']['username']}] ";
       
        files_to_update = [worldName + ".db", worldName + ".fwl"];
        for f_to_update in files_to_update:
            with open(Local_Path + f_to_update, "rb") as file_content:
                content_to_update = repo_obj.get_contents(worldName + "/" + f_to_update);
                repo_obj.update_file(
                    path= content_to_update.path,
                    message= commit_base_message + "File updated",
                    content= file_content.read(),
                    sha= content_to_update.sha
                );
               
        allLocalSaves = os.listdir(Local_Path);
        backup_files_time = [];
        for f in allLocalSaves:
            if worldName in f and "backup" in f and ".db" in f:
                time = GetDateFromFile(f);
                backup_files_time.append(time);
                backup_files_time.append(time[ : 8] + '-' + time[8 : ]); # backups and auto backups have different time format
        backup_files_time = sorted(backup_files_time, reverse=True);

        last_backup_DT = datetime.datetime.strptime(backup_files_time[0].replace("-", ""), '%Y%m%d%H%M%S');
        opt = SelectOption(f" > Last local save was at [{last_backup_DT.strftime("%d-%m-%Y %H:%M:%S")}] Upload this save? (Y or n)",
                     ["y", "n"],
                     "y"
                     );
        if opt == "n":
            sys.exit(0);
        
        print(f" > {worldName} save's description: ");
        commit_desc = input("   >> ");
        for f_to_export in allLocalSaves:
            if backup_files_time[0] in f_to_export or backup_files_time[1] in f_to_export:
                with open(Local_Path + f_to_export, "rb") as file_content:
                      repo_obj.create_file(
                        path= worldName + "/" + f_to_export,
                        message= commit_base_message + commit_desc,
                        content= file_content.read()
                    );
        Log(Debug.SUCCESS, f"{worldName} saved.");
    except Exception as e:
        Log(Debug.ERROR, f"World may not exist in {Local_Path}. Check if the path and world exists. Or you don't have Github permissions to write: {e}");
 
def main():
    print("<-~-~- { VALHEIM SHARED OFFLINE SERVER } -~-~->\n ~ Made by Joao Andre A.\n");
    try:
        git = Github(SETTINGS['Server']['githubToken']);
        repo = git.get_repo(SETTINGS['Server']['githubRepository']);
    except Exception as e:
        Log(Debug.ERROR, f"Connection to the repository rejected. Check your token and repository name: {e}");
   
    operation = SelectOption(f"\n > {Debug.UNDERLINE}Save{Debug.END} or {Debug.UNDERLINE}Load{Debug.END} world save? Or {Debug.UNDERLINE}Create New World{Debug.END} on server?",
                        ["save", "load", "create new world"]
                        );
                       
    if operation == "create new world":
        CreateNewWorld(repo);
        main();
        sys.exit(0);
                       
    print(" > Select the world.", end=" ");
    contents = GetContents(repo);
    worldName = SelectContent(contents);
 
    print(ShowServerStatus(repo, worldName));
    print("- - - - - - - - - - - - - - - - - - - -");
 
    print(f"\n{Debug.UNDERLINE}[SELECTED {worldName}]{Debug.END}");
   
    saveMode = SETTINGS["Client"]["saveMode"];
    if saveMode == "":
        saveMode = SelectOption(f" > Do you want to {operation} world in {Debug.UNDERLINE}Local{Debug.END} or {Debug.UNDERLINE}Cloud{Debug.END} path? (default=cloud)",
                                        ["local", "cloud"],
                                        "cloud"
                                        );
    global Local_Path, IsLocalSaved;
    Local_Path = (SETTINGS['Client']['cloudSavePath']) % (SETTINGS['Client']['steamID']) if saveMode == "cloud" else SETTINGS['Client']['localSavePath'];
    IsLocalSaved = True if saveMode == "local" else False;
    match operation:
        case "save":
            SaveWorld(repo, worldName);
            UpdateServerStatus(repo, worldName, f"{Debug.RED}INACTIVE{Debug.END}", f"{Debug.UNDERLINE}Nobody{Debug.END}");
        
            contents = GetContents(repo, worldName);
            contents_limit = int(SETTINGS['Server']['maxWorldSaves']);
            if len(contents) > contents_limit:
                Log(Debug.WARNING, f"The save limit set on settings.ini was reached. LIMIT = {contents_limit} / SAVES NUMBER = {len(contents)}.)");
                cmd = SelectOption(" > Delete last saves out of limits? (Y or n)",
                            ["y", "n"],
                            "y"
                            );
                if cmd == "n":
                    return;
            for i in range(contents_limit, len(contents)):
                files = [contents[i].path, contents[i].path.replace("db", "fwl")];
                for file in files:
                    repo.delete_file(
                        path= file,
                        message= "Old save number out of limits",
                        sha= contents[i].sha
                    );
                    print(f"{Debug.UNDERLINE + file} DELETED.{Debug.END}");
        
        case "load":
            LoadWorld(repo, worldName);
            UpdateServerStatus(repo, worldName, f"{Debug.SUCCESS}ACTIVE{Debug.END}", f"{Debug.UNDERLINE + SETTINGS['Client']['username'] + Debug.END}");

            cmd = SelectOption("\n > Launch Valheim? (Y or n) ",
                       ["y", "n"],
                       "y"
                       );
            if (cmd == "y"):
                subprocess.Popen("C:/Program Files (x86)/Steam/Steam.exe -applaunch 892970");
main();