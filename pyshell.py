#!/usr/bin/python3
import subprocess
import os
import sys
import readline
from requests import request
import wget
import time
import random
import psutil
# just variables, things like the history and colors
class variables:
    colors = {"RED":'\033[38;5;196m',"YELLOW":'\033[38;5;226m','BLUE':'\033[38;5;20m','GREEN':'\033[38;5;46m','PURPLE':'\033[38;5;93m','WHITE':'\033[38;5;255m','BLACK':'\033[38;5;16m','RESET':'\033[0m'}
    osname = os.name
    recently_deleted = {}
    killed_processes = []
    prompt = f"{colors['BLUE']}{os.getlogin()}@{os.uname()[1]}{colors['PURPLE']}-[{os.getcwd()}]->{colors['RESET']} "
    ql = ['quit','exit','q']
    history = []
    commands = ['wc','req','wget','spinner','killed','wait','rd','recover','cp','mv','ps', 'cat', 'cd', 'clear', 'colors', 'diff', 'echo', 'write', 'cmp', 'grep', 'head', 'history', 'kill', 'trashcat', 'ls', 'mkdir', '$$', 'pwd', 'rm', 'rmdir', 'sleep', 'touch', 'uname']
# holds most of the commands
class commands:
    E = variables.colors['RED']
    # wordcount, counts words or lines in a file
    def wc(mode,file):
        try:
            with open(file,'r')as f:
                c = f.read()
                f.close()
        except:
            return f'{E}Unable to open {file}'
        if mode == "l":
            x = len(c.split('\n'))
            return f"{variables.colors['YELLOW']}{file} : {x}"
        else:
            x = len(c.split(" "))
            return f"{variables.colors['YELLOW']}{file} : {x}"
    # just a stupid spinner for also waiting
    def spinner(s,phrase):
        stages = ['|','/','-','\\','|']#,'/','-','\\','|']
        for i in range(0,s * 2):
            for x in stages:
                sys.stdout.write(f"\r{phrase} {x}")
                time.sleep(0.1)
        print("\n")
    # basically just sleep with a progress bar
    def wait(s):
        l = ["."] * s
        for x in range(0,s):
            sys.stdout.write(f"\r{''.join(l)}")
            time.sleep(1)
            l[x] = "█"
        sys.stdout.write(f"\r{'█' * len (l)}")
        sys.stdout.write(f"\r\n")
    # recreates a file stored in variables.recently_deleted
    def recover(file):
        if file in variables.recently_deleted:
            try:
                with open(file,'w')as f:
                    f.write(variables.recently_deleted[file])
                    f.close()
                return f'{variables.colors["GREEN"]}{file} was recovered'
            except:
                return f'{E}Unable to recover {file}'
        else:
            return f'{E}{file} is not recoverable via recently deleted'
    # either moves a file, renames a file, or copies a file
    def mv(original,new,mode):
        try:
            with open(original,'r')as f:
                c = f.read()
                f.close()
            with open(new,'w')as f:
                f.write(c)
                f.close()
            if mode != "copy":
                variables.recently_deleted[original] = c
                os.remove(original)
        except:
                return f"{E}Unable to {mode} {original} to {new}"
    # just lets you write whatever then save it into a file
    def editor(file=""):
        print(f"{variables.colors['BLUE']}Ctrl+D to save")
        c = sys.stdin.readlines()
        if file == "":
            print("File name : ")
            file = input(f"{variables.colors['GREEN']}-> ")
        try:
            with open(file,'w')as f:
                f.write(''.join(c))
                f.close()
            return "Done!"
        except:
            return(f"Unable to write contents to {file}")
    # lists the contents a directory
    def ls(dir):
        try:
            return(variables.colors['BLUE'] + ''.join([f"{x} " for x in os.listdir(dir)])[:-1])
        except:
            return(f"{E}Unable to list {dir}")
    # changes directory
    def cd(dir):
        try:
            os.chdir(dir)
        except:
            return f'{E}Unable to change to {dir}'
    # prints the contents of a file
    def cat(file):
        try:
            with open(file,'r')as f:
                contents = f.read()
                f.close()
            return contents
        except:
            return f'{E}Unable to open {file}'
    # shows the differences of 2 files
    def diff(f1,f2):
        output = []
        try:
            with open(f1,'r')as f:
                c1 = f.read().split("\n")
                f.close()
            with open(f2,'r')as f:
                c2 = f.read().split("\n")
                f.close()
        except:
            return f"{E}Unable to open the files specified"
        l1,l2 = len(c1),len(c2)
        output.append(f"{f1} {l1} {'>' if l1 > l2 else '<' if l1 < l2 else '=='} {f2} {l2}")
        if l1 > l2:
            for i in range(0,l2):
                try:
                    if c1[i] != c2[i]:
                        output.append(f"{variables.colors['GREEN']}line {i + 1} :\n{f1} : {c1[i]}\n{f2} : {c2[i]}")
                except:
                    break
            output.append(f"{variables.colors['YELLOW']}{f2} ends here.")
        else:
            for i in range(0,l1):
                try:
                    if c2[i] != c1[i]:
                        output.append(f"{E}line {i + 1} :\n{f1} : {c1[i]}\n{f2} : {c2[i]}")
                except:
                    break
            output.append(f"{variables.colors['YELLOW']}{f1} ends here.")
        return ''.join([f"{x}\n" for x in output])
    # creates an empty file
    def touch(name):
        with open(name,'w')as f:
            f.write("")
            f.close()
    # removes a file
    def rm(file):
        try:
            with open(file,'r')as f:
                c = f.read()
                f.close()
            variables.recently_deleted[file] = c
            os.remove(file)
        except:
            return f'{E}Unable to delete {file}'
    # removes a directory
    def rmdir(dir):
        try:
            os.removedirs(dir)
        except:
            return f'{E}Unable to delete {dir}'
    # clears the screen
    def clear():
        if variables.osname == "posix":
            os.system("clear")
        else:
            os.system("cls")
    # outputs a certain amount of lines in a file
    def head(file,lines):
        newline = "\n"
        try:
            with open(file,'r')as f:
                contents = f.read()
                f.close()
            try:
                return ''.join([f"{x}\n" for x in contents.split("\n")[0:lines]])
            except:
                return f'{E}{file} Does not have {lines} lines, it has {len(contents.split(newline))} lines'
        except:
            return f'Unable to open {file}'
    # kills a proccess
    def kill(pid):
        try:
            os.kill(pid,9)
            variables.killed_processes.append(psutil.Process(pid))
        except:
            return f'{E}Unable to kill {pid}'
    # checks if two files are equal
    def fe(f1,f2):
        try:
            with open(f1,'r')as f:
                c1 = f.read()
                f.close()
            with open(f2,'r')as f:
                c2 = f.read()
                f.close()
            if c1 == c2:
                return f"{f1} == {f2}"
            else:
                return f"{f1} != {f2}"
        except:
            return f"{E}Unable to open the files specified"
    # checks if a phrase is in a file
    def grep(file,phrase):
        try:
            with open(file, 'r') as f:
                c = f.read()
                f.close()
        except:
            return(f"{E}Unable to open the file specified")
            quit()
        output = []
        cs = c.split("\n")
        for i in range(0,len(cs) - 1):
            if phrase in cs[i]:
                output.append(f"line : {i + 1}\n{cs[i]}")
        return ''.join([f"{x}\n" for x in output])
    # makes a directory
    def mkdir(dir):
        try:
            os.mkdir(dir)
        except:
            return f"Unable to create {dir}"
