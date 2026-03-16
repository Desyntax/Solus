# SOLUS by DESYNTAX - VERSION indev_4 - CREATED 24/02/26 - LAST UPDATED 16/03/26
print("Starting CLI...")
dangerousProceed = ""
style = {
    "reset": "\x1b[0m",
    "red": "\x1b[91m",
    "yellow": "\x1b[33m",
    "green": "\x1b[92m",
    "blue": "\x1b[36m",
    "pink": "\x1b[95m",
    "underl": "\x1b[4m",
    "bold": "\x1b[1m",
    "hide": "\x1b[8m"}

# imports
try:
    import time, os, sys, shutil, configparser
    from pathlib import Path
except ModuleNotFoundError:
    print(f"""Solus has run into an error and cannot import certain necessary modules. Please ensure you have the following:
os
sys
time
shutil
pathlib
configparser
On your machine's command line, run 'pip install <module>'.
You should be able to run Solus without these modules imported, but functionality will be limited.
Proceed? {style['underl']}(y/N){style['reset']}""")
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
print(f"{style['green']}Loaded necessary modules.{style['reset']}")

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
    choice = input("> ").casefold()
    if choice == "n":
        print("Aborted.")
        exit()
    else:
        Path.touch("config.txt")
        config['SOLUS_INFO'] = {
            'username': 'guest',
            'password': 'password',
            'solusname': 'Solus',
            'version': 'indev_4'}
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
print(f"{style['green']}Loaded configuration file.{style['reset']}")

# variables
welcomeMessage = f"Solus CLI {version}, created by Desyntax on 24/02/2026."
command = ""
inSolusDirectory = "$"
copyr = f"Solus {version}, created by Desyntax. All content, including source code, are public domain."
print(f"{style['green']}Loaded variables.{style['reset']}")

# definitions
def login():
    global solus_info
    print("Please sign in below.")
    while True:
        tryUsername = input("USERNAME> ")
        tryPassword = input(f"PASSWORD> {style['hide']}")
        if tryUsername == solus_info["username"] and tryPassword == solus_info["password"]:
            print(f"{style['reset']}{style['green']}Logged in. Welcome, {solus_info['username']}{style['reset']}")
            del tryUsername, tryPassword
            break
        else:
            print(f"{style['reset']}{style['red']}Incorrect username or password.{style['reset']}")
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
        print(f"{style['red']}'{part}' takes one argument, <str>.{style['reset']}")
print(f"{style['green']}Loaded definitions.{style['reset']}")

# initialise
if dangerousProceed != "y":
    print(f"Found {style['blue']}{os.cpu_count()}{style['reset']} CPU threads.")
    try:
        fileStats = str(os.stat(__file__)).split(", ")
        fileSize = int(str(fileStats[6]).removeprefix("st_size="))
        print(f"Solus occupies {style['blue']}{fileSize:,d}{style['reset']} bytes of disk space.")
        del fileStats, fileSize
    except FileNotFoundError:
        print("Solus couldn't locate itself to record its disk usage. Proceeding anyway...")
    print(f"Solus is running on a {style['blue']}{sys.platform}{style['reset']} system.")
    if sys.platform == "win32":
        dirSep = "\""
    else:
        dirSep = "/"
    cwd = __file__.removesuffix(f"{dirSep}solus.py")
    bootEnd = time.time()
    bootTime = bootEnd - bootStart
    print(f"Booted in {style['blue']}{round((bootTime * 1000), 4)}{style['reset']} milliseconds.")
    del bootStart, bootEnd, bootTime
else:
    print("Skipped checking OS due to missing modules.")
del dangerousProceed
print("No fatal errors encountered during boot.", end="\n\n")
print(welcomeMessage, end="\n\n")
login()

