# SOLUS by DESYNTAX - VERSION indev_3 - CREATED 24/02/26 - LAST UPDATED 11/03/26
print("Starting Solus...")
dangerousProceed = ""

# imports
try:
    import time, os, sys, shutil, configparser
    from pathlib import Path
except ModuleNotFoundError:
    print("""Solus has run into an error and cannot import certain necessary modules. Please ensure you have the following:
os
sys
time
shutil
pathlib
configparser
On your machine's command line, run 'pip install <module>'.
You should be able to run Solus without these modules imported, but functionality will be limited.
Proceed? (y/N)""")
    dangerousProceed = input("> ")
    if dangerousProceed == "y".casefold():
        print("Skipping module imports.")
    else:
        exit()
except MemoryError:
    print("Solus does not have enough memory to import necessary modules. Press RETURN to exit.")
    input("> ")
    exit()
bootStart = time.time()
print("Loaded necessary modules.")

# config
try:
    config = configparser.ConfigParser()
    config.read("config.txt")
    solus_info = {
        "username": config['SOLUS_INFO']['username'],
        "password": config['SOLUS_INFO']['password'],
        "solusname": config['SOLUS_INFO']['solusname']}
    version = config['SOLUS_INFO']['version']
except KeyError:
    print("Error loading configuration file. Would you like to create it? (Y/n)")
    choice = input("> ")
    if choice == "n":
        print("Aborted.")
        exit()
    else:
        Path.touch("config.txt")
        config['SOLUS_INFO'] = {
            'username': 'guest',
            'password': 'password',
            'solusname': 'Solus',
            'version': 'indev_3'}
        with open('config.txt', 'w') as file:
            config.write(file)
    config.read("config.txt")
    solus_info = {
        "username": config['SOLUS_INFO']['username'],
        "password": config['SOLUS_INFO']['password'],
        "solusname": config['SOLUS_INFO']['solusname']}
    version = config['SOLUS_INFO']['version']
    print("Created configuration file.")
    print("Username: 'guest'; password: 'password'.")
print("Loaded configuration file.")

# variables
welcomeMessage = f"Solus CLI {version}, created by Desyntax on 24/02/2026."
command = ""
cwd = __file__.removesuffix("solus.py")
inSolusDirectory = "$"
helpList = f"""Solus command line interface, build {version}. Open-sourced project.
Command format:
command <necessary_arguments> [;optional_arguments] -- Description [modules_necessary]
Interpreter format:
(USERNAME)@(Solusname)(directory)>

help                    -- Displays this help message
logout                  -- Logs out of Solus
exit                    -- Logs out and kills the program
output <str>            -- Prints <str> to the screen
ls                      -- Prints files and dirs in CWD to the screen [os]
cwd <dir>               -- Changes current working directory to <dir> [os]
scan <file>             -- Prints text from <file>
nano <file> [;a]        -- Writes text in <file>
kin <dir>               -- Creates a directory called <dir> [os]
touch <file>            -- Creates a file called <file> [pathlib]
boom <file              -- Deletes <file> from current directory [shutil, os]
rep <file> <str/dir>    -- Renames <file> to <str> or moves <file> to <dir> [os]
copy <file> <dir>       -- Copies <file> to <dir> [pathlib]
username <str>          -- Sets a new username [configparser]
password <str>          -- Sets a new password [configparser]
solusname <str>         -- Sets a new name for Solus [configparser]
info                    -- Prints information about Solus
copyright               -- Prints copyright information about Solus

Use help [command] to view more details about a command."""
copyr = f"Solus {version}, created by Desyntax. All content, including source code, are public domain."
print("Loaded variables.")

# definitions
def login():
    global solus_info
    print("Please sign in below.")
    while True:
        tryUsername = input("USERNAME> ")
        tryPassword = input("PASSWORD> ")
        if tryUsername == solus_info["username"] and tryPassword == solus_info["password"]:
            print(f"Logged in. Welcome, {solus_info["username"]}")
            del tryUsername, tryPassword
            break
        else:
            print("Incorrect username or password.")
