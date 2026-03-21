# SOLUS by DESYNTAX - VERSION v0.1.1 - CREATED 24/02/26 - LAST UPDATED 16/03/26
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
    "hide": "\x1b[8m",
    "dim": "\x1b[2m",
    "italic": "\x1b[3m",
    "dll": "\x1b[2K", # delete latest line
    "mcu": "\x1b[1A", # move cursor up (1 position)
    "rainbow": "" # empty because it's a placeholder
    }

# imports
try:
    import time, os, sys, shutil, stat, errors, ftplib
    from pathlib import Path
    import configparser as cfgparser
    import multiprocessing as mp
except ModuleNotFoundError:
    print(f"""{sty['red']}[Error]{sty['reset']} Solus failed to import certain modules. Please ensure you have the following:

os              -- {sty['gold']}in commands{sty['reset']}
sys             -- {sty['blue']}optional{sty['reset']}
stat            -- {sty['blue']}optional{sty['reset']}
time            -- {sty['gold']}in commands{sty['reset']}
errors (local)  -- {sty['red']}necessary{sty['reset']}
ftplib          -- {sty['gold']}in commands{sty['reset']}
shutil          -- {sty['gold']}in commands{sty['reset']}
pathlib         -- {sty['gold']}in commands{sty['reset']}
configparser    -- {sty['blue']}optional{sty['reset']} {sty['dim']}(as cfgparser){sty['reset']}
multiprocessing -- {sty['gold']}in commands{sty['reset']} {sty['dim']}(as mp){sty['reset']}

where:
{sty['blue']}optional{sty['reset']}        -- used to assess OS or fetch config
{sty['gold']}in commands{sty['reset']}     -- necessary to perform some commands
{sty['red']}necessary{sty['reset']}       -- handles important tasks like error handling

On your machine's command line, run 'pip install <module>'.
Additionally, consider updating Python to 3.12.1 or later.
You might be able to run Solus without these modules imported, but functionality could be severely limited.
Proceed? {sty['underl']}(y/N){sty['reset']}""")
    dangerousProceed = input("> ")
    if dangerousProceed == "y".casefold():
        print(f"{sty['gold']}[Warn]{sty['reset']} Skipping module imports.")
        try:
            with open("help.txt") as file:
                helpList = file.read()
                file.close()
        except Exception:
            print(f"{sty['gold']}[Warn]{sty['reset']} Could not locate 'help.txt' to load local help command.")
    else:
        exit()
except MemoryError:
    print(f"{sty['red']}[Error] Solus does not have enough memory to import necessary modules. Press RETURN to exit.{sty['reset']}")
    input("> ")
    exit()
bootStart = time.perf_counter()
print(f"{sty['green']}[Info]{sty['reset']} Loaded necessary modules.")

# config
try:
    config = cfgparser.ConfigParser()
    config.read("config.txt")
    solus_info = {
        "username": config['SOLUS_INFO']['username'],
        "password": config['SOLUS_INFO']['password'],
        "solusname": config['SOLUS_INFO']['solusname'],
        "login": config['SOLUS_INFO']['login']}
    version = config['SOLUS_INFO']['version']
except Exception:
    print(f"{sty['red']}[Error]{sty['reset']} Failed to load configuration file. Would you like to create it? (Y/n)")
    choice = input("> ").casefold()
    if choice == "n":
        solus_info = {
        'username': 'guest',
        'password': 'pass',
        'solusname': 'Solus',
        'login': True}
        version = 'unknown'
        print(f"{sty['green']}Created temporary guest account.{sty['reset']}")
    else:
        Path.touch("config.txt")
        config['SOLUS_INFO'] = {
            'username': 'guest',
            'password': 'pass',
            'solusname': 'Solus',
            'login': 'True',
            'version': 'unknown'}
        with open('config.txt', 'w') as file:
            config.write(file)
        solus_info = {
        "username": config['SOLUS_INFO']['username'],
        "password": config['SOLUS_INFO']['password'],
        "solusname": config['SOLUS_INFO']['solusname'],
        "login": config['SOLUS_INFO']['login']}
        version = config['SOLUS_INFO']['version']
        print(f"{sty['green']}[Info]{sty['reset']} Created configuration file.")
        config.read("config.txt")
    print("Username: 'guest'; password: 'pass'.")