# just parses user input and runs commands accordingly 
def cmdparse(cmd):
    c = [x for x in cmd.split(" ") if x != ""]
    match c[0]:
        # prints whatever you type
        case "echo":
            print(''.join([f"{b} " for b in c[1:]])[:-1])
        # tells you some system information
        case "uname":
            print(''.join([f"{x} " for x in os.uname()][:-1]))
        case "mkdir":
            try:
                commands.mkdir(c[1])
            except:
                print(f"{variables.colors['RED']}Usage : mkdir dir")
        case "grep":
            try:
                print(commands.grep(c[1],''.join([f"{x} " for x in c[2:]])[:-1]))
            except:
                print(f"{variables.colors['RED']}Usage : grep file words")
        case "cmp":
            try:
                print(commands.fe(c[1], c[2]))
            except:
                print(f"{variables.colors['RED']}Usage : cmp file1 file2")
        case "head":
            try:
                print(commands.head(c[1],int(c[2])))
            except:
                print(f"{variables.colors['RED']}Usage : head file lines")
        case "kill":
            try:
                os.kill(int(c[1]))
            except:
                print(f"{variables.colors['RED']}Usage : kill PID")
        case "clear":
            commands.clear()
        case "rmdir":
            try:
                commands.rmdir(c[1])
            except:
                print(f"{variables.colors['RED']}Usage : rmdir dir")
        case "rm":
            try:
                commands.rm(c[1])
            except:
                print(f"{variables.colors['RED']}Usage : rm file")
        case "touch":
            try:
                commands.touch(c[1])
            except:
                print(f"{variables.colors['RED']}Usage : touch file")
        case "diff":
            try:
                print(commands.diff(c[1],c[2]))
            except:
                print(f"{variables.colors['RED']}Usage : diff file1 file2")
        # tells you your shells process ID
        case "$$":
            print(os.getpid())
        case "cat":
            try:
                print(commands.cat(c[1]))
            except:
                print(f"{variables.colors['RED']}Usage : cat file")
        case "cd":
            try:
                commands.cd(c[1])
            except:
                print(f"{variables.colors['RED']}Usage : cd dir")
        # prints current working directory
        case "pwd":
            print(os.getcwd())
        # does nothing for an amount of time
        case "sleep":
            try:
                time.sleep(int(c[1]))
            except:
                print(f"{variables.colors['RED']}Usage : sleep seconds")
        case "ls":
            try:
                print(commands.ls(c[1]))
            except:
                print(commands.ls("."))
        # imagine lolcat but the colors are uglier and not planned
        case "trashcat":
            try:
                print(''.join([f'\033[38;5;{random.randrange(1,256)}m{x}' for x in [*''.join(f"{i} " for i in c[1:])[:-1]]]))
            except:
                pass
        # shows your command history
        case "history":
            print(''.join([f"{x}\n" for x in variables.history]))
        # shows off the totally cool total of barely any colors I added 
        case "colors":
            blocks = ''.join([f"{variables.colors[i]}██████" for i in variables.colors])
            print(''.join([f"{variables.colors[x]}{x} " for x in variables.colors]) + f"\n{blocks}\n{blocks}")
        # displays all commands
        case "commands":
            print(''.join([f"{x}\n" for x in variables.commands]) + "You can type in a command with no args to see it's usage, commands not here will attempt to run elsewhere")
        case "write":
            try:
                print(commands.editor(c[1]))
            except:
                print(commands.editor())
        # tells you who you are
        case "whoami":
            print(os.getlogin())
        # tells you your hostname
        case "hostname":
            print(os.uname()[1])
        # shows running processes
        case "ps":
            print("PID            NAME            STATUS\n" + ''.join([f"{x}            {psutil.Process(x).name()}            {psutil.Process(x).status()}\n" for x in psutil.pids()]))
        # shows processes you killed during this session
        case "killed":
            print("PID            NAME            STATUS\n" + ''.join([f"{x}            {x.name()}            {x.status()}\n" for x in variables.killed_processes]))
        case "mv":
            try:
                commands.mv(c[1],c[2],"move")
            except:
                print(f"{variables.colors['RED']}Usage : mv original new")
        case "cp":
            try:
                commands.mv(c[1],c[2],"copy")
            except:
                print(f"{variables.colors['RED']}Usage : cp original new")
        # shows recently deleted commands
        case "rd":
            print(''.join([f"{x} " for x in variables.recently_deleted])[:-1])
        case "recover":
            try:
                print(commands.recover(c[1]))
            except:
                print(f"{variables.colors['RED']}Usage : recover file")
        case "wait":
            try:
                commands.wait(int(c[1]))
            except:
                print(f"{variables.colors['RED']}Usage : wait seconds")
        case "spinner":
            try:
                commands.spinner(int(c[1]),''.join([f"{x} " for x in c[2:]])[:-1])
            except:
                print(f"{variables.colors['RED']}Usage : seconds words")
        # uses wget.download to download something
        case "wget":
            try:
                wget.download(c[1])
            except:
                print(f"{variables.colors['RED']}Usage : wget url")
        # uses requests.request then outputs the results in a formatted way
        case "req":
            try:
                r = request(c[1], c[2])
                print(f"{variables.colors['GREEN']}Headers : \n{r.headers}\n\nCookies : \n{r.cookies}\n\n Text : \n{r.text}\n\n Json : \n{r.json}")
            except:
                print(f"{variables.colors['RED']}Usage : req methord url")
        case "wc":
            try:
                print(commands.wc(c[1],c[2]))
            except:
                return f"{variables.colors['RED']}Usage : wc mode file"
        # whenever a non existent command is entered it'll try to run it elsewhere
        case _:
            print(f"{variables.colors['RED']}Command not found : {c[0]}, Running elsewhere\n{variables.colors['RESET']}")
            try:
                print(subprocess.run(c, stdout=subprocess.PIPE).stdout.decode('utf-8'))
            except:
                print(f"{variables.colors['RED']}Command not found elsewhere.")
while True:
    while True:
        t = False
        cmd = input(f"{variables.colors['BLUE']}{os.getlogin()}@{os.uname()[1]}{variables.colors['PURPLE']}-[{os.getcwd()}]->{variables.colors['RESET']} ")
        if cmd == "":
            break
        variables.history.append(cmd)
        if cmd.startswith("time "):
            cmd = ''.join([f"{x} " for x in cmd.split(" ")[1:]])[:-1]
            t = True
            s = time.time()
        if cmd.startswith("rs "):
            try:
                print(subprocess.run([x for x in cmd.split(" ")[1:]], stdout=subprocess.PIPE).stdout.decode('utf-8'))
            except Exception as e:
                print(f"{variables.colors['RED']}Command not found elsewhere.")
        elif cmd in variables.ql:
            quit()
        elif "&&" in cmd:
            cmds = cmd.split("&&")
            for b in cmds:
                cmdparse(b)
        else:
            cmdparse(cmd)
        if t == True:
            print(int(time.time() - s))