def write(mode):
    file = open(f"{command.removeprefix('nano ')}", mode)
    if mode == "w":
        print(f"{command.removeprefix('nano ')} opened in OVERWRITE mode")
    else:
        print(f"{command.removeprefix('nano ')} opened in APPEND mode")
    print("Type <close> to end writing and save.")
    while True:
        newline = input()
        if newline == "<close>":
            print(f"Closed {command.removeprefix('nano ')} and saved all changes.")
            break
        file.write(newline + "\n")
    file.close()
def modifyInfo(part):
    global config, solus_info, command
    if command.startswith(f"{part} "):
        newName = command.removeprefix(f"{part} ")
        config['SOLUS_INFO'][part] = newName
        if part in solus_info:
            solus_info[part] = newName
        with open("config.txt", "w") as f:
            config.write(f)
        print(f"Updated {part} to {newName}.")
    else:
        print(f"'{part}' takes one argument, <str>.")
print("Loaded definitions.")

# initialise
if dangerousProceed != "y":
    print(f"Found {os.cpu_count()} CPU threads.")
    try:
        fileStats = str(os.stat(__file__)).split(", ")
        fileSize = int(str(fileStats[6]).removeprefix("st_size="))
        print(f"Solus occupies {fileSize:,d} bytes of disk space.")
        del fileStats, fileSize
    except FileNotFoundError:
        print("Solus couldn't locate itself to record its disk usage. Proceeding anyway...")
    print(f"Solus is running on a {sys.platform} system.")
    if sys.platform == "win32":
        dirSep = "\"
    else:
        dirSep = "/"
    cwd = __file__.removesuffix(f"{dirSep}solus.py")
    bootEnd = time.time()
    bootTime = bootEnd - bootStart
    print(f"Booted in {round((bootTime * 1000), 4)} milliseconds.")
    del bootStart, bootEnd, bootTime
else:
    print("Skipped checking OS due to missing modules.")
del dangerousProceed
print("No fatal errors encountered during boot.", end="\n\n")
print(welcomeMessage, end="\n\n")
login()