print(f"{sty['green']}[Info]{sty['reset']} Loaded configuration.")

# variables
welcomeMessage = f"Solus CLI {version}, created by Desyntax on 24/02/2026."
dirsym = "$"
legal = f"Solus {version}, created by Desyntax. All content, including source code, are public domain."
print(f"{sty['green']}[Info]{sty['reset']} Loaded variables.")

# definitions
@errors.ExceptionHandler()
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
@errors.ExceptionHandler()
def write(mode):
    filename = nano[1]
    if mode == "w":
        print(f"'{filename}' opened in {sty['blue']}OVERWRITE{sty['reset']} mode")
    else:
        print(f"'{filename}' opened in {sty['blue']}APPEND{sty['reset']} mode")
    print(f"Type {sty['pink']}<close>{sty['reset']} to end writing and save.")
    print(f"Type {sty['pink']}<cancel>{sty['reset']} to revert all changes and close.")
    with open(filename, "r") as old_file:
        content = old_file.read()
    tempfile_name = f".NANO_{filename}"
    Path.touch(tempfile_name)
    with open(tempfile_name, "w") as tempfile:
        tempfile.write(content)
    while True:
        newline = input()
        if newline == "<close>":
            print(f"{sty['green']}Closed {filename} and saved all changes.{sty['reset']}")
            with open(tempfile_name, "r") as tempfile:
                new_content = tempfile.read()
            with open(filename, "w") as output_file:
                output_file.write(new_content)
            os.remove(tempfile_name)
            break
        elif newline == "<cancel>":
            print(f"{sty['green']}Cancelled all changes.{sty['reset']}")
            os.remove(tempfile_name)
            break
        else:
            with open(tempfile_name, "a") as tempfile:
                tempfile.write(newline + "\n")
@errors.ExceptionHandler()
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
@errors.ExceptionHandler()
def sty_rainbow(text):
    global sty
    stymap = [sty["red"], sty["gold"], sty["green"], sty["blue"], sty["pink"]]
    result = ""
    for i, t in enumerate(text):
        color = stymap[i % len(stymap)]
        result += f"{color}{t}"
    result += sty["reset"]
    return result
@errors.ExceptionHandler()
def ls(main, hidden):
    global os, cwd, sty, dirSep
    allinpath = {}
    startTime = time.perf_counter()
    total_size = 0
    task = mp.Process(target=load, args=("Indexing",))
    task.start()
    for node in main:
        total_size = 0
        full_path = os.path.join(cwd, node)
        try:
            if os.path.isfile(full_path):
                if node.startswith(".") and hidden == False:
                    allinpath[node] = (0, "h")
                else:
                    total_size = os.path.getsize(full_path)
                    allinpath[node] = (total_size, "f")
            elif os.path.isdir(full_path) and cwd == "/" and node == "proc":
                allinpath[node] = (0, "p")
            elif os.path.isdir(full_path):
                if node.startswith(".") and hidden == False:
                    allinpath[node] = (0, "h")
                else:
                    total_size = getdirsize(full_path)
                    allinpath[node] = (total_size, "d")
            else:
                allinpath[node] = (0, "f")
        except Exception:
            allinpath[node] = (0, "f")
    if cwd == "/" and os.path.exists("proc"):
        allinpath['proc'] = (0, "p")
    task.terminate()
    print(sty['mcu'], sty['dll'], end="")
    print(f"{sty['blue']}{"Name":<20} {sty['green']}{"Size":>11}{sty['reset']}")
    print("=" * 33)
    for row in main:
        filesize, nodetype = allinpath[row]
        fsm = " B" # file size measurement (bytes, kilobytes, etc)
        if filesize >= 1024**5:
            filesize /= 1024**5
            fsm = "PB"
        elif filesize >= 1024**4:
            filesize /= 1024**4
            fsm = "TB"
        elif filesize >= 1024**3:
            filesize /= 1024**3
            fsm = "GB"
        elif filesize >= 1024**2:
            filesize /= 1024**2
            fsm = "MB"
        elif filesize >= 1024:
            filesize /= 1024
            fsm = "KB"
        filesize = round(filesize, 2)
        if nodetype == "d":
            print(f"{sty['green']}{row:<20}{sty['reset']} {filesize:>10,}{fsm}")
        elif nodetype == "p":
            print(f"{sty['pink']}{row:<20}{sty['reset']} {"N/A":>12}")
        elif nodetype == "h":
            pass
        else:
            print(f"{sty['reset']}{row:<20} {filesize:>10,}{fsm}")
    endTime = time.perf_counter()
    totalTime = endTime - startTime
    print(f"{sty['dim']}Time taken to resolve: {round(totalTime * 1000, 3) if totalTime < 1 else round(totalTime, 3)} {'milliseconds' if totalTime < 1 else 'seconds'}.{sty['reset']}")
    del startTime, endTime, totalTime
