# SOLUS by DESYNTAX - VERSION indev_4 - CREATED 24/02/26 - LAST UPDATED 16/03/26
print("Starting CLI...")
dangerousProceed = ""
sty = {
    "reset": "\x1b[0m",
    "red": "\x1b[91m",
    "gold": "\x1b[93m",
    "green": "\x1b[92m",
    "blue": "\x1b[96m",
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

os              -- in commands
sys             -- optional
time            -- optional
shutil          -- in commands
pathlib         -- in commands
configparser    -- optional

where:
optional        -- used to assess OS or fetch config
in commands     -- necessary to perform some commands

On your machine's command line, run 'pip install <module>'.
You might be able to run Solus without these modules imported, but functionality will be severely limited.
Proceed? {sty['underl']}(y/N){sty['reset']}""")
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
print(f"{sty['green']}Loaded necessary modules.{sty['reset']}")

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
print(f"{sty['green']}Loaded configuration file.{sty['reset']}")

# variables
welcomeMessage = f"Solus CLI {version}, created by Desyntax on 24/02/2026."
command = ""
inSolusDirectory = "$"
copyr = f"Solus {version}, created by Desyntax. All content, including source code, are public domain."
print(f"{sty['green']}Loaded variables.{sty['reset']}")

# definitions
def login():
    global solus_info
    print("Please sign in below.")
    while True:
        tryUsername = input("USERNAME> ")
        tryPassword = input(f"PASSWORD> {sty['hide']}")
        if tryUsername == solus_info["username"] and tryPassword == solus_info["password"]:
            print(f"{sty['reset']}{sty['green']}Logged in. Welcome, {solus_info['username']}{sty['reset']}")
            del tryUsername, tryPassword
            break
        else:
            print(f"{sty['reset']}{sty['red']}Incorrect username or password.{sty['reset']}")
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
        print(f"{sty['red']}'{part}' takes one argument, <str>.{sty['reset']}")
def sty_rainbow(text):
    global sty
    stymap = [sty["red"], sty["gold"], sty["green"], sty["blue"], sty["pink"]]
    result = ""
    for i, t in enumerate(text):
        color = stymap[i % len(stymap)]
        result += f"{color}{t}"
    result += sty["reset"]
    return result
def ls(main, name, size):
    global os, cwd
    allinpath = {}
    print(f"{sty['blue']}{name:<20} {sty['green']}{size:>10}{sty['reset']}")
    print("-" * 32)
    for node in main:
        allinpath[node] = os.path.getsize(node)
        if os.path.isdir(allinpath[node]) == True:
            for path, dirs, files in os.walk(Folderpath):
                for f in files:
                    fp = os.path.join(path, f)
                    size += os.path.getsize(fp)
    for row in main:
        filesize = allinpath[row]
        fsm = " B" # file size measurement (bytes, kilobytes, etc)
        if filesize >= 1024:
            filesize /= 1024
            fsm = "KB"
        elif filesize >= 1048576:
            fsm = "MB"
        elif filesize >= 1073741824:
            fsm = "GB"
        filesize = round(filesize, 2)
        print(f"{row:<20} {filesize:>10,}{fsm}")

print(f"{sty['green']}Loaded definitions.{sty['reset']}")

# initialise
if dangerousProceed != "y":
    print(f"Solus is running on a {sty['blue']}{sys.platform}{sty['reset']} system.")
    if sys.platform == "win32":
        dirSep = "\""
    else:
        dirSep = "/"
    cwd = __file__.removesuffix(f"{dirSep}solus.py")
    print(f"Found {sty['blue']}{os.cpu_count()}{sty['reset']} CPU threads.")
    try:
        print(f"Solus occupies {sty['blue']}{os.path.getsize(f'{cwd}{dirSep}solus.py'):,d}{sty['reset']} bytes of disk space.")
    except FileNotFoundError:
        print("Solus couldn't locate itself to record its disk usage. Proceeding anyway...")
    bootEnd = time.time()
    bootTime = bootEnd - bootStart
    print(f"Booted in {sty['blue']}{round((bootTime * 1000), 4)}{sty['reset']} milliseconds.")
    del bootStart, bootEnd, bootTime
else:
    print("Skipped checking OS due to missing modules.")
del dangerousProceed
print("No fatal errors encountered during boot.", end="\n\n")
print(welcomeMessage, end="\n\n")
login()

while True:
    command = input(f"{sty['reset']}{sty['red']}{solus_info['username'].upper()}{sty['pink']}@{sty['blue']}{solus_info['solusname']}{sty['pink']}{inSolusDirectory}{sty['reset']}> ")
    if command == "help": # help
        try:
            file = open("help.txt", "r")
            helpmsg = file.read()
            helpmsg = helpmsg.format_map(sty)
            print(helpmsg)
            file.close()
            del helpmsg
        except FileNotFoundError:
            print(f"{sty['red']}'help.txt' was not found. Are you in Solus' directory?{sty['reset']}")
        except Exception as e:
            print(f"{sty['red']}Error: {e}{sty['reset']}")
    elif command == "logout": # logout
        print("You have successfully logged out.")
        login()
    elif command.startswith("output"): # output
        if command.startswith("output "):
            try:
                out = command.split(maxsplit=2).casefold()
                if out[2] == "[;f]":
                    print(f"{command.removeprefix('output ')}")
            except Exception:
                print(command.removeprefix('output '))
        else:
            print(f"{sty['red']}'output' takes one argument, <str>.{sty['reset']}")
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
                    print(f"{sty['red']}File '{command.removeprefix('scan ')}' not found. Check your spelling, its existence, or your permissions.{sty['reset']}")
            except Exception as e:
                print(f"{sty['red']}Error: {e}{sty['reset']}")
        else:
            print(f"{sty['red']}'scan' takes one argument, <file>.{sty['reset']}")
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
                print(f"{sty['red']}Error: {e}{sty['reset']}")
        else:
            print(f"{sty['red']}'nano' takes at least one argument, <file>.{sty['reset']}")
    elif command.startswith("info"): # info
        try:
            file = open("info.txt", "r")
            infomsg = file.read()
            infomsg = infomsg
            print(infomsg.format_map({"desyntax": sty_rainbow("Desyntax"), **sty}))
            file.close()
            del infomsg
        except FileNotFoundError:
            print(f"{sty['red']}'info.txt' was not found. Are you in Solus' directory?{sty['reset']}")
        except Exception as e:
            print(f"{sty['red']}Error: {e}{sty['reset']}")
    elif command.startswith("rep"): # rep
        if command.startswith("rep "):
            try:
                rep = command.split(maxsplit=2)
                os.rename(rep[1], rep[2])
                print(f"Successfully modified '{rep[1]}' to '{rep[2]}'.")
                del rep
            except Exception as e:
                print(f"{sty['red']}Error: {e}{sty['reset']}")
        else:
            print("{sty['red']}'rep' takes at least two arguments, <file> and <str/dir>.{sty['reset']}")
    elif command.startswith("ls"): # ls
        if command.startswith("ls "):
            print(f"{sty['red']}'ls' takes zero arguments.{sty['reset']}")
        else:
            print(f"All in '{cwd}':")
            ls(os.listdir(cwd), "Name", "Size")
    elif command.startswith("cwd"):  # cwd
        if command.startswith("cwd "):
            try:
                new_dir = command.removeprefix("cwd ")
                os.chdir(new_dir)
                cwd = os.getcwd()
                print(f"Changed directory to '{cwd}'")
                del new_dir
            except Exception as e:
                print(f"{sty['red']}Error: {e}{sty['reset']}")
        else:
            print(f"{sty['red']}'cwd' takes at least one argument, <dir>.{sty['reset']}")
    elif command.startswith("copyright"): # copyright
        print(copyr)
    elif command.startswith("boom"): # boom
        if command.startswith("boom "):
            try:
                os.remove(command.removeprefix("boom "))
                print(f"Successfully deleted '{command.removeprefix('boom ')}'.")
            except IsADirectoryError:
                print(f"{sty['red']}'{command.removeprefix('boom ')}' is a directory.{sty['reset']} Would you like to remove it? (y/N)")
                choice = input("> ").casefold()
                if choice == "y":
                    try:
                        shutil.rmtree(command.removeprefix('boom '))
                        print(f"Successfully removed '{command.removeprefix('boom ')}'")
                    except Exception as e:
                        print(f"{sty['red']}Error: {e}{sty['reset']}")
                else:
                    print("Aborted.")
            except Exception as e:
                print(f"{sty['red']}Error: {e}{sty['red']}")
        else:
            print(f"{sty['red']}'boom' takes at least one argument, <file>.{sty['reset']}")
    elif command.startswith("kin"): # kin
        if command.startswith("kin "):
            try:
                os.mkdir(command.removeprefix("kin "))
                print(f"Created directory '{command.removeprefix('kin ')}' in '{cwd}'.")
            except Exception as e:
                print(f"{sty['red']}Error: {e}{sty['reset']}")
        else:
            print(f"{sty['red']}'kin' takes at least one argument, <dir>.{sty['reset']}")
    elif command.startswith("touch"): # touch
        if command.startswith("touch "):
            try:
                Path(f"{command.removeprefix('touch ')}").touch()
                print(f"Sucessfully created '{command.removeprefix('touch ')}' at '{cwd}'")
            except FileExistsError:
                print(f"{sty['red']}'{command.removeprefix('touch ')}' already exists in '{cwd}'.{sty['reset']}")
            except PermissionError:
                print(f"{sty['red']}Solus doesn't have the necessary permissions to perform this.{sty['reset']}")
            except Exception as e:
                print(f"{sty['red']}Error: {e}{sty['reset']}")
        else:
            print(f"{sty['red']}'touch' takes at least one argument, <file>.{sty['reset']}")
    elif command.startswith("copy"): # copy
        if command.startswith("copy "):
            try:
                copy = command.split(maxsplit=2)
                shutil.copy2(copy[1], copy[2])
                print(f"Successfully copied '{copy[1]}' to '{copy[2]}'.")
                del copy
            except Exception as e:
                print(f"{sty['red']}Error: {e}{sty['reset']}")
        else:
            print(f"{sty['red']}'copy' takes at least two arguments, <file> and <dir>.{sty['reset']}")
    elif command.startswith("exit"):
        print("Ending CLI...")
        exit()
    else:
        print(f"{sty['red']}'{command}' not a recognised command. Use 'help' to view a list of commands.{sty['reset']}")
    if cwd == __file__.removesuffix(f"{dirSep}solus.py"):
        inSolusDirectory = "$"
    else:
        inSolusDirectory = "~"

# like and subscribe for more epic code