while True:
    command = input(f"{style['underl']}{solus_info['username'].upper()}@{solus_info['solusname']}{inSolusDirectory}{style['reset']}> ")
    if command == "help": # help
        try:
            file = open("help.txt", "r")
            helpmsg = file.read()
            helpmsg = helpmsg.format_map(style)
            print(helpmsg)
            file.close()
            del helpmsg
        except FileNotFoundError:
            print(f"{style['red']}'help.txt' was not found. Are you in Solus' directory?{style['reset']}")
        except OSError:
            print(f"{style['red']}'help.txt' could not be read.{style['reset']}")
    elif command == "logout": # logout
        print("You have successfully logged out.")
        login()
    elif command.startswith("output"): # output
        if command.startswith("output "):
            print(command.removeprefix("output "))
        else:
            print(f"{style['red']}'output' takes one argument, <str>.{style['reset']}")
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
                    print(f"{style['red']}File '{command.removeprefix('scan ')}' not found. Check your spelling, its existence, or your permissions.{style['reset']}")
            except Exception as e:
                print(f"{style['red']}Error: {e}{style['reset']}")
        else:
            print(f"{style['red']}'scan' takes one argument, <file>.{style['reset']}")
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
            except Exception as e:
                print(f"{style['red']}Error: {e}{style['reset']}")
        else:
            print(f"{style['red']}'nano' takes at least one argument, <file>.{style['reset']}")
    elif command.startswith("info"): # info
        if command.startswith("info "):
            if command == "info ":
                try:
                    file = open("info.txt", "r")
                    print(file.read(), end="\n")
                    file.close()
                except FileNotFoundError:
                    print(f"{style['red']}'info.txt' was not found. Are you in Solus' directory?{style['reset']}")
                except Exception:
                    print(f"{style['red']}'info.txt' could not be read.{style['reset']}")
            else:
                print(f"{style['red']}'info' takes zero arguments.{style['reset']}")
        else:
            try:
                file = open("info.txt", "r")
                print(file.read(), end="")
                file.close()
            except FileNotFoundError:
                    print("{style['red']}'info.txt' was not found. Are you in Solus' directory?{style['reset']}")
    elif command.startswith("rep"): # rep
        if command.startswith("rep "):
            try:
                rep = command.split(maxsplit=2)
                os.rename(rep[1], rep[2])
                print(f"Successfully modified '{rep[1]}' to '{rep[2]}'.")
                del rep
            except Exception as e:
                print(f"{style['red']}Error: {e}{style['reset']}")
        else:
            print("{style['red']}'rep' takes at least two arguments, <file> and <str/dir>.{style['reset']}")
    elif command.startswith("ls"): # ls
        if command.startswith("ls "):
            print(f"{style['red']}'ls' takes zero arguments.{style['reset']}")
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
            print(f"{style['red']}'cwd' takes at least one argument, <dir>.{style['reset']}")
    elif command.startswith("copyright"): # copyright
        print(copyr)
    elif command.startswith("boom"): # boom
        if command.startswith("boom "):
            try:
                os.remove(command.removeprefix("boom "))
                print(f"Successfully deleted '{command.removeprefix('boom ')}'.")
            except Exception:
                print(f"{style['red']}'{command.removeprefix('boom ')}' is a directory.{style['reset']} Would you like to remove it? (y/N)")
                choice = input("> ").casefold()
                if choice == "y":
                    try:
                        shutil.rmtree(command.removeprefix('boom '))
                        print(f"Successfully removed '{command.removeprefix('boom ')}'")
                    except Exception as e:
                        print(f"{style['red']}Error: {e}{style['reset']}")
                else:
                    print("Aborted.")
        else:
            print(f"{style['red']}'boom' takes at least one argument, <file>.{style['reset']}")
    elif command.startswith("kin"): # kin
        if command.startswith("kin "):
            try:
                os.mkdir(command.removeprefix("kin "))
                print(f"Created directory '{command.removeprefix('kin ')}' in '{cwd}'.")
            except Exception as e:
                print(f"{style['red']}Error: {e}{style['reset']}")
        else:
            print(f"{style['red']}'kin' takes at least one argument, <dir>.{style['reset']}")
    elif command.startswith("touch"): # touch
        if command.startswith("touch "):
            try:
                Path(f"{command.removeprefix('touch ')}").touch()
                print(f"Sucessfully created '{command.removeprefix('touch ')}' at '{cwd}'")
            except FileExistsError:
                print(f"{style['red']}'{command.removeprefix('touch ')}' already exists in '{cwd}'.{style['reset']}")
            except PermissionError:
                print(f"{style['red']}Solus doesn't have the necessary permissions to perform this.{style['reset']}")
            except Exception as e:
                print(f"{style['red']}Error: {e}{style['reset']}")
        else:
            print(f"{style['red']}'touch' takes at least one argument, <file>.{style['reset']}")
    elif command.startswith("copy"): # copy
        if command.startswith("copy "):
            try:
                copy = command.split(maxsplit=2)
                shutil.copy2(copy[1], copy[2])
                print(f"Successfully copied '{copy[1]}' to '{copy[2]}'.")
                del copy
            except Exception as e:
                print(f"{style['red']}Error: {e}{style['reset']}")
        else:
            print(f"{style['red']}'copy' takes at least two arguments, <file> and <dir>.{style['reset']}")
    elif command.startswith("exit"):
        print("Ending CLI...")
        exit()
    else:
        print(f"{style['red']}'{command}' not a recognised command. Use 'help' to view a list of commands.{style['reset']}")
    if cwd == __file__.removesuffix(f"{dirSep}solus.py"):
        inSolusDirectory = "$"
    else:
        inSolusDirectory = "~"

# like and subscribe for more epic code