@errors.ExceptionHandler()
def getdirsize(start_path):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except FileNotFoundError:
        print(f"{sty['red']}[Error]{sty['reset']} Encountered an issue while resolving '{fp}' {sty['dim']}(Failed to locate){sty['reset']}")
    except PermissionError:
        print(f"{sty['red']}[Error]{sty['reset']} Encountered an issue while resolving '{fp}' {sty['dim']}(Permission error){sty['reset']}")
    except Exception as e:
        print(f"{sty['red']}[Error]{sty['reset']} Encountered an issue while resolving '{fp}' {sty['dim']}({e}){sty['reset']}")
    return total_size
@errors.ExceptionHandler()
def load(msg):
    print()
    while True:
        print(f"{sty['mcu']}{sty['dll']}[|] {msg}")
        time.sleep(0.5)
        print(f"{sty['mcu']}{sty['dll']}[/] {msg}.")
        time.sleep(0.5)
        print(f"{sty['mcu']}{sty['dll']}[-] {msg}..")
        time.sleep(0.5)
        print(f"{sty['mcu']}{sty['dll']}[\\] {msg}...")
        time.sleep(0.5)
@errors.ExceptionHandler()
def ftpmode():
    global ftpmain
    while True:
        ftpcmd = input(f"{sty['red']}ftp{sty['green']}@{sty['blue']}{ftpmain.host}{sty['reset']}> ")
        if ftpcmd == "help":
            file = open(f"{cwd}{dirSep}ftp_help.txt", "r")
            ftphelp = file.read()
            ftphelp = ftphelp.format_map(sty)
            print(ftphelp)
            file.close()
            del ftphelp
        elif ftpcmd == "exit":
            ftpmain.close()
            break
        elif ftpcmd == "ls":
            ftpmain.retrlines("LIST")
        elif ftpcmd.startswith("copy"):
            try:
                cmdsplit = ftpcmd.split(maxsplit=3)
                Path.touch(cmdsplit[2])
                with open(cmdsplit[2], 'wb') as copy:
                    ftpmain.retrbinary(f'RETR {cmdsplit[1]}', copy.write)
                print(f"{sty['green']}Successfully copied '{cmdsplit[1]}' to '{cmdsplit[2]}'.{sty['reset']}")
            except Exception as e:
                print(f"{sty['red']}[Error]{sty['reset']} {e}")
        elif ftpcmd.startswith("cwd"):
            try:
                cmdsplit = ftpcmd.split(maxsplit=2)
                ftpmain.cwd(cmdsplit[1])
                print(f"{sty['green']}Now in '{cmdsplit[1]}'.{sty['reset']}")
            except Exception as e:
                print(f"{sty['red']}[Error]{sty['reset']} {e}")
        elif ftpcmd.startswith("cmd"):
            try:
                cmdsplit = ftpcmd.split(maxsplit=2)
                print(ftpmain.sendcmd(cmdsplit[1]))
            except Exception as e:
                print(f"{sty['red']}[Error]{sty['reset']} {e}")
        else:
            print(f"{sty['red']}'{ftpcmd}' is not a valid FTP operation.{sty['reset']}")