while True:
    command = input(f"{solus_info['username'].upper()}@{solus_info['solusname']}{inSolusDirectory}> ")
    if command == "help": # help
        print(helpList)
    elif command == "logout": # logout
        print("You have successfully logged out.")
        login()
    elif command.startswith("output"): # output
        if command.startswith("output "):
            print(command.removeprefix("output "))
        else:
            print("'output' takes one argument, <str>.")
    elif command.startswith("scan"): # scan
        if command.startswith("scan "):
            try:
                file = open(command.removeprefix('scan '))
                file.close()
                try:
                    file = open(f"{command.removeprefix('scan ')}", "r")
                    print(file.read())
                    file.close()
                except FileNotFoundError:
                    print(f"File '{command.removeprefix('scan ')}' not found. Check your spelling, its existence, or your permissions.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("'scan' takes one argument, <file>.")
    elif command.startswith("username"): # username
        modifyInfo("username")
    elif command.startswith("password"): # password
        modifyInfo("password")
    elif command.startswith("solusname"): # solusname
        modifyInfo("solusname")
    elif command.startswith("nano"): # nano
        if command.startswith("nano "):
            try:
                file = open(command.removeprefix('nano '))
                file.close()
                try:
                    command.index(f"{command.removeprefix('nano ')}", command.find(";"))
                    write("a")
                except Exception:
                    write("w")
            except FileNotFoundError:
                print(f"File '{command.removeprefix('nano ')}' cannot be accessed. You may not have permissions to modify it.")
            except PermissionError:
                print(f"File '{command.removeprefix('nano ')}' cannot be accessed due to unqualified permission.")
        else:
            print("'nano' takes at least one argument, <file>.")
    elif command.startswith("info"): # info
        if command.startswith("info "):
            if command == "info ":
                try:
                    file = open("info.txt", "r")
                    print(file.read(), end="\n")
                    file.close()
                except FileNotFoundError:
                    print("'info.txt' was not found. Are you in Solus' directory?")
                except PermissionError:
                    print("'info.txt' could not be read.")
            else:
                print(f"'info' takes zero arguments.")
        else:
            try:
                file = open("info.txt", "r")
                print(file.read(), end="")
                file.close()
            except FileNotFoundError:
                    print("'info.txt' was not found. Are you in Solus' directory?")
    elif command.startswith("rep"): # rep
        if command.startswith("rep "):
            rep = command.split(maxsplit=2)
            os.rename(rep[1], rep[2])
            print(f"Successfully modified '{rep[1]}' to '{rep[2]}'.")
            del rep
        else:
            print("'rep' takes at least two arguments, <file> and <str/dir>.")
    elif command.startswith("ls"): # ls
        if command.startswith("ls "):
            print("'ls' takes zero arguments.")
        else:
            print(f"All in '{cwd}':")
            print(os.listdir(cwd))
    elif command.startswith("cwd"):  # cwd
        if command.startswith("cwd "):
            try:
                new_dir = command.removeprefix("cwd ")
                os.chdir(new_dir)
                cwd = os.getcwd()
                print(f"Changed directory to '{cwd}'")
                del new_dir
            except FileNotFoundError:
                print(f"Directory '{command.removeprefix('cwd ')}' doesn't exist.")
            except NotADirectoryError:
                print(f"'{command.removeprefix('cwd')}' is a file, not a directory.")
            except PermissionError:
                print(f"Solus doesn't have permission to change to this directory.")
            except OSError:
                print(f"Your operating system ran into an issue trying to perform this task.")
        else:
            print("'cwd' takes at least one argument, <dir>.")
    elif command.startswith("copyright"): # copyright
        if command.startswith("copyright "):
            print("'copyright' takes zero arguments.")
        else:
            print(copyr)
    elif command.startswith("boom"): # boom
        if command.startswith("boom "):
            try:
                os.remove(command.removeprefix("boom "))
                print(f"Successfully deleted '{command.removeprefix('boom ')}'.")
            except Exception:
                print(f"'{command.removeprefix('boom ')}' is a directory. Would you like to remove it? (y/N)")
                choice = input("> ")
                if choice == "y":
                    try:
                        shutil.rmtree(command.removeprefix('boom '))
                        print(f"Successfully removed '{command.removeprefix('boom ')}'")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Aborted.")
        else:
            print("'rm' takes at least one argument, <file>")
    elif command.startswith("kin"): # kin
        if command.startswith("kin "):
            try:
                os.mkdir(command.removeprefix("kin "))
                print(f"Created directory '{command.removeprefix('kin ')}' in '{cwd}'.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("'kin' takes at least one argument, <dir>")
    elif command.startswith("touch"): # touch
        if command.startswith("touch "):
            try:
                Path(f"{command.removeprefix('touch ')}").touch()
                print(f"Sucessfully created '{command.removeprefix('touch ')}' at '{cwd}'")
            except FileExistsError:
                print(f"'{command.removeprefix('touch ')}' already exists in '{cwd}'.")
            except PermissionError:
                print("Solus doesn't have the necessary permissions to perform this.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("'touch' takes at least one argument, <file>.")
    elif command.startswith("copy"): # copy
        if command.startswith("copy "):
            copy = command.split(maxsplit=2)
            shutil.copy2(copy[1], copy[2])
            print(f"Successfully copied '{copy[1]}' to '{copy[2]}'.")
            del copy
        else:
            print("'copy' takes at least two arguments, <file> and <dir>.")
    elif command.startswith("exit"):
        print("Ending process...")
        exit()
    else:
        print(f"'{command}' not a recognised command. Use 'help' to view a list of commands.")
    if cwd == __file__.removesuffix("solus.py"):
        inSolusDirectory = "$"
    else:
        inSolusDirectory = "~"

# like and subscribe for more epic code