print(f"{sty['green']}[Info]{sty['reset']} Loaded definitions.")

# initialise
if __name__ == "__main__":
    if dangerousProceed != "y":
        print(f"{sty['blue']}[OS]{sty['reset']} Solus is running on a {sty['blue']}{sys.platform}{sty['reset']} system.")
        dirSep = os.sep
        cwd = __file__.removesuffix(f"{dirSep}solus.py")
        print(f"{sty['blue']}[OS]{sty['reset']} Found {sty['blue']}{os.cpu_count()}{sty['reset']} CPU threads.")
        try:
            print(f"{sty['blue']}[OS]{sty['reset']} Solus occupies {sty['blue']}{os.path.getsize(f'{cwd}{dirSep}solus.py'):,d}{sty['reset']} bytes of disk space.")
            print(f"{sty['blue']}[OS]{sty['reset']} Solus directory size: {sty['blue']}{getdirsize(cwd):,d}{sty['reset']} bytes of disk space.")
        except FileNotFoundError:
            print(f"{sty['gold']}[Warn]{sty['reset']} Solus couldn't locate itself to record its disk usage. Proceeding anyway...")
        bootEnd = time.perf_counter()
        bootTime = bootEnd - bootStart
        print(f"{sty['green']}[Info]{sty['reset']} Booted in {sty['blue']}{round(bootTime * 1000, 4)}{sty['reset']} milliseconds.")
        del bootStart, bootEnd, bootTime
    else:
        print(f"{sty['gold']}[Warn]{sty['reset']} Skipped checking OS due to missing modules.")
    print(f"{sty['green']}[Info]{sty['reset']} No fatal errors encountered during boot.", end="\n\n")
    print(welcomeMessage, end="\n\n")
    if solus_info['login'] == "True":
        login()

    while True:
        command = input(f"{sty['red']}{solus_info['username'].upper()}{sty['green']}@{sty['blue']}{solus_info['solusname']}{sty['green']}{dirsym}{sty['reset']}> ")
        if command == "help": # help
            if dangerousProceed == "y":
                print(helpList.format_map(sty))
            else:
                try:
                    file = open(f"{cwd}{dirSep}help.txt", "r")
                    helpmsg = file.read()
                    helpmsg = helpmsg.format_map(sty)
                    print(helpmsg)
                    file.close()
                    del helpmsg
                except FileNotFoundError:
                    print(f"{sty['red']}'help.txt' was not found. Are you in Solus' directory?{sty['reset']}")
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['red']} {e}")
        elif command == "logout": # logout
            print("You have successfully logged out.")
            if solus_info['login'] == "True":
                login()
            else:
                exit()
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
                    scan = command.split(maxsplit=2)
                    if scan[2] == ";m":
                        if os.path.isabs(scan[1]):
                            file = open(f"{cwd}{dirSep}{scan[1]}", "r")
                        else:
                            file = open(scan[1], "r")
                        scan = file.read()
                        scan = scan.format_map(sty)
                        print(scan)
                        file.close()
                    else:
                        file = open(scan[1])
                        print(file.read())
                        file.close()
                except IndexError:
                    file = open(scan[1])
                    print(file.read())
                    file.close()
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['reset']} {e}")
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
                nano = command.split(maxsplit=3)
                try:
                    file = open(nano[1])
                    file.close()
                    try:
                        if nano[2] == ";a":
                            write("a")
                        else:
                            write("w")
                    except Exception:
                        write("w")
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['red']} {e}")
            else:
                print(f"{sty['red']}'nano' takes at least one argument, <file>.{sty['reset']}")
        elif command.startswith("info"): # info
            try:
                file = open(f"{cwd}{dirSep}info.txt", "r")
                infomsg = file.read()
                print(infomsg.format_map(sty))
                file.close()
                del infomsg
            except FileNotFoundError:
                print(f"{sty['red']}'info.txt' was not found. Are you in Solus' directory?{sty['reset']}")
            except Exception as e:
                print(f"{sty['red']}[Error]{sty['red']} {e}")
        elif command.startswith("rep"): # rep
            if command.startswith("rep "):
                try:
                    rep = command.split(maxsplit=2)
                    dest = rep[2]
                    if os.path.isdir(dest):
                        dest = os.path.join(dest, os.path.basename(rep[1]))
                    os.rename(rep[1], dest)
                    print(f"Successfully modified '{rep[1]}' to '{rep[2]}'.")
                    del rep
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['red']} {e}")
            else:
                print("{sty['red']}'rep' takes at least two arguments, <file> and <str/dir>.{sty['reset']}")
        elif command.startswith("ls"): # ls
            if command.startswith("ls "):
                cmd = command.split(maxsplit=2)
                if cmd[1] == ";h":
                    print(f"{sty['green']}All in '{cwd}': {sty['reset']}")
                    ls(os.listdir(cwd), True)
                del cmd
            else:
                print(f"{sty['green']}All in '{cwd}':{sty['reset']}")
                ls(os.listdir(cwd), False)
        elif command.startswith("cwd"):  # cwd
            if command.startswith("cwd "):
                try:
                    new_dir = command.removeprefix("cwd ")
                    if new_dir == "proc" or new_dir == "/proc" and os.path.realpath(new_dir) == "/proc":
                        print(f"{sty['red']}[Error]{sty['reset']} 'proc' is not accessible due to its pseudo-directory nature.")
                    else:
                        os.chdir(new_dir)
                        cwd = os.getcwd()
                        print(f"{sty['green']}Changed directory to '{cwd}'{sty['reset']}")
                    del new_dir
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['reset']} {e}")
            else:
                print(f"{sty['red']}'cwd' takes at least one argument, <dir>.{sty['reset']}")
        elif command.startswith("license"): # license
            print(legal)
        elif command.startswith("boom"): # boom
            if command.startswith("boom "):
                try:
                    os.remove(command.removeprefix("boom "))
                    print(f"Successfully deleted '{command.removeprefix('boom ')}'.")
                except IsADirectoryError:
                    print(f"{sty['gold']}[Warn]{sty['reset']} '{command.removeprefix('boom ')}' is a directory. Would you like to remove it? (y/N)")
                    choice = input("> ").casefold()
                    if choice == "y":
                        try:
                            shutil.rmtree(command.removeprefix('boom '))
                            print(f"Successfully removed '{command.removeprefix('boom ')}'")
                        except Exception as e:
                            print(f"{sty['red']}[Error]{sty['red']} {e}")
                    else:
                        print("Aborted.")
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['red']} {e}")
            else:
                print(f"{sty['red']}'boom' takes at least one argument, <file>.{sty['reset']}")
        elif command.startswith("kin"): # kin
            if command.startswith("kin "):
                try:
                    os.mkdir(command.removeprefix("kin "))
                    print(f"Created directory '{command.removeprefix('kin ')}' in '{cwd}'.")
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['reset']} {e}")
            else:
                print(f"{sty['red']}'kin' takes at least one argument, <dir>.{sty['reset']}")
        elif command.startswith("touch"): # touch
            if command.startswith("touch "):
                try:
                    Path(f"{command.removeprefix('touch ')}").touch()
                    print(f"Sucessfully created '{command.removeprefix('touch ')}' at '{cwd}'")
                except FileExistsError:
                    print(f"{sty['red']}[Error]{sty['reset']}'{command.removeprefix('touch ')}' already exists in '{cwd}'.")
                except PermissionError:
                    print(f"{sty['red']}[Error]{sty['reset']} Solus doesn't have the necessary permissions to perform this.")
                except Exception as e:
                    print(f"{sty['red']}[Error]{sty['reset']} {e}")
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
                    print(f"{sty['red']}[Error]{sty['reset']} {e}")
            else:
                print(f"{sty['red']}'copy' takes at least two arguments, <file> and <dir>.{sty['reset']}")
        elif command.startswith("exit"): # exit
            print("Ending CLI...")
            exit()
        elif command.startswith("sign"): # sign
            sign = command.split(maxsplit=2)
            try:
                meta = os.stat(sign[1])
                print(f"{sty['green']}Metadata from '{sign[1]}'{sty['reset']}")
                print(f"Path: {cwd}{dirSep}{sign[1]}")
                print(f"Type: {'Directory' if os.path.isdir(sign[1]) else 'File' if os.path.isfile(sign[1]) else 'Other'}")
                print(f"Last accessed: {time.ctime(meta.st_mtime)}")
                print(f"Size: {meta.st_size if os.path.isfile(sign[1]) else getdirsize(sign[1]) if os.path.isdir(sign[1]) else 'Unknown'} bytes")
                print(f"Storage device: {meta.st_dev}")
                print(f"Owner ID: {meta.st_uid}")
                print(f"Permissions: {stat.filemode(meta.st_mode)}")
                del meta, sign
            except Exception as e:
                print(f"{sty['red']}[Error]{sty['reset']} {e}")
        elif command.startswith("login"): # login
            if command.startswith("login "):
                log = command.split(maxsplit=2)
                log[1] = log[1].casefold()
                if log[1] == "true" or log[1] == "y":
                    config['SOLUS_INFO']['login'] = "True"
                    print(f"{sty['green']}Toggled login prompt on.{sty['reset']}")
                elif log[1] == "false" or log[1] == "n":
                    config['SOLUS_INFO']['login'] = "False"
                    print(f"{sty['green']}Toggled login prompt off.{sty['reset']}")
                del log
            else:
                print(f"{sty['red']}'login' takes at least one argument, <bool>.{sty['reset']}")
        elif command.startswith("home"): # home
            cwd = __file__.removesuffix(f"{dirSep}solus.py")
            print(f"{sty['green']}Changed working directory to '{cwd}'.{sty['reset']}")
        elif command.startswith("ftp"): # ftp
            server = command.split(maxsplit=2)
            try:
                print(f"Connecting to '{server[1]}'...")
                ftpUser = input("ftp:USERNAME> ")
                ftpPass = input(f"ftp:PASSWORD> {sty['hide']}")
                print(sty['reset'], end="")
                task = mp.Process(target=load, args=("Connecting",))
                task.start()
                ftpmain = ftplib.FTP(host=server[1], user=ftpUser, passwd=ftpPass)
                ftplib.FTP.login(ftpmain)
                task.terminate()
                print(sty['mcu'], sty['dll'], end="", sep="")
                print(f"{sty['green']}Logged in at '{server[1]}'.{sty['reset']}")
                print(f"Server message:\n{ftplib.FTP.getwelcome(ftpmain)}")
                ftpmode()
            except Exception as e:
                task.terminate()
                print(sty['mcu'], sty['dll'], end="", sep="")
                print(f"{sty['red']}[Error]{sty['reset']} {e}")
        else:
            print(f"{sty['red']}'{command}' not a recognised command. Use 'help' to view a list of commands.{sty['reset']}")
        if cwd == __file__.removesuffix(f"{dirSep}solus.py"):
            dirsym = "$"
        elif cwd == "/" or cwd == "C:\\":
            dirsym = "/"
        else:
            dirsym = "~"

# like and subscribe for more epic code
